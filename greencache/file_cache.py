from os.path impoer join as joinpath

from redlib.api.misc import md5hash

from .simple_cache import SimpleCache
from .data_dir import DataDir
from . import config as g_config


class FileCacheStrategy:
        LRU = 0


class FileCacheConfig:

        def __init__(self):
                self.strategy = FileCacheStrategy.LRU
                self.max = 50
                self.no_db = True
                self.datetime_suffix_fmt = '_%Y_%m_%d_%H_%M_%S'
                self.prefix = 'cached'
                self.dirpath = None


        def hash(self):
                return md5hash(self.dirpath)


class FileCache:

        def __init__(self, config=FileCacheConfig()):
                self._config = config

                data_dir = DataDir(g_config.home_dir_name)
                self._mr_datetime = SimpleCache(
                                        joinpath(data_dir.fullpath, g_config.most_recent_dt_cache_filename)


        def check_dir(self):
                pass


        def add_file(self, src_filepath, ext=None, date_time=None):
                dest_filename = self._config.prefix
                                + '.%s'%ext if (ext is not None and len(ext) > 0) else ''
                dest_filepath = joinpath(self._config.dirpath, dest_filename)

                copy(src_filepath, dest_filepath)

                dt = now() if date_time is None else date_time
                self._mr_datetime.add(self._config.hash(), dt, pickle=True)

                self.check_max()


        def check_max(self):
                glob_path = joinpath(self._config.dirpath, self._config.prefix)
                cached_files = glob(glob_path)

                if len(cached_files) <= self._config.max:
                        return

                self.remove_multiple_files(sorted(cached_files)[self._config.max : ])


        def move_most_recent_file_down(self):
                ext = None
                try:
                        _, ext = self.get_most_recent_file_name_ext()
                except NoMostRecentFile:
                        return

                dt = self._mr_datetime.get(self._config.hash()) or now()

                dest_filename = self._config.prefix
                                + strptime(self._config.datetime_suffix_fmt, dt)
                                + '.%s'%ext if (ext is not None and len(ext) > 0) else ''
                dest_filepath = joinpath(self._config.dirpath, dest_filename)

                copy(self._config.prefix + ext, dest_filepath)


        def get_most_recent_file_name_ext(self):
                for f in listdir(self._config.dirpath):
                        name, ext = splitext(f)
                        if name == self._config.prefix:
                                return name, ext
                raise NoMostRecentFile()


        def get_file(self, index=0):
                pass


        def clear(self):
                glob_path = joinpath(self._config.dirpath, self._config.prefix)
                cached_files = glob(glob_path)
                self.remove_multiple_files(cached_files)


        def remove_multiple_files(self, filepath_list):
                err_msg = ''
                for f in cached_files:
                        try:
                                remove(f)
                        except (OSError, IOError) as e:
                                err_msg += e.message

                if len(err_msg) > 0:
                        raise FileCacheError(err_msg)


        def make_most_recent(self, index):
                pass


        def extract_datetime_from_filename(self, filename):
                pass
