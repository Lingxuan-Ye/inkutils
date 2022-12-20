from sys import version_info

assert version_info >= (3, 10)

import argparse
import re
from collections import Counter
from pathlib import Path
from typing import Iterable, Optional

try:
    from .utils import Pavlov, filter
except ImportError:
    from utils import Pavlov, filter


class _Stats(Counter):

    __header = 'STATISTICS'
    __sep = '='

    def __init__(
        self,
        header: Optional[str] = None,
        sep: Optional[str] = None
    ) -> None:
        if header is not None:
            self.header = header
        if sep is not None:
            self.sep = sep

    @property
    def header(self) -> str:
        return self.__header  + '\n'

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

    def line(self, key: str, name: Optional[str] = None) -> str:
        name = key.title() if name is None else name
        return f'{name + ":":<28}{self[key]:>8}\n'

    def __str__(self) -> str:
        return ''.join((
            self.header,
            self.seps,
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


def statistics(
    path: Optional[Path | str] = None,
    include: Optional[Iterable[str]] = None,
    exclude: Optional[Iterable[str]] = None,
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
    for i in filter(path, include, exclude, recursive):
        try:
            with open(i, encoding='utf-8') as f:
                _raw = f.read()
        except UnicodeDecodeError:
            continue
        _stats = _Stats(str(path), '-')
        _groups: list[tuple[str, ...]] = re.findall(
            r'([\u4E00-\u9FFF])|'
            r'([\u3400-\u4DBF\U00020000-\U0002A6DF\U0002A700-\U0002EBEF\U00030000-\U0003134F])|'
            r'([\u3040-\u309F])|'
            r'([\u30A0-\u30FF])|'
            r'(\w)|'
            r'(\S)|'
            r'((\s*\n)+)|'
            r'(\s)|'
            r'(.)',
            _raw
        )
        for j, k, l, m, n, o, p, _, q, r in _groups:
            # note that bool('') is False
            if j:  # CJK Unified Ideographs
                _stats['cjk'] += 1
                _stats['words'] += 1
            elif k:  # CJK Extension
                _stats['cjk'] += 1
                _stats['words'] += 1
            elif l:  # Hiragana
                _stats['hiragana'] += 1
                _stats['words'] += 1
            elif m:  # Katakana
                _stats['katakana'] += 1
                _stats['words'] += 1
            elif n:  # r'\w'
                _stats['words'] += 1
            elif o:  # r'\S'
                _stats['punctuations'] += 1
            elif p:  # r'(\s*\n)+'
                _linefeeds: int = p.count('\n')
                if _linefeeds > 1:
                    _stats['paragraphs'] += 1
                _stats['non_blank_lines'] += 1
                _stats['lines'] += _linefeeds
                _stats['whitespaces'] += len(p)
            elif q:  # r'\s'; note that bool(' ') is True
                _stats['whitespaces'] += 1
            elif r: # r'.'
                _stats['others'] += 1
        _linefeeds_at_EOF: int = _groups[-1][7].count('\n')
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

    message = str(stats)

    if verbose:
        message += '\n\n' + '\n'.join((
            f"DETAILS\n{'=' * 40}\n",
            *(str(i) for i in inventory)
        ))

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


@Pavlov()
def main():
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

    args = parser.parse_args()

    statistics(
        args.path,
        args.include,
        args.exclude,
        args.recursive,
        args.verbose
    )


if __name__ == '__main__':
    main()
