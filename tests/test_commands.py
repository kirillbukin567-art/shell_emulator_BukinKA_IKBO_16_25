"""Тесты реестра команд и служебных команд VFS."""

import unittest

from session import Session
from tests.helpers import run_command, write_vfs_file
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

    def test_vfs_init_discards_changes(self):
        """vfs-init отбрасывает изменения, сделанные в памяти."""
        run_command(self.session, "mkdir temp")
        run_command(self.session, "vfs-init")
        self.assertFalse(self.session.vfs.is_dir("temp"))

    def test_vfs_init_rejects_arguments(self):
        """vfs-init с лишними аргументами выдаёт ошибку."""
        output = run_command(self.session, "vfs-init x")
        self.assertIn("не принимает", output[0])

    def test_vfs_info_lists_files(self):
        """vfs-info показывает файлы текущей VFS."""
        text = "\n".join(run_command(self.session, "vfs-info"))
        self.assertIn("readme.txt", text)


class VfsLoadTest(unittest.TestCase):
    """Проверки команды vfs-load."""

    def setUp(self):
        """Создаёт сеанс с VFS по умолчанию."""
        self.session = Session(default_vfs())

    def test_load_replaces_vfs(self):
        """vfs-load заменяет VFS, запоминает путь и сбрасывает каталог."""
        path = write_vfs_file(self, {"new/file.txt": b"data"})
        self.session.cwd = "docs"
        output = run_command(self.session, ["vfs-load", path])
        self.assertIn("загружена VFS", output[0])
        self.assertTrue(self.session.vfs.is_file("new/file.txt"))
        self.assertEqual(self.session.vfs_path, path)
        self.assertEqual(self.session.cwd, "")

    def test_load_discards_changes(self):
        """Повторная загрузка отбрасывает изменения в памяти."""
        path = write_vfs_file(self, {"a.txt": b"x"})
        run_command(self.session, ["vfs-load", path])
        run_command(self.session, "mkdir temp")
        run_command(self.session, ["vfs-load", path])
        self.assertFalse(self.session.vfs.is_dir("temp"))

    def test_load_missing_file_keeps_vfs(self):
        """При ошибке загрузки текущая VFS не меняется."""
        output = run_command(self.session, "vfs-load no_such_file.b64")
        self.assertIn("не удалось прочитать файл", output[0])
        self.assertEqual(self.session.vfs.name, "vfs")
        self.assertTrue(self.session.vfs.is_file("readme.txt"))

    def test_load_broken_file_keeps_vfs(self):
        """Неверный файл VFS выдаёт ошибку, VFS не меняется."""
        path = write_vfs_file(self, {"a.txt": b"x"})
        with open(path, "wb") as target:
            target.write(b"!!! not base64")
        output = run_command(self.session, ["vfs-load", path])
        self.assertIn("vfs-load", output[0])
        self.assertEqual(self.session.vfs.name, "vfs")

    def test_load_requires_one_argument(self):
        """vfs-load без аргументов и с лишними выдаёт ошибку."""
        for command in ("vfs-load", "vfs-load a b"):
            output = run_command(self.session, command)
            self.assertIn("нужен один аргумент", output[0])


if __name__ == "__main__":
    unittest.main()