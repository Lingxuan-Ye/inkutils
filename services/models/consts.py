from pathlib import Path


def locate() -> Path:
    return Path(__file__).resolve()


def locate_root() -> Path:
    """
    This function depends on a strong assumption about
    the directory structure.
    """
    for i in locate().parents:
        if i.name == 'services':
            return i.parent
    return Path.home() / 'inkutils'


HOME = Path.home()

ROOT = locate_root()
DOCUMENTATION = ROOT / 'documentation'
LIBRARY = ROOT / 'library'
SCRIPTS = ROOT / 'scripts'
SERVICES = ROOT / 'services'
DOTFILES = ROOT / 'dotfiles'

CONFIG_GLOBAL = SERVICES / 'data/default.yml'
CONFIG_USER = ROOT / 'config.yml'

if ROOT.drive:
    ROOT_STR = '/' + ''.join(ROOT.as_posix().split(':', 1))
else:
    ROOT_STR = ROOT.as_posix()
