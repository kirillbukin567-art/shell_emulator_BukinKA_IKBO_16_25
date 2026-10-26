"""Параметры командной строки эмулятора."""

import argparse

NOT_SET = "<не задан>"


def build_parser():
    """Создаёт разборщик параметров командной строки."""
    parser = argparse.ArgumentParser(
        prog="emulator",
        description="Эмулятор оболочки UNIX.",
    )
    parser.add_argument(
        "--vfs",
        metavar="ПУТЬ",
        help="путь к физическому расположению VFS",
    )
    parser.add_argument(
        "--script",
        metavar="ПУТЬ",
        help="путь к стартовому скрипту",
    )
    return parser


def parse_args(argv=None):
    """Разбирает параметры. argv=None означает sys.argv[1:]."""
    return build_parser().parse_args(argv)


def print_debug(args):
    """Выводит все заданные параметры запуска (отладочный вывод)."""
    print("[отладка] Параметры запуска:")
    print(f"[отладка]   --vfs    = {args.vfs or NOT_SET}")
    print(f"[отладка]   --script = {args.script or NOT_SET}")