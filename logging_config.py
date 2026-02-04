"""
logging_config.py - Centralized logging configuration for the blob processor.

Provides structured logging with context fields for easy debugging and failure tracking.
"""

import logging
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ContextLogger:
    """
    A logger wrapper that adds file and stage context to log messages.
    
    Usage:
        logger = get_file_logger("example.xlsx")
        logger.info("download", "Starting download")
        logger.error("taxonomy", "Failed to load", exc_info=True)
    """
    
    def __init__(self, logger: logging.Logger, filename: str):
        self.logger = logger
        self.filename = filename
    
    def _format_message(self, stage: str, message: str, **kwargs) -> str:
        """Format message with context fields."""
        extra_context = ""
        for key, value in kwargs.items():
            if key not in ('exc_info',):
                extra_context += f" [{key}:{value}]"
        return f"[file:{self.filename}] [stage:{stage}]{extra_context} {message}"
    
    def debug(self, stage: str, message: str, **kwargs) -> None:
        exc_info = kwargs.pop('exc_info', False)
        self.logger.debug(self._format_message(stage, message, **kwargs), exc_info=exc_info)
    
    def info(self, stage: str, message: str, **kwargs) -> None:
        exc_info = kwargs.pop('exc_info', False)
        self.logger.info(self._format_message(stage, message, **kwargs), exc_info=exc_info)
    
    def warning(self, stage: str, message: str, **kwargs) -> None:
        exc_info = kwargs.pop('exc_info', False)
        self.logger.warning(self._format_message(stage, message, **kwargs), exc_info=exc_info)
    
    def error(self, stage: str, message: str, **kwargs) -> None:
        exc_info = kwargs.pop('exc_info', True)  # Default to True for errors
        self.logger.error(self._format_message(stage, message, **kwargs), exc_info=exc_info)
    
    def critical(self, stage: str, message: str, **kwargs) -> None:
        exc_info = kwargs.pop('exc_info', True)  # Default to True for critical
        self.logger.critical(self._format_message(stage, message, **kwargs), exc_info=exc_info)


# Global logger instance
_logger: Optional[logging.Logger] = None


def setup_logging(
    log_file: Optional[str] = None,
    level: str = "INFO",
    console_level: str = "INFO"
) -> logging.Logger:
    """
    Configure logging with both console and file handlers.
    
    Args:
        log_file: Path to log file. If None, defaults to logs/processor_YYYYMMDD.log
        level: File log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_level: Console log level (default: INFO)
    
    Returns:
        Configured logger instance
    """
    global _logger
    
    # Create logs directory if needed
    logs_dir = Path("logs")
    logs_dir.mkdir(exist_ok=True)
    
    if log_file is None:
        log_file = logs_dir / f"processor_{datetime.now().strftime('%Y%m%d')}.log"
    else:
        log_file = Path(log_file)
        log_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Custom formatter with milliseconds
    formatter = logging.Formatter(
        '%(asctime)s.%(msecs)03d | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Get or create logger
    logger = logging.getLogger("blob_processor")
    logger.setLevel(logging.DEBUG)  # Capture all levels, handlers will filter
    
    # Remove existing handlers to avoid duplicates on reconfiguration
    logger.handlers.clear()
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(getattr(logging, console_level.upper(), logging.INFO))
    logger.addHandler(console_handler)
    
    # File handler
    file_handler = logging.FileHandler(str(log_file), encoding='utf-8')
    file_handler.setFormatter(formatter)
    file_handler.setLevel(getattr(logging, level.upper(), logging.DEBUG))
    logger.addHandler(file_handler)
    
    # Store globally
    _logger = logger
    
    logger.info(f"Logging initialized. File: {log_file}, Level: {level}")
    
    return logger


def get_logger() -> logging.Logger:
    """
    Get the configured logger instance.
    
    Returns:
        Logger instance. Sets up default logging if not already configured.
    """
    global _logger
    if _logger is None:
        _logger = setup_logging()
    return _logger


def get_file_logger(filename: str) -> ContextLogger:
    """
    Get a context logger for a specific file being processed.
    
    Args:
        filename: Name of the file being processed (used in log context)
    
    Returns:
        ContextLogger instance with file context pre-attached
    """
    return ContextLogger(get_logger(), filename)


def log_system(stage: str, message: str, level: str = "INFO", **kwargs) -> None:
    """
    Log a system-level message (not tied to a specific file).
    
    Args:
        stage: Processing stage (e.g., "startup", "connection", "shutdown")
        message: Log message
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        **kwargs: Additional context fields to include
    """
    logger = get_logger()
    
    extra_context = ""
    for key, value in kwargs.items():
        if key not in ('exc_info',):
            extra_context += f" [{key}:{value}]"
    
    formatted = f"[system] [stage:{stage}]{extra_context} {message}"
    exc_info = kwargs.get('exc_info', False)
    
    log_method = getattr(logger, level.lower(), logger.info)
    log_method(formatted, exc_info=exc_info)


if __name__ == "__main__":
    # Quick test
    setup_logging(level="DEBUG")
    
    # System-level logging
    log_system("startup", "Blob processor starting up")
    log_system("connection", "Connected to Azure Blob Storage", container="test-container")
    
    # File-level logging
    file_logger = get_file_logger("example.xlsx")
    file_logger.info("download", "Starting download from input/example.xlsx")
    file_logger.info("download", "Downloaded successfully", size_kb=245.3)
    file_logger.info("taxonomy", "Loading taxonomy from Tags sheet")
    file_logger.info("taxonomy", "Loaded tags", count=52)
    file_logger.debug("classify", "Classifying row", row=0)
    
    # Error logging with traceback
    try:
        raise ValueError("Test error for logging")
    except Exception:
        file_logger.error("taxonomy", "Failed to load taxonomy")
    
    print("\nLogging test complete. Check logs/ directory for output file.")
