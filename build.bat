@echo off
echo Building Speech2Text executable...
uv run python build_exe.py
echo.
echo Build complete! Check the dist folder for Speech2Text.exe
pause