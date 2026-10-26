@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Test 1: --script with basic commands ===
py src\main.py --script scripts\startup_basic.emu

echo.
echo === Test 2: --script with erroneous lines ===
py src\main.py --script scripts\startup_errors.emu

echo.
echo === Test 3: --script, file does not exist ===
py src\main.py --script scripts\missing.emu