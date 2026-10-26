"""Тесты команд cd и ls."""

import unittest

from tests.helpers import make_session, run_command


class CdTest(unittest.TestCase):
    """Проверки команды cd."""

    def setUp(self):
        """Создаёт сеанс с тестовой VFS."""
        self.session = make_session()

    def test_cd_into_directory(self):
        """cd переходит в каталог."""
        run_command(self.session, "cd docs")
        self.assertEqual(self.session.cwd, "docs")

    def test_cd_relative_and_parent(self):
        """cd понимает вложенные пути и ..."""
        run_command(self.session, "cd docs/deep")
        run_command(self.session, "cd ..")
        self.assertEqual(self.session.cwd, "docs")

    def test_cd_absolute_path(self):
        """cd понимает абсолютный путь."""
        run_command(self.session, "cd docs")
        run_command(self.session, "cd /empty")
        self.assertEqual(self.session.cwd, "empty")

    def test_cd_without_args_goes_to_root(self):
        """cd без аргумента переходит в корень."""
        run_command(self.session, "cd docs")
        run_command(self.session, "cd")
        self.assertEqual(self.session.cwd, "")

    def test_cd_above_root_stays_in_root(self):
        """Выше корня подняться нельзя."""
        run_command(self.session, "cd ../..")
        self.assertEqual(self.session.cwd, "")

    def test_cd_missing_directory(self):
        """cd в несуществующий каталог выдаёт ошибку."""
        output = run_command(self.session, "cd nothing")
        self.assertEqual(self.session.cwd, "")
        self.assertIn("Нет такого файла или каталога", output[0])

    def test_cd_to_file(self):
        """cd в файл выдаёт ошибку."""
        output = run_command(self.session, "cd readme.txt")
        self.assertEqual(self.session.cwd, "")
        self.assertIn("Не является каталогом", output[0])

    def test_cd_too_many_arguments(self):
        """cd с двумя аргументами выдаёт ошибку."""
        output = run_command(self.session, "cd docs empty")
        self.assertIn("слишком много аргументов", output[0])


class LsTest(unittest.TestCase):
    """Проверки команды ls."""

    def setUp(self):
        """Создаёт сеанс с тестовой VFS."""
        self.session = make_session()

    def test_ls_root_hides_hidden_files(self):
        """ls без опций не показывает скрытые файлы."""
        output = run_command(self.session, "ls")
        expected = ["bin.dat", "docs", "empty", "long.txt", "readme.txt"]
        self.assertEqual(output, expected)

    def test_ls_all_shows_hidden(self):
        """ls -a показывает скрытые файлы."""
        output = run_command(self.session, "ls -a")
        self.assertEqual(output[0], ".hidden")

    def test_ls_long_format(self):
        """ls -l показывает тип и размер."""
        output = run_command(self.session, "ls -l docs")
        self.assertRegex(output[0], r"^- +2 a\.txt$")
        self.assertRegex(output[1], r"^d +- deep$")

    def test_ls_combined_flags(self):
        """Опции можно объединять: ls -la."""
        output = run_command(self.session, "ls -la")
        self.assertRegex(output[0], r"\.hidden$")

    def test_ls_relative_to_cwd(self):
        """ls без пути показывает текущий каталог."""
        run_command(self.session, "cd docs")
        output = run_command(self.session, "ls")
        self.assertEqual(output, ["a.txt", "deep"])

    def test_ls_file(self):
        """ls для файла показывает его имя."""
        output = run_command(self.session, "ls docs/a.txt")
        self.assertEqual(output, ["a.txt"])

    def test_ls_empty_directory(self):
        """ls пустого каталога ничего не печатает."""
        self.assertEqual(run_command(self.session, "ls empty"), [])

    def test_ls_multiple_paths(self):
        """При нескольких путях печатаются заголовки."""
        output = run_command(self.session, "ls docs empty")
        expected = ["docs:", "a.txt", "deep", "", "empty:"]
        self.assertEqual(output, expected)

    def test_ls_missing_path(self):
        """ls несуществующего пути выдаёт ошибку."""
        output = run_command(self.session, "ls nothing")
        self.assertIn("невозможно получить доступ", output[0])

    def test_ls_unknown_option(self):
        """Неизвестная опция выдаёт ошибку."""
        output = run_command(self.session, "ls -z")
        self.assertIn("неизвестная опция", output[0])


if __name__ == "__main__":
    unittest.main()