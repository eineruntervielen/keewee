import json
import datetime as dt
from collections import defaultdict


class KeeWeeDB(dict):
    def __missing__(self, kee):
        wee = self[kee] = type(self)()
        return wee


class KeeWee:
    _store = {}

    def __set_name__(self, owner, name):
        self.public_name = name
        self.private_name = '_' + name
        self._store[owner.__name__] = {}
        self._store[owner.__name__][name] = {}

    def __get__(self, obj, obj_type=None):
        return obj.__dict__.get(self.private_name)

    def __set__(self, obj, value):
        obj.__dict__[self.private_name] = value

        owner = obj.__class__.__name__
        instance_name = str(obj)
        if not self._store[owner][self.public_name].get(instance_name):
            self._store[owner][self.public_name][instance_name] = {}
        self._store[owner][self.public_name][instance_name][dt.datetime.now().time().isoformat()] = value

    @classmethod
    def dump(cls, file_name: str):
        with open(file_name, "w") as f:
            json.dump(cls._store, f)

    @classmethod
    def dumps(cls):
        return json.dumps(cls._store)

    @classmethod
    def dumpd(cls):
        return cls._store
