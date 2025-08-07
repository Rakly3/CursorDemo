"""
Platform Detection and Hardware Optimization System
==================================================

This module provides comprehensive platform detection and hardware optimization
for cross-platform Pygame applications. It automatically detects the current
platform (Windows, Linux, macOS) and hardware capabilities to provide optimal
performance settings.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import os
import sys
import platform
import psutil
import threading
import time
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class PlatformType(Enum):
    """Enumeration of supported platforms"""
    WINDOWS = "windows"
    LINUX = "linux"
    MACOS = "macos"
    UNKNOWN = "unknown"


class ArchitectureType(Enum):
    """Enumeration of CPU architectures"""
    X86_64 = "x86_64"
    ARM64 = "arm64"
    ARM32 = "arm32"
    UNKNOWN = "unknown"


@dataclass
class HardwareInfo:
    """Data class containing hardware information"""
    cpu_count: int
    cpu_frequency: float
    memory_total: int
    memory_available: int
    architecture: ArchitectureType
    platform: PlatformType
    is_high_performance: bool


class PlatformDetector:
    """
    Advanced platform detection and hardware analysis system
    
    This class provides comprehensive platform detection, hardware analysis,
    and optimization recommendations for cross-platform applications.
    """
    
    def __init__(self):
        """Initialize the platform detector with comprehensive analysis"""
        self._hardware_info: Optional[HardwareInfo] = None
        self._optimization_settings: Dict[str, Any] = {}
        self._detection_complete = False
        self._detection_lock = threading.Lock()
        
        # Perform initial detection
        self._detect_platform_and_hardware()
    
    def _detect_platform_and_hardware(self) -> None:
        """
        Perform comprehensive platform and hardware detection
        
        This method analyzes the current system to determine:
        - Operating system and version
        - CPU architecture and capabilities
        - Memory availability
        - Performance characteristics
        """
        try:
            print("🔍 [PLATFORM] Starting comprehensive platform detection...")
            
            # Detect platform
            system = platform.system().lower()
            if system == "windows":
                platform_type = PlatformType.WINDOWS
            elif system == "linux":
                platform_type = PlatformType.LINUX
            elif system == "darwin":
                platform_type = PlatformType.MACOS
            else:
                platform_type = PlatformType.UNKNOWN
            
            print(f"📱 [PLATFORM] Detected platform: {platform_type.value}")
            
            # Detect architecture
            machine = platform.machine().lower()
            if machine in ["x86_64", "amd64"]:
                architecture = ArchitectureType.X86_64
            elif machine in ["arm64", "aarch64"]:
                architecture = ArchitectureType.ARM64
            elif machine in ["arm", "armv7l"]:
                architecture = ArchitectureType.ARM32
            else:
                architecture = ArchitectureType.UNKNOWN
            
            print(f"🔧 [PLATFORM] Detected architecture: {architecture.value}")
            
            # Get CPU information
            cpu_count = psutil.cpu_count(logical=True)
            cpu_freq = psutil.cpu_freq()
            cpu_frequency = cpu_freq.current if cpu_freq else 0.0
            
            print(f"🖥️ [PLATFORM] CPU cores: {cpu_count}, Frequency: {cpu_frequency:.2f} MHz")
            
            # Get memory information
            memory = psutil.virtual_memory()
            memory_total = memory.total
            memory_available = memory.available
            
            print(f"💾 [PLATFORM] Total memory: {memory_total // (1024**3):.1f} GB")
            print(f"💾 [PLATFORM] Available memory: {memory_available // (1024**3):.1f} GB")
            
            # Determine if this is a high-performance system
            is_high_performance = (
                cpu_count >= 4 and 
                cpu_frequency >= 2000.0 and 
                memory_total >= 8 * (1024**3)  # 8 GB
            )
            
            print(f"⚡ [PLATFORM] High performance system: {is_high_performance}")
            
            # Create hardware info object
            self._hardware_info = HardwareInfo(
                cpu_count=cpu_count,
                cpu_frequency=cpu_frequency,
                memory_total=memory_total,
                memory_available=memory_available,
                architecture=architecture,
                platform=platform_type,
                is_high_performance=is_high_performance
            )
            
            # Generate optimization settings
            self._generate_optimization_settings()
            
            self._detection_complete = True
            print("✅ [PLATFORM] Platform detection completed successfully!")
            
        except Exception as e:
            print(f"❌ [PLATFORM] Error during platform detection: {e}")
            # Fallback to basic detection
            self._hardware_info = HardwareInfo(
                cpu_count=1,
                cpu_frequency=1000.0,
                memory_total=1024**3,
                memory_available=512**3,
                architecture=ArchitectureType.UNKNOWN,
                platform=PlatformType.UNKNOWN,
                is_high_performance=False
            )
            self._detection_complete = True
    
    def _generate_optimization_settings(self) -> None:
        """
        Generate platform-specific optimization settings
        
        This method creates a dictionary of optimization settings based on
        the detected platform and hardware capabilities.
        """
        if not self._hardware_info:
            return
        
        # Base settings
        settings = {
            "target_fps": 60,
            "vsync": True,
            "double_buffer": True,
            "hardware_acceleration": True,
            "multithreading": True,
            "particle_count": 1000,
            "texture_quality": "high",
            "audio_quality": "high",
            "debug_mode": False
        }
        
        # Platform-specific optimizations
        if self._hardware_info.platform == PlatformType.WINDOWS:
            settings.update({
                "renderer": "direct3d",
                "audio_driver": "directsound",
                "input_driver": "directinput",
                "window_flags": ["HIDDEN", "RESIZABLE", "DOUBLEBUF"]
            })
            print("🪟 [OPTIMIZATION] Applied Windows-specific optimizations")
            
        elif self._hardware_info.platform == PlatformType.LINUX:
            settings.update({
                "renderer": "opengl",
                "audio_driver": "pulseaudio",
                "input_driver": "x11",
                "window_flags": ["HIDDEN", "RESIZABLE", "DOUBLEBUF"]
            })
            print("🐧 [OPTIMIZATION] Applied Linux-specific optimizations")
            
        elif self._hardware_info.platform == PlatformType.MACOS:
            settings.update({
                "renderer": "metal",
                "audio_driver": "coreaudio",
                "input_driver": "cocoa",
                "window_flags": ["HIDDEN", "RESIZABLE", "DOUBLEBUF", "OPENGL"]
            })
            print("🍎 [OPTIMIZATION] Applied macOS-specific optimizations")
        
        # Hardware-specific optimizations
        if self._hardware_info.is_high_performance:
            settings.update({
                "target_fps": 120,
                "particle_count": 2000,
                "texture_quality": "ultra",
                "audio_quality": "ultra",
                "multithreading": True
            })
            print("🚀 [OPTIMIZATION] Applied high-performance optimizations")
        else:
            settings.update({
                "target_fps": 30,
                "particle_count": 500,
                "texture_quality": "medium",
                "audio_quality": "medium",
                "multithreading": False
            })
            print("⚙️ [OPTIMIZATION] Applied performance-balanced optimizations")
        
        # Architecture-specific optimizations
        if self._hardware_info.architecture == ArchitectureType.ARM64:
            settings.update({
                "renderer": "opengl",
                "hardware_acceleration": False,  # Some ARM systems have issues
                "particle_count": int(settings["particle_count"] * 0.8)
            })
            print("🔧 [OPTIMIZATION] Applied ARM64-specific optimizations")
        
        self._optimization_settings = settings
    
    def get_hardware_info(self) -> HardwareInfo:
        """Get the detected hardware information"""
        if not self._detection_complete:
            with self._detection_lock:
                if not self._detection_complete:
                    self._detect_platform_and_hardware()
        return self._hardware_info
    
    def get_optimization_settings(self) -> Dict[str, Any]:
        """Get the platform-specific optimization settings"""
        if not self._detection_complete:
            with self._detection_lock:
                if not self._detection_complete:
                    self._detect_platform_and_hardware()
        return self._optimization_settings.copy()
    
    def get_platform_summary(self) -> str:
        """Get a human-readable platform summary"""
        if not self._hardware_info:
            return "Platform detection failed"
        
        info = self._hardware_info
        return (
            f"Platform: {info.platform.value.title()}\n"
            f"Architecture: {info.architecture.value.upper()}\n"
            f"CPU Cores: {info.cpu_count}\n"
            f"CPU Frequency: {info.cpu_frequency:.1f} MHz\n"
            f"Memory: {info.memory_total // (1024**3):.1f} GB\n"
            f"High Performance: {info.is_high_performance}"
        )
    
    def is_detection_complete(self) -> bool:
        """Check if platform detection is complete"""
        return self._detection_complete


# Global platform detector instance
_platform_detector: Optional[PlatformDetector] = None


def get_platform_detector() -> PlatformDetector:
    """Get the global platform detector instance"""
    global _platform_detector
    if _platform_detector is None:
        _platform_detector = PlatformDetector()
    return _platform_detector


def get_optimization_settings() -> Dict[str, Any]:
    """Get platform-specific optimization settings"""
    return get_platform_detector().get_optimization_settings()


def get_hardware_info() -> HardwareInfo:
    """Get current hardware information"""
    return get_platform_detector().get_hardware_info()


def get_platform_summary() -> str:
    """Get a human-readable platform summary"""
    return get_platform_detector().get_platform_summary()


if __name__ == "__main__":
    # Test the platform detector
    print("🧪 Testing Platform Detector...")
    detector = PlatformDetector()
    print("\n" + "="*50)
    print("PLATFORM SUMMARY:")
    print("="*50)
    print(detector.get_platform_summary())
    print("\n" + "="*50)
    print("OPTIMIZATION SETTINGS:")
    print("="*50)
    for key, value in detector.get_optimization_settings().items():
        print(f"{key}: {value}")
    print("="*50) 