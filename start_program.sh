#!/bin/bash
# ============================================================
#  start_program.sh  —  Priyanka's Tennis Academy
#  Activates the venv and launches the Flask development server
#  Mac / Linux version
# ============================================================

echo ""
echo " =============================================="
echo "  Priyanka's Tennis Academy — Starting Server"
echo " =============================================="
echo ""

# Check venv exists
if [ ! -f "venv/bin/activate" ]; then
    echo " [ERROR] Virtual environment not found."
    echo " Please run:  bash start_environment.sh"
    exit 1
fi

echo " Activating virtual environment..."
source venv/bin/activate

echo " Initialising database and launching Flask..."
echo ""
echo " --------------------------------------------------"
echo "  Website:  http://127.0.0.1:5000"
echo "  Admin:    http://127.0.0.1:5000/admin"
echo " --------------------------------------------------"
echo "  Press CTRL+C to stop the server."
echo ""

export FLASK_APP=app.py
export FLASK_ENV=development
export FLASK_DEBUG=1

python app.py
