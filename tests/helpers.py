"""Общие вспомогательные средства для тестов."""

import io
from contextlib import redirect_stdout

from commands import execute
from session import Session
from vfs import build_vfs

LONG_TEXT = "".join(f"{number}\n" for number in range(1, 13)).encode()

TEST_ENTRIES = {
    "readme.txt": b"line1\nline2\nline3\n",
    "docs/": None,
    "docs/a.txt": b"A\n",
    "docs/deep/b.txt": b"B1\nB2\n",
    ".hidden": b"h\n",
    "bin.dat": b"\x00\x01\x02",
    "empty/": None,
    "long.txt": LONG_TEXT,
}


def make_session():
    """Создаёт сеанс с тестовой VFS."""
    return Session(build_vfs("test", TEST_ENTRIES))


def run_command(session, line):
    """Выполняет команду из строки и возвращает список строк вывода."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        execute(session, line.split())
    return buffer.getvalue().splitlines()