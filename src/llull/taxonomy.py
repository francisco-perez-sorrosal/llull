import dataclasses
from typing import Any, Dict, Iterable, List, Optional, Type
from urllib.parse import urlparse

from loguru import logger

from .taxon import Taxon
from .utils import download_file


class Taxonomy:
    def __init__(self, name: str):
        self.name: str = name
        self.root: Optional[Taxon] = None
        self.search_table: Dict[str, Taxon] = {}
        self.nodes_count = 0

    def __eq__(self, other):
        return (
            self.name == other.name
            and self.root == other.root
            and self.search_table == other.search_table
            and self.nodes_count == other.nodes_count
        )

    def add(self, parent_id: Optional[str], node: Taxon):
        def add(current: Taxon, parent_id: str, node: Taxon, level: int):
            if parent_id == current.name:
                # logger.debug(f"Including {node.name} in {current.id}")
                node.level = level
                node.parent = current
                current.children[str(node.id)] = node
                self.search_table[str(node.id)] = node
                return 1
            else:
                count = 0
                if parent_id in self.search_table.keys():  # Insert straight!!!
                    parent_taxon = self.search_table[parent_id]
                    # logger.debug(f"Jumping to {parent_taxon.id}")
                    count += add(parent_taxon, parent_id, node, parent_taxon.level + 1)
                else:  # Defensive code
                    logger.warning(f"Very unlikely!!! Trying to add {node.id} to the children of {current.id}")
                    for k in current.children.keys():
                        count += add(current.children[k], parent_id, node, level + 1)
                return count

        if node.id in self.search_table:
            # logger.debug(f"Node {node.id} already in the taxonomy. Skipping...")
            return
        # Root is empty then the node will become the root
        if parent_id is None:
            if self.root is None:
                node.level = 0
                node.parent = None
                self.root = node
                self.search_table[str(node.id)] = node
                logger.info(f"Root nodee setup to taxon {node}")
                self.nodes_count = 1
        else:
            assert self.root is not None
            self.nodes_count += add(self.root, parent_id, node, 1)

    def taxons_in_level(self, level: int) -> List[Taxon]:
        def get_level_from_children(level: int, current_taxon: Taxon = None) -> List[Taxon]:
            level_taxons: List[Taxon] = []

            assert current_taxon is not None
            if len(current_taxon.children) > 0:
                for child in current_taxon.children.values():
                    if child.level == level:
                        level_taxons.append(child)
                    else:
                        level_taxons += get_level_from_children(level, child)
            return level_taxons

        level_taxons: List[Taxon] = []
        if not self.root:
            return level_taxons

        if level == 0:
            level_taxons.append(self.root)
        else:
            level_taxons += get_level_from_children(level, self.root)

        return level_taxons

    def lineage(self, taxon_id: str, reversed: bool = False, as_str: bool = False) -> Iterable[Any]:
        lineage = []
        current_taxon = self.search_table.get(taxon_id, None)
        if not current_taxon:
            logger.info(f"Sorry, taxon {taxon_id} not found")
        else:
            lineage.append(current_taxon)
            while current_taxon.parent:
                current_taxon = current_taxon.parent
                lineage.append(current_taxon)

        if reversed:
            lineage.reverse()
        if as_str:
            return [str(taxon.name) for taxon in lineage]

        return lineage

    def strpath(self, taxon_id: str, sep: str = "/") -> str:
        return sep + sep.join(self.lineage(taxon_id, True, True))

    @classmethod
    def create_subtaxonomy(cls: Type["Taxonomy"], name: str, new_root_id: str, t: "Taxonomy") -> "Taxonomy":
        def add_children(current_taxon: Taxon):
            for child in current_taxon.children.values():
                child_copy = dataclasses.replace(child)
                sub_t.add(current_taxon.id, child_copy)
                add_children(child)

        sub_t = Taxonomy(name)

        new_root = t.search_table.get(new_root_id, None)
        if new_root is None:
            raise ValueError(f"Root node id {new_root_id} not found. Can't create taxonomy")
        new_root_copy = dataclasses.replace(new_root)
        sub_t.add(None, new_root_copy)
        add_children(new_root_copy)

        return sub_t

    @classmethod
    def create_from_file(
        cls: Type["Taxonomy"],
        name: str,
        uri: str,
        sep: str = "/",
        add_root_taxon: bool = False,
        skip_header: bool = False,
        header_lines=0,
    ) -> "Taxonomy":

        parsed_uri = urlparse(uri)
        if parsed_uri.scheme == "file" or not parsed_uri.scheme:
            logger.info(f"Getting taxonomy from {uri}")
            filename = parsed_uri.path
        elif parsed_uri.scheme == "http" or parsed_uri.scheme == "https":
            filename = download_file(parsed_uri)
        else:
            raise ValueError(f"URI scheme {parsed_uri.scheme} not valid")

        with open(filename) as f:
            t = Taxonomy(name)

            previous_line_nodes: List[str] = []
            skipped_header_lines = 0
            for line in f.read().splitlines():
                if skip_header and skipped_header_lines < header_lines:
                    skipped_header_lines += 1
                    logger.info(f"Skipping header line {skipped_header_lines}: {line}")
                    continue
                nodes_in_line = list(filter(None, line.split(sep)))
                if add_root_taxon:
                    nodes_in_line = ["root"] + nodes_in_line
                if len(set(nodes_in_line).intersection(set(previous_line_nodes))) == len(nodes_in_line) - 1:
                    current_node = Taxon(nodes_in_line[-1])
                    t.add(nodes_in_line[-2], current_node)
                else:
                    i = 0
                    parent_node_id = None
                    logger.debug(f"Nodes in line: {nodes_in_line}")
                    while i < len(nodes_in_line):
                        current_node = Taxon(nodes_in_line[i])
                        t.add(parent_node_id, current_node)
                        parent_node_id = current_node.id
                        i += 1
                previous_line_nodes = nodes_in_line
        return t
