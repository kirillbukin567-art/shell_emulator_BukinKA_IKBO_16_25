@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === VFS with several files ===
py src\main.py --vfs data\several_files.b64 --script scripts\vfs_info.emu