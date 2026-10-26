"""Выполнение команд: обработка строки, стартовый скрипт и цикл REPL."""

from cmd_parser import parse_line
from commands import execute

COMMENT_PREFIX = "#"


def make_prompt(vfs_name):
    """Возвращает приглашение к вводу с именем VFS."""
    return f"{vfs_name}$ "


def handle_line(line):
    """Выполняет одну строку. Возвращает False, если нужно выйти."""
    try:
        words = parse_line(line)
    except ValueError as error:
        print(f"Ошибка разбора: {error}")
        return True
    if not words:
        return True
    if words[0] == "exit":
        return False
    execute(words)
    return True


def is_skippable(line):
    """Истинно для пустых строк и комментариев."""
    stripped = line.strip()
    return not stripped or stripped.startswith(COMMENT_PREFIX)


def run_script(path, vfs_name):
    """Выполняет команды из файла, показывая ввод и вывод как диалог.

    Пустые строки и комментарии пропускаются, ошибочные строки
    выдают сообщение и тоже пропускаются. Возвращает False, если
    в скрипте встретилась команда exit.
    """
    with open(path, encoding="utf-8-sig") as script:
        for raw_line in script:
            line = raw_line.rstrip("\r\n")
            if is_skippable(line):
                continue
            print(f"{make_prompt(vfs_name)}{line}")
            if not handle_line(line):
                return False
    return True


def run_repl(vfs_name):
    """Читает команды пользователя, пока не будет введён exit."""
    while True:
        try:
            line = input(make_prompt(vfs_name))
        except EOFError:
            print()
            break
        if not handle_line(line):
            break