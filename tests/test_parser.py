"""Тесты разбора строки команды."""

import os
import unittest
from unittest import mock

from cmd_parser import parse_line


class ParseLineTest(unittest.TestCase):
    """Проверки функции parse_line."""

    def test_splits_words(self):
        """Строка делится на слова по пробелам."""
        self.assertEqual(parse_line("ls -l /tmp"), ["ls", "-l", "/tmp"])

    def test_quotes_keep_words_together(self):
        """Текст в кавычках остаётся одним словом."""
        self.assertEqual(parse_line('cd "my dir"'), ["cd", "my dir"])

    def test_expands_environment_variable(self):
        """$NAME заменяется значением переменной окружения."""
        with mock.patch.dict(os.environ, {"EMU_TEST_VAR": "value"}):
            self.assertEqual(
                parse_line("echo $EMU_TEST_VAR ${EMU_TEST_VAR}"),
                ["echo", "value", "value"],
            )

    def test_unknown_variable_is_empty(self):
        """Неизвестная переменная заменяется пустой строкой."""
        self.assertEqual(parse_line("echo $NO_SUCH_VAR_XYZ"), ["echo", ""])

    def test_unclosed_quote_raises(self):
        """Незакрытая кавычка вызывает ValueError."""
        with self.assertRaises(ValueError):
            parse_line('cd "abc')


if __name__ == "__main__":
    unittest.main()