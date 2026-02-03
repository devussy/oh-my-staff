"""Logging configuration with sensitive data masking."""

import logging
import os
import re
from typing import Any


class SensitiveDataFilter(logging.Filter):
    """Filter to mask sensitive data in logs."""

    SENSITIVE_PATTERNS = [
        (re.compile(r"(token[\"']?\s*[:=]\s*[\"']?)([^\"'\s]+)([\"']?)", re.IGNORECASE), r"\1***MASKED***\3"),
        (re.compile(r"(api[_-]?key[\"']?\s*[:=]\s*[\"']?)([^\"'\s]+)([\"']?)", re.IGNORECASE), r"\1***MASKED***\3"),
        (re.compile(r"(password[\"']?\s*[:=]\s*[\"']?)([^\"'\s]+)([\"']?)", re.IGNORECASE), r"\1***MASKED***\3"),
        (re.compile(r"(secret[\"']?\s*[:=]\s*[\"']?)([^\"'\s]+)([\"']?)", re.IGNORECASE), r"\1***MASKED***\3"),
        (re.compile(r"(bearer\s+)([^\s]+)", re.IGNORECASE), r"\1***MASKED***"),
        (re.compile(r"(xox[bp]-[^\s]+)", re.IGNORECASE), r"***MASKED_SLACK_TOKEN***"),
    ]

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filter log record to mask sensitive data.

        Args:
            record: Log record

        Returns:
            True (always process the record)
        """
        record.msg = mask_sensitive_data(str(record.msg))
        if record.args:
            record.args = tuple(
                mask_sensitive_data(str(arg)) if isinstance(arg, str) else arg
                for arg in record.args
            )
        return True


def mask_sensitive_data(text: str) -> str:
    """
    Mask sensitive data in text.

    Args:
        text: Text to mask

    Returns:
        Masked text
    """
    for pattern, replacement in SensitiveDataFilter.SENSITIVE_PATTERNS:
        text = pattern.sub(replacement, text)
    return text


def setup_logging(
    name: str,
    log_level: str = None,
    log_file: str = None,
) -> logging.Logger:
    """
    Set up logging with sensitive data filtering.

    Args:
        name: Logger name (typically __name__)
        log_level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional log file path

    Returns:
        Configured logger
    """
    # Get configuration from environment
    if log_level is None:
        log_level = os.getenv("LOG_LEVEL", "INFO")

    if log_file is None:
        log_file = os.getenv("LOG_FILE")

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, log_level.upper()))

    # Avoid adding handlers multiple times
    if logger.handlers:
        return logger

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, log_level.upper()))
    console_handler.setFormatter(formatter)
    console_handler.addFilter(SensitiveDataFilter())
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        try:
            file_handler = logging.FileHandler(log_file)
            file_handler.setLevel(getattr(logging, log_level.upper()))
            file_handler.setFormatter(formatter)
            file_handler.addFilter(SensitiveDataFilter())
            logger.addHandler(file_handler)
        except OSError as e:
            logger.warning(f"Could not create log file {log_file}: {e}")

    return logger
