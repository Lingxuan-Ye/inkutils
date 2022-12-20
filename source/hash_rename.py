from sys import version_info

assert version_info >= (3, 10)

import argparse
from pathlib import Path
from typing import Iterable, Literal, Optional

try:
    from .utils import Pavlov, filter, hexdigest
except ImportError:
    from utils import Pavlov, filter, hexdigest


def rename(
    path: Optional[Path | str] = None,
    include: Optional[Iterable[str]] = None,
    exclude: Optional[Iterable[str]] = None,
    prefix: Optional[str] = None,
    drop_suffix: bool = False,
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
        parent = Path() if flatten else path.parent
        suffix = '' if drop_suffix else ''.join(i.suffixes)
        new = path.rename(
            parent / (prefix + hexdigest(path, algorithm) + suffix)
        )
        if not quiet:
            print(f"'{path}' -> '{new}'.", end='\n\n')


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

    flatten = """
        if specified, extract renamed files in subdirectories to
        working directory
    """

    algorithm = """
        hash algorithm (available: 'md5', 'sha1', 'sha256' and 'sha512');
        use 'sha256' if invalid value passed in
    """

    quiet = """
        if specified, run quietly
    """


@Pavlov()
def main() -> None:
    parser = argparse.ArgumentParser('Hash-Rename')
    parser.add_argument('path', nargs='*', help=_Help.path)
    parser.add_argument(
        '-i',
        '--include',
        action='extend',
        nargs='+',
        help=_Help.include,
        metavar=''
    )
    parser.add_argument(
        '-e',
        '--exclude',
        action='extend',
        nargs='+',
        help=_Help.exclude,
        metavar=''
    )
    parser.add_argument('-p', '--prefix', help=_Help.prefix, metavar='')
    parser.add_argument(
        '-d',
        '--drop_suffix',
        action='store_true',
        help=_Help.drop_suffix
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
        help=_Help.algorithm,
        metavar=''
    )
    parser.add_argument(
        '-q',
        '--quiet',
        action='store_true',
        help=_Help.quiet
    )

    args = parser.parse_args()

    if not args.path:
        args.path.append(Path())

    for i in args.path:
        rename(
            i,
            args.include,
            args.exclude,
            args.prefix,
            args.drop_suffix,
            args.flatten,
            args.algorithm,
            args.quiet
        )


if __name__ == '__main__':
    main()
