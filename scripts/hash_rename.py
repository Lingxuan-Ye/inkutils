#!/usr/bin/env python

from sys import version_info

assert version_info >= (3, 10)

import argparse
from pathlib import Path
from typing import Iterable, Literal, Sequence

from utils import filter, hexdigest, pavlov


def rename(
    path: Path | str | None = None,
    include: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
    prefix: str | None = None,
    drop_suffix: bool = False,
    case_: Literal['lower', 'upper', 'keep'] = 'lower',
    flatten: bool = False,
    algorithm: Literal['md5', 'sha1', 'sha256', 'sha512'] = 'sha256',
    quiet: bool = False
) -> None:
    """
    Parameters
    ----------
    path :
        Specify working directory. If None, use current working directory;
        If is a file, `include` and `exclude` will be omitted.
    include :
        Pass a Iterable of which every elements are str specifying file
        types to be renamed. Both suffix and extension are acceptable.
        If None, all files under working directory not excluded
        will be renamed.
    exclude :
        Pass a Iterable of which every elements are str specifying file
        types to be excluded. Both suffix and extension are acceptable.
        Due to the implementation, `exclude` is prior to `include`.
    prefix :
        Prefix before hash digest. May be expansible in future version.
    drop_suffix :
        If True, drop file suffix.
    case_ :
        Set file name case.
    flatten :
        If True, extract renamed files in subdirectories to working directory.
    algorithm :
        Specify hash algorithm.
    quiet :
        If True, run quietly.
    """
    if path is None:
        path = Path()
    elif isinstance(path, str):
        path = Path(path)

    if prefix is None:
        prefix = ''

    for i in filter(path, include, exclude):
        parent = Path() if flatten else i.parent
        suffix = '' if drop_suffix else ''.join(i.suffixes)
        name = prefix + hexdigest(i, algorithm) + suffix
        match case_.lower():
            case 'lower':
                name = name.lower()
            case 'upper':
                name = name.upper()
            case 'keep':
                pass
            case _:
                raise ValueError(
                    f"value '{case_}' is invalid, "
                    "expect 'lower', 'upper' or 'keep'."
                )
        new = i.rename(parent / name)
        if not quiet:
            print(f"'{i}' -> '{new}'.", end='\n\n')


class _Help:

    path = """
        specify working directory; if omitted, use current
        working directory; if is a file, `--include` and `--exclude`
        will be omitted
    """

    include = """
        specify file types to be renamed with their suffixes/extensions;
        if omitted, all files under working directory not excluded
        will be renamed
    """

    exclude = """
        specify file types to be excluded with their suffixes/extensions;
        this option is prior to `--include`
    """

    prefix = """
        prefix before hash digest
    """

    drop_suffix = """
        if specified, drop file suffix
    """

    case = """
        set file name case (available: 'lower', 'upper' and 'keep')
    """

    flatten = """
        if specified, extract renamed files in subdirectories to
        working directory
    """

    algorithm = """
        hash algorithm (available: 'md5', 'sha1', 'sha256' and 'sha512')
    """

    quiet = """
        if specified, run quietly
    """


@pavlov
def main(args: Sequence[str] | None = None) -> None:
    parser = argparse.ArgumentParser('Hash-Rename')
    parser.add_argument('path', nargs='*', help=_Help.path)
    parser.add_argument(
        '-i',
        '--include',
        action='extend',
        nargs='+',
        help=_Help.include
    )
    parser.add_argument(
        '-x',
        '--exclude',
        action='extend',
        nargs='+',
        help=_Help.exclude
    )
    parser.add_argument('-p', '--prefix', help=_Help.prefix, metavar='')
    parser.add_argument(
        '-d',
        '--drop_suffix',
        action='store_true',
        help=_Help.drop_suffix
    )
    parser.add_argument(
        '-c',
        '--case',
        choices=('lower', 'upper', 'keep'),
        default='lower',
        help=_Help.case
    )
    parser.add_argument(
        '-f',
        '--flatten',
        action='store_true',
        help=_Help.flatten
    )
    parser.add_argument(
        '-a',
        '--algorithm',
        choices=('md5', 'sha1', 'sha256', 'sha512'),
        default='sha256',
        help=_Help.algorithm
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help=_Help.quiet
    )

    options = parser.parse_args(args)

    if not options.path:
        options.path.append(Path())

    for i in options.path:
        rename(
            i,
            options.include,
            options.exclude,
            options.prefix,
            options.drop_suffix,
            options.case,
            options.flatten,
            options.algorithm,
            options.quiet
        )


if __name__ == '__main__':
    main()
