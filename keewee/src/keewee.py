from __future__ import annotations
import json
import datetime as dt
import inspect
from typing import overload, cast


class KeeWeeDB(dict):
    def __missing__(self, kee):
        wee = self[kee] = type(self)()
        return wee


class KeeWee:
    _store = {}

    def __init__(self, blame: bool = False):
        self.blame = blame

    def __set_name__(self, owner: type[object], name: str) -> None:
        self.public_name = name
        self.private_name = '_' + name
        self._store[owner.__name__] = {}
        self._store[owner.__name__][name] = {}

    def __set__(self, obj: object, value: int) -> None:
        obj.__dict__[self.private_name] = value

        owner = obj.__class__.__name__
        instance_name = str(obj)
        if not self._store[owner][self.public_name].get(instance_name):
            self._store[owner][self.public_name][instance_name] = {}
        if self.blame:
            mutator = inspect.getouterframes(inspect.currentframe(), 2)[1][3]
            self._store[owner][self.public_name][instance_name][dt.datetime.now().time().isoformat()] = (value, mutator)
        else:
            self._store[owner][self.public_name][instance_name][dt.datetime.now().time().isoformat()] = value

    @overload
    def __get__(self, obj: None, obj_type: None) -> KeeWee:
        ...

    @overload
    def __get__(self, obj: object, obj_type: type[object]) -> int:
        ...

    def __get__(self, obj: object | None, obj_type: type[object] | None = None) -> KeeWee | int:
        if obj is None:
            return self
        return cast(int, obj.__dict__.get(self.private_name))

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
