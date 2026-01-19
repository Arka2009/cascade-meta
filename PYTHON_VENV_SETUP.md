# Setting Up Python 3.10+ Virtual Environment (Air-Gapped)

This guide helps you install Python 3.10+ and create a virtual environment on an air-gapped server.

## Why Python 3.10+?

The Cascade fuzzer codebase uses:
- **`match/case` statements** (Python 3.10+) - Used in `fuzzer/cascade/basicblock.py:156`
- **`functools.cache`** (Python 3.9+) - Compatibility shim added for Python 3.8

**Minimum required: Python 3.8** (with compatibility fixes for functools.cache)
**Recommended: Python 3.10+** (for full native support of match/case)

## Option 1: Install Python 3.10+ from Source (If not already installed)

### On a connected machine (for downloading):

```bash
# Download Python 3.10.x source
wget https://www.python.org/ftp/python/3.10.13/Python-3.10.13.tgz

# Download required dependencies (for Debian/Ubuntu-based systems)
apt-get download build-essential libssl-dev zlib1g-dev \
    libncurses5-dev libncursesw5-dev libreadline-dev libsqlite3-dev \
    libgdbm-dev libdb5.3-dev libbz2-dev libexpat1-dev liblzma-dev \
    tk-dev libffi-dev

# Transfer Python-3.10.13.tgz and all .deb files to your air-gapped server
```

### On your air-gapped server:

```bash
# Install dependencies (if you have the .deb files)
sudo dpkg -i *.deb

# Extract and build Python
tar -xzf Python-3.10.13.tgz
cd Python-3.10.13

# Configure to install in $HOME/.local
./configure --prefix=$HOME/.local --enable-optimizations

# Build and install (this takes 5-15 minutes)
make -j$(nproc)
make install

# Verify installation
$HOME/.local/bin/python3.10 --version
```

## Option 2: Use System Python 3.10+ (If available)

Check if Python 3.10+ is already installed:

```bash
python3 --version
python3.10 --version  # Try specific version
python3.11 --version
```

If you have Python 3.10+ available, skip to the next section.

## Creating a Virtual Environment

Python 3.3+ includes `venv` module (no need for virtualenv or conda):

```bash
cd ~/Desktop/cascade-meta

# Create virtual environment using Python 3.10+
# Replace python3.10 with your actual Python binary
$HOME/.local/bin/python3.10 -m venv cascade-venv

# Or if system Python is 3.10+:
python3 -m venv cascade-venv
```

This creates a `cascade-venv/` directory with:
- `bin/` - Python executables and activation scripts
- `lib/` - Installed packages
- `include/` - Header files

## Activating the Virtual Environment

```bash
# Activate the virtual environment
source cascade-venv/bin/activate

# Your prompt should change to show (cascade-venv)
# Verify Python version
python --version  # Should show 3.10+

# Verify pip is available
pip --version
```

## Installing Packages in the Virtual Environment (Air-Gapped)

### Method 1: Download packages on connected machine

On a **connected machine** with the **same Python version**:

```bash
# Create a directory for packages
mkdir cascade-python-packages
cd cascade-python-packages

# Download all required packages and their dependencies
pip download tqdm matplotlib numpy filelock

# This downloads .whl files for all packages
# Transfer the entire cascade-python-packages/ directory to air-gapped server
```

On your **air-gapped server**:

```bash
# Activate virtual environment
source cascade-venv/bin/activate

# Install from downloaded packages
pip install --no-index --find-links=cascade-python-packages tqdm matplotlib numpy filelock

# Verify installation
python -c "import tqdm, matplotlib, numpy, filelock; print('All packages installed!')"
```

### Method 2: Install from wheels on air-gapped server

If you already have the packages somewhere:

```bash
source cascade-venv/bin/activate
pip install --no-index --find-links=/path/to/wheels tqdm matplotlib numpy filelock
```

## Integrating with Cascade (Update env-custom.sh)

The virtual environment should be activated **before** sourcing env-custom.sh:

```bash
# Add to your ~/.bashrc or create a wrapper script
source ~/Desktop/cascade-meta/cascade-venv/bin/activate
source ~/Desktop/cascade-meta/env-custom.sh
```

Or create a convenience script `setup_cascade_env.sh`:

```bash
#!/bin/bash
# setup_cascade_env.sh

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Activate virtual environment
source "$SCRIPT_DIR/cascade-venv/bin/activate"

# Source Cascade environment
source "$SCRIPT_DIR/env-custom.sh"

echo "Cascade environment with Python $(python --version) activated"
```

Then use it:

```bash
chmod +x setup_cascade_env.sh
source setup_cascade_env.sh
```

## Verifying the Setup

```bash
# Source your environment
source setup_cascade_env.sh

# Check Python version (should be 3.10+)
python --version

# Check packages
python -c "import sys; print('Python:', sys.version)"
python -c "import tqdm, matplotlib, numpy, filelock, makeelf; print('All imports OK')"

# Check RISC-V tools
which spike
which riscv64-unknown-elf-objcopy

# Try running the fuzzer
cd fuzzer
python do_genmanyelfs.py 2
```

## Deactivating the Virtual Environment

When you're done:

```bash
deactivate
```

## Troubleshooting

### Issue: "No module named '_ctypes'"

Missing libffi-dev when building Python. On connected machine:

```bash
apt-get download libffi-dev
# Transfer to air-gapped and install
```

### Issue: "No module named '_ssl'"

Missing libssl-dev when building Python. Rebuild Python with:

```bash
sudo dpkg -i libssl-dev*.deb
./configure --prefix=$HOME/.local --enable-optimizations
make clean && make -j$(nproc) && make install
```

### Issue: pip not working in venv

Ensure ensurepip was available when creating venv:

```bash
python3.10 -m ensurepip --upgrade
python3.10 -m venv --clear cascade-venv
```

### Issue: "match" statement still not working

Verify Python version in venv:

```bash
source cascade-venv/bin/activate
python --version  # Must show 3.10+, not 3.8
which python      # Should point to cascade-venv/bin/python
```

## Quick Reference

```bash
# Create venv (once)
python3.10 -m venv cascade-venv

# Activate venv (every session)
source cascade-venv/bin/activate

# Install packages (once, on air-gapped)
pip install --no-index --find-links=packages/ tqdm matplotlib numpy filelock

# Use Cascade
source env-custom.sh
cd fuzzer
python do_genmanyelfs.py

# Deactivate when done
deactivate
```

## File Structure

After setup, your directory should look like:

```
~/Desktop/cascade-meta/
├── cascade-venv/              # Virtual environment
│   ├── bin/
│   │   ├── python -> python3.10
│   │   ├── pip
│   │   └── activate
│   └── lib/python3.10/site-packages/
├── env-custom.sh              # Cascade environment config
├── setup_cascade_env.sh       # Convenience script (optional)
├── fuzzer/
└── tools/
    └── makeelf/
```
