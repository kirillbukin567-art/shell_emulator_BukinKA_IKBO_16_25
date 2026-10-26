@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Test 1: only --vfs ===
echo exit | py src\main.py --vfs data\vfs