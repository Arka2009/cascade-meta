#!/bin/bash
# Script to download Python packages for air-gapped installation
# Run this on a CONNECTED machine with Python 3.10+

set -e

# Configuration
PYTHON_VERSION="3.10"
PACKAGES="tqdm matplotlib numpy filelock"
OUTPUT_DIR="cascade-python-packages"

echo "========================================"
echo "Python Package Downloader for Air-Gapped Installation"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: python3 not found"
    exit 1
fi

CURRENT_PYTHON=$(python3 --version | awk '{print $2}')
echo "Current Python version: $CURRENT_PYTHON"
echo "Target Python version: $PYTHON_VERSION+"
echo ""

# Check pip
if ! command -v pip3 &> /dev/null; then
    echo "ERROR: pip3 not found"
    echo "Install with: python3 -m ensurepip --upgrade"
    exit 1
fi

# Create output directory
mkdir -p "$OUTPUT_DIR"
echo "Output directory: $OUTPUT_DIR"
echo ""

# Download packages
echo "Downloading packages and dependencies..."
echo "Packages: $PACKAGES"
echo ""

pip3 download --dest "$OUTPUT_DIR" $PACKAGES

echo ""
echo "========================================"
echo "✓ Download complete!"
echo "========================================"
echo ""
echo "Files downloaded to: $OUTPUT_DIR"
echo "Total files: $(ls -1 $OUTPUT_DIR/*.whl 2>/dev/null | wc -l)"
echo ""
echo "Next steps:"
echo "1. Transfer the '$OUTPUT_DIR/' directory to your air-gapped server"
echo "2. On the air-gapped server, activate your virtual environment"
echo "3. Install with:"
echo "   pip install --no-index --find-links=$OUTPUT_DIR $PACKAGES"
echo ""
echo "File list:"
ls -lh "$OUTPUT_DIR"
