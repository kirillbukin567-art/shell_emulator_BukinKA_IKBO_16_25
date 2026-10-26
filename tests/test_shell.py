"""Тесты выполнения команд и стартового скрипта."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from shell import handle_line, run_script


def capture(function, *args):
    """Вызывает функцию и возвращает пару (результат, вывод)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class HandleLineTest(unittest.TestCase):
    """Проверки функции handle_line."""

    def test_exit_returns_false(self):
        """Команда exit сигнализирует о выходе."""
        result, _ = capture(handle_line, "exit")
        self.assertFalse(result)

    def test_command_returns_true(self):
        """Обычная команда выполняется, работа продолжается."""
        result, output = capture(handle_line, "ls /tmp")
        self.assertTrue(result)
        self.assertIn("ls", output)

    def test_parse_error_is_reported(self):
        """Ошибка разбора выводится, работа продолжается."""
        result, output = capture(handle_line, 'cd "abc')
        self.assertTrue(result)
        self.assertIn("Ошибка разбора", output)


class RunScriptTest(unittest.TestCase):
    """Проверки функции run_script."""

    def write_script(self, text):
        """Создаёт временный скрипт и возвращает путь к нему."""
        handle, path = tempfile.mkstemp(suffix=".emu")
        os.close(handle)
        self.addCleanup(os.remove, path)
        with open(path, "w", encoding="utf-8") as script:
            script.write(text)
        return path

    def test_shows_input_and_output(self):
        """В диалоге видны и введённая строка, и вывод команды."""
        path = self.write_script("ls -l\n")
        result, output = capture(run_script, path, "vfs")
        self.assertTrue(result)
        self.assertIn("vfs$ ls -l", output)
        self.assertIn("ls: аргументы ['-l']", output)

    def test_skips_comments_and_errors(self):
        """Комментарии пропускаются, ошибочные строки не мешают."""
        path = self.write_script("# comment\n\nfoo\nls\n")
        result, output = capture(run_script, path, "vfs")
        self.assertTrue(result)
        self.assertNotIn("comment", output)
        self.assertIn("foo: команда не найдена", output)
        self.assertIn("vfs$ ls", output)

    def test_exit_stops_script(self):
        """После exit остальные строки не выполняются."""
        path = self.write_script("exit\nls\n")
        result, output = capture(run_script, path, "vfs")
        self.assertFalse(result)
        self.assertNotIn("ls:", output)


if __name__ == "__main__":
    unittest.main()