# Custom environment configuration for using pre-installed RISC-V tools
# Source this file instead of env.sh, or source it after env.sh to override settings

# First source the default env.sh to get all other settings
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/env.sh"

# ============================================================================
# CUSTOM CONFIGURATION: Use existing RISC-V tools from $HOME/.local
# ============================================================================

# Point to your existing RISC-V toolchain installation
export RISCV=$HOME/.local

# Use rv64 instead of rv32 (this is already the default in env.sh, but making it explicit)
export CASCADE_RISCV_BITWIDTH=64

# Update compiler variables to use rv64 (these aren't used by Python scripts but good to set)
export CASCADE_GCC=riscv64-unknown-elf-gcc
export CASCADE_OBJDUMP=riscv64-unknown-elf-objdump

# Prioritize your existing tools in PATH
# This ensures spike and riscv64-unknown-elf-* tools from $HOME/.local/bin are found first
export PATH=$HOME/.local/bin:$PATH

# Override PREFIX_CASCADE if you want to avoid installing bundled tools
# Uncomment the line below if you want to store Cascade's own tools separately
# export PREFIX_CASCADE=$HOME/prefix-cascade

# Set data directories (customize as needed for your air-gapped machine)
export CASCADE_DATADIR=$HOME/cascade-data
export CASCADE_PATH_TO_FIGURES=$HOME/cascade-figures

# Create directories if they don't exist
mkdir -p "$CASCADE_DATADIR"
mkdir -p "$CASCADE_PATH_TO_FIGURES"

# Verify tools are available
echo "=== Verifying RISC-V Tools ==="
which spike || echo "WARNING: spike not found in PATH"
which riscv64-unknown-elf-gcc || echo "WARNING: riscv64-unknown-elf-gcc not found in PATH"
which riscv64-unknown-elf-objcopy || echo "WARNING: riscv64-unknown-elf-objcopy not found in PATH"
which riscv64-unknown-elf-objdump || echo "WARNING: riscv64-unknown-elf-objdump not found in PATH"

echo "CASCADE_RISCV_BITWIDTH=$CASCADE_RISCV_BITWIDTH"
echo "RISCV=$RISCV"
echo "CASCADE environment configured for rv64 with existing tools"
