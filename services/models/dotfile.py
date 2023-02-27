import re
import shlex
from pathlib import Path

from .tag import tagparse_s


class DotfileDeployer:

    source: Path
    to: Path
    delimiter = ('{%', '%}')

    __line: list[str]
    __tag_tokens: list[str]
    __line_pattern = re.compile(r'^(?P<lwhitespaces>\s*)(?P<body>.*)\n$')
    __stop_parsing = re.compile(r'^\s*#\s*stop\s*$', re.IGNORECASE)
    __whitespace = re.compile(r'\s')

    def __init__(
        self,
        source: Path | str,
        to: Path | str,
        *,
        delimiter: tuple[str, str] | None = None
    ) -> None:
        self.source = source if isinstance(source, Path) else Path(source)
        self.to = to if isinstance(to, Path) else Path(to)
        if delimiter is not None:
            self.delimiter = delimiter
        self.__line = []
        self.__tag_tokens = []

    def _line_inject(self, line: str) -> str:
        match = self.__line_pattern.fullmatch(line)
        assert match is not None
        self.__tag_tokens.clear()
        self.__line.clear()
        self.__line.append(match.group('lwhitespaces'))
        ld, rd = self.delimiter[0], self.delimiter[1]
        active: bool = False
        for token in shlex.split(match.group('body')):
            if not active:
                if not token.endswith(ld):
                    if self.__whitespace.search(token):
                        token = f'"{token}"'
                    self.__line.append(token + ' ')
                    continue
                if self.__whitespace.search(token):
                    token = f'"{token}"'
                    self.__line.append(token + ' ')
                    continue
                active = True
                self.__line.append(token.rstrip(ld))
                continue
            if (not token.startswith(rd)) or self.__whitespace.search(token):
                self.__tag_tokens.append(token)
                continue
            self.__line.append(shlex.quote(tagparse_s(self.__tag_tokens)))
            self.__tag_tokens.clear()
            if token := token.lstrip(rd):
                self.__line.append(token + ' ')
            active = False
        return ''.join(self.__line).rstrip() + '\n'

    def deploy(self) -> None:
        if self.to.exists():
            prev = Path(f'{self.to}.prev')
            if prev.exists():
                prev.unlink()
            self.to.rename(prev)
        with (
            open(self.source, encoding='utf-8') as src,
            open(self.to, 'w', encoding='utf-8') as to
        ):
            for line in src:
                if self.__stop_parsing.fullmatch(line):
                    break
                to.write(self._line_inject(line))
            for line in src:
                to.write(line)


def deploy_dotfile( source: Path | str, to: Path | str):
    DotfileDeployer(source, to).deploy()
