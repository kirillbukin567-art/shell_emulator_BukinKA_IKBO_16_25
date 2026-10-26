@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Stage 5: mkdir and vfs-load ===
py src\main.py --vfs data\minimal.b64 --script scripts\startup_stage5.emu