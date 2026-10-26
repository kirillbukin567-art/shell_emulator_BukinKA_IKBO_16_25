"""Команды эмулятора. На этапе 1 команды ls и cd являются заглушками."""


def print_stub(name, args):
    """Выводит имя команды и её аргументы."""
    print(f"{name}: аргументы {args}")


def cmd_ls(args):
    """Заглушка команды ls."""
    print_stub("ls", args)


def cmd_cd(args):
    """Заглушка команды cd."""
    print_stub("cd", args)


COMMANDS = {
    "ls": cmd_ls,
    "cd": cmd_cd,
}


def execute(words):
    """Выполняет команду, заданную списком слов."""
    name = words[0]
    handler = COMMANDS.get(name)
    if handler is None:
        print(f"{name}: команда не найдена")
        return
    handler(words[1:])