from pathlib import Path
from typing import Any, Callable

from . import config
from .consts import ROOT_STR


class TagError(Exception):
    pass


class TagParser:

    registry: dict[str, Callable[..., Any]] = {}

    def __init__(self, tokens: list[str]) -> None:
        self.tag = tokens.pop(0)
        self.args = tokens

    @classmethod
    def register(cls, func: Callable[..., Any]) -> Callable[..., Any]:
        cls.registry[func.__name__.lstrip('_').lower()] = func
        return func

    def parse(self) -> Any:
        func = self.registry.get(self.tag)
        if func is not None:
            return func(*self.args)
        raise TagError(f"tag '{self.tag}' not supported")


def tagparse(tokens: list[str]) -> Any:
    return TagParser(tokens).parse()


def tagparse_s(tokens: list[str]) -> str:
    return str(tagparse(tokens))


@TagParser.register
def _config(key: str, *_) -> Any:
    """
    A key with `.` is considered invalid due to the implementation.
    """
    value: Any = config.load()
    try:
        for i in key.split('.'):
            # AssertionError if `value` is a str
            # (str is a Container as well)
            assert not isinstance(value, str)
            try:
                value = value[i]
            except:
                # IndexError if `int(i)` out of range
                # KeyError if `int(i)` is not in `value`
                # ValueError if `i` is invalid literal for `int()`
                value = value[int(i)]
    except (AssertionError, IndexError, KeyError, ValueError):
        raise TagError('key invalid')
    return value


@TagParser.register
def _root(*_) -> str:
    return ROOT_STR
