"""Команды навигации по VFS: cd и ls."""

from vfs import NO_SUCH, join_path, resolve

LS_FLAGS = {"l", "a"}
MAX_CD_ARGS = 1
SINGLE_PATH = 1


def cmd_cd(session, args):
    """Переходит в каталог VFS; без аргумента переходит в корень."""
    if len(args) > MAX_CD_ARGS:
        print("cd: слишком много аргументов")
        return
    target = resolve(session.cwd, args[0]) if args else ""
    vfs = session.vfs
    if vfs.is_file(target):
        print(f"cd: {args[0]}: Не является каталогом")
    elif not vfs.is_dir(target):
        print(f"cd: {args[0]}: {NO_SUCH}")
    else:
        session.cwd = target


def parse_ls_args(args):
    """Разбирает аргументы ls. Возвращает (флаги, пути) или None."""
    flags = set()
    paths = []
    for arg in args:
        if arg.startswith("-") and arg != "-":
            unknown = set(arg[1:]) - LS_FLAGS
            if unknown:
                print(f"ls: неизвестная опция -- '{sorted(unknown)[0]}'")
                return None
            flags.update(arg[1:])
        else:
            paths.append(arg)
    return flags, paths


def entry_line(vfs, path, name, long_format):
    """Формирует строку вывода ls для одного элемента."""
    if not long_format:
        return name
    if vfs.is_dir(path):
        return f"d {'-':>6} {name}"
    return f"- {len(vfs.files[path]):>6} {name}"


def list_directory(vfs, path, flags):
    """Печатает содержимое каталога."""
    names = vfs.children(path)
    if "a" not in flags:
        names = [name for name in names if not name.startswith(".")]
    for name in names:
        full_path = join_path(path, name)
        print(entry_line(vfs, full_path, name, "l" in flags))


def list_target(session, arg, flags, with_header):
    """Печатает результат ls для одного пути."""
    vfs = session.vfs
    path = resolve(session.cwd, arg)
    if vfs.is_file(path):
        name = path.split("/")[-1]
        print(entry_line(vfs, path, name, "l" in flags))
    elif not vfs.is_dir(path):
        print(f"ls: невозможно получить доступ к '{arg}': {NO_SUCH}")
    else:
        if with_header:
            print(f"{arg}:")
        list_directory(vfs, path, flags)


def cmd_ls(session, args):
    """Показывает каталог. Опции: -l (подробно), -a (скрытые файлы)."""
    parsed = parse_ls_args(args)
    if parsed is None:
        return
    flags, paths = parsed
    paths = paths or ["."]
    with_header = len(paths) > SINGLE_PATH
    for index, arg in enumerate(paths):
        if with_header and index:
            print()
        list_target(session, arg, flags, with_header)