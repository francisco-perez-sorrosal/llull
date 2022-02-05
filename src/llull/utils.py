import os
from pathlib import Path
from urllib.parse import ParseResult

import requests
from loguru import logger


def check_and_create_dir(path: str):
    """If a directory doesn't exist, then its created.

    Args:
        path: The directory to create.
    """
    if not os.path.exists(path):
        os.makedirs(path)
        logger.info(f"Directory {path} created")
    else:
        logger.warning(f"Directory {path} already exists")


def download_file(uri: ParseResult) -> str:
    logger.info(f"Downloading taxonomy from {uri.geturl()}")
    r = requests.get(uri.geturl(), allow_redirects=True)
    basename = os.path.basename(uri.path)
    filename = Path(Path.home(), ".cache", "llull", basename).as_posix()
    check_and_create_dir(Path(Path.home(), ".cache", "llull").as_posix())
    open(filename, "wb").write(r.content)
    logger.info(f"Taxonomy saved into {filename}")
    return filename
