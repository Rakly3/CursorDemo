"""
Mathematical Utilities
=====================

This module provides mathematical utility functions commonly used in
game development and graphics programming.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import math
import random
from typing import Tuple, List, Union, Optional
import numpy as np


def clamp(value: float, min_val: float, max_val: float) -> float:
    """
    Clamp a value between a minimum and maximum
    
    Args:
        value: Value to clamp
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Clamped value
    """
    return max(min_val, min(value, max_val))


def lerp(start: float, end: float, t: float) -> float:
    """
    Linear interpolation between two values
    
    Args:
        start: Start value
        end: End value
        t: Interpolation factor (0.0 to 1.0)
        
    Returns:
        Interpolated value
    """
    return start + (end - start) * clamp(t, 0.0, 1.0)


def smooth_step(edge0: float, edge1: float, x: float) -> float:
    """
    Smooth step interpolation
    
    Args:
        edge0: Lower edge
        edge1: Upper edge
        x: Input value
        
    Returns:
        Smooth step value
    """
    t = clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def random_range(min_val: float, max_val: float) -> float:
    """
    Generate a random float between min and max
    
    Args:
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Random value
    """
    return random.uniform(min_val, max_val)


def random_int_range(min_val: int, max_val: int) -> int:
    """
    Generate a random integer between min and max (inclusive)
    
    Args:
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Random integer
    """
    return random.randint(min_val, max_val)


def random_choice(choices: List) -> any:
    """
    Choose a random element from a list
    
    Args:
        choices: List of choices
        
    Returns:
        Random choice
    """
    return random.choice(choices)


def random_weighted_choice(choices: List, weights: List[float]) -> any:
    """
    Choose a random element from a list with weights
    
    Args:
        choices: List of choices
        weights: List of weights
        
    Returns:
        Random choice based on weights
    """
    return random.choices(choices, weights=weights, k=1)[0]


def distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate Euclidean distance between two points
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
        
    Returns:
        Distance between points
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return math.sqrt(dx * dx + dy * dy)


def distance_squared(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
    """
    Calculate squared Euclidean distance between two points
    
    Args:
        point1: First point (x, y)
        point2: Second point (x, y)
        
    Returns:
        Squared distance between points
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    return dx * dx + dy * dy


def normalize_vector(vector: Tuple[float, float]) -> Tuple[float, float]:
    """
    Normalize a 2D vector
    
    Args:
        vector: Input vector (x, y)
        
    Returns:
        Normalized vector
    """
    length = math.sqrt(vector[0] * vector[0] + vector[1] * vector[1])
    if length == 0:
        return (0, 0)
    return (vector[0] / length, vector[1] / length)


def dot_product(vector1: Tuple[float, float], vector2: Tuple[float, float]) -> float:
    """
    Calculate dot product of two 2D vectors
    
    Args:
        vector1: First vector (x, y)
        vector2: Second vector (x, y)
        
    Returns:
        Dot product
    """
    return vector1[0] * vector2[0] + vector1[1] * vector2[1]


def cross_product(vector1: Tuple[float, float], vector2: Tuple[float, float]) -> float:
    """
    Calculate cross product of two 2D vectors
    
    Args:
        vector1: First vector (x, y)
        vector2: Second vector (x, y)
        
    Returns:
        Cross product (scalar for 2D)
    """
    return vector1[0] * vector2[1] - vector1[1] * vector2[0]


def rotate_point(point: Tuple[float, float], center: Tuple[float, float], angle: float) -> Tuple[float, float]:
    """
    Rotate a point around a center by an angle
    
    Args:
        point: Point to rotate (x, y)
        center: Center of rotation (x, y)
        angle: Rotation angle in radians
        
    Returns:
        Rotated point
    """
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    
    dx = point[0] - center[0]
    dy = point[1] - center[1]
    
    new_x = center[0] + dx * cos_a - dy * sin_a
    new_y = center[1] + dx * sin_a + dy * cos_a
    
    return (new_x, new_y)


def angle_between_vectors(vector1: Tuple[float, float], vector2: Tuple[float, float]) -> float:
    """
    Calculate angle between two 2D vectors
    
    Args:
        vector1: First vector (x, y)
        vector2: Second vector (x, y)
        
    Returns:
        Angle in radians
    """
    dot = dot_product(vector1, vector2)
    det = cross_product(vector1, vector2)
    return math.atan2(det, dot)


def point_in_circle(point: Tuple[float, float], center: Tuple[float, float], radius: float) -> bool:
    """
    Check if a point is inside a circle
    
    Args:
        point: Point to check (x, y)
        center: Circle center (x, y)
        radius: Circle radius
        
    Returns:
        True if point is inside circle
    """
    return distance_squared(point, center) <= radius * radius


def point_in_rect(point: Tuple[float, float], rect: Tuple[float, float, float, float]) -> bool:
    """
    Check if a point is inside a rectangle
    
    Args:
        point: Point to check (x, y)
        rect: Rectangle (x, y, width, height)
        
    Returns:
        True if point is inside rectangle
    """
    return (rect[0] <= point[0] <= rect[0] + rect[2] and
            rect[1] <= point[1] <= rect[1] + rect[3])


def circles_intersect(center1: Tuple[float, float], radius1: float,
                     center2: Tuple[float, float], radius2: float) -> bool:
    """
    Check if two circles intersect
    
    Args:
        center1: First circle center (x, y)
        radius1: First circle radius
        center2: Second circle center (x, y)
        radius2: Second circle radius
        
    Returns:
        True if circles intersect
    """
    dist = distance(center1, center2)
    return dist <= radius1 + radius2


def rects_intersect(rect1: Tuple[float, float, float, float],
                   rect2: Tuple[float, float, float, float]) -> bool:
    """
    Check if two rectangles intersect
    
    Args:
        rect1: First rectangle (x, y, width, height)
        rect2: Second rectangle (x, y, width, height)
        
    Returns:
        True if rectangles intersect
    """
    return not (rect1[0] + rect1[2] < rect2[0] or
                rect2[0] + rect2[2] < rect1[0] or
                rect1[1] + rect1[3] < rect2[1] or
                rect2[1] + rect2[3] < rect1[1])


def bezier_curve(p0: Tuple[float, float], p1: Tuple[float, float],
                p2: Tuple[float, float], p3: Tuple[float, float], t: float) -> Tuple[float, float]:
    """
    Calculate point on a cubic Bezier curve
    
    Args:
        p0: Start point (x, y)
        p1: First control point (x, y)
        p2: Second control point (x, y)
        p3: End point (x, y)
        t: Parameter (0.0 to 1.0)
        
    Returns:
        Point on curve
    """
    t = clamp(t, 0.0, 1.0)
    u = 1.0 - t
    tt = t * t
    uu = u * u
    uuu = uu * u
    ttt = tt * t
    
    x = uuu * p0[0] + 3 * uu * t * p1[0] + 3 * u * tt * p2[0] + ttt * p3[0]
    y = uuu * p0[1] + 3 * uu * t * p1[1] + 3 * u * tt * p2[1] + ttt * p3[1]
    
    return (x, y)


def ease_in_out(t: float) -> float:
    """
    Ease-in-out function for smooth transitions
    
    Args:
        t: Input value (0.0 to 1.0)
        
    Returns:
        Eased value
    """
    t = clamp(t, 0.0, 1.0)
    return t * t * (3.0 - 2.0 * t)


def ease_in(t: float) -> float:
    """
    Ease-in function for smooth transitions
    
    Args:
        t: Input value (0.0 to 1.0)
        
    Returns:
        Eased value
    """
    t = clamp(t, 0.0, 1.0)
    return t * t


def ease_out(t: float) -> float:
    """
    Ease-out function for smooth transitions
    
    Args:
        t: Input value (0.0 to 1.0)
        
    Returns:
        Eased value
    """
    t = clamp(t, 0.0, 1.0)
    return 1.0 - (1.0 - t) * (1.0 - t)


def noise_2d(x: float, y: float, seed: int = 0) -> float:
    """
    Simple 2D noise function
    
    Args:
        x: X coordinate
        y: Y coordinate
        seed: Random seed
        
    Returns:
        Noise value (-1.0 to 1.0)
    """
    # Simple hash-based noise
    n = int(x + y * 57 + seed * 131)
    n = (n << 13) ^ n
    return (1.0 - ((n * (n * n * 15731 + 789221) + 1376312589) & 0x7fffffff) / 1073741824.0)


def perlin_noise_2d(x: float, y: float, octaves: int = 4, persistence: float = 0.5) -> float:
    """
    Perlin-like 2D noise function
    
    Args:
        x: X coordinate
        y: Y coordinate
        octaves: Number of octaves
        persistence: Persistence value
        
    Returns:
        Noise value (-1.0 to 1.0)
    """
    total = 0.0
    frequency = 1.0
    amplitude = 1.0
    max_value = 0.0
    
    for i in range(octaves):
        total += noise_2d(x * frequency, y * frequency, i) * amplitude
        max_value += amplitude
        amplitude *= persistence
        frequency *= 2.0
    
    return total / max_value


def generate_noise_map(width: int, height: int, scale: float = 50.0, octaves: int = 4) -> List[List[float]]:
    """
    Generate a 2D noise map
    
    Args:
        width: Map width
        height: Map height
        scale: Noise scale
        octaves: Number of octaves
        
    Returns:
        2D noise map
    """
    noise_map = []
    for y in range(height):
        row = []
        for x in range(width):
            nx = x / scale
            ny = y / scale
            value = perlin_noise_2d(nx, ny, octaves)
            row.append(value)
        noise_map.append(row)
    return noise_map


if __name__ == "__main__":
    # Test mathematical utilities
    print("🧪 Testing Mathematical Utilities...")
    
    # Test basic functions
    print(f"clamp(5, 0, 10) = {clamp(5, 0, 10)}")
    print(f"lerp(0, 100, 0.5) = {lerp(0, 100, 0.5)}")
    print(f"smooth_step(0, 10, 5) = {smooth_step(0, 10, 5)}")
    print(f"random_range(1, 10) = {random_range(1, 10)}")
    
    # Test vector operations
    v1 = (3, 4)
    v2 = (1, 2)
    print(f"distance({v1}, {v2}) = {distance(v1, v2)}")
    print(f"normalize({v1}) = {normalize_vector(v1)}")
    print(f"dot_product({v1}, {v2}) = {dot_product(v1, v2)}")
    
    # Test geometric functions
    point = (5, 5)
    center = (0, 0)
    print(f"point_in_circle({point}, {center}, 10) = {point_in_circle(point, center, 10)}")
    
    # Test easing functions
    print(f"ease_in_out(0.5) = {ease_in_out(0.5)}")
    print(f"ease_in(0.5) = {ease_in(0.5)}")
    print(f"ease_out(0.5) = {ease_out(0.5)}")
    
    # Test noise functions
    print(f"noise_2d(10, 10) = {noise_2d(10, 10)}")
    print(f"perlin_noise_2d(10, 10) = {perlin_noise_2d(10, 10)}")
    
    print("✅ Mathematical utilities test completed!") 