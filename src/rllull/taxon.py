from dataclasses import dataclass, field
from typing import Dict

# @dataclass
# class _Tree(Protocol):
#     def __init__(
#             self,
#             data: int,
#             left: Optional['_Tree'] = None,
#             right: Optional['_Tree'] = None,
#     ) -> None: ...


@dataclass
class Taxon:
    name: str
    level: int = -1
    children: Dict[str, "Taxon"] = field(default_factory=lambda: ({}))
