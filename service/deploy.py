import subprocess
import sys
from pathlib import Path

from library.consts import ROOT, TEMPLATE

VENV_NAME = 'ink'
SINPPET = f'''
rm -rf "~/venv/{VENV_NAME}/"
python -m venv "~/venv/{VENV_NAME}/"
source "~/venv/{VENV_NAME}/Scripts/activate"
pip install --upgrade pip
pip install -r "{ROOT}/requirements.txt"
'''


def main() -> None:

    while True:
        reply = input('Install PyYAML(dependency)? [y/n]: ').lower()
        if reply.startswith('y'):
            subprocess.run('pip install PyYAML')
            from library.dotfile import deploy_dotfile
            break
        elif reply.startswith('n'):
            try:
                from library.dotfile import deploy_dotfile
            except ImportError:
                print('Missing dependencies.')
                sys.exit()
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    while True:
        reply = input('Deploy dotfiles? [y/n]: ').lower()
        if reply.startswith('y'):
            for i in TEMPLATE.rglob('*'):
                if not i.is_file():
                    continue
                deploy_dotfile(i, Path.home() / i.name)
            break
        elif reply.startswith('n'):
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    while True:
        reply = input('Deploy Python virtual environment? [y/n]: ').lower()
        if reply.startswith('y'):
            subprocess.run(
                SINPPET,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                shell=True
            )
            break
        elif reply.startswith('n'):
            break
        print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == '__main__':
    main()
