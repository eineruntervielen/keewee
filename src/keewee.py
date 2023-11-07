"""Implements an autovivification dictionary for global state recording and management"""
from __future__ import annotations

import datetime as dt
import inspect
import json

from pprint import pp
from typing import overload, cast, Any, Callable, TypeAlias

ISOFormat: TypeAlias = str


class KeeWeeRepo(dict):
    """Global application state repository for recording and management.
    Implements the missing-dunder method for autovivification."""

    def __missing__(self, kee):
        wee = self[kee] = type(self)()
        return wee


KEEWEE_REPO = KeeWeeRepo()


def rec_mode_direct(kw_store: dict[str, set], key: str, value: Any) -> None:
    """default mode that sets a value for a key into a dictionary

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: any value
    """
    kw_store[key] = value


def rec_mode_set(kw_store: dict[str, set], key: str, value: Any) -> None:
    """Collects the occurring values in a set.

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: any value added to a set
    """
    if not kw_store.get(key):
        kw_store[key] = set()
    kw_store[key].add(value)


def rec_mode_list(kw_store: dict[str, list], key: str, value: Any) -> None:
    """Collects the occurring values in a list.

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: any value added to a list
    """
    if not kw_store.get(key):
        kw_store[key] = []
    kw_store[key].append(value)


def rec_mode_dtv(kw_store: dict[str, dict[ISOFormat, Any]], key: str, value: Any) -> None:
    """Collects the occurring values in dictionary that maps the current timestamp
    in ISO-format to the new value

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: any value added to a mapping of timestamp to value
    """
    if not kw_store.get(key):
        kw_store[key] = {}
    kw_store[key][dt.datetime.now().time().isoformat()] = value


def rec_mode_sum(kw_store: dict[str, int | float], key: str, value: int | float) -> None:
    """Sums al occurring values

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: numerical value
    """
    if kw_store.get(key) is None:
        kw_store[key] = value
    else:
        kw_store[key] += value


def rec_mode_max(kw_store: dict[str, int | float], key: str, value: int | float) -> None:
    """Stores the maximum of all occurring values

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: numerical value
    """
    if kw_store.get(key) is None:
        kw_store[key] = value
    kw_store[key] = max(kw_store.get(key), value)


def rec_mode_min(kw_store: dict[str, int | float], key: str, value: int | float) -> None:
    """Stores the minimum of all occurring values

    :param kw_store: The global KeeWee repository
    :param key: a string key
    :param value: numerical value
    """
    if kw_store.get(key) is None:
        kw_store[key] = value
    kw_store[key] = min(kw_store.get(key), value)


RECORD_MODES: dict[str, Callable[..., None]] = {
    "direct": rec_mode_direct,
    "list": rec_mode_list,
    "set": rec_mode_set,
    "dtv": rec_mode_dtv,  # iso-format
    "sum": rec_mode_sum,
    "max": rec_mode_max,
    "min": rec_mode_min,
}


class KeeWee:
    """KeeWee implements the descriptor-protocol and hooks into a specific
    recording method for keeping the state
    """
    _repo = KEEWEE_REPO

    def __init__(self, mode: str = "list", blame: bool = False):
        self.blame = blame
        self.record_mode = RECORD_MODES.get(mode, RECORD_MODES['list'])
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

