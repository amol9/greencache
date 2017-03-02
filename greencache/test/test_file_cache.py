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
                self.cleanup()


        def cleanup(self):
                if exists(self.root):
                        rmtree(self.root)
                if exists(config.home_dir_name):
                        rmtree(config.home_dir_name)


        def test_cleanup(self):
                self.cleanup()


        def get_root_path(self, dirpath):
                return joinpath(self.root, dirpath)


        def create_file_cache_obj(self, dirpath, max_f=None, max_index=None):
                cfg = FileCacheConfig()
                cfg.dirpath = self.get_root_path(dirpath)
                cfg.max = max_f or cfg.max
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

                a = 0 if 0 in r else 1
                for i in range(50, 60):
                        self.create_file(fn, content=str(i + 1))
                        self.assertEqual(fc.add(fn), i + a)


        def test_max_limit(self):
                '''
                Tests that the number of files is limited to max_f.
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


        def test_rollover(self):
                '''
                Add max_index number of files to cache.
                Add one more and test if the cache rolls over.
                Add one more and test if the appropriate index is removed from rollover map (and hence, raises an error).
                '''

                max_index = 100
                max_f = 10

                fc = self.create_file_cache_obj('test_cache', max_f=max_f, max_index=max_index)
                fn = self.get_root_path('test.txt')
                for i in range(0, max_index):
                        self.create_file(fn, content=str(i + 1))
                        fc.add(fn)

                max_index_c = max(fc.get_all_indices())
                self.assertEqual(max_index_c, max_index - 1)

                fc.add(fn)
                file_count = lambda : len(fc.get_all_files())
                self.assertEqual(file_count(), max_f)
                self.assertEqual(fc._index.current_index, max_f)
                
                
                f = fc.get(index=max_index)
                fi = fc._get_index_from_filename(f)
                self.assertEqual(fi, max_f - 1)

                fc.add(fn)
                with self.assertRaises(FileCacheError):
                        f = fc.get(index = max_f + 2)


        def test_make_most_recent(self):
                fc = self.create_file_cache_obj('test_cache')
                fn = self.get_root_path('test.txt')
                for i in range(0, 10):
                        self.create_file(fn, content=str(i + 1))
                        fc.add(fn)

                oldpath = fc.get(index=9)
                index, filepath = fc.make_most_recent(index=9)
                self.assertEqual(index, 11)
                self.assertIsNotNone(filepath)
                self.assertExists(filepath)
                self.assertNotExists(oldpath)


        def assertExists(self, filepath):
                self.assertTrue(exists(filepath))


        def assertNotExists(self, filepath):
                self.assertFalse(exists(filepath))


if __name__ == '__main__':
        ut_main()
        cleanup_after_test()
