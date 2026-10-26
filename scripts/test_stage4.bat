@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Stage 4: ls, cd, tac, tail, find on deep VFS ===
py src\main.py --vfs data\deep.b64 --script scripts\startup_stage4.emu