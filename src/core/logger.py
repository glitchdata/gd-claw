"""Logging configuration for MediaWiki AI Agent."""

import sys
from pathlib import Path
from loguru import logger

# Get project root
PROJECT_ROOT = Path(__file__).parent.parent.parent


def configure_logging(
    level: str = "INFO",
    log_file: str = "logs/agent.log",
    max_file_size: int = 100,
) -> None:
    """
    Configure logging for the application.
    
    Args:
        level: Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Path to log file
        max_file_size: Max file size in MB before rotation
    """
    # Remove default handler
    logger.remove()
    
    # Console handler
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
    )
    
    # File handler with rotation
    log_path = PROJECT_ROOT / log_file
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    logger.add(
        str(log_path),
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level=level,
        rotation=f"{max_file_size} MB",
        retention="7 days",
    )


def get_logger(name: str) -> "logger":
    """Get a logger instance."""
    return logger.bind(name=name)
