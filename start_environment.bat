@echo off
REM ============================================================
REM  start_environment.bat  —  Priyanka's Tennis Academy
REM  Sets up the Python virtual environment and installs deps
REM ============================================================

echo.
echo  ==============================================
echo   Priyanka's Tennis Academy — Environment Setup
echo  ==============================================
echo.

REM Check Python is installed
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Python is not installed or not on PATH.
    echo  Please install Python 3.10+ from https://python.org
    pause
    exit /b 1
)

echo  [1/3] Creating virtual environment...
python -m venv venv
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
)
echo       Done.

echo  [2/3] Activating virtual environment...
call venv\Scripts\activate.bat

echo  [3/3] Installing dependencies from requirements.txt...
pip install --upgrade pip --quiet
pip install -r requirements.txt
IF %ERRORLEVEL% NEQ 0 (
    echo  [ERROR] Failed to install dependencies.
    pause
    exit /b 1
)
echo       Done.

echo.
echo  ================================================
echo   Environment ready! Run start_program.bat next.
echo  ================================================
echo.
pause
