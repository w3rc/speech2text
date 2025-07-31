@echo off
echo ========================================
echo    Speech2Text - Complete Build Suite
echo ========================================
echo.

REM Check if uv is available
where uv >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo ERROR: uv not found. Please install uv first.
    echo Visit: https://docs.astral.sh/uv/getting-started/installation/
    pause
    exit /b 1
)

echo Choose build option:
echo.
echo [1] EXE only (PyInstaller - single file)
echo [2] MSI installer (cx_Freeze)
echo [3] MSI installer (WiX Toolset - Professional)
echo [4] Build both EXE and MSI
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto build_exe
if "%choice%"=="2" goto build_msi_cx
if "%choice%"=="3" goto build_msi_wix
if "%choice%"=="4" goto build_all
goto invalid_choice

:build_exe
echo.
echo ====================================
echo    Building EXE with PyInstaller
echo ====================================
echo.
uv run python build_exe.py
goto end

:build_msi_cx
echo.
echo ====================================
echo    Building MSI with cx_Freeze
echo ====================================
echo.
uv run python build_msi.py
goto end

:build_msi_wix
echo.
echo ====================================
echo    Building MSI with WiX Toolset
echo ====================================
echo.
python build_msi_simple.py
goto end

:build_all
echo.
echo ====================================
echo    Building Both EXE and MSI
echo ====================================
echo.
echo [STEP 1/2] Building EXE...
uv run python build_exe.py
echo.
echo [STEP 2/2] Building MSI...
python build_msi_simple.py
goto end

:invalid_choice
echo.
echo Invalid choice. Please run the script again and choose 1-4.
goto end

:end
echo.
if %ERRORLEVEL% equ 0 (
    echo ====================================
    echo       BUILD COMPLETED SUCCESSFULLY
    echo ====================================
    echo.
    echo Check the 'dist' folder for your built files:
    echo - Speech2Text.exe (standalone executable)
    echo - Speech2Text.msi (Windows installer)
    echo.
    echo Distribution options:
    echo - EXE: Simple, single-file distribution
    echo - MSI: Professional installer with shortcuts and uninstall
) else (
    echo ====================================
    echo           BUILD FAILED
    echo ====================================
    echo.
    echo Check the error messages above for details.
    echo Make sure all dependencies are installed.
)

echo.
echo Press any key to exit...
pause >nul