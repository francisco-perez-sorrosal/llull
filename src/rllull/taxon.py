from dataclasses import dataclass, field
from typing import Dict, Optional


@dataclass
class Taxon:
    id: str
    name: Optional[str] = None
    level: int = -1
    parent: Optional["Taxon"] = None
    children: Dict[str, "Taxon"] = field(default_factory=lambda: ({}))

    def __post_init__(self):
        if self.name is None:
            self.name = self.id

    def __eq__(self, other):
        return (
            self.id == other.id
            and self.name == other.name
            and self.level == other.level
            and self.children == other.children
        )
