#!/usr/bin/env python

from sys import version_info

assert version_info >= (3, 10)

import argparse
import json
from collections import UserDict
from pathlib import Path
from pprint import pprint
from typing import Literal, TypeVar

Self = TypeVar('Self', bound='Config')


class Config(UserDict):

    __instance: 'Config | None' = None
    __path: Path = Path('~/.inkonfig').expanduser()

    def __new__(cls, *args, **kwargs) -> 'Config':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, path: Path | str | None = None) -> None:
        self.set_path(path)
        self.data = {}

    def get_path(self) -> Path:
        return self.__path

    def set_path(self, __value: Path | str | None) -> None:
        if __value is None:
            return
        if isinstance(__value, str):
            __value = Path(__value).expanduser()
        assert isinstance(__value, Path)
        self.__path = __value

    path = property(fget=get_path, fset=set_path)

    def load(self: Self) -> Self:
        try:
            with open(self.__path, 'a+', encoding='utf-8') as f:
                f.seek(0)
                config = json.load(f)
        except json.JSONDecodeError:
            pass
        else:
            assert isinstance(config, dict)
            self.data.clear()
            self.data.update(config)
        return self

    def dump(self: Self) -> Self:
        with open(self.__path, 'w', encoding='utf-8', newline='\n') as f:
            json.dump(self.data, f, indent=4)
        return self

    def __enter__(self: Self) -> Self:
        return self.load()

    def __exit__(self, exc_type, exc_value, traceback) -> Literal[False]:
        self.dump()
        return False


config = Config()


class _Help:

    read = """
        read config value by given key;
        if value does not exist, return None;
        if option ommited, return all
    """

    write = """
        not implemented
    """


def main() -> None:
    parser = argparse.ArgumentParser('Inkonfig')

    io = parser.add_mutually_exclusive_group()
    io.add_argument('-r', '--read', help=_Help.read)
    io.add_argument(
        '-w',
        '--write',
        action='extend',
        nargs=2,
        help=_Help.write
    )

    args = parser.parse_args()

    with config:
        match (args.read, args.write):
            case (None, None):
                pprint(config)
            case (read, None):
                pprint(config.get(read))
            case (None, write):
                print(_Help.write)
            case (read, write):
                print(_Help.write)


if __name__ == '__main__':
    main()
