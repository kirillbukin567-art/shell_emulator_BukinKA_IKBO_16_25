"""Состояние сеанса эмулятора."""

from dataclasses import dataclass
from typing import Optional

from vfs import Vfs


@dataclass
class Session:
    """Текущее состояние: загруженная VFS и путь к её файлу."""

    vfs: Vfs
    vfs_path: Optional[str] = None