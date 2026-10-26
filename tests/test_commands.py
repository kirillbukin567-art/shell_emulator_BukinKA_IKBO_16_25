"""Тесты реестра команд и служебных команд VFS."""

import unittest

from session import Session
from tests.helpers import run_command
from vfs import build_vfs, default_vfs


class ExecuteTest(unittest.TestCase):
    """Проверки функции execute и команд vfs-init, vfs-info."""

    def setUp(self):
        """Создаёт сеанс с VFS по умолчанию."""
        self.session = Session(default_vfs())

    def test_unknown_command(self):
        """Неизвестная команда сообщает об ошибке."""
        output = run_command(self.session, "foo")
        self.assertIn("команда не найдена", output[0])

    def test_vfs_init_restores_default(self):
        """vfs-init возвращает VFS по умолчанию и сбрасывает состояние."""
        self.session.vfs = build_vfs("other", {"a.txt": b"x"})
        self.session.vfs_path = "data/other.b64"
        self.session.cwd = "docs"
        output = run_command(self.session, "vfs-init")
        self.assertEqual(self.session.vfs.name, "vfs")
        self.assertIsNone(self.session.vfs_path)
        self.assertEqual(self.session.cwd, "")
        self.assertIn("vfs-init", output[0])

    def test_vfs_init_rejects_arguments(self):
        """vfs-init с лишними аргументами выдаёт ошибку."""
        output = run_command(self.session, "vfs-init x")
        self.assertIn("не принимает", output[0])

    def test_vfs_info_lists_files(self):
        """vfs-info показывает файлы текущей VFS."""
        text = "\n".join(run_command(self.session, "vfs-info"))
        self.assertIn("readme.txt", text)


if __name__ == "__main__":
    unittest.main()