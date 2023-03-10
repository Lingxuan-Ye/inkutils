from pathlib import Path
from typing import Generator, Iterable


def filter(
    path: Path | str | None = None,
    include: Iterable[str] | None = None,
    exclude: Iterable[str] | None = None,
    recursive: bool = False
) -> Generator[Path, None, None]:
    """
    Parameters
    ----------
    path :
        Specify working directory. If None, use current working directory;
        If is a file, `include` and `exclude` will be omitted.
    include :
        Pass a Iterable of which every elements are str specifying file
        types to be included. Both suffix and extension are acceptable.
        If None, all files under working directory will be included.
    exclude :
        Pass a Iterable of which every elements are str specifying file
        types to be excluded. Both suffix and extension are acceptable.
        Due to the implementation, `exclude` is prior than `include`.
    recursive :
        If True, filter files recursively.
    """
    if path is None:
        path = Path()
    elif isinstance(path, str):
        path = Path(path)

    if path.is_file():
        yield path
        return None

    if include is not None:
        include = set(f'.{i.lstrip(".")}' for i in include)
    if exclude is not None:
        exclude = set(f".{i.lstrip('.')}" for i in exclude)

    paths = path.rglob('*') if recursive else path.glob('*')

    for i in paths:
        if not i.is_file():
            continue
        suffix = i.suffix
        suffixes = ''.join(i.suffixes)
        if exclude is not None:
            if suffix in exclude or suffixes in exclude:
                continue
        if include is not None:
            if suffix not in include and suffixes not in include:
                continue
        yield i
        
    return None
