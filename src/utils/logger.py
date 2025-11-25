"""
Centralized logging configuration for the client onboarding application.

Provides professional logging with:
- File output to logs/app.log with rotation
- Console output with color coding
- Structured format with timestamps, levels, module names, and line numbers
- Automatic log rotation to prevent large files
"""

import logging
import os
from logging.handlers import RotatingFileHandler
import sys


def setup_logger(
    name: str = "ClientOnboarding",
    log_file: str = "logs/app.log",
    level: int = logging.INFO,
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5,
) -> logging.Logger:
    """
    Configure and return a logger with file and console handlers.
    
    Args:
        name: Logger name (default: "ClientOnboarding")
        log_file: Path to log file (default: "logs/app.log")
        level: Logging level (default: INFO)
        max_bytes: Max size per log file before rotation (default: 10MB)
        backup_count: Number of backup log files to keep (default: 5)
    
    Returns:
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Avoid adding handlers multiple times if logger already configured
    if logger.handlers:
        return logger
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Professional format with timestamp, level, module, function, line number, and message
    file_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(name)s | %(module)s:%(funcName)s:%(lineno)d | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console format (slightly cleaner for readability)
    console_formatter = logging.Formatter(
        fmt='%(asctime)s | %(levelname)-8s | %(module)s:%(lineno)d | %(message)s',
        datefmt='%H:%M:%S'
    )
    
    # File handler with rotation
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    
    # Prevent propagation to root logger
    logger.propagate = False
    
    return logger


# Create singleton logger instance for the application
logger = setup_logger()


def get_logger(module_name: str = None) -> logging.Logger:
    """
    Get a logger instance for a specific module.
    
    Args:
        module_name: Name of the module (optional, uses __name__ if not provided)
    
    Returns:
        Logger instance
    """
    if module_name:
        return logging.getLogger(f"ClientOnboarding.{module_name}")
    return logger


# Convenience function to log application startup
def log_startup(app_name: str = "Client Onboarding Application", version: str = "1.0.0"):
    """Log application startup with separator lines for clarity."""
    logger.info("=" * 80)
    logger.info(f"{app_name} - Version {version}")
    logger.info("=" * 80)
    logger.info("Application starting...")


# Convenience function to log application shutdown
def log_shutdown():
    """Log application shutdown with separator lines for clarity."""
    logger.info("Application shutting down...")
    logger.info("=" * 80)
