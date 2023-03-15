from __future__ import annotations
import json
import datetime as dt
import inspect
from enum import Enum
from functools import singledispatchmethod
from typing import overload, cast, Any


class KeeWeeDB(dict):
    def __missing__(self, kee):
        wee = self[kee] = type(self)()
        return wee


_store: KeeWeeDB = KeeWeeDB()
_vars = {}


def keewee(var_name):
    global _store
    if not _store.get(var_name):
        _store[var_name] = []

    def getter():
        return _vars.get(var_name)

    def setter(value):
        _store[var_name].append(value)
        _vars[var_name] = value

    return getter, setter


MODES: dict[str, Any] = {
    "list": list(),
    "dict": dict(),
    "set": set()
}


class KeeWee:
    _store = KeeWeeDB()

    def __init__(self, blame: bool = False, mode: str = "list"):
        self.blame = blame
        self.mode = MODES[mode]

    def __set_name__(self, owner: type[object], name: str) -> None:
        """Does not seem to change over the mode"""
        self.public_name = name
        self.private_name = '_' + name

    def __set__(self, obj: object, value: int) -> None:
        obj.__dict__[self.private_name] = value
        owner = obj.__class__.__name__
        instance_name = str(obj)
        if self.blame:
            value = (value, inspect.getouterframes(inspect.currentframe(), 2)[1][3])

        self.record(self.mode, owner, instance_name, value)

    @singledispatchmethod
    def record(self, mode, owner, instance, value) -> None:
        raise NotImplementedError("Cannot record ")

    @record.register
    def _(self, mode: set, owner, instance, value) -> None:
        if not self._store[owner][self.public_name].get(instance):
            self._store[owner][self.public_name][instance] = set()
        self._store[owner][self.public_name][instance].add(value)

    @record.register
    def _(self, mode: list, owner, instance, value):
        if not self._store[owner][self.public_name].get(instance):
            self._store[owner][self.public_name][instance] = []
        self._store[owner][self.public_name][instance].append(value)

    @record.register
    def _(self, mode: dict, owner, instance, value):
        if not self._store[owner][self.public_name].get(instance):
            self._store[owner][self.public_name][instance] = {}
        self._store[owner][self.public_name][instance][dt.datetime.now().time().isoformat()] = value

    @overload
    def __get__(self, obj: None, obj_type: None) -> KeeWee:
        ...

    @overload
    def __get__(self, obj: object, obj_type: type[object]) -> int:
        ...

    def __get__(self, obj: object | None, obj_type: type[object] | None = None) -> KeeWee | int:
        """Does not seem to change over the mode"""
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
