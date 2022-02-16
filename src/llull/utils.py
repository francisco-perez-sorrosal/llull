import os
from pathlib import Path
from typing import Dict, List
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


def extract_header_from(line: str, sep: str = "\t") -> List[str]:
    elems = list(filter(None, line.split(sep)))
    return list(map(lambda e: e.strip(), elems))


def build_llull_to_taxo_map(structure_desc_file: str) -> Dict[str, str]:
    llull_to_taxo_map = {}
    with open(structure_desc_file) as f:
        for line in f.read().splitlines():
            mapping = list(map(lambda e: e.strip(), line.split("=")))
            assert len(mapping) == 2, f"Mapping: {mapping}"
            llull_to_taxo_map[mapping[0]] = mapping[1]
    return llull_to_taxo_map
