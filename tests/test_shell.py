"""Тесты выполнения команд и стартового скрипта."""

import io
import os
import tempfile
import unittest
from contextlib import redirect_stdout

from session import Session
from shell import handle_line, make_prompt, run_script
from vfs import build_vfs, default_vfs


def capture(function, *args):
    """Вызывает функцию и возвращает пару (результат, вывод)."""
    buffer = io.StringIO()
    with redirect_stdout(buffer):
        result = function(*args)
    return result, buffer.getvalue()


class HandleLineTest(unittest.TestCase):
    """Проверки функции handle_line."""

    def setUp(self):
        """Создаёт сеанс с VFS по умолчанию."""
        self.session = Session(default_vfs())

    def test_exit_returns_false(self):
        """Команда exit сигнализирует о выходе."""
        result, _ = capture(handle_line, self.session, "exit")
        self.assertFalse(result)

    def test_command_returns_true(self):
        """Обычная команда выполняется, работа продолжается."""
        result, output = capture(handle_line, self.session, "ls docs")
        self.assertTrue(result)
        self.assertIn("notes.txt", output)

    def test_parse_error_is_reported(self):
        """Ошибка разбора выводится, работа продолжается."""
        result, output = capture(handle_line, self.session, 'cd "abc')
        self.assertTrue(result)
        self.assertIn("Ошибка разбора", output)


class MakePromptTest(unittest.TestCase):
    """Проверки функции make_prompt."""

    def test_root_prompt(self):
        """В корне приглашение содержит имя VFS и /."""
        session = Session(default_vfs())
        self.assertEqual(make_prompt(session), "vfs:/$ ")

    def test_prompt_with_directory(self):
        """В приглашении виден текущий каталог."""
        session = Session(default_vfs(), cwd="docs")
        self.assertEqual(make_prompt(session), "vfs:/docs$ ")


class RunScriptTest(unittest.TestCase):
    """Проверки функции run_script."""

    def setUp(self):
        """Создаёт сеанс с VFS по умолчанию."""
        self.session = Session(default_vfs())

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
        result, output = capture(run_script, path, self.session)
        self.assertTrue(result)
        self.assertIn("vfs:/$ ls -l", output)
        self.assertIn("readme.txt", output)

    def test_skips_comments_and_errors(self):
        """Комментарии пропускаются, ошибочные строки не мешают."""
        path = self.write_script("# comment\n\nfoo\nls\n")
        result, output = capture(run_script, path, self.session)
        self.assertTrue(result)
        self.assertNotIn("comment", output)
        self.assertIn("foo: команда не найдена", output)
        self.assertIn("vfs:/$ ls", output)

    def test_exit_stops_script(self):
        """После exit остальные строки не выполняются."""
        path = self.write_script("exit\nls\n")
        result, output = capture(run_script, path, self.session)
        self.assertFalse(result)
        self.assertNotIn("readme.txt", output)

    def test_prompt_changes_after_vfs_init(self):
        """После vfs-init в приглашении появляется имя VFS по умолчанию."""
        self.session.vfs = build_vfs("other", {"a.txt": b"x"})
        path = self.write_script("ls\nvfs-init\nls\n")
        _, output = capture(run_script, path, self.session)
        self.assertIn("other:/$ ls", output)
        self.assertIn("vfs:/$ ls", output)

    def test_prompt_shows_current_directory(self):
        """После cd в приглашении виден новый каталог."""
        path = self.write_script("cd docs\nls\n")
        _, output = capture(run_script, path, self.session)
        self.assertIn("vfs:/docs$ ls", output)
        self.assertIn("notes.txt", output)


if __name__ == "__main__":
    unittest.main()