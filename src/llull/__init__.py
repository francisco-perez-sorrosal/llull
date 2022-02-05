"""
llull package.

Taxonomy Manager
"""

import os
import sys
from typing import List

from loguru import logger

__all__: List[str] = []  # noqa: WPS410 (the only __variable__ we use)

home = os.environ.get("HOME")
logdir = os.environ.get("LULIO_LOGDIR", home)

from loguru import logger

config = {
    "handlers": [
        {
            "sink": sys.stdout,
            "format": "<level>{level: <8}</level>|<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        }
    ]
}
logger.configure(**config)

# logger.add(f"{logdir}/lulio_log.log", rotation="500MB", encoding="utf-8", enqueue=True, retention="1 days")
