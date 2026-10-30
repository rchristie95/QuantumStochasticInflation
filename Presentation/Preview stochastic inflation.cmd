@echo off
setlocal
cd /d "%~dp0"
if not exist "previews\stochastic\slides\CutoffDraft.json" (
    echo The separate stochastic-inflation preview has not been rendered.
    pause
    exit /b 1
)
start "" "..\.manim-venv\Scripts\pythonw.exe" -m manim_slides present --hide-info-window --folder "previews\stochastic\slides" CutoffDraft
exit /b 0
