@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>&1
if errorlevel 1 (
  where py >nul 2>&1
  if errorlevel 1 (
    echo Python not found. Install Python 3.10+ and add it to PATH.
    exit /b 1
  )
  py -3 -m venv .venv
  if errorlevel 1 exit /b 1
) else (
  python -m venv .venv
  if errorlevel 1 exit /b 1
)

if not exist ".venv\Scripts\activate.bat" (
  echo Failed to create venv. Check Python installation and PATH.
  exit /b 1
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 exit /b 1

python -m pip install -U pip
if errorlevel 1 exit /b 1

python -m pip install -e ".[dev]"
if errorlevel 1 exit /b 1

echo Environment ready. Activate with: .venv\Scripts\activate.bat
