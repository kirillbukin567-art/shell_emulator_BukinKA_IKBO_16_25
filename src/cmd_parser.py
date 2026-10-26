"""Разбор строки команды: токенизация и раскрытие переменных."""

import os
import re
import shlex

VAR_PATTERN = re.compile(r"\$(\w+)|\$\{(\w+)\}")


def _lookup_variable(match):
    """Возвращает значение переменной окружения из совпадения."""
    name = match.group(1) or match.group(2)
    value = os.environ.get(name)
    if value is None and name == "HOME":
        value = os.path.expanduser("~")
    return value or ""


def expand_variables(text):
    """Заменяет $NAME и ${NAME} значениями переменных окружения."""
    return VAR_PATTERN.sub(lambda m: _lookup_variable(m), text)


def parse_line(line):
    """Разбивает строку на слова и раскрывает переменные в каждом.

    Бросает ValueError, если в строке не закрыта кавычка.
    """
    words = shlex.split(line)
    return [expand_variables(word) for word in words]