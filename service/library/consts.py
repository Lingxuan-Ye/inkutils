from pathlib import Path


def locate() -> Path:
    return Path(__file__).resolve()


def locate_root() -> Path:
    """
    This function depends on a strong assumption about
    the directory structure.
    """
    for i in locate().parents:
        if i.name == 'service':
            return i.parent
    return Path.home() / 'inkutils'


ROOT = locate_root()
DOCUMENTATION = ROOT / 'documentation'
LIBRARY = ROOT / 'library'
SCRIPT = ROOT / 'script'
SERVICE = ROOT / 'service'
TEMPLATE = ROOT / 'template'

CONFIG_GLOBAL = SERVICE / 'data/default.yml'
CONFIG_USER = ROOT / 'config.yml'
