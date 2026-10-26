"""Команды, изменяющие VFS (только в памяти): mkdir."""

from vfs import EXISTS, NO_SUCH, NOT_A_DIR, parent_dirs, parent_of, resolve


def parse_mkdir_args(args):
    """Разбирает аргументы mkdir. Возвращает (родители, пути) или None."""
    parents = False
    paths = []
    for arg in args:
        if arg == "-p":
            parents = True
        elif arg.startswith("-") and arg != "-":
            print(f"mkdir: неизвестная опция '{arg}'")
            return None
        else:
            paths.append(arg)
    return parents, paths


def fail(arg, reason):
    """Печатает ошибку создания каталога."""
    print(f"mkdir: невозможно создать каталог '{arg}': {reason}")


def make_with_parents(vfs, arg, path):
    """Создаёт каталог и недостающих родителей (mkdir -p)."""
    chain = parent_dirs(path) | {path}
    if any(vfs.is_file(item) for item in chain):
        fail(arg, NOT_A_DIR)
        return
    vfs.add_dir(path, with_parents=True)


def make_plain(vfs, arg, path):
    """Создаёт каталог, родитель которого уже должен существовать."""
    parent = parent_of(path)
    if vfs.is_file(parent):
        fail(arg, NOT_A_DIR)
    elif not vfs.is_dir(parent):
        fail(arg, NO_SUCH)
    else:
        vfs.add_dir(path)


def make_one(session, arg, parents):
    """Создаёт один каталог по аргументу командной строки."""
    vfs = session.vfs
    path = resolve(session.cwd, arg)
    if vfs.is_file(path) or vfs.is_dir(path):
        if not (parents and vfs.is_dir(path)):
            fail(arg, EXISTS)
        return
    if parents:
        make_with_parents(vfs, arg, path)
    else:
        make_plain(vfs, arg, path)


def cmd_mkdir(session, args):
    """Создаёт каталоги в VFS (только в памяти). Опция -p: с родителями."""
    parsed = parse_mkdir_args(args)
    if parsed is None:
        return
    parents, paths = parsed
    if not paths:
        print("mkdir: отсутствует операнд")
        return
    for arg in paths:
        make_one(session, arg, parents)