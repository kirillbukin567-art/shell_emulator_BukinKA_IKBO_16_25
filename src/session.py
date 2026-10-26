"""Состояние сеанса эмулятора."""

from dataclasses import dataclass
from typing import Optional

from vfs import Vfs


@dataclass
class Session:
    """Текущее состояние: VFS, путь к её файлу и текущий каталог."""

    vfs: Vfs
    vfs_path: Optional[str] = None
    cwd: str = ""