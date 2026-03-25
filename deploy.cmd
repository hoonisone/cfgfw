@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
python -m pip install -q -e ".[dev]"
if not exist "dist" (
    echo dist\ not found. Run build.cmd first.
    exit /b 1
)
python -m twine check dist/*
python -m twine upload dist/* --verbose
echo Upload finished.
