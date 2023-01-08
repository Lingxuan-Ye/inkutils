from functools import wraps
from typing import Callable


class Pavlov:
    """
    Decorator for command-line output.
    """
    __prolog: str = ''
    __epilog: str = 'press any key to exit...'

    def __init__(
        self,
        prolog: str | None = None,
        epilog: str | None = None
    ) -> None:
        if prolog is not None:
            self.prolog = prolog
        if epilog is not None:
            self.epilog = epilog

    @property
    def prolog(self) -> str:
        return self.__prolog

    @prolog.setter
    def prolog(self, __value: str) -> None:
        self.__prolog = __value.strip()

    @property
    def epilog(self) -> str:
        return self.__epilog

    @epilog.setter
    def epilog(self, __value: str) -> None:
        self.__epilog = __value.strip()

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print()
            print(self.prolog + '\n\n')
            result = func(*args, **kwargs)
            input('\n\n' + self.epilog)
            return result
        return wrapper
