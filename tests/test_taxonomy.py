from rllull.taxon import Taxon
from rllull.taxonomy import Taxonomy


def test_root_node():

    t = Taxonomy("test")

    assert t.name == "test"

    root_node = Taxon("root")

    t.add(None, root_node)

    assert t.nodes_count == 1

    level_1_node = Taxon("a_level_1")
    level_1_node2 = Taxon("another_level_1")

    t.add(root_node, level_1_node)
    t.add(root_node, level_1_node2)

    assert t.nodes_count == 3


def test_simple_structured_taxonomy():

    simple_text_taxo = (
        "/root/level1_a\n/root/level1_b\n/root/level1_b/level2_b\n/root/level1_c\n/root/level1_c/level2_c\n"
    )

    t = Taxonomy("test")

    for line in simple_text_taxo.splitlines():
        nodes_in_line = list(filter(None, line.split("/")))
        i = 0
        parent_node = None
        print(f"Nodes in line: {nodes_in_line}")
        while i < len(nodes_in_line):
            current_node = Taxon(nodes_in_line[i])
            t.add(parent_node, current_node)
            parent_node = current_node
            i += 1

    assert t.nodes_count == 6
    assert len(t.search_table) == t.nodes_count
    assert t.search_table["root"].level == 0
    assert t.search_table["level1_c"].level == 1
    assert t.search_table["level2_b"].level == 2
    assert t.search_table["level2_c"].level == 2


def test_taxons_in_level():

    simple_text_taxo = (
        "/root/level1_a\n/root/level1_b\n/root/level1_b/level2_b\n/root/level1_c\n/root/level1_c/level2_c\n"
    )

    t = Taxonomy("test")

    for line in simple_text_taxo.splitlines():
        nodes_in_line = list(filter(None, line.split("/")))
        i = 0
        parent_node = None
        print(f"Nodes in line: {nodes_in_line}")
        while i < len(nodes_in_line):
            current_node = Taxon(nodes_in_line[i])
            t.add(parent_node, current_node)
            parent_node = current_node
            i += 1

    assert t.nodes_count == 6
    assert len(t.search_table) == t.nodes_count
    assert len(t.taxons_in_level(0)) == 1
    assert len(t.taxons_in_level(1)) == 3
    assert len(t.taxons_in_level(2)) == 2
    assert t.taxons_in_level(2)[0] == Taxon("level2_b", 2)
    assert t.taxons_in_level(2)[1] == Taxon("level2_c", 2)
