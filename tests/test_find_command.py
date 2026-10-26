"""Тесты команды find."""

import unittest

from tests.helpers import make_session, run_command


class FindTest(unittest.TestCase):
    """Проверки команды find."""

    def setUp(self):
        """Создаёт сеанс с тестовой VFS."""
        self.session = make_session()

    def test_find_all_from_cwd(self):
        """find без аргументов обходит текущий каталог."""
        output = run_command(self.session, "find")
        expected = [
            ".", "./.hidden", "./bin.dat", "./docs", "./docs/a.txt",
            "./docs/deep", "./docs/deep/b.txt", "./empty", "./long.txt",
            "./readme.txt",
        ]
        self.assertEqual(output, expected)

    def test_find_path(self):
        """find путь обходит указанный каталог."""
        output = run_command(self.session, "find docs")
        expected = ["docs", "docs/a.txt", "docs/deep", "docs/deep/b.txt"]
        self.assertEqual(output, expected)

    def test_name_filter(self):
        """-name фильтрует по шаблону имени."""
        output = run_command(self.session, "find -name *.txt")
        expected = [
            "./docs/a.txt", "./docs/deep/b.txt", "./long.txt",
            "./readme.txt",
        ]
        self.assertEqual(output, expected)

    def test_type_dir(self):
        """-type d оставляет только каталоги."""
        output = run_command(self.session, "find -type d")
        expected = [".", "./docs", "./docs/deep", "./empty"]
        self.assertEqual(output, expected)

    def test_type_file(self):
        """-type f оставляет только файлы."""
        output = run_command(self.session, "find docs -type f")
        self.assertEqual(output, ["docs/a.txt", "docs/deep/b.txt"])

    def test_name_and_type(self):
        """-name и -type работают вместе."""
        output = run_command(self.session, "find / -name b.txt -type f")
        self.assertEqual(output, ["/docs/deep/b.txt"])

    def test_from_subdirectory(self):
        """Относительный путь считается от текущего каталога."""
        run_command(self.session, "cd docs")
        output = run_command(self.session, "find deep")
        self.assertEqual(output, ["deep", "deep/b.txt"])

    def test_file_start(self):
        """find для файла выводит сам файл."""
        output = run_command(self.session, "find readme.txt")
        self.assertEqual(output, ["readme.txt"])

    def test_missing_path(self):
        """find несуществующего пути выдаёт ошибку."""
        output = run_command(self.session, "find nothing")
        self.assertIn("Нет такого файла или каталога", output[0])

    def test_bad_type(self):
        """Неверный тип выдаёт ошибку."""
        output = run_command(self.session, "find -type x")
        self.assertIn("неизвестный тип", output[0])

    def test_missing_value(self):
        """Условие без значения выдаёт ошибку."""
        output = run_command(self.session, "find -name")
        self.assertIn("не указано значение", output[0])

    def test_unknown_argument(self):
        """Неизвестный аргумент выдаёт ошибку."""
        output = run_command(self.session, "find -foo bar")
        self.assertIn("неизвестный аргумент", output[0])


if __name__ == "__main__":
    unittest.main()