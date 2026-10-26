"""Эмулятор оболочки UNIX: точка входа и цикл REPL."""

from cmd_parser import parse_line
from commands import execute

VFS_NAME = "vfs"


def make_prompt(vfs_name):
    """Возвращает приглашение к вводу с именем VFS."""
    return f"{vfs_name}$ "


def run_repl(vfs_name):
    """Читает команды пользователя, пока не будет введён exit."""
    while True:
        try:
            line = input(make_prompt(vfs_name))
        except EOFError:
            print()
            break
        try:
            words = parse_line(line)
        except ValueError as error:
            print(f"Ошибка разбора: {error}")
            continue
        if not words:
            continue
        if words[0] == "exit":
            break
        execute(words)


def main():
    """Точка входа приложения."""
    run_repl(VFS_NAME)


if __name__ == "__main__":
    main()