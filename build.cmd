@echo off
setlocal
cd /d "%~dp0"
if exist ".venv\Scripts\activate.bat" call ".venv\Scripts\activate.bat"
python -m pip install -q -e ".[dev]"
python -m build
if errorlevel 1 exit /b 1
echo Done. Artifacts: dist\
