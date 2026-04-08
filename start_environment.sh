#!/bin/bash
# ============================================================
#  start_environment.sh  —  Priyanka's Tennis Academy
#  Sets up the Python virtual environment and installs deps
#  Mac / Linux version
# ============================================================

echo ""
echo " =============================================="
echo "  Priyanka's Tennis Academy — Environment Setup"
echo " =============================================="
echo ""

# Check Python3 is installed
if ! command -v python3 &> /dev/null; then
    echo " [ERROR] python3 is not installed."
    echo " Install it from https://python.org or via Homebrew:"
    echo "   brew install python"
    exit 1
fi

echo " [1/3] Creating virtual environment (venv)..."
python3 -m venv venv
if [ $? -ne 0 ]; then
    echo " [ERROR] Failed to create virtual environment."
    exit 1
fi
echo "       Done."

echo " [2/3] Activating virtual environment..."
source venv/bin/activate

echo " [3/3] Installing dependencies from requirements.txt..."
pip install --upgrade pip --quiet
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo " [ERROR] Failed to install dependencies."
    exit 1
fi
echo "       Done."

echo ""
echo " ================================================"
echo "  Environment ready! Run start_program.sh next."
echo " ================================================"
echo ""
