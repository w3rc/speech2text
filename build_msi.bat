@echo off
echo ====================================
echo    Speech2Text MSI Installer Builder
echo ====================================
echo.

REM Check if uv is available
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv not found. Please install uv first.
    echo Visit: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo Building MSI installer...
echo.

REM Run the MSI build script
uv run python build_msi.py

echo.
if %ERRORLEVEL% equ 0 (
    echo ====================================
    echo    MSI BUILD COMPLETED SUCCESSFULLY
    echo ====================================
    echo.
    echo The MSI installer has been created in the 'dist' folder.
    echo You can now distribute the .msi file to install Speech2Text on other computers.
) else (
    echo ====================================
    echo         MSI BUILD FAILED
    echo ====================================
    echo.
    echo Check the error messages above for details.
    echo If cx_Freeze fails, you can use the EXE version instead:
    echo Run: build.bat
)

echo.
pause