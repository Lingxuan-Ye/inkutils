from collections import UserDict
from pathlib import Path
from typing import Self

import yaml

from .consts import CONFIG_GLOBAL, CONFIG_USER


class Config(UserDict):
    """
    YAML files should be modified manually to keep them reader-friendly.
    """
    __instance: 'Config | None' = None

    def __new__(cls, *args, **kwargs) -> 'Config':
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, path: Path | str | None = None) -> None:
        self.data = {}
        self._set_path(path)

    def _get_path(self) -> Path:
        return self.__path

    def _set_path(self, __value: Path | str | None) -> None:
        if __value is None:
            __value = CONFIG_USER
        elif isinstance(__value, str):
            __value = Path(__value)
        assert isinstance(__value, Path)
        self.__path = __value

    path = property(fget=_get_path, fset=_set_path)

    def load(self) -> Self:
        self.data.clear()
        with open(CONFIG_GLOBAL, encoding='utf-8') as g:
            self.data.update(yaml.safe_load(g))
        with open(self.__path, encoding='utf-8') as u:
            self.data.update(yaml.safe_load(u))
        return self


def load(path: Path | str | None = None) -> Config:
    return Config(path).load()
