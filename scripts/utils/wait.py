from time import perf_counter_ns
from typing import Literal


def wait(duration: int | float, unit: Literal['s', 'ms', 'ns'] = 'ms') -> None:
    match unit.lower():
        case 's':
            duration *= 10 ** 9
        case 'ms':
            duration *= 10 ** 6
        case 'ns':
            pass
        case _:
            raise ValueError('Invalid unit.')
    start: int = perf_counter_ns()
    while perf_counter_ns() - start < duration:
        pass
