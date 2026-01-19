# Cascade Fuzzer - Complete Dependency Installation Guide

This guide lists ALL Python and system dependencies needed to run Cascade fuzzer scripts.

## Python Version Requirement

**Minimum: Python 3.8+** (Python 3.9+ recommended)

The codebase has been made compatible with Python 3.8 by adding a compatibility shim for `functools.cache` (which was introduced in Python 3.9).

Check your Python version:
```bash
python3 --version
```

## Python Dependencies

### Standard Library (Built-in - No Installation Needed)
These come with Python 3 and should never be installed via pip:
- `functools` ✓
- `subprocess` ✓
- `os` ✓
- `sys` ✓
- `itertools` ✓
- `collections` ✓

### Required Python Packages (Install via pip)
```bash
pip3 install --user tqdm matplotlib numpy filelock
```

Individual packages:
- `tqdm` - Progress bars
- `matplotlib` - Plotting and visualization
- `numpy` - Numerical operations
- `filelock` - File locking for parallel operations

### Custom Libraries (From tools/ directory)
- `makeelf` - ELF file manipulation (from tools/makeelf submodule)

## System Dependencies (RISC-V Tools)

### Required Executables
These must be in your PATH (typically in `$HOME/.local/bin`):

1. **spike** - RISC-V ISA Simulator
   - Used for: Executing and tracing RISC-V programs
   - Check: `which spike`

2. **riscv64-unknown-elf-objcopy** - Binary file converter
   - Used for: Converting ELF formats (ELF32 ↔ ELF64)
   - Check: `which riscv64-unknown-elf-objcopy`

3. **riscv64-unknown-elf-gcc** (optional)
   - Used for: Some compilation tasks
   - Check: `which riscv64-unknown-elf-gcc`

4. **riscv64-unknown-elf-objdump** (optional)
   - Used for: Disassembly and debugging
   - Check: `which riscv64-unknown-elf-objdump`

## Complete Installation Steps

### Step 1: Install Python Packages
```bash
pip3 install --user tqdm matplotlib numpy filelock
```

### Step 2: Source the Cascade Environment
```bash
cd /path/to/cascade-meta
source env-custom.sh
```

This will:
- Set up all environment variables
- Add makeelf to Python path
- Configure for RV64
- Verify RISC-V tools are accessible

### Step 3: Verify Installation
```bash
# Check Python imports
python3 -c "import tqdm, matplotlib, numpy, filelock, makeelf; print('All packages OK')"

# Check RISC-V tools
which spike
which riscv64-unknown-elf-objcopy
spike --version
```

### Step 4: Run Fuzzer Scripts
```bash
cd fuzzer

# Generate 10 test ELF files
python3 do_genmanyelfs.py 10

# Run a single fuzzer instance
python3 do_fuzzsingle.py

# Fuzz a design
python3 do_fuzzdesign.py <design_name> <num_cores> <seed_offset>
```

## Common Errors and Solutions

### Error: "No module named 'functools'"
**Wrong diagnosis!** `functools` is built-in. The actual error is usually something else.
Check the full traceback for the real missing module.

### Error: "No module named 'makeelf'"
**Solution:** Source `env-custom.sh` which adds makeelf to PYTHONPATH
```bash
source env-custom.sh
```

### Error: "No module named 'filelock'"
**Solution:** Install filelock
```bash
pip3 install --user filelock
```

### Error: "FileNotFoundError: 'spike'"
**Solution:** Ensure spike is in your PATH
```bash
export PATH=$HOME/.local/bin:$PATH
which spike  # Should show the path to spike
```

### Error: "The Cascade environment must be sourced"
**Solution:** Always source env-custom.sh before running scripts
```bash
source env-custom.sh
```

## Quick Setup Script

Create this script for convenience:

```bash
#!/bin/bash
# setup_cascade.sh

# Install Python packages (only needed once)
pip3 install --user tqdm matplotlib numpy filelock

# Add to your ~/.bashrc or ~/.zshrc for persistence:
echo 'export PATH=$HOME/.local/bin:$PATH' >> ~/.bashrc

# Source Cascade environment
source /path/to/cascade-meta/env-custom.sh

echo "Cascade environment ready!"
```

## Verification Checklist

Before running fuzzer scripts, verify:

- [ ] Python 3.9+ installed: `python3 --version`
- [ ] All pip packages installed: `pip3 list | grep -E "tqdm|matplotlib|numpy|filelock"`
- [ ] makeelf accessible: `python3 -c "import makeelf"`
- [ ] spike installed: `spike --version`
- [ ] objcopy installed: `riscv64-unknown-elf-objcopy --version`
- [ ] Environment sourced: `echo $CASCADE_ENV_SOURCED` (should show "yes")
- [ ] PYTHONPATH includes makeelf: `echo $PYTHONPATH | grep makeelf`

## For Air-Gapped Machines

Download packages on a connected machine:
```bash
pip3 download tqdm matplotlib numpy filelock -d ./cascade-deps
```

Transfer `cascade-deps/` directory to air-gapped machine and install:
```bash
pip3 install --user --no-index --find-links=./cascade-deps tqdm matplotlib numpy filelock
```
