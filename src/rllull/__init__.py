"""
rllull package.

Taxonomy Manager
"""

import os
from loguru import logger
from typing import List

__all__: List[str] = []  # noqa: WPS410 (the only __variable__ we use)

home = os.environ.get('HOME')
logdir = os.environ.get('LULIO_LOGDIR', home)
logger.add(f"{logdir}/lulio_log.log",rotation="500MB", encoding="utf-8", enqueue=True, retention="1 days")