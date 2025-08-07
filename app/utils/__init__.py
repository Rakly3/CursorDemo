"""
Utility Functions Package
========================

This package contains utility functions and helper classes for the
Cursor IDE demo application.

Author: Cursor IDE Demo
Version: 1.0.0
"""

from .logger import setup_logging, get_logger
from .performance import PerformanceMonitor, FPSMonitor
from .math_utils import clamp, lerp, smooth_step, random_range
from .color_utils import Color, hex_to_rgb, rgb_to_hex, blend_colors

__all__ = [
    'setup_logging',
    'get_logger',
    'PerformanceMonitor',
    'FPSMonitor',
    'clamp',
    'lerp',
    'smooth_step',
    'random_range',
    'Color',
    'hex_to_rgb',
    'rgb_to_hex',
    'blend_colors'
] 