#!/usr/bin/env python

from sys import version_info

assert version_info >= (3, 10)

import argparse
import re
from collections import Counter
from pathlib import Path
from textwrap import dedent
from typing import Iterable, Sequence

from utils import filter, pavlov


class _Stats(Counter):

    __header = 'STATISTICS'
    __sep = '='
    __description = ''

    def __init__(
        self,
        header: str | None = None,
        sep: str | None = None,
        description: str | None = None
    ) -> None:
        if header is not None:
            self.header = header
        if sep is not None:
            self.sep = sep
        if description is not None:
            self.description = description

    @property
    def header(self) -> str:
        return self.__header + '\n'

    @header.setter
    def header(self, __value: str) -> None:
        self.__header = __value.strip()

    @property
    def sep(self) -> str:
        return self.__sep

    @sep.setter
    def sep(self, __value: str) -> None:
        assert len(__value) == 1
        self.__sep = __value

    @property
    def seps(self) -> str:
        return self.__sep * 36 + '\n'

    @property
    def description(self) -> str:
        if self.__description:
            return self.__description + '\n\n'
        return self.__description

    @description.setter
    def description(self, __value: str) -> None:
        self.__description = __value.strip()

    def line(self, key: str, name: str | None = None) -> str:
        name = key.title() if name is None else name
        return f'{name + ":":<28}{self[key]:>8}\n'

    def __str__(self) -> str:
        return ''.join((
            self.header,
            self.seps,
            self.description,
            self.line('paragraphs'),
            self.line('non_blank_lines', 'Non-Blank Lines'),
            self.line('lines'),
            '\n',
            self.line('words'),
            self.line('cjk', 'Chinese'),
            self.line('hiragana'),
            self.line('katakana'),
            self.line('punctuations'),
            self.line('whitespaces'),
            self.line('others', 'Other Characters'),
            '\n',
            self.line('chars_no_spaces', 'Characters (no spaces)'),
            self.line('chars_with_spaces', 'Characters (with spaces)')
        ))


_PATTERN: re.Pattern = re.compile(
    r'([\u4E00-\u9FFF\u3400-\u4DBF\U00020000-\U0002A6DF\U0002A700-\U0002EBEF\U00030000-\U0003134F])|'
    r'([\u3040-\u309F])|'
    r'([\u30A0-\u30FF])|'
    r'(\w)|'
    r'(\S)|'
    r'((\s*\n)+)|'
    r'(\s)|'
    r'(.)'
)


def statistics(
    path: Path | str | None = None,
    include: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
    recursive: bool = False,
    verbose: bool = False
) -> None:

    if path is None:
        path = Path()
    elif isinstance(path, str):
        path = Path(path)

    if verbose:
        inventory: list[_Stats] = []

    stats = _Stats()
    count = 0
    for i in filter(path, include, exclude, recursive):
        try:
            with open(i, encoding='utf-8') as f:
                _raw = f.read()
        except UnicodeDecodeError:
            continue

        count += 1

        _stats = _Stats(str(i), '-')
        _groups: list[tuple[str, ...]] = _PATTERN.findall(_raw)

        if not _groups:
            continue

        for j, k, l, m, n, o, _, p, q in _groups:  # `_` for '(\s*\n)'
            if j:  # CJK Unified Ideographs and CJK Extension
                _stats['cjk'] += 1
                _stats['words'] += 1
            elif k:  # Hiragana
                _stats['hiragana'] += 1
                _stats['words'] += 1
            elif l:  # Katakana
                _stats['katakana'] += 1
                _stats['words'] += 1
            elif m:  # r'\w'
                _stats['words'] += 1
            elif n:  # r'\S'
                _stats['punctuations'] += 1
            elif o:  # r'(\s*\n)+'
                _linefeeds: int = o.count('\n')
                if _linefeeds > 1:
                    _stats['paragraphs'] += 1
                _stats['non_blank_lines'] += 1
                _stats['lines'] += _linefeeds
                _stats['whitespaces'] += len(p)
            elif p:  # r'\s'
                _stats['whitespaces'] += 1
            elif q: # r'.'
                _stats['others'] += 1

        _linefeeds_at_EOF: int = _groups[-1][6].count('\n')
        if _linefeeds_at_EOF == 0:
            _stats['paragraphs'] += 1
            _stats['non_blank_lines'] += 1
            _stats['lines'] += 1
        elif _linefeeds_at_EOF == 1:
            _stats['paragraphs'] += 1
        _stats['chars_no_spaces'] = _stats['words'] + _stats['punctuations'] + _stats['others']
        _stats['chars_with_spaces'] = _stats['chars_no_spaces'] + _stats['whitespaces']
        stats.update(_stats)

        if verbose:
            inventory.append(_stats)

    stats.description = f'{"Files:":<28}{count:>8}'

    message = str(stats)

    if verbose:
        details = '\n\n'.join(str(i) for i in inventory)
        message += (
            '\n'
            '\n'
            '\n'
            'DETAILS\n' +
            stats.seps +
            '\n'
            '\n' +
            details
        )

    print(message)


class _Help:

    path = """
        specify working directory; if omitted, use current
        working directory; if is a file, `include` and `exclude`
        will be omitted
    """

    include = """
        specify file types to be counted with their suffixes/extensions;
        if omitted, all files under working directory not excluded
        will be counted
    """

    exclude = """
        specify file types to be excluded with their suffixes/extensions
    """

    recursive = """
        count files recursively
    """

    verbose = """
        print verbosely
    """


@pavlov
def main(args: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser('Stats')
    parser.add_argument('path', nargs='?', help=_Help.path)
    parser.add_argument(
        '-i',
        '--include',
        action='extend',
        nargs='+',
        help=_Help.include,
        metavar=''
    )
    parser.add_argument(
        '-x',
        '--exclude',
        action='extend',
        nargs='+',
        help=_Help.exclude,
        metavar=''
    )
    parser.add_argument(
        '-r',
        '--recursive',
        action='store_true',
        help=_Help.recursive
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help=_Help.verbose
    )

    options = parser.parse_args(args)

    statistics(
        options.path,
        options.include,
        options.exclude,
        options.recursive,
        options.verbose
    )


if __name__ == '__main__':
    main()
