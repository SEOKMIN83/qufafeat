from pandas import DataFrame
from typing import Set

from .coldepset import ColDepSet
from .coldepnode import ColDepNode


class ColDepTree:
    def __init__(self, df: DataFrame):
        self._roots: Set[ColDepNode] = set()
        self._build(ColDepSet(df))

    def _build(self, coldeps: ColDepSet):
        for coldep in coldeps:
            cnset_lhs = coldep.get_lhs_cnset()
            node_lhs = self._find_node(cnset_lhs)
            if node_lhs is None:
                node_lhs = ColDepNode(cnset_lhs)
                self._roots.add(node_lhs)

            cnset_rhs = coldep.get_rhs_cnset()
            node_rhs = self._find_node(cnset_rhs)
            if node_rhs is None:
                node_rhs = ColDepNode(cnset_rhs)
                node_lhs.add_child(cnset_lhs, node_rhs)
            else:
                if node_lhs.is_ancestor(node_rhs) or node_rhs.has_descendent(cnset_lhs):
                    node_lhs.squash(node_rhs)
                    if node_lhs in self._roots:
                        self._roots.remove(node_lhs)
                else:
                    if node_rhs in self._roots:
                        self._roots.remove(node_rhs)
                    node_lhs.add_child(cnset_lhs, node_rhs)

    def _find_node(self, cnset: frozenset):
        for root in self._roots:
            node = root.find(cnset)
            if node is not None:
                return node
        return None

    def __repr__(self):
        traversed = []
        root_descs = []
        for root in self._roots:
            root_descs.append(root.get_desc(traversed))
        return "\n".join(root_descs)