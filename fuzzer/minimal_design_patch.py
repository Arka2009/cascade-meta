"""
Minimal design configuration patch for standalone demo

This patches the design config functions to work without RTL files
"""

import common.designcfgs as designcfgs

# Store original functions
_original_funcs = {}

def patch_for_demo_design():
    """Monkey-patch design config functions for 'demo' design"""

    # Save originals
    _original_funcs['is_design_32bit'] = designcfgs.is_design_32bit
    _original_funcs['design_has_float_support'] = designcfgs.design_has_float_support
    _original_funcs['design_has_double_support'] = designcfgs.design_has_double_support
    _original_funcs['design_has_muldiv_support'] = designcfgs.design_has_muldiv_support
    _original_funcs['design_has_atop_support'] = designcfgs.design_has_atop_support
    _original_funcs['design_has_misaligned_data_support'] = designcfgs.design_has_misaligned_data_support
    _original_funcs['get_design_boot_addr'] = designcfgs.get_design_boot_addr
    _original_funcs['design_has_supervisor_mode'] = designcfgs.design_has_supervisor_mode
    _original_funcs['design_has_user_mode'] = designcfgs.design_has_user_mode
    _original_funcs['design_has_compressed_support'] = designcfgs.design_has_compressed_support
    _original_funcs['design_has_pmp'] = designcfgs.design_has_pmp

    # Minimal RV64GC configuration (common for testing)
    DEMO_CONFIG = {
        'is_32bit': False,           # RV64
        'has_float': True,            # F extension
        'has_double': True,           # D extension
        'has_muldiv': True,           # M extension
        'has_atomics': True,          # A extension
        'has_misaligned': True,       # Allow misaligned access
        'boot_addr': 0x80000000,      # Standard RISC-V
        'has_supervisor': False,      # Keep it simple for demo
        'has_user': False,            # Keep it simple for demo
        'has_compressed': False,      # C extension (disabled for clarity)
        'has_pmp': False,             # Physical memory protection
    }

    # Patched functions
    def is_design_32bit_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['is_32bit']
        return _original_funcs['is_design_32bit'](design_name)

    def design_has_float_support_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_float']
        return _original_funcs['design_has_float_support'](design_name)

    def design_has_double_support_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_double']
        return _original_funcs['design_has_double_support'](design_name)

    def design_has_muldiv_support_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_muldiv']
        return _original_funcs['design_has_muldiv_support'](design_name)

    def design_has_atop_support_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_atomics']
        return _original_funcs['design_has_atop_support'](design_name)

    def design_has_misaligned_data_support_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_misaligned']
        return _original_funcs['design_has_misaligned_data_support'](design_name)

    def get_design_boot_addr_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['boot_addr']
        return _original_funcs['get_design_boot_addr'](design_name)

    def design_has_supervisor_mode_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_supervisor']
        return _original_funcs['design_has_supervisor_mode'](design_name)

    def design_has_user_mode_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_user']
        return _original_funcs['design_has_user_mode'](design_name)

    def design_has_compressed_support_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_compressed']
        return _original_funcs['design_has_compressed_support'](design_name)

    def design_has_pmp_patched(design_name):
        if design_name == 'demo':
            return DEMO_CONFIG['has_pmp']
        return _original_funcs['design_has_pmp'](design_name)

    # Apply patches
    designcfgs.is_design_32bit = is_design_32bit_patched
    designcfgs.design_has_float_support = design_has_float_support_patched
    designcfgs.design_has_double_support = design_has_double_support_patched
    designcfgs.design_has_muldiv_support = design_has_muldiv_support_patched
    designcfgs.design_has_atop_support = design_has_atop_support_patched
    designcfgs.design_has_misaligned_data_support = design_has_misaligned_data_support_patched
    designcfgs.get_design_boot_addr = get_design_boot_addr_patched
    designcfgs.design_has_supervisor_mode = design_has_supervisor_mode_patched
    designcfgs.design_has_user_mode = design_has_user_mode_patched
    designcfgs.design_has_compressed_support = design_has_compressed_support_patched
    designcfgs.design_has_pmp = design_has_pmp_patched

def unpatch_design_functions():
    """Restore original functions"""
    if not _original_funcs:
        return

    designcfgs.is_design_32bit = _original_funcs['is_design_32bit']
    designcfgs.design_has_float_support = _original_funcs['design_has_float_support']
    designcfgs.design_has_double_support = _original_funcs['design_has_double_support']
    designcfgs.design_has_muldiv_support = _original_funcs['design_has_muldiv_support']
    designcfgs.design_has_atop_support = _original_funcs['design_has_atop_support']
    designcfgs.design_has_misaligned_data_support = _original_funcs['design_has_misaligned_data_support']
    designcfgs.get_design_boot_addr = _original_funcs['get_design_boot_addr']
    designcfgs.design_has_supervisor_mode = _original_funcs['design_has_supervisor_mode']
    designcfgs.design_has_user_mode = _original_funcs['design_has_user_mode']
    designcfgs.design_has_compressed_support = _original_funcs['design_has_compressed_support']
    designcfgs.design_has_pmp = _original_funcs['design_has_pmp']
