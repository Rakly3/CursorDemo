"""
Performance Monitoring System
============================

This module provides comprehensive performance monitoring capabilities for the
Cursor IDE demo application, including FPS tracking, memory usage monitoring,
and performance profiling.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import time
import psutil
import threading
from typing import Dict, List, Optional, Callable, Any
from collections import deque
from dataclasses import dataclass
from .logger import get_logger


@dataclass
class PerformanceMetrics:
    """Data class for performance metrics"""
    fps: float
    frame_time: float
    cpu_usage: float
    memory_usage: float
    memory_available: float
    timestamp: float


class FPSMonitor:
    """
    FPS (Frames Per Second) monitoring system
    
    This class provides accurate FPS tracking with configurable sample sizes
    and statistical analysis capabilities.
    """
    
    def __init__(self, sample_size: int = 60):
        """
        Initialize the FPS monitor
        
        Args:
            sample_size: Number of frames to average for FPS calculation
        """
        self.sample_size = sample_size
        self.frame_times = deque(maxlen=sample_size)
        self.last_frame_time = time.time()
        self.fps = 0.0
        self.frame_count = 0
        self.start_time = time.time()
        
        self.logger = get_logger("FPSMonitor")
    
    def update(self) -> float:
        """
        Update FPS calculation
        
        Returns:
            Current FPS value
        """
        current_time = time.time()
        frame_time = current_time - self.last_frame_time
        
        if frame_time > 0:
            self.frame_times.append(frame_time)
            self.frame_count += 1
        
        self.last_frame_time = current_time
        
        # Calculate FPS
        if len(self.frame_times) > 0:
            avg_frame_time = sum(self.frame_times) / len(self.frame_times)
            self.fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0.0
        else:
            self.fps = 0.0
        
        return self.fps
    
    def get_fps(self) -> float:
        """Get current FPS value"""
        return self.fps
    
    def get_frame_time(self) -> float:
        """Get average frame time in milliseconds"""
        if len(self.frame_times) > 0:
            return (sum(self.frame_times) / len(self.frame_times)) * 1000.0
        return 0.0
    
    def get_stats(self) -> Dict[str, float]:
        """Get FPS statistics"""
        if len(self.frame_times) == 0:
            return {
                'fps': 0.0,
                'frame_time': 0.0,
                'min_fps': 0.0,
                'max_fps': 0.0,
                'avg_fps': 0.0
            }
        
        frame_times = list(self.frame_times)
        fps_values = [1.0 / ft if ft > 0 else 0.0 for ft in frame_times]
        
        return {
            'fps': self.fps,
            'frame_time': self.get_frame_time(),
            'min_fps': min(fps_values),
            'max_fps': max(fps_values),
            'avg_fps': sum(fps_values) / len(fps_values)
        }
    
    def reset(self) -> None:
        """Reset FPS monitor"""
        self.frame_times.clear()
        self.fps = 0.0
        self.frame_count = 0
        self.start_time = time.time()
        self.last_frame_time = time.time()


class PerformanceMonitor:
    """
    Comprehensive performance monitoring system
    
    This class provides system-wide performance monitoring including:
    - CPU usage tracking
    - Memory usage monitoring
    - Performance metrics collection
    - Performance alerts and logging
    """
    
    def __init__(self, update_interval: float = 1.0):
        """
        Initialize the performance monitor
        
        Args:
            update_interval: Update interval in seconds
        """
        self.update_interval = update_interval
        self.metrics_history: List[PerformanceMetrics] = []
        self.max_history_size = 300  # 5 minutes at 1 second intervals
        
        self.fps_monitor = FPSMonitor()
        self.cpu_usage = 0.0
        self.memory_usage = 0.0
        self.memory_available = 0.0
        
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.logger = get_logger("PerformanceMonitor")
        
        # Performance thresholds
        self.fps_threshold = 30.0
        self.cpu_threshold = 80.0
        self.memory_threshold = 85.0
    
    def start(self) -> None:
        """Start performance monitoring"""
        if self.running:
            return
        
        self.running = True
        self.monitor_thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.monitor_thread.start()
        self.logger.info("Performance monitoring started")
    
    def stop(self) -> None:
        """Stop performance monitoring"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=2.0)
        self.logger.info("Performance monitoring stopped")
    
    def _monitor_loop(self) -> None:
        """Main monitoring loop"""
        while self.running:
            try:
                self._update_metrics()
                time.sleep(self.update_interval)
            except Exception as e:
                self.logger.error(f"Error in performance monitoring: {e}")
    
    def _update_metrics(self) -> None:
        """Update performance metrics"""
        # Get CPU usage
        self.cpu_usage = psutil.cpu_percent(interval=0.1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        self.memory_usage = memory.percent
        self.memory_available = memory.available / (1024**3)  # GB
        
        # Create metrics object
        metrics = PerformanceMetrics(
            fps=self.fps_monitor.get_fps(),
            frame_time=self.fps_monitor.get_frame_time(),
            cpu_usage=self.cpu_usage,
            memory_usage=self.memory_usage,
            memory_available=self.memory_available,
            timestamp=time.time()
        )
        
        # Add to history
        self.metrics_history.append(metrics)
        if len(self.metrics_history) > self.max_history_size:
            self.metrics_history.pop(0)
        
        # Check for performance issues
        self._check_performance_alerts(metrics)
    
    def _check_performance_alerts(self, metrics: PerformanceMetrics) -> None:
        """Check for performance issues and log alerts"""
        alerts = []
        
        if metrics.fps < self.fps_threshold:
            alerts.append(f"Low FPS: {metrics.fps:.1f}")
        
        if metrics.cpu_usage > self.cpu_threshold:
            alerts.append(f"High CPU: {metrics.cpu_usage:.1f}%")
        
        if metrics.memory_usage > self.memory_threshold:
            alerts.append(f"High Memory: {metrics.memory_usage:.1f}%")
        
        if alerts:
            self.logger.warning(f"Performance alerts: {' | '.join(alerts)}")
    
    def update_fps(self) -> float:
        """Update FPS calculation"""
        return self.fps_monitor.update()
    
    def get_current_metrics(self) -> PerformanceMetrics:
        """Get current performance metrics"""
        if not self.metrics_history:
            return PerformanceMetrics(
                fps=0.0,
                frame_time=0.0,
                cpu_usage=0.0,
                memory_usage=0.0,
                memory_available=0.0,
                timestamp=time.time()
            )
        return self.metrics_history[-1]
    
    def get_average_metrics(self, duration: float = 60.0) -> PerformanceMetrics:
        """Get average metrics over a time period"""
        if not self.metrics_history:
            return self.get_current_metrics()
        
        cutoff_time = time.time() - duration
        recent_metrics = [
            m for m in self.metrics_history 
            if m.timestamp >= cutoff_time
        ]
        
        if not recent_metrics:
            return self.get_current_metrics()
        
        return PerformanceMetrics(
            fps=sum(m.fps for m in recent_metrics) / len(recent_metrics),
            frame_time=sum(m.frame_time for m in recent_metrics) / len(recent_metrics),
            cpu_usage=sum(m.cpu_usage for m in recent_metrics) / len(recent_metrics),
            memory_usage=sum(m.memory_usage for m in recent_metrics) / len(recent_metrics),
            memory_available=sum(m.memory_available for m in recent_metrics) / len(recent_metrics),
            timestamp=time.time()
        )
    
    def get_performance_summary(self) -> Dict[str, Any]:
        """Get a comprehensive performance summary"""
        current = self.get_current_metrics()
        average = self.get_average_metrics()
        
        return {
            'current': {
                'fps': current.fps,
                'frame_time': current.frame_time,
                'cpu_usage': current.cpu_usage,
                'memory_usage': current.memory_usage,
                'memory_available': current.memory_available
            },
            'average': {
                'fps': average.fps,
                'frame_time': average.frame_time,
                'cpu_usage': average.cpu_usage,
                'memory_usage': average.memory_usage,
                'memory_available': average.memory_available
            },
            'alerts': {
                'low_fps': current.fps < self.fps_threshold,
                'high_cpu': current.cpu_usage > self.cpu_threshold,
                'high_memory': current.memory_usage > self.memory_threshold
            }
        }
    
    def set_thresholds(self, fps: float = None, cpu: float = None, memory: float = None) -> None:
        """Set performance thresholds"""
        if fps is not None:
            self.fps_threshold = fps
        if cpu is not None:
            self.cpu_threshold = cpu
        if memory is not None:
            self.memory_threshold = memory
    
    def reset(self) -> None:
        """Reset performance monitor"""
        self.metrics_history.clear()
        self.fps_monitor.reset()
        self.logger.info("Performance monitor reset")


class PerformanceProfiler:
    """
    Performance profiling utility
    
    This class provides context manager functionality for profiling
    specific code sections and operations.
    """
    
    def __init__(self, name: str, logger: Optional[Any] = None):
        """
        Initialize the profiler
        
        Args:
            name: Profile name
            logger: Logger instance
        """
        self.name = name
        self.logger = logger or get_logger("PerformanceProfiler")
        self.start_time = None
        self.end_time = None
    
    def __enter__(self):
        """Context manager entry"""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.end_time = time.time()
        duration = self.end_time - self.start_time
        self.logger.performance(self.name, duration)
    
    def get_duration(self) -> float:
        """Get profiling duration"""
        if self.start_time is None:
            return 0.0
        end_time = self.end_time or time.time()
        return end_time - self.start_time


# Global performance monitor instance
_performance_monitor: Optional[PerformanceMonitor] = None


def get_performance_monitor() -> PerformanceMonitor:
    """Get the global performance monitor instance"""
    global _performance_monitor
    if _performance_monitor is None:
        _performance_monitor = PerformanceMonitor()
    return _performance_monitor


def profile_operation(name: str):
    """Decorator for profiling operations"""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            with PerformanceProfiler(name):
                return func(*args, **kwargs)
        return wrapper
    return decorator


if __name__ == "__main__":
    # Test the performance monitoring system
    print("🧪 Testing Performance Monitoring System...")
    
    # Test FPS monitor
    fps_monitor = FPSMonitor()
    for i in range(10):
        time.sleep(0.016)  # Simulate 60 FPS
        fps = fps_monitor.update()
        print(f"Frame {i+1}: FPS = {fps:.1f}")
    
    print(f"FPS Stats: {fps_monitor.get_stats()}")
    
    # Test performance monitor
    monitor = PerformanceMonitor(update_interval=0.5)
    monitor.start()
    
    # Simulate some work
    for i in range(5):
        time.sleep(1.0)
        current = monitor.get_current_metrics()
        print(f"CPU: {current.cpu_usage:.1f}%, Memory: {current.memory_usage:.1f}%")
    
    monitor.stop()
    
    print("✅ Performance monitoring test completed!") 