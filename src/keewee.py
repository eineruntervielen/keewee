from __future__ import annotations

import json
import datetime as dt
import inspect
import uuid
import logging

from functools import singledispatch
from pprint import pp
from typing import overload, cast, Any, Callable

from .keewee_repo import _repo

logging.basicConfig(level=logging.DEBUG)


def rec_mode_set(kw_store: dict[str, set | None], key: str, value: Any) -> None:
    if not kw_store.get(key):
        kw_store[key] = set()
    kw_store[key].add(value)


def rec_mode_list(kw_store: dict[str, list | None], key: str, value: Any) -> None:
    if not kw_store.get(key):
        kw_store[key] = []
    kw_store[key].append(value)


def rec_mode_dtv(kw_store: dict[str, dict[dt.time.isoformat, Any] | None], key: str, value: Any) -> None:
    if not kw_store.get(key):
        kw_store[key] = {}
    kw_store[key][dt.datetime.now().time().isoformat()] = value


RECORD_MODES: dict[str, Callable[..., None]] = {
    "list": rec_mode_list,
    "set": rec_mode_set,
    "dtv": rec_mode_dtv
}


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
        _repo[var_id] = value
        if mode is not None:
            record(mode, value)

    setter(initial)

    class IntProxy(int):
        def __new__(cls, value, *args, **kwargs):
            return super(cls, cls).__new__(cls, _repo.get(var_id))

        def __int__(self):
            return _repo.get(var_id)

        def __repr__(self) -> str:
            return f"{int(self)}"

        def __eq__(self, __o: object) -> bool:
            return int(self) == __o

    match initial:
        case int():
            return IntProxy(initial), setter


class KeeWee:
    """KeeWee implements the descriptor-protocol and hooks into a specific
    recording method for keeping the state
    """
    _repo = _repo

    def __init__(self, blame: bool = False, mode: str = "list"):
        self.blame = blame
        self.record_mode = RECORD_MODES.get(mode)
        self.public_name = ""
        self.private_name = ""

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
            self.record_mode(kw_store=self._repo[owner][self.public_name], key=instance_name, value=blamed_value)
        else:
            self.record_mode(kw_store=self._repo[owner][self.public_name], key=instance_name, value=value)

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
    def pprint(cls) -> None:
        pp(cls._repo)

    @classmethod
    def dump(cls, file_name: str):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(cls._repo, f)

    @classmethod
    def dumps(cls):
        return json.dumps(cls._repo)

    @classmethod
    def dumpd(cls):
        return cls._repo
