"""Implements an autovivification dictionary for global state recording and management"""
from __future__ import annotations

import datetime as dt
import inspect
import json

from pprint import pp
from typing import Any, Callable, cast, overload


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


def rec_mode_index_closure() -> Callable[[dict[str, Any], str, Any], None]:
    """Closure for storing the current index"""
    index = 0

    def rec_mode_index(kw_store: dict[str, Any], key: str, value: Any) -> None:
        """Collects the occurring values in dictionary that maps the current index
        the new value

        :param kw_store: The global KeeWee repository
        :param key: a string key
        :param value: any value added to a mapping of index to value
        """

        nonlocal index
        if not kw_store.get(key):
            kw_store[key] = {}
        kw_store[key][index] = value
        index += 1

    return rec_mode_index


def rec_mode_mean_closure() -> Callable[[dict[str, Any], str, Any], None]:
    """Closure for storing the current index for the calculation of the mean"""
    index = 1
    print(NotImplemented)

    def rec_mode_mean(kw_store: dict[str, Any], key: str, value: int | float) -> None:
        """Calculates the mean of all occurring values

         :param kw_store: The global KeeWee repository
         :param key: a string key
         :param value: numerical value
         """
        nonlocal index
        if not kw_store.get(key):
            kw_store[key] = value
        old_value = kw_store[key] * (index)
        kw_store[key] = (old_value + value) / index
        index += 1

    return rec_mode_mean


def rec_mode_dtv(kw_store: dict[str, dict[str, Any]], key: str, value: Any) -> None:
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
    """Sums all occurring values

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


DISPATCH_MODE: dict[str, Callable[..., None]] = {
    "direct": rec_mode_direct,
    "dtv": rec_mode_dtv,
    "idx": rec_mode_index_closure(),
    "list": rec_mode_list,
    "max": rec_mode_max,
    "mean": rec_mode_mean_closure(),
    "min": rec_mode_min,
    "set": rec_mode_set,
    "sum": rec_mode_sum,
}


class KeeWee:
    """KeeWee implements the descriptor-protocol and hooks into a specific
    recording method for keeping the state
    """
    _repo = KEEWEE_REPO

    def __init__(self, mode: str = "list", blame: bool = False, private: bool = False):
        self.blame = blame
        self.private = private
        self.record_mode = DISPATCH_MODE.get(mode, DISPATCH_MODE['list'])
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
        if self.private:
            calling_member = inspect.stack()[1].function
            if not hasattr(obj, calling_member):
                raise ValueError("not allowed")
        if obj is None:
            return self
        return cast(int, obj.__dict__.get(self.private_name))

    @classmethod
    def pprint(cls) -> None:
        pp(cls._repo)

    @classmethod
    def dump(cls, file_name: str):
        with open(file_name, "w", encoding="utf-8") as f:
            json.dump(cls._repo, f, default=str)

    @classmethod
    def dumps(cls):
        return json.dumps(cls._repo, default=str)

    @classmethod
    def dumpd(cls):
        return cls._repo

