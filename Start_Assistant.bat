@echo off
title RadarCore
echo ===================================================
echo Starting RadarCore...
echo ===================================================
echo.
echo Loading virtual environment and Streamlit...

cd /d "%~dp0"
call venv\Scripts\activate.bat
streamlit run app.py

echo.
echo The application has been closed.
pause
