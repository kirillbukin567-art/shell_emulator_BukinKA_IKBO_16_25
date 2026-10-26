"""Виртуальная файловая система в памяти, загружаемая из ZIP-архива."""

import base64
import io
import os
import zipfile

DEFAULT_NAME = "vfs"
ZIP_MAGIC = b"PK"
NO_SUCH = "Нет такого файла или каталога"
NOT_A_DIR = "Не является каталогом"
EXISTS = "Файл существует"

DEFAULT_ENTRIES = {
    "readme.txt": b"Default VFS\n",
    "docs/": None,
    "docs/notes.txt": b"Default notes\n",
}


class VfsError(Exception):
    """Ошибка загрузки или использования VFS."""


def dir_prefix(path):
    """Возвращает префикс путей внутри каталога ('' для корня)."""
    return f"{path}/" if path else ""


class Vfs:
    """Виртуальная файловая система: каталоги и файлы в памяти."""

    def __init__(self, name, dirs, files):
        """Создаёт VFS: имя, множество каталогов, словарь файлов."""
        self.name = name
        self.dirs = dirs
        self.files = files

    def all_paths(self):
        """Возвращает множество путей всех каталогов и файлов."""
        return self.dirs | set(self.files)

    def is_dir(self, path):
        """Истинно, если путь — каталог (корень — пустой путь)."""
        return path == "" or path in self.dirs

    def is_file(self, path):
        """Истинно, если путь — файл."""
        return path in self.files

    def children(self, path):
        """Возвращает отсортированные имена прямых потомков каталога."""
        prefix = dir_prefix(path)
        names = set()
        for item in self.all_paths():
            if item.startswith(prefix):
                names.add(item[len(prefix):].split("/")[0])
        return sorted(names)

    def descendants(self, path):
        """Возвращает отсортированные пути всех вложенных элементов."""
        prefix = dir_prefix(path)
        items = self.all_paths()
        return sorted(item for item in items if item.startswith(prefix))

    def add_dir(self, path, with_parents=False):
        """Добавляет каталог в память; при with_parents и его родителей."""
        if with_parents:
            self.dirs.update(parent_dirs(path))
        self.dirs.add(path)


def split_path(path):
    """Делит путь на непустые части."""
    return [part for part in path.split("/") if part]


def resolve(cwd, path):
    """Приводит путь (абсолютный или относительный) к пути в VFS.

    Обрабатывает '.', '..' и повторные слеши. Выше корня подняться
    нельзя. Результат без слешей по краям, '' означает корень.
    """
    parts = [] if path.startswith("/") else split_path(cwd)
    for part in split_path(path):
        if part == "..":
            if parts:
                parts.pop()
        elif part != ".":
            parts.append(part)
    return "/".join(parts)


def join_path(base, name):
    """Склеивает путь каталога и имя элемента."""
    return f"{base}/{name}" if base else name


def parent_of(path):
    """Возвращает путь родительского каталога ('' для корня)."""
    return path.rpartition("/")[0]


def parent_dirs(path):
    """Возвращает все родительские каталоги пути."""
    parts = path.split("/")[:-1]
    return {"/".join(parts[:i + 1]) for i in range(len(parts))}


def build_vfs(name, entries):
    """Строит VFS из словаря путь -> байты (None означает каталог)."""
    dirs = set()
    files = {}
    for raw_path, content in entries.items():
        path = raw_path.strip("/")
        if not path:
            continue
        dirs.update(parent_dirs(path))
        if content is None:
            dirs.add(path)
        else:
            files[path] = content
    return Vfs(name, dirs, files)


def default_vfs():
    """Возвращает встроенную VFS по умолчанию."""
    return build_vfs(DEFAULT_NAME, DEFAULT_ENTRIES)


def decode_archive(raw):
    """Возвращает байты ZIP: файл содержит сам ZIP или его base64-текст."""
    if raw.startswith(ZIP_MAGIC):
        return raw
    compact = b"".join(raw.split())
    try:
        return base64.b64decode(compact, validate=True)
    except ValueError as error:
        raise VfsError("файл не ZIP и не base64-текст") from error


def read_zip(archive):
    """Читает ZIP в память: путь -> байты (None для каталога)."""
    entries = {}
    try:
        with zipfile.ZipFile(io.BytesIO(archive)) as zip_file:
            for info in zip_file.infolist():
                entries[info.filename] = (
                    None if info.is_dir() else zip_file.read(info)
                )
    except zipfile.BadZipFile as error:
        raise VfsError("повреждённый или неверный ZIP-архив") from error
    return entries


def load_vfs(path):
    """Загружает VFS из файла (ZIP или base64-текст ZIP)."""
    try:
        with open(path, "rb") as source:
            raw = source.read()
    except OSError as error:
        raise VfsError(f"не удалось прочитать файл: {error}") from error
    name = os.path.splitext(os.path.basename(path))[0]
    return build_vfs(name, read_zip(decode_archive(raw)))