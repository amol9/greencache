from unittest import TestCase, main as ut_main
from os import remove
from os.path import exists, join as joinpath
from shutil import rmtree
from random import randint, sample

from .test_config import setup_for_test, cleanup_after_test
setup_for_test()

from .. import config
from ..file_cache import FileCache, FileCacheConfig, FileCacheError
from ..simple_cache import SimpleCache
from ..data_dir import DataDir


class TestFileCache(TestCase):
        root = 'fc_test'


        def test_bad_config(self):
                with self.assertRaises(FileCacheError):
                        fc = FileCache()


        def setUp(self):
                pass


        def tearDown(self):
                #return
                self.cleanup()


        def cleanup(self):
                if exists(self.root):
                        rmtree(self.root)
                if exists(config.home_dir_name):
                        rmtree(config.home_dir_name)

                '''sc = SimpleCache(joinpath(DataDir(config.home_dir_name).fullpath, config.file_cache_index_store_filename))
                sc.clear()'''


        def test_cleanup(self):
                self.cleanup()


        def get_root_path(self, dirpath):
                return joinpath(self.root, dirpath)


        def create_file_cache_obj(self, dirpath, max=None, max_index=None):
                cfg = FileCacheConfig()
                cfg.dirpath = self.get_root_path(dirpath)
                cfg.max = max or cfg.max
                cfg.max_index = max_index or cfg.max_index

                fc = FileCache(config=cfg)
                return fc


        def test_simple(self):
                fc = self.create_file_cache_obj('test_cache')
                fn = self.get_root_path('test.txt')
                self.create_file(fn)
                for i in range(0, 50):
                        self.assertEqual(fc.add(fn), i + 1)


        def create_file(self, filename, content=None):
                with open(filename, 'w') as f:
                        content and f.write(content)


        # test: roll over
        # test: exc on not found
        
        def test_with_content(self):
                fc = self.create_file_cache_obj('test_cache')
                fn = self.get_root_path('test.txt')
                for i in range(0, 50):
                        self.create_file(fn, content=str(i + 1))
                        self.assertEqual(fc.add(fn), i + 1)

                for i in range(0, 50):
                        fp = fc.get(index=i)
                        c = None
                        with open(fp, 'r') as f:
                                c = f.read()
                        
                        self.assertEqual(c, str(i) if i > 0 else '50')


        def test_remove_add(self):
                '''
                Creates a cache, removes a random number of files from it randomly, then, adds more files to the cache and checks if proper index is returned.
                '''

                fc = self.create_file_cache_obj('test_cache')
                fn = self.get_root_path('test.txt')
                for i in range(0, 50):
                        self.create_file(fn, content=str(i + 1))
                        fc.add(fn)

                r = sample(range(0, 50), k=randint(0, 50))
                for i in r:
                        fp = fc.get(index=i)
                        remove(fp)

                print('removed %d files from cache'%len(r))

                a = 0 if 0 in r else 1
                for i in range(50, 60):
                        self.create_file(fn, content=str(i + 1))
                        self.assertEqual(fc.add(fn), i + a)


        def test_max_limit(self):
                '''
                Tests that the number of files is limited to max.
                '''

                fc = self.create_file_cache_obj('test_cache')
                fn = self.get_root_path('test.txt')
                for i in range(0, 50):
                        self.create_file(fn, content=str(i + 1))
                        fc.add(fn)

                file_count = lambda : len(fc.get_all_files())

                for i in range(0, 10):
                        fc.add(fn)
                        self.assertEqual(file_count(), 50)

                self.assertEqual(max(fc.get_all_indices()), 59)


if __name__ == '__main__':
        ut_main()
        cleanup_after_test()
