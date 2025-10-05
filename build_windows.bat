@echo off
setlocal enabledelayedexpansion
REM Build standalone Windows bundle with PyInstaller (one-folder)
REM Usage:
REM   build_windows.bat

set PROJECT_DIR=%~dp0
pushd %PROJECT_DIR%

set VENV_DIR=.venv-build

if not exist "%VENV_DIR%" (
  py -3 -m venv "%VENV_DIR%"
)
call "%VENV_DIR%\Scripts\activate.bat"
python -m pip install --upgrade pip wheel
python -m pip install -r requirements.txt pyinstaller

REM Clean old builds
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul

REM Build with spec (one-folder so relative icons/ paths work)
pyinstaller pyinstaller.spec

echo.
echo Build complete. Output in dist\session-tracker\
echo Launch dist\session-tracker\session-tracker.exe

popd
endlocal
