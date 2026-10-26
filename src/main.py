"""Эмулятор оболочки UNIX: точка входа."""

import sys

from config import parse_args, print_debug
from shell import run_repl, run_script

VFS_NAME = "vfs"
EXIT_ERROR = 1


def run_startup_script(path):
    """Выполняет стартовый скрипт.

    Возвращает True, если после скрипта нужно продолжить работу.
    Если файл прочитать нельзя, завершает программу с ошибкой.
    """
    try:
        return run_script(path, VFS_NAME)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Ошибка чтения скрипта: {error}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def main():
    """Точка входа приложения."""
    args = parse_args()
    print_debug(args)
    if args.script and not run_startup_script(args.script):
        return
    run_repl(VFS_NAME)


if __name__ == "__main__":
    main()