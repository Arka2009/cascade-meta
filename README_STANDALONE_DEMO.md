# Cascade Fuzzer - Standalone Demo (No RTL Required)

## Problem

The default Cascade scripts (`do_fuzzsingle.py`, `do_genmanyelfs.py`) expect design-specific RTL configuration files like:
```
/cascade-boom/meta/cfg.json
```

This causes errors when you just want to understand **how Cascade works** without setting up the full RTL environment.

## Solution: Standalone Demo Script

I've created `fuzzer/demo_cascade_standalone.py` that demonstrates Cascade's core algorithm **without requiring any RTL files**.

### What It Does

1. **Generates random RISC-V programs** using Cascade's fuzzing algorithm
2. **Demonstrates control & data entanglement** (Cascade's key innovation)
3. **Creates ELF files** you can inspect or run on Spike
4. **No design files needed** - uses a minimal RV64GC configuration

## Usage

### Basic Usage

```bash
# 1. Set up environment
source env-custom.sh

# 2. Run the demo
cd fuzzer
python3 demo_cascade_standalone.py
```

### Output Example

```
======================================================================
CASCADE FUZZER - Standalone Demo
======================================================================
Seed: 42

Step 1: Generating basic blocks with control/data entanglement...
  ✓ Generated 10 basic blocks
  ✓ Total instructions: 245

Program Structure:
  BB0: 32 instructions
    [0] addi x3, x0, 1
    [1] lui x4, 0x12
    [2] add x5, x3, x4
    ... (29 more instructions)
  BB1: 28 instructions
  ...

Step 2: Generating ELF file...
  ✓ ELF file created: /path/to/cascade_demo_42.elf
  ✓ File size: 1524 bytes
```

### Advanced Usage

```bash
# Generate with specific seed
python3 demo_cascade_standalone.py --seed 12345

# Show detailed entanglement analysis
python3 demo_cascade_standalone.py --analyze

# Generate multiple programs
python3 demo_cascade_standalone.py --count 5

# Quiet mode (minimal output)
python3 demo_cascade_standalone.py --quiet
```

## Understanding Cascade's Innovation

### Key Concept: Control & Data Entanglement

Run with `--analyze` to see how Cascade creates dependencies:

```bash
python3 demo_cascade_standalone.py --analyze
```

This shows:
- Which registers are written and read in each basic block
- How many registers are in dependency chains
- Why this stresses out-of-order processors

### Example Analysis Output

```
CONTROL & DATA ENTANGLEMENT ANALYSIS
====================================================================

Cascade's key innovation: Instructions are not independent!
Each instruction's operands depend on previous results,
creating complex dependency chains.

Register Dependency Analysis:

Basic Block 0:
  Instructions: 32
  Registers written: ['x1', 'x2', 'x3', 'x4', 'x5']
  Registers read: ['x1', 'x2', 'x3', 'x4']
  Dependency chain: 4 regs both read and written
    → This creates data hazards in out-of-order CPUs!

...

This entanglement is WHY Cascade finds bugs that random
testing misses: it creates realistic dependency patterns!
```

## How It Works

### 1. Minimal Design Patch

The script uses `minimal_design_patch.py` to provide a minimal RV64GC configuration:

```python
DEMO_CONFIG = {
    'is_32bit': False,           # RV64
    'has_float': True,            # F extension
    'has_double': True,           # D extension
    'has_muldiv': True,           # M extension
    'has_atomics': True,          # A extension
    'boot_addr': 0x80000000,      # Standard RISC-V
    # Supervisor/user modes disabled for simplicity
}
```

This monkey-patches the design config functions so they don't try to read RTL files.

### 2. Core Fuzzing Logic

The script calls the **same functions** that the full fuzzer uses:

```python
from cascade.fuzzerstate import FuzzerState
from cascade.basicblock import gen_basicblocks  # The CORE algorithm!
from cascade.genelf import gen_elf_from_bbs

# Create fuzzer state
fuzzerstate = FuzzerState(...)

# Generate program with entangled control & data
gen_basicblocks(fuzzerstate)  # ← This is where the magic happens!

# Create ELF
gen_elf_from_bbs(fuzzerstate, ...)
```

### 3. What's Skipped

The demo **SKIPS**:
- RTL simulation (Verilator/ModelSim)
- Design-specific profiling (`profile_get_medeleg_mask`)
- Spike speed calibration
- Bug detection (no comparison with expected values)

But you **STILL GET**:
- Cascade's program generation algorithm
- Control & data entanglement
- Valid RISC-V ELF files
- Understanding of how Cascade works!

## Inspecting Generated Programs

### Disassemble with objdump

```bash
riscv64-unknown-elf-objdump -d /path/to/generated.elf
```

### Run on Spike (if available)

```bash
spike --isa=rv64gc /path/to/generated.elf
```

## What You Learn

By running this demo, you understand:

1. **How Cascade generates programs**
   - Not purely random!
   - Creates dependency chains between instructions

2. **Why entanglement matters**
   - Realistic instruction patterns
   - Stresses microarchitectural features
   - Finds bugs that random testing misses

3. **Cascade's algorithm structure**
   - FuzzerState tracks register dependencies
   - Basic block generation with coverage goals
   - Control flow and data flow are intertwined

## Comparison: Random vs. Cascade

### Random Fuzzer
```
addi x1, x0, 5    # Independent
addi x2, x0, 10   # Independent
addi x3, x0, 15   # Independent
```
No dependencies → Doesn't stress pipeline/OoO execution

### Cascade Fuzzer
```
addi x1, x0, 5    # x1 = 5
add x2, x1, x1    # x2 = x1 + x1 (depends on x1)
sll x3, x2, x1    # x3 = x2 << x1 (depends on x1 and x2)
```
Dependency chain → Stresses forwarding, hazards, OoO scheduling

## Troubleshooting

### Error: "CASCADE_ENV_SOURCED not set"

```bash
source env-custom.sh
```

### Error: "No module named 'makeelf'"

```bash
# env-custom.sh should add makeelf to PYTHONPATH
echo $PYTHONPATH | grep makeelf
```

### Error: "No module named minimal_design_patch"

```bash
# Make sure you're in the fuzzer/ directory
cd fuzzer
python3 demo_cascade_standalone.py
```

## Next Steps

Once you understand the algorithm:

1. **Add Spike validation** - Compare fuzzer output with Spike execution
2. **Add RTL simulation** - Run on real hardware designs
3. **Add bug detection** - Compare RTL vs. Spike results
4. **Add coverage tracking** - Measure code coverage improvements

But for understanding **how Cascade works**, this demo is all you need!

## References

- Cascade paper: [Control and Data Flow Entanglement for Processor Verification](https://flaviensolt.github.io/docs/solt2023cascade.pdf)
- Key insight: "Cascade entangles control and data flow to create realistic instruction patterns that expose microarchitectural bugs"

---

**TL;DR**: Run `python3 demo_cascade_standalone.py --analyze` to see Cascade's entanglement algorithm in action, no RTL required!
