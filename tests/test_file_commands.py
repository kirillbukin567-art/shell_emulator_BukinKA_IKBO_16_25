"""Тесты команд tac и tail."""

import unittest

from tests.helpers import make_session, run_command


class TacTest(unittest.TestCase):
    """Проверки команды tac."""

    def setUp(self):
        """Создаёт сеанс с тестовой VFS."""
        self.session = make_session()

    def test_reverses_lines(self):
        """tac выводит строки в обратном порядке."""
        output = run_command(self.session, "tac readme.txt")
        self.assertEqual(output, ["line3", "line2", "line1"])

    def test_several_files(self):
        """tac обрабатывает несколько файлов по очереди."""
        output = run_command(self.session, "tac docs/a.txt docs/deep/b.txt")
        self.assertEqual(output, ["A", "B2", "B1"])

    def test_no_operand(self):
        """tac без файла выдаёт ошибку."""
        output = run_command(self.session, "tac")
        self.assertIn("отсутствует операнд", output[0])

    def test_missing_file(self):
        """tac несуществующего файла выдаёт ошибку."""
        output = run_command(self.session, "tac nothing")
        self.assertIn("Нет такого файла или каталога", output[0])

    def test_directory(self):
        """tac каталога выдаёт ошибку."""
        output = run_command(self.session, "tac docs")
        self.assertIn("Это каталог", output[0])

    def test_binary_file(self):
        """tac двоичного файла выдаёт ошибку."""
        output = run_command(self.session, "tac bin.dat")
        self.assertIn("двоичный файл", output[0])


class TailTest(unittest.TestCase):
    """Проверки команды tail."""

    def setUp(self):
        """Создаёт сеанс с тестовой VFS."""
        self.session = make_session()

    def test_default_ten_lines(self):
        """По умолчанию tail выводит 10 последних строк."""
        output = run_command(self.session, "tail long.txt")
        expected = [str(number) for number in range(3, 13)]
        self.assertEqual(output, expected)

    def test_short_file_prints_all(self):
        """Если строк меньше 10, выводится весь файл."""
        output = run_command(self.session, "tail readme.txt")
        self.assertEqual(output, ["line1", "line2", "line3"])

    def test_n_option(self):
        """Опция -n задаёт число строк."""
        output = run_command(self.session, "tail -n 2 long.txt")
        self.assertEqual(output, ["11", "12"])

    def test_n_zero(self):
        """tail -n 0 ничего не выводит."""
        self.assertEqual(run_command(self.session, "tail -n 0 long.txt"), [])

    def test_several_files_headers(self):
        """Для нескольких файлов печатаются заголовки."""
        output = run_command(
            self.session, "tail -n 1 docs/a.txt docs/deep/b.txt"
        )
        expected = [
            "==> docs/a.txt <==", "A", "",
            "==> docs/deep/b.txt <==", "B2",
        ]
        self.assertEqual(output, expected)

    def test_bad_count(self):
        """Нечисловое значение -n выдаёт ошибку."""
        output = run_command(self.session, "tail -n x long.txt")
        self.assertIn("неверное число строк", output[0])

    def test_n_without_value(self):
        """-n без значения выдаёт ошибку."""
        output = run_command(self.session, "tail -n")
        self.assertIn("требует аргумент", output[0])

    def test_negative_count(self):
        """Отрицательное значение -n выдаёт ошибку."""
        output = run_command(self.session, "tail -n -3 long.txt")
        self.assertIn("неверное число строк", output[0])

    def test_unknown_option(self):
        """Неизвестная опция выдаёт ошибку."""
        output = run_command(self.session, "tail -q long.txt")
        self.assertIn("неизвестная опция", output[0])

    def test_no_operand(self):
        """tail без файла выдаёт ошибку."""
        output = run_command(self.session, "tail")
        self.assertIn("отсутствует операнд", output[0])

    def test_missing_file(self):
        """tail несуществующего файла выдаёт ошибку."""
        output = run_command(self.session, "tail nothing")
        self.assertIn("Нет такого файла или каталога", output[0])


if __name__ == "__main__":
    unittest.main()