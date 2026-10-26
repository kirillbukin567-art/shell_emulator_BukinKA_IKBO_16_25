@echo off
chcp 65001 >nul
cd /d "%~dp0.."

echo === Broken archive (valid base64, not a ZIP) ===
py src\main.py --vfs data\broken.b64

echo.
echo === Missing VFS file ===
py src\main.py --vfs data\missing.b64