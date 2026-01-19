# Using Cascade with Existing RISC-V Tools (RV64)

This guide explains how to use Cascade with your pre-installed RISC-V toolchain and Spike simulator instead of the bundled tools.

## Prerequisites

You mentioned you have the following tools installed in `$HOME/.local`:
- RISC-V GNU Toolchain (riscv64-unknown-elf-*)
- Spike RISC-V ISA Simulator

## Quick Setup

### Option 1: Use the Custom Environment Script (Recommended)

Simply source the custom environment file instead of the default `env.sh`:

```bash
source env-custom.sh
```

This will:
- Load all default Cascade settings
- Override tool paths to use your `$HOME/.local` installation
- Configure for RV64 (64-bit RISC-V)
- Verify that required tools are in your PATH

### Option 2: Manual Configuration

If you prefer to modify `env.sh` directly, make these changes:

```bash
# In env.sh, around line 43 (already set to 64 by default):
export CASCADE_RISCV_BITWIDTH=64

# Around line 119:
export RISCV=$HOME/.local

# Around lines 139-140:
export CASCADE_GCC=riscv64-unknown-elf-gcc
export CASCADE_OBJDUMP=riscv64-unknown-elf-objdump

# Make sure your tools are in PATH (around line 152):
export PATH=$HOME/.local/bin:$PATH
```

## Key Configuration Variables

### RISCV Bitwidth
```bash
CASCADE_RISCV_BITWIDTH=64  # Use 64 for rv64, 32 for rv32
```

This variable is used by:
- `fuzzer/common/bytestoelf.py:40,42,45` - to call `riscv64-unknown-elf-objcopy`
- Various fuzzer scripts to determine ISA features

### Tool Locations
```bash
RISCV=$HOME/.local  # Where your RISC-V toolchain is installed
```

The fuzzer expects these executables in `$RISCV/bin` or in `PATH`:
- `spike` - The RISC-V ISA simulator
- `riscv64-unknown-elf-objcopy` - Used to manipulate ELF files
- `riscv64-unknown-elf-objdump` - Used for disassembly (optional)
- `riscv64-unknown-elf-gcc` - Used for some compilation tasks (optional)

## Verification

After sourcing the environment, verify your setup:

```bash
# Check environment variables
echo $CASCADE_RISCV_BITWIDTH  # Should be 64
echo $RISCV                    # Should be $HOME/.local
echo $CASCADE_ENV_SOURCED      # Should be 'yes'

# Check tools are accessible
which spike
which riscv64-unknown-elf-objcopy
which riscv64-unknown-elf-gcc

# Test tool versions
spike --version
riscv64-unknown-elf-gcc --version
```

## Python Dependencies

The fuzzer also requires these Python packages:
```bash
pip install tqdm matplotlib numpy
```

Plus the custom `makeelf` library (from `tools/makeelf`):
```bash
cd tools/makeelf
git submodule update --init  # if needed
python3 setup.py install --user
```

## Running the Fuzzer

Once configured, you can run fuzzer scripts normally:

```bash
# Generate a single test
cd fuzzer
python3 do_fuzzsingle.py

# Fuzz a specific design (if you have RTL designs configured)
python3 do_fuzzdesign.py <design_name> <num_cores> <seed_offset>
```

## What Gets Skipped

By using your existing tools, you can skip building:
- ❌ `tools/riscv-gnu-toolchain` (submodule)
- ❌ `tools/riscv-isa-sim` (Spike submodule)

You still may need (depending on what fuzzer features you use):
- ✅ `tools/makeelf` - Python library for ELF manipulation (required)
- ⚠️  `tools/verilator` - Only if running RTL simulations
- ⚠️  `tools/cascade-yosys` - Only if doing synthesis analysis

## Troubleshooting

### "riscv64-unknown-elf-objcopy: command not found"
Your tools aren't in PATH. Make sure `$HOME/.local/bin` is in your PATH:
```bash
export PATH=$HOME/.local/bin:$PATH
```

### "spike: command not found"
Same as above - verify spike is in `$HOME/.local/bin` or add it to PATH.

### "Wrong bitwidth" or ELF format errors
Make sure `CASCADE_RISCV_BITWIDTH=64` is set and you have the rv64 toolchain, not rv32.

### Import errors for Python modules
Make sure you're running from the `fuzzer/` directory, or add it to PYTHONPATH:
```bash
export PYTHONPATH=/path/to/cascade-meta/fuzzer:$PYTHONPATH
```

## Air-Gapped Machine Notes

For your air-gapped machine, you'll need to transfer:
1. This entire cascade-meta repository
2. Python packages (tqdm, matplotlib, numpy) - can use `pip download` on a connected machine
3. The makeelf library from `tools/makeelf` submodule

Since you already have the RISC-V toolchain and Spike installed, you're mostly ready to go!
