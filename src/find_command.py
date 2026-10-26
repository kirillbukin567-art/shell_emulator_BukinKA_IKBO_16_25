"""Команда find: поиск файлов и каталогов в VFS."""

import fnmatch

from vfs import NO_SUCH, resolve

TYPE_FILE = "f"
TYPE_DIR = "d"
OPTION_SIZE = 2


def parse_find_args(args):
    """Разбирает аргументы find. Возвращает (пути, шаблон, тип) или None."""
    index = 0
    while index < len(args) and not args[index].startswith("-"):
        index += 1
    paths = args[:index]
    options = {"-name": None, "-type": None}
    rest = args[index:]
    while rest:
        flag = rest[0]
        if flag not in options:
            print(f"find: неизвестный аргумент: '{flag}'")
            return None
        if len(rest) < OPTION_SIZE:
            print(f"find: для '{flag}' не указано значение")
            return None
        options[flag] = rest[1]
        rest = rest[OPTION_SIZE:]
    if options["-type"] not in (None, TYPE_FILE, TYPE_DIR):
        print(f"find: неизвестный тип '{options['-type']}' (нужно f или d)")
        return None
    return paths or ["."], options["-name"], options["-type"]


def find_entries(vfs, arg, path):
    """Возвращает записи (вывод, путь в VFS, имя) для начала и потомков."""
    shown_base = arg.rstrip("/")
    entries = [(arg, path, shown_base.split("/")[-1] or "/")]
    cut = len(path) + 1 if path else 0
    for item in vfs.descendants(path):
        relative = item[cut:]
        shown = f"{shown_base}/{relative}"
        entries.append((shown, item, relative.split("/")[-1]))
    return entries


def keep(vfs, entry, pattern, kind):
    """Проверяет запись на соответствие условиям -name и -type."""
    _, path, name = entry
    if pattern is not None:
        if not fnmatch.fnmatchcase(name, pattern):
            return False
    if kind == TYPE_FILE:
        return vfs.is_file(path)
    if kind == TYPE_DIR:
        return vfs.is_dir(path)
    return True


def cmd_find(session, args):
    """Ищет в VFS: find [путь...] [-name шаблон] [-type f|d]."""
    parsed = parse_find_args(args)
    if parsed is None:
        return
    paths, pattern, kind = parsed
    vfs = session.vfs
    for arg in paths:
        path = resolve(session.cwd, arg)
        if not (vfs.is_dir(path) or vfs.is_file(path)):
            print(f"find: '{arg}': {NO_SUCH}")
            continue
        for entry in find_entries(vfs, arg, path):
            if keep(vfs, entry, pattern, kind):
                print(entry[0])