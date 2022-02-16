import os
from pathlib import Path

from llull.utils import build_llull_to_taxo_map, extract_header_from


def test_header_extration():
    line = "A\tB\tC\n"
    assert extract_header_from(line) == ["A", "B", "C"]


def test_llull_to_taxo_building():
    current_path = Path(os.path.dirname(os.path.realpath(__file__)))
    mapping_path = current_path / "resources" / "iab_mapping.txt"

    l2t = build_llull_to_taxo_map(mapping_path)

    assert len(l2t) == 3
    assert list(l2t.keys()) == ["id", "parent_id", "name"]
