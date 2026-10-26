"""Команды чтения файлов VFS: tac и tail."""

from vfs import NO_SUCH, resolve

DEFAULT_TAIL_LINES = 10
BINARY_MARK = b"\x00"
SINGLE_FILE = 1


def read_text(session, command, arg):
    """Возвращает текст файла VFS или None, выведя сообщение об ошибке."""
    vfs = session.vfs
    path = resolve(session.cwd, arg)
    if vfs.is_dir(path):
        print(f"{command}: {arg}: Это каталог")
        return None
    if not vfs.is_file(path):
        print(f"{command}: {arg}: {NO_SUCH}")
        return None
    data = vfs.files[path]
    if BINARY_MARK in data:
        print(f"{command}: {arg}: двоичный файл")
        return None
    return data.decode("utf-8", errors="replace")


def cmd_tac(session, args):
    """Выводит строки файлов в обратном порядке."""
    if not args:
        print("tac: отсутствует операнд файла")
        return
    for arg in args:
        text = read_text(session, "tac", arg)
        if text is not None:
            for line in reversed(text.splitlines()):
                print(line)


def parse_count(value):
    """Преобразует значение опции -n в число; при ошибке печатает текст."""
    if value is None:
        print("tail: опция -n требует аргумент")
        return None
    if not value.isdigit():
        print(f"tail: неверное число строк: '{value}'")
        return None
    return int(value)


def parse_tail_args(args):
    """Разбирает аргументы tail. Возвращает (число, файлы) или None."""
    count = DEFAULT_TAIL_LINES
    files = []
    arguments = iter(args)
    for arg in arguments:
        if arg == "-n":
            count = parse_count(next(arguments, None))
            if count is None:
                return None
        elif arg.startswith("-"):
            print(f"tail: неизвестная опция '{arg}'")
            return None
        else:
            files.append(arg)
    return count, files


def print_tail(session, arg, count, with_header):
    """Печатает последние строки одного файла."""
    text = read_text(session, "tail", arg)
    if text is None:
        return
    if with_header:
        print(f"==> {arg} <==")
    lines = text.splitlines()
    for line in lines[max(len(lines) - count, 0):]:
        print(line)


def cmd_tail(session, args):
    """Выводит последние строки файлов (по умолчанию 10, опция -n N)."""
    parsed = parse_args_or_none = parse_tail_args(args)
    if parsed is None:
        return
    count, files = parsed
    if not files:
        print("tail: отсутствует операнд файла")
        return
    with_header = len(files) > SINGLE_FILE
    for index, arg in enumerate(files):
        if with_header and index:
            print()
        print_tail(session, arg, count, with_header)