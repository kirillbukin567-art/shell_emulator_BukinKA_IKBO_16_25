"""Общие вспомогательные средства для тестов."""

import base64
import io
import os
import tempfile
import zipfile
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


def run_command(session, command):
    """Выполняет команду и возвращает список строк вывода.

    Команда задаётся строкой (делится по пробелам) или списком слов.
    """
    words = command.split() if isinstance(command, str) else list(command)
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        execute(session, words)
    return buffer.getvalue().splitlines()


def make_zip(entries):
    """Возвращает байты ZIP-архива с заданными записями."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for path, content in entries.items():
            archive.writestr(path, content)
    return buffer.getvalue()


def write_vfs_file(testcase, entries):
    """Создаёт временный файл VFS (base64 от ZIP), удаляемый после теста."""
    handle, path = tempfile.mkstemp(suffix=".b64")
    os.close(handle)
    testcase.addCleanup(os.remove, path)
    with open(path, "wb") as target:
        target.write(base64.encodebytes(make_zip(entries)))
    return path