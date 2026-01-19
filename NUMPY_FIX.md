# Fixing NumPy Import Error with Custom-Compiled Python

## Problem
When using a custom-compiled Python 3.10, you may encounter:
```
ModuleNotFoundError: No module named 'numpy.core._multiarray_umath'
ImportError: numpy C-extensions failed
```

## Root Cause
NumPy binary wheels (`.whl` files) are pre-compiled for specific Python versions and platforms. When you compile Python from source, the NumPy binary may be incompatible due to:
- Different Python ABI (Application Binary Interface)
- Missing or incompatible system libraries
- Architecture mismatches

## Solution: Rebuild NumPy from Source

### In your virtual environment:

```bash
# Activate your venv
source rvdbvenv/bin/activate

# Uninstall existing NumPy
pip uninstall numpy -y

# Install NumPy from source (no binary wheels)
# This will compile NumPy specifically for your Python installation
pip install --no-binary :all: numpy

# Or install a specific version
pip install --no-binary :all: numpy==1.24.2
```

**Note:** Building from source takes 5-15 minutes and requires:
- C compiler (gcc)
- BLAS/LAPACK libraries (optional, for better performance)

### For Air-Gapped Installation:

On a **connected machine with same architecture**:

```bash
# Download NumPy source distribution (.tar.gz, not .whl)
pip download --no-binary :all: numpy -d numpy-source/

# This downloads:
# - numpy-X.X.X.tar.gz (source)
# - All dependencies needed to build

# Transfer numpy-source/ directory to air-gapped server
```

On **air-gapped server**:

```bash
source rvdbvenv/bin/activate

# Uninstall existing NumPy
pip uninstall numpy -y

# Install from source tarball
pip install --no-index --find-links=numpy-source/ --no-binary :all: numpy

# This will build NumPy from source on your air-gapped machine
```

## Alternative: Try Different NumPy Version

Sometimes newer or older NumPy versions work better:

```bash
source rvdbvenv/bin/activate

# Uninstall current
pip uninstall numpy -y

# Try NumPy 1.26.x (latest stable for Python 3.10)
pip install --no-binary :all: numpy==1.26.4

# Or try NumPy 1.23.x if 1.24.2 has issues
pip install --no-binary :all: numpy==1.23.5
```

## Verify the Fix

```bash
python -c "import numpy as np; print('NumPy version:', np.__version__); print('NumPy works!')"
python -c "import numpy; numpy.test('full')"  # Optional: run full test suite
```

## If Building from Source Fails

You may need development libraries:

**On Debian/Ubuntu:**
```bash
sudo apt-get install python3-dev gcc gfortran libopenblas-dev
```

**On RHEL/CentOS:**
```bash
sudo yum install python3-devel gcc gcc-gfortran openblas-devel
```

For air-gapped systems, download these packages on a connected machine:
```bash
apt-get download python3-dev gcc gfortran libopenblas-dev libblas-dev liblapack-dev
# Transfer and install .deb files
```

## Quick Fix Commands

```bash
# One-liner to fix NumPy in your venv
source rvdbvenv/bin/activate && pip uninstall numpy -y && pip install --no-binary :all: numpy
```

## Why This Happens

Your error shows:
- Python: `/home/arka.maity/Desktop/RISCV_TOOLCHAINS/rvdbvenv/bin/python3` (compiled Python 3.10)
- NumPy: `1.24.2` (pre-built wheel)

The pre-built wheel was compiled for a different Python installation (likely system Python or official Python.org binaries), causing ABI incompatibility.

Building from source ensures NumPy is compiled specifically for **your** Python installation.
