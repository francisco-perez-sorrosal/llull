import pytest

from rllull.taxon import Taxon
from rllull.taxonomy import Taxonomy


@pytest.fixture(name="t")
def simple_taxo():
    simple_text_taxo = (
        "/root/level1_a\n/root/level1_b\n/root/level1_b/level2_b\n/root/level1_c\n/root/level1_c/level2_c\n/root/level1_c/level2_d\n"
    )

    t = Taxonomy("test")

    for line in simple_text_taxo.splitlines():
        nodes_in_line = list(filter(None, line.split("/")))
        i = 0
        parent_node_id = None
        print(f"Nodes in line: {nodes_in_line}")
        while i < len(nodes_in_line):
            current_node = Taxon(nodes_in_line[i])
            t.add(parent_node_id, current_node)
            parent_node_id = current_node.id
            i += 1
    yield t


def test_basic_node_properties():

    t = Taxonomy("test")

    assert t.name == "test"

    # Add a root node
    root_node = Taxon("root")
    assert root_node.id == root_node.name

    t.add(None, root_node)
    assert t.nodes_count == 1

    # Add a just two level 1 nodes node
    level_1_node = Taxon("a_level_1")
    level_1_node2 = Taxon("another_level_1")

    t.add(root_node.id, level_1_node)
    t.add(root_node.id, level_1_node2)
    assert t.nodes_count == 3

    # Check structure
    assert t.search_table["root"].parent == None
    assert t.search_table["a_level_1"].parent == t.search_table["another_level_1"].parent == root_node


def test_simple_structured_taxonomy(t):
    assert t.nodes_count == 7
    assert len(t.search_table) == t.nodes_count
    assert t.search_table["root"].level == 0
    assert t.search_table["level1_c"].level == 1
    assert t.search_table["level2_b"].level == 2
    assert t.search_table["level2_c"].level == 2


def test_taxons_in_level(t):
    assert t.nodes_count == 7
    assert len(t.search_table) == t.nodes_count
    assert len(t.taxons_in_level(0)) == 1
    assert len(t.taxons_in_level(1)) == 3
    assert len(t.taxons_in_level(2)) == 3


def test_lineage(t):
    assert len(t.lineage("root")) == 1
    assert len(t.lineage("level1_a")) == 2
    assert len(t.lineage("level1_b")) == 2
    assert len(t.lineage("level2_c")) == 3

    # Basic lineage
    lineage = t.lineage("level2_c")
    assert lineage[-1] == t.root
    assert lineage[0].name == "level2_c"
    assert lineage[0].parent.name == "level1_c"

    # Reversed lineage
    lineage = t.lineage("level2_c", reversed=True)
    assert lineage[-1].name == "level2_c"
    assert lineage[0].name == "root"
    assert lineage[0].parent == None

    # Lineage as str and reversed
    lineage = t.lineage("level2_c", reversed=True, as_str=True)
    assert lineage[0] == "root"
    assert lineage[1] == "level1_c"
    assert lineage[-1] == "level2_c"


def test_subtaxonomy(t):
    sub_t = Taxonomy.create_subtaxonomy("new_taxonomy", "level1_c", t)
    assert sub_t.name == "new_taxonomy"
    assert sub_t.nodes_count == 3
    assert sub_t.root.name == "level1_c"
    assert len(sub_t.search_table) == sub_t.nodes_count
    lineage = sub_t.lineage("level2_c")
    assert lineage[-1] == sub_t.root
    assert lineage[0].name == "level2_c"
    assert lineage[0].parent.name == "level1_c"
