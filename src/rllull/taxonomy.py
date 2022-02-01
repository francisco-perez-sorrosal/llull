import dataclasses
from typing import Dict, List, Optional, Union

from .taxon import Taxon


class Taxonomy:
    def __init__(self, name: str):
        self.name: str = name
        self.root: Optional[Taxon] = None
        self.search_table: Dict[str, Taxon] = {}
        self.nodes_count = 0

    def add(self, parent_id: str, node: Taxon):
        def add(current: Taxon, parent_id: str, node: Taxon, level: int):
            if parent_id == current.name:
                # print(f"Including {node.name} in {root}")
                node.level = level
                node.parent = current
                current.children[node.name] = node
                self.search_table[node.name] = node
                return 1
            else:
                count = 0
                for k in current.children.keys():
                    # print(f"key {k}")
                    count += add(current.children[k], parent_id, node, level + 1)
                return count

        if node.name in self.search_table:
            print(f"Self node {node} already in the taxonomy. Skipping...")
            return
        # Root is empty then the node will become the root
        if parent_id is None:
            if self.root is None:
                node.level = 0
                node.parent = None
                self.root = node
                self.search_table[node.name] = node
                print(f"Root node setup to taxon {node}")
                self.nodes_count = 1
        else:
            assert self.root is not None
            self.nodes_count += add(self.root, parent_id, node, 1)
            # print(self.nodes_count)

    def taxons_in_level(self, level: int) -> List[Taxon]:
        def get_level_from_children(level: int, current_taxon: Taxon = None) -> List[Taxon]:
            level_taxons: List[Taxon] = []
            # if not current_taxon:
            #     return level_taxons

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

    def lineage(self, taxon_id: str, reversed: bool = False, as_str: bool = False) -> Union[List[Taxon], List[str]]:
        lineage = []
        current_taxon = self.search_table.get(taxon_id, None)
        if not current_taxon:
            print("Sorry, taxon {taxon_id} not found")
        else:
            lineage.append(current_taxon)
            while current_taxon.parent:
                current_taxon = current_taxon.parent
                lineage.append(current_taxon)

        if reversed:
            lineage.reverse()
        if as_str:
            return [taxon.name for taxon in lineage]

        return lineage

    @classmethod
    def create_subtaxonomy(cls: str, name: str, new_root_id: str, t: "Taxonomy") -> "Taxonomy":
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
