@echo off
REM ============================================================
REM  start_program.bat  —  Priyanka's Tennis Academy
REM  Activates the venv and launches the Flask development server
REM ============================================================

echo.
echo  ==============================================
echo   Priyanka's Tennis Academy — Starting Server
echo  ==============================================
echo.

REM Check venv exists
IF NOT EXIST "venv\Scripts\activate.bat" (
    echo  [ERROR] Virtual environment not found.
    echo  Please run start_environment.bat first.
    pause
    exit /b 1
)

echo  Activating virtual environment...
call venv\Scripts\activate.bat

echo  Initialising database and launching Flask...
echo.
echo  --------------------------------------------------
echo   Website:  http://127.0.0.1:5000
echo   Admin:    http://127.0.0.1:5000/admin
echo  --------------------------------------------------
echo   Press CTRL+C to stop the server.
echo.

set FLASK_APP=app.py
set FLASK_ENV=development
set FLASK_DEBUG=1

python app.py

pause
