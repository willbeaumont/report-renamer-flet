from __future__ import annotations

import logging
import sys
from typing import ClassVar


class Logger:
    _instances: ClassVar[dict[str, logging.Logger]] = {}

    @classmethod
    def get_logger(cls, name):
        if name not in cls._instances:
            cls._instances[name] = cls._setup_logger(name)
        return cls._instances[name]

    @staticmethod
    def _setup_logger(name):
        logger = logging.getLogger(name)

        if not logger.handlers:
            logger.setLevel(logging.DEBUG)

            # Create console handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.DEBUG)

            # Create formatter
            formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(formatter)

            # Add console handler to logger
            logger.addHandler(console_handler)

        return logger
