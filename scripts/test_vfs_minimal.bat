@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Minimal VFS: one file ===
py src\main.py --vfs data\minimal.b64 --script scripts\vfs_info.emu