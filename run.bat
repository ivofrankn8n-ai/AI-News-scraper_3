@echo off
echo Running AI News Pipeline...
python tools/run_pipeline.py
echo.
echo Starting Dashboard Server...
python serve.py
pause