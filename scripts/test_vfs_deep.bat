@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Deep VFS: 5 levels, binary file, all commands ===
py src\main.py --vfs data\deep.b64 --script scripts\startup_stage3.emu