#!/usr/bin/env python3
"""
Test Script for Cursor IDE Demo
===============================

This script tests the main components of the demo application
to ensure everything is working correctly.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import sys
import time
from pathlib import Path

# Add the app directory to the Python path
sys.path.insert(0, str(Path(__file__).parent / "app"))

def test_platform_detection():
    """Test platform detection system"""
    print("🧪 Testing Platform Detection...")
    try:
        from system.platform_detector import get_platform_detector
        detector = get_platform_detector()
        info = detector.get_hardware_info()
        settings = detector.get_optimization_settings()
        
        print(f"✅ Platform: {info.platform.value}")
        print(f"✅ Architecture: {info.architecture.value}")
        print(f"✅ CPU Cores: {info.cpu_count}")
        print(f"✅ High Performance: {info.is_high_performance}")
        print(f"✅ Target FPS: {settings.get('target_fps', 'N/A')}")
        return True
    except Exception as e:
        print(f"❌ Platform detection failed: {e}")
        return False

def test_configuration():
    """Test configuration system"""
    print("\n🧪 Testing Configuration System...")
    try:
        from config.config_manager import get_config_manager
        config = get_config_manager()
        
        width = config.get("Display", "width")
        height = config.get("Display", "height")
        target_fps = config.get("Display", "target_fps")
        
        print(f"✅ Display: {width}x{height}")
        print(f"✅ Target FPS: {target_fps}")
        return True
    except Exception as e:
        print(f"❌ Configuration failed: {e}")
        return False

def test_logging():
    """Test logging system"""
    print("\n🧪 Testing Logging System...")
    try:
        from utils.logger import setup_logging
        logger = setup_logging("TestDemo", "INFO")
        
        logger.info("Test info message")
        logger.warning("Test warning message")
        logger.error("Test error message")
        
        print("✅ Logging system working")
        return True
    except Exception as e:
        print(f"❌ Logging failed: {e}")
        return False

def test_performance():
    """Test performance monitoring"""
    print("\n🧪 Testing Performance Monitoring...")
    try:
        from utils.performance import get_performance_monitor
        monitor = get_performance_monitor()
        
        # Start monitoring
        monitor.start()
        time.sleep(1)
        
        # Get metrics
        metrics = monitor.get_current_metrics()
        print(f"✅ FPS: {metrics.fps:.1f}")
        print(f"✅ CPU: {metrics.cpu_usage:.1f}%")
        print(f"✅ Memory: {metrics.memory_usage:.1f}%")
        
        # Stop monitoring
        monitor.stop()
        return True
    except Exception as e:
        print(f"❌ Performance monitoring failed: {e}")
        return False

def test_math_utils():
    """Test mathematical utilities"""
    print("\n🧪 Testing Math Utilities...")
    try:
        from utils.math_utils import clamp, lerp, random_range
        from utils.color_utils import Color, random_color
        
        # Test math functions
        result1 = clamp(5, 0, 10)
        result2 = lerp(0, 100, 0.5)
        result3 = random_range(1, 10)
        
        print(f"✅ Clamp: {result1}")
        print(f"✅ Lerp: {result2}")
        print(f"✅ Random: {result3}")
        
        # Test color utilities
        color = random_color()
        print(f"✅ Random Color: {color}")
        
        return True
    except Exception as e:
        print(f"❌ Math utilities failed: {e}")
        return False

def test_particle_system():
    """Test particle system"""
    print("\n🧪 Testing Particle System...")
    try:
        from frontend.particle_system import ParticleSystem, create_fire_effect
        
        # Create particle system
        particle_system = ParticleSystem()
        
        # Add fire effect
        fire_emitter = create_fire_effect(400, 300)
        particle_system.add_emitter(fire_emitter)
        
        # Update system
        particle_system.update(0.016)  # 60 FPS
        
        particle_count = particle_system.get_total_particles()
        print(f"✅ Particle count: {particle_count}")
        
        return True
    except Exception as e:
        print(f"❌ Particle system failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Cursor IDE Demo Tests...")
    print("=" * 60)
    
    tests = [
        test_platform_detection,
        test_configuration,
        test_logging,
        test_performance,
        test_math_utils,
        test_particle_system
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Demo application is ready to run.")
        print("\nTo run the demo:")
        print("python app/main.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main() 