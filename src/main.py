"""Эмулятор оболочки UNIX: точка входа."""

import sys

from config import parse_args, print_debug
from session import Session
from shell import run_repl, run_script
from vfs import VfsError, default_vfs, load_vfs

EXIT_ERROR = 1


def create_session(vfs_path):
    """Создаёт сеанс: загружает VFS из файла или берёт VFS по умолчанию."""
    if vfs_path is None:
        return Session(default_vfs())
    try:
        return Session(load_vfs(vfs_path), vfs_path)
    except VfsError as error:
        print(f"Ошибка загрузки VFS: {error}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def run_startup_script(path, session):
    """Выполняет стартовый скрипт.

    Возвращает True, если после скрипта нужно продолжить работу.
    Если файл прочитать нельзя, завершает программу с ошибкой.
    """
    try:
        return run_script(path, session)
    except (OSError, UnicodeDecodeError) as error:
        print(f"Ошибка чтения скрипта: {error}", file=sys.stderr)
        sys.exit(EXIT_ERROR)


def main():
    """Точка входа приложения."""
    args = parse_args()
    print_debug(args)
    session = create_session(args.vfs)
    if args.script and not run_startup_script(args.script, session):
        return
    run_repl(session)


if __name__ == "__main__":
    main()