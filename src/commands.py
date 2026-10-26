"""Реестр команд эмулятора."""

from file_commands import cmd_tac, cmd_tail
from find_command import cmd_find
from nav_commands import cmd_cd, cmd_ls
from vfs import default_vfs


def cmd_vfs_init(session, args):
    """Заменяет текущую VFS на VFS по умолчанию."""
    if args:
        print("vfs-init: команда не принимает аргументов")
        return
    session.vfs = default_vfs()
    session.vfs_path = None
    session.cwd = ""
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
    "tac": cmd_tac,
    "tail": cmd_tail,
    "find": cmd_find,
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