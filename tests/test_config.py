"""Тесты параметров командной строки."""

import io
import unittest
from contextlib import redirect_stderr, redirect_stdout

from config import NOT_SET, parse_args, print_debug


class ParseArgsTest(unittest.TestCase):
    """Проверки функции parse_args."""

    def test_defaults(self):
        """Без параметров оба значения не заданы."""
        args = parse_args([])
        self.assertIsNone(args.vfs)
        self.assertIsNone(args.script)

    def test_both_params(self):
        """Оба параметра читаются из списка аргументов."""
        args = parse_args(["--vfs", "data", "--script", "start.emu"])
        self.assertEqual(args.vfs, "data")
        self.assertEqual(args.script, "start.emu")

    def test_unknown_param_exits(self):
        """Неизвестный параметр завершает программу с ошибкой."""
        with redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                parse_args(["--unknown"])


class PrintDebugTest(unittest.TestCase):
    """Проверки функции print_debug."""

    def test_prints_all_params(self):
        """Отладочный вывод содержит все параметры."""
        args = parse_args(["--vfs", "data"])
        buffer = io.StringIO()
        with redirect_stdout(buffer):
            print_debug(args)
        output = buffer.getvalue()
        self.assertIn("data", output)
        self.assertIn(NOT_SET, output)


if __name__ == "__main__":
    unittest.main()