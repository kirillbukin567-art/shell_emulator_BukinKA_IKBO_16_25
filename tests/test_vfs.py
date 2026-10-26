"""Тесты виртуальной файловой системы."""

import base64
import io
import os
import tempfile
import unittest
import zipfile

from vfs import VfsError, build_vfs, default_vfs, load_vfs, resolve


def make_zip(entries):
    """Возвращает байты ZIP-архива с заданными записями."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for path, content in entries.items():
            archive.writestr(path, content)
    return buffer.getvalue()


class BuildVfsTest(unittest.TestCase):
    """Проверки функции build_vfs."""

    def test_parent_dirs_created(self):
        """Для вложенного файла создаются все родительские каталоги."""
        vfs = build_vfs("t", {"a/b/c.txt": b"x"})
        self.assertEqual(vfs.dirs, {"a", "a/b"})
        self.assertEqual(vfs.files, {"a/b/c.txt": b"x"})

    def test_explicit_dir(self):
        """Запись со значением None считается каталогом."""
        vfs = build_vfs("t", {"empty/": None})
        self.assertEqual(vfs.dirs, {"empty"})
        self.assertEqual(vfs.files, {})

    def test_default_vfs_name(self):
        """VFS по умолчанию называется vfs."""
        self.assertEqual(default_vfs().name, "vfs")


class LoadVfsTest(unittest.TestCase):
    """Проверки функции load_vfs."""

    def write_file(self, suffix, data):
        """Создаёт временный файл с данными и возвращает путь."""
        handle, path = tempfile.mkstemp(suffix=suffix)
        os.close(handle)
        self.addCleanup(os.remove, path)
        with open(path, "wb") as target:
            target.write(data)
        return path

    def test_load_zip(self):
        """Обычный ZIP-файл загружается в память."""
        archive = make_zip({"docs/a.txt": b"hi"})
        vfs = load_vfs(self.write_file(".zip", archive))
        self.assertEqual(vfs.files["docs/a.txt"], b"hi")
        self.assertIn("docs", vfs.dirs)

    def test_load_base64_binary_data(self):
        """ZIP в base64 загружается, двоичные данные сохраняются."""
        archive = make_zip({"a.bin": b"\x00\x01\xff"})
        encoded = base64.encodebytes(archive)
        vfs = load_vfs(self.write_file(".b64", encoded))
        self.assertEqual(vfs.files["a.bin"], b"\x00\x01\xff")

    def test_name_from_file(self):
        """Имя VFS берётся из имени файла без расширения."""
        archive = make_zip({"a.txt": b""})
        path = self.write_file(".zip", archive)
        expected = os.path.splitext(os.path.basename(path))[0]
        self.assertEqual(load_vfs(path).name, expected)

    def test_missing_file(self):
        """Несуществующий файл вызывает VfsError."""
        with self.assertRaises(VfsError):
            load_vfs("no_such_file.b64")

    def test_not_an_archive(self):
        """Корректный base64, но не ZIP, вызывает VfsError."""
        path = self.write_file(".b64", base64.b64encode(b"hello"))
        with self.assertRaises(VfsError):
            load_vfs(path)

    def test_garbage(self):
        """Файл, не являющийся ни ZIP, ни base64, вызывает VfsError."""
        path = self.write_file(".b64", b"!!! not base64")
        with self.assertRaises(VfsError):
            load_vfs(path)


class ResolveTest(unittest.TestCase):
    """Проверки функции resolve."""

    def test_relative_path(self):
        """Относительный путь считается от текущего каталога."""
        self.assertEqual(resolve("home/user", "docs"), "home/user/docs")

    def test_absolute_path(self):
        """Абсолютный путь не зависит от текущего каталога."""
        self.assertEqual(resolve("home/user", "/etc"), "etc")

    def test_dots(self):
        """Части . и .. обрабатываются."""
        self.assertEqual(resolve("a/b", "../c/./d"), "a/c/d")

    def test_above_root(self):
        """Выше корня подняться нельзя."""
        self.assertEqual(resolve("", "../.."), "")

    def test_root(self):
        """Путь / ведёт в корень."""
        self.assertEqual(resolve("a", "/"), "")

    def test_repeated_slashes(self):
        """Повторные и конечные слеши игнорируются."""
        self.assertEqual(resolve("", "a//b/"), "a/b")


class VfsQueriesTest(unittest.TestCase):
    """Проверки методов Vfs."""

    def setUp(self):
        """Создаёт небольшую VFS."""
        entries = {"a/b/c.txt": b"x", "a/d.txt": b"y", "e.txt": b"z"}
        self.vfs = build_vfs("t", entries)

    def test_is_dir(self):
        """Корень и вложенные каталоги являются каталогами."""
        self.assertTrue(self.vfs.is_dir(""))
        self.assertTrue(self.vfs.is_dir("a/b"))
        self.assertFalse(self.vfs.is_dir("e.txt"))

    def test_is_file(self):
        """Файлы определяются по словарю файлов."""
        self.assertTrue(self.vfs.is_file("a/d.txt"))
        self.assertFalse(self.vfs.is_file("a"))

    def test_children_of_root(self):
        """У корня только прямые потомки."""
        self.assertEqual(self.vfs.children(""), ["a", "e.txt"])

    def test_children_of_directory(self):
        """У каталога a два прямых потомка."""
        self.assertEqual(self.vfs.children("a"), ["b", "d.txt"])

    def test_descendants_of_directory(self):
        """Потомки включают вложенные уровни."""
        expected = ["a/b", "a/b/c.txt", "a/d.txt"]
        self.assertEqual(self.vfs.descendants("a"), expected)

    def test_descendants_of_root(self):
        """У корня потомками являются все элементы."""
        self.assertEqual(len(self.vfs.descendants("")), 5)


if __name__ == "__main__":
    unittest.main()