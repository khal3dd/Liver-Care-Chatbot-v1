import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from core.config import settings


def get_logger(name: str) -> logging.Logger:
    """
    Create and return a named logger.
    - Console handler: بيطبع في الـ terminal
    - File handler: بيحفظ في logs/app.log مع rotation
    """
    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    # الـ level من الـ config
    level = getattr(logging, settings.log_level.upper(), logging.DEBUG)
    logger.setLevel(level)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Console Handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # --- File Handler ---
    log_path = Path(settings.log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    file_handler = RotatingFileHandler(
        filename=str(log_path),
        maxBytes=settings.log_max_bytes,
        backupCount=settings.log_backup_count,
        encoding="utf-8",
    )
    file_handler.setLevel(level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.propagate = False

    return logger