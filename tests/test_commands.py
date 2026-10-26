"""Тесты команд эмулятора."""

import io
import unittest
from contextlib import redirect_stdout

from commands import execute


def run_command(words):
    """Выполняет команду и возвращает всё, что она напечатала."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        execute(words)
    return buffer.getvalue()


class ExecuteTest(unittest.TestCase):
    """Проверки функции execute."""

    def test_ls_prints_name_and_args(self):
        """Заглушка ls печатает имя и аргументы."""
        output = run_command(["ls", "-l", "/tmp"])
        self.assertIn("ls", output)
        self.assertIn("['-l', '/tmp']", output)

    def test_cd_prints_name_and_args(self):
        """Заглушка cd печатает имя и аргументы."""
        output = run_command(["cd", "/home"])
        self.assertIn("cd", output)
        self.assertIn("['/home']", output)

    def test_unknown_command(self):
        """Неизвестная команда сообщает об ошибке."""
        output = run_command(["foo"])
        self.assertIn("команда не найдена", output)


if __name__ == "__main__":
    unittest.main()