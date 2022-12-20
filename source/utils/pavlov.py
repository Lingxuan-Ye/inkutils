from functools import wraps
from typing import Callable, Optional


class Pavlov:
    """
    Decorator for command-line output.
    """
    __prolog = 'proceeding...'
    __epilog = 'press any key to exit...'

    def __init__(
        self,
        prolog: Optional[str] = None,
        epilog: Optional[str] = None
    ) -> None:
        if prolog is not None:
            self.prolog = prolog
        if epilog is not None:
            self.epilog = epilog

    @property
    def prolog(self) -> str:
        return self.__prolog + '\n'

    @prolog.setter
    def prolog(self, __value: str) -> None:
        self.__prolog = __value.strip()

    @property
    def epilog(self) -> str:
        return self.__epilog + '\n'

    @epilog.setter
    def epilog(self, __value: str) -> None:
        self.__epilog = __value.strip()

    def __call__(self, func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            print(self.prolog)
            print('\n\n', end='')
            result = func(*args, **kwargs)
            print('\n\n', end='')
            input(self.epilog)
            return result
        return wrapper
