from os.path import exists
from os import remove

from redlib.api.py23 import *


class SimpleCache:

        def __init__(self, filepath):
                self._filepath = filepath
                self.load()


        def load(self):
                self._map = {}

                if exists(self._filepath):
                        self._map = pickleload(self._filepath)


        def save(self):
                pickledump(self._map, self._filepath)


        def add(self, key, value, pickle=False):
                self._map[key] = value if not pickle else pickledumps(value)
                self.save()


        def get(self, key, default=None, pickle=False):
                value = self._map.get(key, default)
                return value if not pickle else pickleloads(value)


        def clear(self):
                if exists(self._filepath):
                        remove(self._filepath)
