@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Test 1: no parameters ===
echo exit | py src\main.py

echo.
echo === Test 2: --vfs and --script together ===
py src\main.py --vfs data\minimal.b64 --script scripts\startup_basic.emu

echo.
echo === Test 3: --help ===
py src\main.py --help

echo.
echo === Test 4: unknown parameter ===
py src\main.py --unknown

echo.
echo === Test 5: --vfs without value ===
py src\main.py --vfs