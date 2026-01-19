#!/usr/bin/env python3
"""
Standalone Cascade Fuzzer Demo - No RTL Required

This script demonstrates Cascade's core fuzzing algorithm:
- Control and data entanglement
- Random program generation
- Basic block construction

No design-specific RTL files needed!
"""

import os
import sys
import random

# Set up environment
if "CASCADE_ENV_SOURCED" not in os.environ:
    print("ERROR: Please source env-custom.sh first")
    print("  source env-custom.sh")
    sys.exit(1)

# IMPORTANT: Apply minimal design patch BEFORE importing cascade modules
from minimal_design_patch import patch_for_demo_design
patch_for_demo_design()

# Minimal design configuration (no RTL files needed)
MINIMAL_DESIGN = {
    'name': 'demo',
    'boot_addr': 0x80000000,  # Standard RISC-V boot address
    'is_32bit': False,        # RV64
}

def create_minimal_fuzzerstate(randseed=42, memsize=1024*64, nmax_bbs=10):
    """Create a FuzzerState without needing design config files"""
    from cascade.fuzzerstate import FuzzerState

    random.seed(randseed)

    # Create fuzzer state with minimal config
    fuzzerstate = FuzzerState(
        design_base_addr=MINIMAL_DESIGN['boot_addr'],
        design_name=MINIMAL_DESIGN['name'],
        memsize=memsize,
        randseed=randseed,
        nmax_bbs=nmax_bbs,
        authorize_privileges=False,  # Disable privilege mode for simplicity
        nmax_instructions=None,
        nodependencybias=False     # Enable dependency bias (key to Cascade!)
    )

    return fuzzerstate

def generate_cascade_program(randseed=42, verbose=True):
    """
    Generate a program using Cascade's algorithm

    This demonstrates the CORE of Cascade:
    - Control-flow and data-flow entanglement
    - Coverage-directed fuzzing
    """
    from cascade.basicblock import gen_basicblocks
    from cascade.genelf import gen_elf_from_bbs

    if verbose:
        print("="*70)
        print("CASCAD FUZZER - Standalone Demo")
        print("="*70)
        print(f"Seed: {randseed}")
        print()

    # Create fuzzer state
    fuzzerstate = create_minimal_fuzzerstate(randseed)

    if verbose:
        print("Step 1: Generating basic blocks with control/data entanglement...")

    # THIS IS THE CORE: Generate basic blocks with entangled control and data
    gen_basicblocks(fuzzerstate)

    if verbose:
        print(f"  ✓ Generated {len(fuzzerstate.bbs)} basic blocks")
        print(f"  ✓ Total instructions: {fuzzerstate.get_num_instructions()}")
        print()

        # Show some details about the generated program
        print("Program Structure:")
        for i, bb in enumerate(fuzzerstate.bbs):
            print(f"  BB{i}: {len(bb.instrs)} instructions")
            if i < 3:  # Show first 3 BBs in detail
                for j, instr in enumerate(bb.instrs[:5]):  # First 5 instrs
                    print(f"    [{j}] {instr}")
                if len(bb.instrs) > 5:
                    print(f"    ... ({len(bb.instrs)-5} more instructions)")
        print()

    # Generate ELF file
    if verbose:
        print("Step 2: Generating ELF file...")

    elf_path = gen_elf_from_bbs(
        fuzzerstate,
        False,  # is_spike
        'demo',  # elf_type
        f'cascade_demo_{randseed}',  # instance_str
        fuzzerstate.design_base_addr
    )

    if verbose:
        print(f"  ✓ ELF file created: {elf_path}")
        file_size = os.path.getsize(elf_path)
        print(f"  ✓ File size: {file_size} bytes")
        print()

    return fuzzerstate, elf_path

def demonstrate_entanglement(fuzzerstate, num_samples=5):
    """
    Demonstrate how Cascade entangles control and data flow

    Key insight: Instructions are chosen based on PREVIOUS results,
    creating complex dependencies that stress the processor.
    """
    print("="*70)
    print("CONTROL & DATA ENTANGLEMENT ANALYSIS")
    print("="*70)
    print()
    print("Cascade's key innovation: Instructions are not independent!")
    print("Each instruction's operands depend on previous results,")
    print("creating complex dependency chains.")
    print()

    # Analyze register dependencies
    print("Register Dependency Analysis:")
    for i, bb in enumerate(fuzzerstate.bbs[:num_samples]):
        print(f"\nBasic Block {i}:")
        print(f"  Instructions: {len(bb.instrs)}")

        # Track which registers are read and written
        written_regs = set()
        read_regs = set()

        for instr in bb.instrs[:10]:  # Sample first 10
            instr_str = str(instr)

            # Simple heuristic to find register usage
            # (Cascade tracks this internally in fuzzerstate)
            if hasattr(instr, 'rd') and instr.rd is not None:
                written_regs.add(f"x{instr.rd}")
            if hasattr(instr, 'rs1') and instr.rs1 is not None:
                read_regs.add(f"x{instr.rs1}")
            if hasattr(instr, 'rs2') and instr.rs2 is not None:
                read_regs.add(f"x{instr.rs2}")

        print(f"  Registers written: {sorted(written_regs)}")
        print(f"  Registers read: {sorted(read_regs)}")

        # Calculate dependency ratio
        if written_regs and read_regs:
            deps = written_regs & read_regs
            print(f"  Dependency chain: {len(deps)} regs both read and written")
            print(f"    → This creates data hazards in out-of-order CPUs!")

    print()
    print("This entanglement is WHY Cascade finds bugs that random")
    print("testing misses: it creates realistic dependency patterns!")
    print()

def main():
    import argparse

    parser = argparse.ArgumentParser(
        description='Cascade Fuzzer Demo - No RTL Required',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a simple program
  python demo_cascade_standalone.py

  # Generate with specific seed
  python demo_cascade_standalone.py --seed 12345

  # Show detailed analysis
  python demo_cascade_standalone.py --analyze

  # Generate multiple programs
  python demo_cascade_standalone.py --count 3
"""
    )

    parser.add_argument('--seed', type=int, default=42,
                        help='Random seed (default: 42)')
    parser.add_argument('--analyze', action='store_true',
                        help='Show detailed entanglement analysis')
    parser.add_argument('--count', type=int, default=1,
                        help='Number of programs to generate')
    parser.add_argument('--quiet', action='store_true',
                        help='Minimal output')

    args = parser.parse_args()

    try:
        for i in range(args.count):
            seed = args.seed + i

            # Generate program
            fuzzerstate, elf_path = generate_cascade_program(
                randseed=seed,
                verbose=not args.quiet
            )

            # Show entanglement analysis if requested
            if args.analyze and not args.quiet:
                demonstrate_entanglement(fuzzerstate)

            if not args.quiet:
                print("="*70)
                print("SUCCESS!")
                print("="*70)
                print(f"Generated ELF: {elf_path}")
                print()
                print("You can disassemble with:")
                print(f"  riscv64-unknown-elf-objdump -d {elf_path}")
                print()
                print("Or run on Spike (if available):")
                print(f"  spike --isa=rv64gc {elf_path}")
                print("="*70)
                print()

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

    return 0

if __name__ == '__main__':
    sys.exit(main())
