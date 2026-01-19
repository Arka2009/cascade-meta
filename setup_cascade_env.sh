#!/bin/bash
# Cascade Environment Setup Script
# This script activates the Python virtual environment and sources env-custom.sh

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if virtual environment exists
VENV_DIR="$SCRIPT_DIR/cascade-venv"
if [ ! -d "$VENV_DIR" ]; then
    echo "ERROR: Virtual environment not found at: $VENV_DIR"
    echo "Please create it first:"
    echo "  python3.10 -m venv cascade-venv"
    return 1 2>/dev/null || exit 1
fi

# Activate virtual environment
echo "Activating Python virtual environment..."
source "$VENV_DIR/bin/activate"

# Verify Python version
PYTHON_VERSION=$(python --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check if Python is 3.10+
PYTHON_MAJOR=$(python -c "import sys; print(sys.version_info.major)")
PYTHON_MINOR=$(python -c "import sys; print(sys.version_info.minor)")

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 10 ]); then
    echo "WARNING: Python 3.10+ recommended. Current version: $PYTHON_VERSION"
    echo "Some features (like match statements) may not work."
fi

# Source Cascade environment
echo "Loading Cascade environment..."
source "$SCRIPT_DIR/env-custom.sh"

echo ""
echo "✓ Cascade environment ready!"
echo "  Python: $PYTHON_VERSION"
echo "  RISCV tools: $RISCV"
echo "  Data dir: $CASCADE_DATADIR"
echo ""
echo "To deactivate when done: deactivate"
