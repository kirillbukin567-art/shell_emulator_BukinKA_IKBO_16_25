"""Генерирует тестовые VFS (ZIP в base64) в папке data."""

import base64
import io
import os
import zipfile

OUTPUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "data"
)
FIXED_DATE = (2026, 1, 1, 0, 0, 0)
BROKEN_TEXT = "aGVsbG8=\n"

VARIANTS = {
    "minimal": {
        "hello.txt": "Hello, VFS!\n",
    },
    "several_files": {
        "readme.txt": "Several files VFS\n",
        "notes.txt": "First note\nSecond note\nThird note\n",
        "data.csv": "id,name\n1,alpha\n2,beta\n3,gamma\n",
        "script.sh": "#!/bin/sh\necho hello\n",
    },
    "deep": {
        "etc/": None,
        "etc/app.conf": "mode=test\n",
        "home/user/docs/work/report.txt": "Quarterly report\n",
        "home/user/docs/work/todo.txt": "1. test VFS\n2. write docs\n",
        "home/user/docs/notes.txt": "Deep notes\n",
        "home/user/pics/icon.bin": bytes(range(16)),
        "home/user/.profile": "export EDITOR=vi\n",
        "var/log/boot.log": "boot ok\n",
        "tmp/": None,
    },
}


def to_bytes(content):
    """Превращает текст в байты, байты оставляет как есть."""
    if isinstance(content, str):
        return content.encode("utf-8")
    return content


def make_archive(entries):
    """Возвращает байты ZIP-архива с заданными записями."""
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w") as archive:
        for path, content in entries.items():
            info = zipfile.ZipInfo(path, date_time=FIXED_DATE)
            data = b"" if content is None else to_bytes(content)
            archive.writestr(info, data)
    return buffer.getvalue()


def write_text(name, text):
    """Записывает текстовый файл в папку data."""
    path = os.path.join(OUTPUT_DIR, name)
    with open(path, "w", encoding="ascii", newline="\n") as target:
        target.write(text)
    print(f"создан: {os.path.normpath(path)}")


def main():
    """Создаёт все тестовые файлы VFS."""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    for name, entries in VARIANTS.items():
        encoded = base64.encodebytes(make_archive(entries))
        write_text(f"{name}.b64", encoded.decode("ascii"))
    write_text("broken.b64", BROKEN_TEXT)


if __name__ == "__main__":
    main()