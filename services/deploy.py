import subprocess
import sys
import venv

from models.consts import DOTFILES, HOME, ROOT

VENV_NAME = 'ink'


def main() -> None:

    while True:
        reply = input('Install PyYAML(dependency)? [y/n]: ').lower()
        if reply.startswith('y'):
            subprocess.run('pip install PyYAML')
            from models.dotfile import deploy_dotfile
            break
        elif reply.startswith('n'):
            try:
                from models.dotfile import deploy_dotfile
            except ImportError:
                print('Missing dependencies.')
                sys.exit()
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    while True:
        reply = input('Deploy dotfiles? [y/n]: ').lower()
        if reply.startswith('y'):
            for i in DOTFILES.rglob('*'):
                if not i.is_file():
                    continue
                deploy_dotfile(i, HOME / i.name)
            break
        elif reply.startswith('n'):
            break
        print("Invalid input. Please enter 'y' or 'n'.")

    while True:
        reply = input('Deploy Python virtual environment? [y/n]: ').lower()
        if reply.startswith('y'):
            dir = HOME / f'venv/{VENV_NAME}'
            if not dir.exists():
                venv.main([str(dir)])
            root = ROOT.as_posix()
            subprocess.run(
                f'{dir}/Scripts/pip install -r {root}/requirements.txt'
            )
            break
        elif reply.startswith('n'):
            break
        print("Invalid input. Please enter 'y' or 'n'.")


if __name__ == '__main__':
    main()
