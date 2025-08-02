@echo off
echo Building Speech2Text Electron Application...

echo.
echo Installing dependencies...
call npm install

echo.
echo Building renderer...
call npm run build-renderer

echo.
echo Building main process...
call npm run build-main

echo.
echo Creating distribution package...
call npm run dist

echo.
echo Build complete! Check the dist-electron folder.
pause