"""
Color Utilities
==============

This module provides color utility functions and classes for the
Cursor IDE demo application, including color manipulation, conversion,
and generation.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import colorsys
import random
from typing import Tuple, List, Optional, Union
from dataclasses import dataclass


@dataclass
class Color:
    """
    Color class with RGB components
    
    This class provides color manipulation and conversion capabilities
    with support for RGB, HSV, and HSL color spaces.
    """
    r: int
    g: int
    b: int
    a: int = 255
    
    def __post_init__(self):
        """Validate color components after initialization"""
        self.r = max(0, min(255, int(self.r)))
        self.g = max(0, min(255, int(self.g)))
        self.b = max(0, min(255, int(self.b)))
        self.a = max(0, min(255, int(self.a)))
    
    def to_tuple(self) -> Tuple[int, int, int, int]:
        """Convert to RGBA tuple"""
        return (self.r, self.g, self.b, self.a)
    
    def to_rgb_tuple(self) -> Tuple[int, int, int]:
        """Convert to RGB tuple"""
        return (self.r, self.g, self.b)
    
    def to_hex(self) -> str:
        """Convert to hexadecimal string"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"
    
    def to_hex_alpha(self) -> str:
        """Convert to hexadecimal string with alpha"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}{self.a:02x}"
    
    def to_hsv(self) -> Tuple[float, float, float]:
        """Convert to HSV tuple"""
        h, s, v = colorsys.rgb_to_hsv(self.r / 255.0, self.g / 255.0, self.b / 255.0)
        return (h, s, v)
    
    def to_hsl(self) -> Tuple[float, float, float]:
        """Convert to HSL tuple"""
        h, l, s = colorsys.rgb_to_hls(self.r / 255.0, self.g / 255.0, self.b / 255.0)
        return (h, s, l)
    
    def brightness(self) -> float:
        """Calculate color brightness (0.0 to 1.0)"""
        return (0.299 * self.r + 0.587 * self.g + 0.114 * self.b) / 255.0
    
    def is_dark(self) -> bool:
        """Check if color is dark"""
        return self.brightness() < 0.5
    
    def is_light(self) -> bool:
        """Check if color is light"""
        return self.brightness() >= 0.5
    
    def contrast_color(self) -> 'Color':
        """Get contrasting color (black or white)"""
        return Color(0, 0, 0) if self.is_light() else Color(255, 255, 255)
    
    def blend(self, other: 'Color', factor: float = 0.5) -> 'Color':
        """Blend with another color"""
        factor = max(0.0, min(1.0, factor))
        r = int(self.r * (1 - factor) + other.r * factor)
        g = int(self.g * (1 - factor) + other.g * factor)
        b = int(self.b * (1 - factor) + other.b * factor)
        a = int(self.a * (1 - factor) + other.a * factor)
        return Color(r, g, b, a)
    
    def darken(self, factor: float = 0.2) -> 'Color':
        """Darken the color"""
        factor = max(0.0, min(1.0, factor))
        r = int(self.r * (1 - factor))
        g = int(self.g * (1 - factor))
        b = int(self.b * (1 - factor))
        return Color(r, g, b, self.a)
    
    def lighten(self, factor: float = 0.2) -> 'Color':
        """Lighten the color"""
        factor = max(0.0, min(1.0, factor))
        r = int(self.r + (255 - self.r) * factor)
        g = int(self.g + (255 - self.g) * factor)
        b = int(self.b + (255 - self.b) * factor)
        return Color(r, g, b, self.a)
    
    def saturate(self, factor: float = 0.2) -> 'Color':
        """Increase color saturation"""
        h, s, v = self.to_hsv()
        s = min(1.0, s + factor)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color(int(r * 255), int(g * 255), int(b * 255), self.a)
    
    def desaturate(self, factor: float = 0.2) -> 'Color':
        """Decrease color saturation"""
        h, s, v = self.to_hsv()
        s = max(0.0, s - factor)
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color(int(r * 255), int(g * 255), int(b * 255), self.a)
    
    def rotate_hue(self, angle: float) -> 'Color':
        """Rotate hue by angle (0.0 to 1.0)"""
        h, s, v = self.to_hsv()
        h = (h + angle) % 1.0
        r, g, b = colorsys.hsv_to_rgb(h, s, v)
        return Color(int(r * 255), int(g * 255), int(b * 255), self.a)
    
    def __str__(self) -> str:
        return f"Color({self.r}, {self.g}, {self.b}, {self.a})"
    
    def __repr__(self) -> str: 
        return self.__str__() # Explain __str__: This is a special method in Python that is used to define the string representation of an object. It is called when the object is converted to a string, such as when it is printed or used in a string concatenation.


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hexadecimal color to RGB tuple
    
    Args:
        hex_color: Hexadecimal color string (e.g., "#FF0000")
        
    Returns:
        RGB tuple
    """
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3:
        hex_color = ''.join([c * 2 for c in hex_color])
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB values to hexadecimal string
    
    Args:
        r: Red component (0-255)
        g: Green component (0-255)
        b: Blue component (0-255)
        
    Returns:
        Hexadecimal color string
    """
    return f"#{r:02x}{g:02x}{b:02x}"


def blend_colors(color1: Color, color2: Color, factor: float = 0.5) -> Color:
    """
    Blend two colors
    
    Args:
        color1: First color
        color2: Second color
        factor: Blend factor (0.0 to 1.0)
        
    Returns:
        Blended color
    """
    return color1.blend(color2, factor)


def random_color() -> Color:
    """Generate a random color"""
    return Color(
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def random_bright_color() -> Color:
    """Generate a random bright color"""
    h = random.random()
    s = random.uniform(0.5, 1.0)
    v = random.uniform(0.7, 1.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return Color(int(r * 255), int(g * 255), int(b * 255))


def random_pastel_color() -> Color:
    """Generate a random pastel color"""
    h = random.random()
    s = random.uniform(0.2, 0.5)
    v = random.uniform(0.8, 1.0)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return Color(int(r * 255), int(g * 255), int(b * 255))


def random_dark_color() -> Color:
    """Generate a random dark color"""
    h = random.random()
    s = random.uniform(0.3, 0.8)
    v = random.uniform(0.1, 0.4)
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return Color(int(r * 255), int(g * 255), int(b * 255))


def color_gradient(color1: Color, color2: Color, steps: int) -> List[Color]:
    """
    Generate a gradient between two colors
    
    Args:
        color1: Start color
        color2: End color
        steps: Number of steps in gradient
        
    Returns:
        List of colors forming the gradient
    """
    colors = []
    for i in range(steps):
        factor = i / (steps - 1) if steps > 1 else 0
        colors.append(color1.blend(color2, factor))
    return colors


def rainbow_colors(steps: int) -> List[Color]:
    """
    Generate rainbow colors
    
    Args:
        steps: Number of colors to generate
        
    Returns:
        List of rainbow colors
    """
    colors = []
    for i in range(steps):
        h = i / steps
        r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        colors.append(Color(int(r * 255), int(g * 255), int(b * 255)))
    return colors


def complementary_color(color: Color) -> Color:
    """
    Get complementary color
    
    Args:
        color: Input color
        
    Returns:
        Complementary color
    """
    h, s, v = color.to_hsv()
    h = (h + 0.5) % 1.0
    r, g, b = colorsys.hsv_to_rgb(h, s, v)
    return Color(int(r * 255), int(g * 255), int(b * 255))


def analogous_colors(color: Color, count: int = 3) -> List[Color]:
    """
    Generate analogous colors
    
    Args:
        color: Base color
        count: Number of colors to generate
        
    Returns:
        List of analogous colors
    """
    h, s, v = color.to_hsv()
    colors = []
    step = 0.0833  # 30 degrees in hue space
    
    for i in range(count):
        offset = (i - count // 2) * step
        new_h = (h + offset) % 1.0
        r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
        colors.append(Color(int(r * 255), int(g * 255), int(b * 255)))
    
    return colors


def triadic_colors(color: Color) -> List[Color]:
    """
    Generate triadic colors
    
    Args:
        color: Base color
        
    Returns:
        List of triadic colors
    """
    h, s, v = color.to_hsv()
    colors = []
    
    for i in range(3):
        new_h = (h + i * 0.3333) % 1.0
        r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
        colors.append(Color(int(r * 255), int(g * 255), int(b * 255)))
    
    return colors


def tetradic_colors(color: Color) -> List[Color]:
    """
    Generate tetradic colors
    
    Args:
        color: Base color
        
    Returns:
        List of tetradic colors
    """
    h, s, v = color.to_hsv()
    colors = []
    
    for i in range(4):
        new_h = (h + i * 0.25) % 1.0
        r, g, b = colorsys.hsv_to_rgb(new_h, s, v)
        colors.append(Color(int(r * 255), int(g * 255), int(b * 255)))
    
    return colors


def color_from_name(name: str) -> Optional[Color]:
    """
    Get color from common color name
    
    Args:
        name: Color name
        
    Returns:
        Color object or None if not found
    """
    color_map = {
        'red': Color(255, 0, 0),
        'green': Color(0, 255, 0),
        'blue': Color(0, 0, 255),
        'yellow': Color(255, 255, 0),
        'cyan': Color(0, 255, 255),
        'magenta': Color(255, 0, 255),
        'white': Color(255, 255, 255),
        'black': Color(0, 0, 0),
        'gray': Color(128, 128, 128),
        'orange': Color(255, 165, 0),
        'purple': Color(128, 0, 128),
        'pink': Color(255, 192, 203),
        'brown': Color(165, 42, 42),
        'lime': Color(0, 255, 0),
        'navy': Color(0, 0, 128),
        'teal': Color(0, 128, 128),
        'olive': Color(128, 128, 0),
        'maroon': Color(128, 0, 0),
        'silver': Color(192, 192, 192),
        'gold': Color(255, 215, 0)
    }
    
    return color_map.get(name.lower())


def color_distance(color1: Color, color2: Color) -> float:
    """
    Calculate color distance using RGB space
    
    Args:
        color1: First color
        color2: Second color
        
    Returns:
        Color distance
    """
    dr = color1.r - color2.r
    dg = color1.g - color2.g
    db = color1.b - color2.b
    return (dr * dr + dg * dg + db * db) ** 0.5


def find_closest_color(target: Color, colors: List[Color]) -> Color:
    """
    Find the closest color from a list
    
    Args:
        target: Target color
        colors: List of colors to search
        
    Returns:
        Closest color
    """
    if not colors:
        return target
    
    closest = colors[0]
    min_distance = color_distance(target, closest)
    
    for color in colors[1:]:
        distance = color_distance(target, color)
        if distance < min_distance:
            min_distance = distance
            closest = color
    
    return closest


if __name__ == "__main__":
    # Test color utilities
    print("🧪 Testing Color Utilities...")
    
    # Test Color class
    red = Color(255, 0, 0)
    blue = Color(0, 0, 255)
    print(f"Red: {red}")
    print(f"Blue: {blue}")
    print(f"Red brightness: {red.brightness():.3f}")
    print(f"Red is dark: {red.is_dark()}")
    
    # Test color blending
    purple = red.blend(blue, 0.5)
    print(f"Red + Blue = {purple}")
    
    # Test color conversion
    print(f"Red to hex: {red.to_hex()}")
    print(f"Red to HSV: {red.to_hsv()}")
    print(f"Red to HSL: {red.to_hsl()}")
    
    # Test utility functions
    print(f"Random color: {random_color()}")
    print(f"Random bright color: {random_bright_color()}")
    print(f"Random pastel color: {random_pastel_color()}")
    
    # Test color schemes
    print(f"Complementary to red: {complementary_color(red)}")
    print(f"Analogous to red: {analogous_colors(red)}")
    print(f"Triadic to red: {triadic_colors(red)}")
    
    # Test color names
    print(f"Color from name 'green': {color_from_name('green')}")
    
    print("✅ Color utilities test completed!") 