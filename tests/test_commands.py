"""Тесты команд эмулятора."""

import io
import unittest
from contextlib import redirect_stdout

from commands import execute
from session import Session
from vfs import build_vfs, default_vfs


def run_command(session, words):
    """Выполняет команду и возвращает всё, что она напечатала."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        execute(session, words)
    return buffer.getvalue()


class ExecuteTest(unittest.TestCase):
    """Проверки функции execute."""

    def setUp(self):
        """Создаёт сеанс с VFS по умолчанию."""
        self.session = Session(default_vfs())

    def test_ls_prints_name_and_args(self):
        """Заглушка ls печатает имя и аргументы."""
        output = run_command(self.session, ["ls", "-l", "/tmp"])
        self.assertIn("ls", output)
        self.assertIn("['-l', '/tmp']", output)

    def test_cd_prints_name_and_args(self):
        """Заглушка cd печатает имя и аргументы."""
        output = run_command(self.session, ["cd", "/home"])
        self.assertIn("cd", output)
        self.assertIn("['/home']", output)

    def test_unknown_command(self):
        """Неизвестная команда сообщает об ошибке."""
        output = run_command(self.session, ["foo"])
        self.assertIn("команда не найдена", output)

    def test_vfs_init_restores_default(self):
        """vfs-init возвращает VFS по умолчанию и забывает путь."""
        self.session.vfs = build_vfs("other", {"a.txt": b"x"})
        self.session.vfs_path = "data/other.b64"
        output = run_command(self.session, ["vfs-init"])
        self.assertEqual(self.session.vfs.name, "vfs")
        self.assertIsNone(self.session.vfs_path)
        self.assertIn("vfs-init", output)

    def test_vfs_init_rejects_arguments(self):
        """vfs-init с лишними аргументами выдаёт ошибку."""
        output = run_command(self.session, ["vfs-init", "x"])
        self.assertIn("не принимает", output)

    def test_vfs_info_lists_files(self):
        """vfs-info показывает файлы текущей VFS."""
        output = run_command(self.session, ["vfs-info"])
        self.assertIn("readme.txt", output)


if __name__ == "__main__":
    unittest.main()