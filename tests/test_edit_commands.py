"""Тесты команды mkdir."""

import unittest

from tests.helpers import make_session, run_command


class MkdirTest(unittest.TestCase):
    """Проверки команды mkdir."""

    def setUp(self):
        """Создаёт сеанс с тестовой VFS."""
        self.session = make_session()

    def test_creates_directory(self):
        """mkdir создаёт каталог в памяти."""
        output = run_command(self.session, "mkdir new")
        self.assertEqual(output, [])
        self.assertTrue(self.session.vfs.is_dir("new"))

    def test_creates_several_directories(self):
        """mkdir создаёт все перечисленные каталоги."""
        run_command(self.session, "mkdir one two")
        self.assertTrue(self.session.vfs.is_dir("one"))
        self.assertTrue(self.session.vfs.is_dir("two"))

    def test_relative_to_cwd(self):
        """Относительный путь считается от текущего каталога."""
        run_command(self.session, "cd docs")
        run_command(self.session, "mkdir inner")
        self.assertTrue(self.session.vfs.is_dir("docs/inner"))

    def test_absolute_path(self):
        """Абсолютный путь не зависит от текущего каталога."""
        run_command(self.session, "cd docs")
        run_command(self.session, "mkdir /top")
        self.assertTrue(self.session.vfs.is_dir("top"))

    def test_new_directory_visible_in_ls(self):
        """Созданный каталог виден в ls."""
        run_command(self.session, "mkdir zzz")
        self.assertIn("zzz", run_command(self.session, "ls"))

    def test_parents_option(self):
        """mkdir -p создаёт цепочку каталогов."""
        output = run_command(self.session, "mkdir -p x/y/z")
        self.assertEqual(output, [])
        for path in ("x", "x/y", "x/y/z"):
            self.assertTrue(self.session.vfs.is_dir(path))

    def test_parents_option_existing_is_silent(self):
        """mkdir -p для существующего каталога не выдаёт ошибку."""
        self.assertEqual(run_command(self.session, "mkdir -p docs"), [])

    def test_missing_parent(self):
        """Без -p отсутствие родителя выдаёт ошибку."""
        output = run_command(self.session, "mkdir nope/child")
        self.assertIn("Нет такого файла или каталога", output[0])
        self.assertFalse(self.session.vfs.is_dir("nope"))

    def test_existing_directory(self):
        """Существующий каталог выдаёт ошибку."""
        output = run_command(self.session, "mkdir docs")
        self.assertIn("Файл существует", output[0])

    def test_existing_file(self):
        """Файл с таким именем выдаёт ошибку, в том числе с -p."""
        for command in ("mkdir readme.txt", "mkdir -p readme.txt"):
            output = run_command(self.session, command)
            self.assertIn("Файл существует", output[0])

    def test_root_exists(self):
        """Корень уже существует."""
        output = run_command(self.session, "mkdir /")
        self.assertIn("Файл существует", output[0])

    def test_parent_is_file(self):
        """Если родитель — файл, выдаётся ошибка, с -p тоже."""
        for command in ("mkdir readme.txt/c", "mkdir -p readme.txt/c"):
            output = run_command(self.session, command)
            self.assertIn("Не является каталогом", output[0])

    def test_no_operand(self):
        """mkdir без аргументов выдаёт ошибку."""
        output = run_command(self.session, "mkdir")
        self.assertIn("отсутствует операнд", output[0])

    def test_unknown_option(self):
        """Неизвестная опция выдаёт ошибку."""
        output = run_command(self.session, "mkdir -z dir")
        self.assertIn("неизвестная опция", output[0])
        self.assertFalse(self.session.vfs.is_dir("dir"))

    def test_error_does_not_stop_other_arguments(self):
        """Ошибка по одному пути не мешает остальным."""
        output = run_command(self.session, "mkdir docs fresh")
        self.assertIn("Файл существует", output[0])
        self.assertTrue(self.session.vfs.is_dir("fresh"))


if __name__ == "__main__":
    unittest.main()