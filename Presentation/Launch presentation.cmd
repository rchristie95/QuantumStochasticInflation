@echo off
setlocal
cd /d "%~dp0"
if not exist "..\.manim-venv\Scripts\pythonw.exe" (
    echo The presentation's Python environment could not be found.
    echo See README.md in this folder for setup instructions.
    pause
    exit /b 1
)
if not exist "slides\QuantumStochasticOpening.json" (
    echo The rendered presentation could not be found.
    echo See README.md in this folder for rendering instructions.
    pause
    exit /b 1
)
start "" "..\.manim-venv\Scripts\pythonw.exe" -m manim_slides present --hide-info-window QuantumStochasticOpening
exit /b 0
