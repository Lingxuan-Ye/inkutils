from sys import version_info

assert version_info >= (3, 10)

import hashlib
from pathlib import Path
from typing import Literal


class Digest:

    def __init__(
        self,
        path: Path | str,
        algorithm: Literal['md5', 'sha1', 'sha256', 'sha512'] = 'sha256'
    ) -> None:
        self.path = path
        self.set_algorithm(algorithm)
        self.__hash: 'hashlib._Hash' | None = None

    def set_algorithm(
        self,
        algorithm: Literal['md5', 'sha1', 'sha256', 'sha512']
    ) -> None:
        match algorithm.strip().lower():
            case 'md5':
                self.algorithm = hashlib.md5
            case 'sha1':
                self.algorithm = hashlib.sha1
            case 'sha256':
                self.algorithm = hashlib.sha256
            case 'sha512':
                self.algorithm = hashlib.sha512
            case _:
                raise ValueError(
                    f"value '{algorithm}' is invalid, "
                    "expect 'md5', 'sha1', 'sha256' or 'sha512'."
                )

    @property
    def hash(self) -> 'hashlib._Hash':
        if self.__hash is None:
            self.__hash = self.algorithm()
            with open(self.path, 'rb') as f:
                while True:
                    data = f.read(0x1000000)  # 16 MB
                    if not data:
                        break
                    self.__hash.update(data)
        return self.__hash

    def digest(self) -> bytes:
        return self.hash.digest()

    def hexdigest(self) -> str:
        return self.hash.hexdigest()


def digest(
    path: Path | str,
    algorithm: Literal['md5', 'sha1', 'sha256', 'sha512'] = 'sha256'
) -> bytes:
    return Digest(path, algorithm).digest()


def hexdigest(
    path: Path | str,
    algorithm: Literal['md5', 'sha1', 'sha256', 'sha512'] = 'sha256'
) -> str:
    return Digest(path, algorithm).hexdigest()
