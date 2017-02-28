
from .. import config
from .. import data_dir


def setup_for_test():
        config.test = True
        config.home_dir_name = 'gc_test_home'


        class DataDirMock(data_dir.DataDir):
                def __init__(self, dontcare):
                        self._path = config.home_dir_name
                        self.check()

        data_dir.DataDir = DataDirMock


def cleanup_after_test():
        config.test = False
