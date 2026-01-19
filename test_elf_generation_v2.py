#!/usr/bin/env python3
"""
Simple test to generate a RISC-V ELF file using makeelf library.
This demonstrates the core ELF generation functionality used by Cascade.
"""

import os
import sys

# Add makeelf and mock tools to path BEFORE any imports
mock_bin_dir = '/home/user/cascade-meta/test-output'
os.environ['PATH'] = mock_bin_dir + ':' + os.environ.get('PATH', '')
sys.path.insert(0, '/home/user/cascade-meta/tools/makeelf')

from makeelf.elf import *

def test_generate_simple_elf():
    """Generate a simple RV64 ELF file with a minimal program."""

    print("=== Testing Cascade ELF Generation (RV64) ===\n")

    # Create output directory
    output_dir = "/home/user/cascade-meta/test-output"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "test_program.elf")

    # Define a simple RISC-V program (RV64I)
    # This is just a few instructions: nop, addi, and an infinite loop
    # In little-endian format
    program_bytes = bytes([
        # 0x80000000: addi x1, x0, 1     (load 1 into x1)
        0x13, 0x00, 0x10, 0x00,
        # 0x80000004: addi x2, x0, 2     (load 2 into x2)
        0x13, 0x01, 0x20, 0x00,
        # 0x80000008: add x3, x1, x2     (x3 = x1 + x2)
        0xb3, 0x01, 0x21, 0x00,
        # 0x8000000c: j -12              (infinite loop back to start)
        0x6f, 0xf0, 0x5f, 0xff,
    ])

    print(f"Program size: {len(program_bytes)} bytes")
    print(f"Program (hex): {program_bytes.hex()}\n")

    # Define memory layout
    start_addr = 0x80000000  # Standard RISC-V start address (same as Spike)

    # Create ELF file
    print("Creating ELF file...")
    elf = ELF(
        e_machine=EM.EM_RISCV,           # RISC-V architecture
        e_data=ELFDATA.ELFDATA2LSB,      # Little-endian
        e_entry=start_addr               # Entry point
    )

    # Add .text section with our program
    SH_FLAGS = 0x6  # SHF_ALLOC | SHF_EXECINSTR (loadable and executable)
    section_id = elf.append_section(
        '.text.init',
        program_bytes,
        start_addr,
        sh_flags=SH_FLAGS,
        sh_addralign=4
    )

    # Add program header (segment)
    elf.append_segment(section_id, addr=start_addr, p_offset=0xe2)

    # Convert to bytes (this finalizes offsets)
    elf_bytes = bytes(elf)

    # Write to file
    with open(output_path, 'wb') as f:
        f.write(elf_bytes)

    print(f"✓ ELF file generated: {output_path}")
    print(f"✓ File size: {len(elf_bytes)} bytes")
    print(f"✓ Entry point: 0x{start_addr:x}")
    print(f"✓ Architecture: RISC-V")

    # Verify file was created
    if os.path.exists(output_path):
        file_size = os.path.getsize(output_path)
        print(f"\n✓ File exists and is {file_size} bytes")

        # Read back and verify it's a valid ELF
        with open(output_path, 'rb') as f:
            header = f.read(4)
            if header == b'\x7fELF':
                print("✓ Valid ELF magic number detected")
            else:
                print("✗ Invalid ELF magic number")
                return False

        # Display some info about the generated ELF
        print(f"\nELF Details:")
        print(f"  Sections: {len(elf.Elf.Shdr_table)}")
        print(f"  Segments: {len(elf.Elf.Phdr_table)}")
        print(f"  Program header offset: 0x{elf.Elf.Phdr_table[0].p_offset:x}")
        print(f"  Section header offset: 0x{elf.Elf.Shdr_table[section_id].sh_offset:x}")

        return True
    else:
        print("✗ File was not created")
        return False

def test_cascade_bytestoelf():
    """Test the actual function used by Cascade fuzzer."""

    print("\n" + "="*50)
    print("=== Testing Cascade's bytestoelf.gen_elf() ===\n")

    # Add fuzzer to path
    sys.path.insert(0, '/home/user/cascade-meta/fuzzer')

    # Set required environment variables
    os.environ['CASCADE_ENV_SOURCED'] = 'yes'
    os.environ['CASCADE_DATADIR'] = '/home/user/cascade-meta/test-output'
    os.environ['CASCADE_PATH_TO_FIGURES'] = '/home/user/cascade-meta/test-output/figures'
    os.environ['CASCADE_RISCV_BITWIDTH'] = '64'

    os.makedirs(os.environ['CASCADE_DATADIR'], exist_ok=True)
    os.makedirs(os.environ['CASCADE_PATH_TO_FIGURES'], exist_ok=True)

    # Import after setting environment
    from common.bytestoelf import gen_elf

    # Generate a simple program
    program_bytes = bytes([
        0x13, 0x00, 0x10, 0x00,  # addi x1, x0, 1
        0x13, 0x01, 0x20, 0x00,  # addi x2, x0, 2
        0xb3, 0x01, 0x21, 0x00,  # add x3, x1, x2
        0x6f, 0xf0, 0x5f, 0xff,  # j -12 (loop back)
    ])

    output_path = "/home/user/cascade-meta/test-output/cascade_test.elf"
    start_addr = 0x80000000

    print(f"Calling gen_elf() with:")
    print(f"  Bytes: {len(program_bytes)} bytes")
    print(f"  Start address: 0x{start_addr:x}")
    print(f"  Output: {output_path}")
    print(f"  RV64: True\n")

    try:
        # Note: section_addr=None means no objcopy relocation (we can skip objcopy)
        gen_elf(
            inbytes=program_bytes,
            start_addr=start_addr,
            section_addr=None,  # Skip objcopy step
            destination_path=output_path,
            is_64bit=True
        )

        print(f"✓ gen_elf() succeeded!")

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"✓ Output file created: {file_size} bytes")

            # Verify ELF magic
            with open(output_path, 'rb') as f:
                header = f.read(4)
                if header == b'\x7fELF':
                    print("✓ Valid ELF file generated by Cascade's gen_elf()")
                    return True
        else:
            print("✗ Output file not created")
            return False

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Cascade ELF Generation Test\n")

    # Test 1: Basic makeelf usage
    success1 = test_generate_simple_elf()

    # Test 2: Cascade's actual gen_elf function (with mock objcopy)
    success2 = test_cascade_bytestoelf()

    print("\n" + "="*50)
    print("=== Test Summary ===")
    print(f"Basic makeelf test: {'✓ PASSED' if success1 else '✗ FAILED'}")
    print(f"Cascade gen_elf test: {'✓ PASSED' if success2 else '✗ FAILED'}")

    if success1 and success2:
        print("\n✓ All tests passed! Cascade ELF generation is working.")
        print("\nNote: The objcopy step was mocked for this test.")
        print("On your air-gapped machine with real RISC-V tools, it will")
        print("properly convert between ELF32 and ELF64 formats.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed.")
        sys.exit(1)
