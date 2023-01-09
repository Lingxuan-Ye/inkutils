#!/usr/bin/env python

from sys import version_info

assert version_info >= (3, 10)

from pathlib import Path

try:
    from .config import config
except ImportError:
    from config import config


def main() -> None:
    top_level_dir = str(Path(__file__).resolve().parent.parent)
    with config:
        config['top_level_dir'] = top_level_dir
    print(top_level_dir)


if __name__ == '__main__':
    main()
