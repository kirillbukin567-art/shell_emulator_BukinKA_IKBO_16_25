"""Команды эмулятора. Команды ls и cd пока являются заглушками."""

from vfs import default_vfs


def print_stub(name, args):
    """Выводит имя команды и её аргументы."""
    print(f"{name}: аргументы {args}")


def cmd_ls(session, args):
    """Заглушка команды ls."""
    print_stub("ls", args)


def cmd_cd(session, args):
    """Заглушка команды cd."""
    print_stub("cd", args)


def cmd_vfs_init(session, args):
    """Заменяет текущую VFS на VFS по умолчанию."""
    if args:
        print("vfs-init: команда не принимает аргументов")
        return
    session.vfs = default_vfs()
    session.vfs_path = None
    print("vfs-init: загружена VFS по умолчанию")


def cmd_vfs_info(session, args):
    """Служебная команда: показывает состав текущей VFS."""
    vfs = session.vfs
    source = session.vfs_path or "встроенная"
    print(f"VFS «{vfs.name}», источник: {source}")
    print(f"каталогов: {len(vfs.dirs)}, файлов: {len(vfs.files)}")
    for path in sorted(vfs.dirs):
        print(f"  [dir]  {path}/")
    for path in sorted(vfs.files):
        print(f"  [file] {path} ({len(vfs.files[path])} байт)")


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
    "vfs-init": cmd_vfs_init,
    "vfs-info": cmd_vfs_info,
}


def execute(session, words):
    """Выполняет команду, заданную списком слов."""
    name = words[0]
    handler = COMMANDS.get(name)
    if handler is None:
        print(f"{name}: команда не найдена")
        return
    handler(session, words[1:])