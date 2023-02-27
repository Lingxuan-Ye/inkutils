try:
    from numpy.random import normal

    def randrange(start: int, stop: int | None = None, step: int = 1) -> int:
        if stop is None:
            start, stop = 0, start
        mu: float = (start + stop) / 2
        sigma: float = abs(start - stop) / 6
        period, offset = divmod(normal(mu, sigma), step)
        period = int(period)
        towards_start_bias: float = abs(offset)
        towards_stop_bias: float = abs(step) - towards_start_bias
        if towards_start_bias < towards_stop_bias:
            return start + period * step
        return start + (period + 1) * step

except ImportError:
    from random import randrange
