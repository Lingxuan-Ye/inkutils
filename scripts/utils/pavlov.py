from functools import wraps
from typing import Callable


class Pavlov:
    """
    Decorator for command-line output.
    """
    prolog: str = ''
    epilog: str = 'Press any key to exit...'

    def __init__(
        self,
        prolog: str | None = None,
        epilog: str | None = None
    ) -> None:
        if prolog is not None:
            self.prolog = prolog
        if epilog is not None:
            self.epilog = epilog

    def __call__(self, func: Callable) -> Callable:

        @wraps(func)
        def wrapper(*args, **kwargs):
            print()
            print(self.prolog + '\n\n')
            result = func(*args, **kwargs)
            input('\n\n' + self.epilog)
            return result

        return wrapper


def pavlov(func: Callable) -> Callable:
    """
    Default decorator.
    """
    return Pavlov()(func)
