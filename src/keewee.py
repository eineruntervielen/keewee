from __future__ import annotations

import json
import datetime as dt
import inspect
import uuid
import logging

from functools import singledispatchmethod, singledispatch
from pprint import pp
from typing import overload, cast, Any

logging.basicConfig(level=logging.DEBUG)

MODES: dict[str, Any] = {
    "list": list(),
    "dict": dict(),
    "set": set()
}


class KeeWeeDB(dict):
    def __missing__(self, kee):
        wee = self[kee] = type(self)()
        return wee


_store: KeeWeeDB = KeeWeeDB()


def keewee(initial: Any, mode: str | None = None):
    var_id: str = uuid.uuid4().hex
    mode = MODES[mode] if mode else None

    @singledispatch
    def record(mode, value):
        raise NotImplementedError("Cannot record ")

    @record.register
    def _(mode: list, value):
        logging.debug(msg="not implemented yet!!!")

    def setter(value):
        _store[var_id] = value
        if mode is not None:
            record(mode, value)

    setter(initial)

    class IntProxy(int):
        def __new__(cls, value, *args, **kwargs):
            return super(cls, cls).__new__(cls, _store.get(var_id))

        def __int__(self):
            return _store.get(var_id)

        def __repr__(self) -> str:
            return f"{int(self)}"

        def __eq__(self, __o: object) -> bool:
            return int(self) == __o

    match initial:
        case int():
            return IntProxy(initial), setter


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
            blamed_value: tuple[int, str] = (value, inspect.getouterframes(inspect.currentframe(), 2)[1][3])
            self.record(self.mode, owner, instance_name, blamed_value)
        else:
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
    def pprint(cls):
        pp(cls._store)

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
