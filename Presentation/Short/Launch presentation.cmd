@echo off
setlocal
cd /d "%~dp0"
if exist "Portable\index.html" (
    start "" "%~dp0Portable\index.html"
    exit /b 0
)
if not exist "..\..\.manim-venv\Scripts\pythonw.exe" (
    echo The presentation Python environment could not be found.
    pause
    exit /b 1
)
if not exist "slides\QuantumStochasticShort.json" (
    echo Render the short presentation first. See README.md.
    pause
    exit /b 1
)
start "" "..\..\.manim-venv\Scripts\pythonw.exe" -m manim_slides present --hide-info-window QuantumStochasticShort
exit /b 0
