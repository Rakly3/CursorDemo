"""
Logging System
=============

This module provides a comprehensive logging system for the Cursor IDE demo
application with support for multiple output formats, log levels, and
performance monitoring.

Author: Cursor IDE Demo
Version: 1.0.0
"""

import logging
import logging.handlers
import os
import sys
import time
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """
    Custom formatter that adds colors to log messages
    
    This formatter enhances log readability by adding ANSI color codes
    to different log levels and providing structured formatting.
    """
    
    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',      # Cyan
        'INFO': '\033[32m',       # Green
        'WARNING': '\033[33m',    # Yellow
        'ERROR': '\033[31m',      # Red
        'CRITICAL': '\033[35m',   # Magenta
        'RESET': '\033[0m'        # Reset
    }
    
    def __init__(self, fmt: str = None, datefmt: str = None, use_colors: bool = True):
        """
        Initialize the colored formatter
        
        Args:
            fmt: Log format string
            datefmt: Date format string
            use_colors: Whether to use colors in output
        """
        super().__init__(fmt, datefmt)
        self.use_colors = use_colors
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors"""
        # Add colors if enabled and output is to terminal
        if self.use_colors and hasattr(sys.stderr, 'isatty') and sys.stderr.isatty():
            levelname = record.levelname
            if levelname in self.COLORS:
                record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"
        
        return super().format(record)


class DemoLogger:
    """
    Advanced logging system for the Cursor IDE demo
    
    This class provides comprehensive logging capabilities including:
    - Multiple output destinations (console, file, network)
    - Log rotation and archiving
    - Performance monitoring integration
    - Structured logging with context
    - Color-coded output for better readability
    """
    
    def __init__(self, name: str = "CursorDemo"):
        """
        Initialize the demo logger
        
        Args:
            name: Logger name
        """
        self.name = name
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        self._setup_handlers()
        self._setup_formatters()
    
    def _setup_handlers(self) -> None:
        """Set up logging handlers"""
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        self.logger.addHandler(console_handler)
        
        # File handler with rotation
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        log_file = log_dir / f"{self.name.lower()}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_file = log_dir / f"{self.name.lower()}_errors.log"
        error_handler = logging.handlers.RotatingFileHandler(
            error_file,
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )
        error_handler.setLevel(logging.ERROR)
        self.logger.addHandler(error_handler)
        
        self.handlers = {
            'console': console_handler,
            'file': file_handler,
            'error': error_handler
        }
    
    def _setup_formatters(self) -> None:
        """Set up log formatters"""
        # Console formatter with colors
        console_format = (
            "%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(filename)s:%(lineno)d | %(message)s"
        )
        console_formatter = ColoredFormatter(
            console_format,
            datefmt='%H:%M:%S',
            use_colors=True
        )
        self.handlers['console'].setFormatter(console_formatter)
        
        # File formatter (detailed)
        file_format = (
            "%(asctime)s | %(levelname)-8s | %(name)s | "
            "%(filename)s:%(lineno)d | %(funcName)s | %(message)s"
        )
        file_formatter = logging.Formatter(
            file_format,
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        self.handlers['file'].setFormatter(file_formatter)
        self.handlers['error'].setFormatter(file_formatter)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log debug message"""
        self.logger.debug(message, extra=kwargs)
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log info message"""
        self.logger.info(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log warning message"""
        self.logger.warning(message, extra=kwargs)
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log error message"""
        self.logger.error(message, extra=kwargs)
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log critical message"""
        self.logger.critical(message, extra=kwargs)
    
    def performance(self, operation: str, duration: float, **kwargs: Any) -> None:
        """Log performance information"""
        message = f"PERFORMANCE | {operation} | {duration:.3f}s"
        self.logger.info(message, extra=kwargs)
    
    def platform_info(self, info: Dict[str, Any]) -> None:
        """Log platform information"""
        message = f"PLATFORM | {info}"
        self.logger.info(message)
    
    def demo_event(self, event: str, **kwargs: Any) -> None:
        """Log demo-specific events"""
        message = f"DEMO | {event}"
        self.logger.info(message, extra=kwargs)


# Global logger instance
_logger: Optional[DemoLogger] = None


def setup_logging(name: str = "CursorDemo", level: str = "INFO") -> DemoLogger:
    """
    Set up the global logging system
    
    Args:
        name: Logger name
        level: Log level
        
    Returns:
        Configured logger instance
    """
    global _logger
    
    if _logger is None:
        _logger = DemoLogger(name)
    
    # Set log level
    level_map = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }
    
    if level.upper() in level_map:
        _logger.logger.setLevel(level_map[level.upper()])
    
    return _logger


def get_logger(name: str = "CursorDemo") -> DemoLogger:
    """
    Get the global logger instance
    
    Args:
        name: Logger name
        
    Returns:
        Logger instance
    """
    global _logger
    
    if _logger is None:
        _logger = setup_logging(name)
    
    return _logger


def log_performance(operation: str, duration: float) -> None:
    """
    Log performance information
    
    Args:
        operation: Operation name
        duration: Duration in seconds
    """
    logger = get_logger()
    logger.performance(operation, duration)


def log_platform_info(info: Dict[str, Any]) -> None:
    """
    Log platform information
    
    Args:
        info: Platform information dictionary
    """
    logger = get_logger()
    logger.platform_info(info)


def log_demo_event(event: str, **kwargs: Any) -> None:
    """
    Log demo-specific events
    
    Args:
        event: Event description
        **kwargs: Additional event data
    """
    logger = get_logger()
    logger.demo_event(event, **kwargs)


if __name__ == "__main__":
    # Test the logging system
    print("🧪 Testing Logging System...")
    
    logger = setup_logging("TestLogger", "DEBUG")
    
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")
    
    logger.performance("test_operation", 0.123)
    logger.platform_info({"platform": "test", "version": "1.0"})
    logger.demo_event("test_event", data="test_data")
    
    print("✅ Logging system test completed!") 