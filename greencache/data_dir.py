from os.path import join as joinpath, exists, expanduser
from os import mkdirs, environ as env

from redlib.api.system import is_windows

class DataDir:

        def __init__(self, path, home=True):
                if home:
                        if is_windows():
                                self._path = joinpath(env['APPDATA'], path)
                        else:
                                self._path = joinpath(expanduser('~'), path)
                else:
                        self._path = path

                self.check()


        def check(self):
                if not exists(self._path):
                        mkdirs(self._path)


        def get_fullpath(self):
                return self._path


        fullpath = property(get_fullpath)
        