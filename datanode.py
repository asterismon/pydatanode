from typing import Any, Iterator

__version__ = "0.3.17"

error_level = 0


def level(level: int) -> None:
    global error_level
    """
    Change the error level of all ListNodes and TreeNodes.
    Args:
        level: 
            0:Error
            1:Warning
            2:No output.
        Defaults to 0.
    """
    error_level = level
    return


class ListNode:
    class ListNodeInterrupt(Exception):
        pass

    def __init__(self, value: Any = None, level: int = error_level) -> None:
        self.val: Any = value
        self.next: ListNode | None = None
        self.prev: ListNode | None = None
        self.level = level
        return

    def __iter__(self) -> Iterator:
        class __ListNode_Iter:
            def __init__(self, value: ListNode | None):
                self.current_value = value

            def __next__(self):
                if self.current_value is None:
                    raise StopIteration
                value, self.current_value = self.current_value, self.current_value.next
                return value

            def __iter__(self):
                return self

        return __ListNode_Iter(self)

    def __setattr__(self, __name: str, __value: "ListNode" | Any) -> None:
        if __name == "next" and __value is not None:
            try:
                __value.prev = self
            except:
                raise TypeError(f"{type(__value)} is not supported")
        self.__dict__[__name] = __value
        return

    def __repr__(self) -> str:
        return f"ListNode(value:{self.val} , next:{self.next} , prev:{self.prev})"

    def merge(self, other: "ListNode") -> "ListNode":
        if self.next or other.prev:
            if self.level == 0:
                raise ListNode.ListNodeInterrupt()
            elif self.level == 1:
                print(f"Warning:ListNode Interrupted.left:{self},right:{other}")
            elif self.level == 2:
                pass
        self.next = other
        return self

    def delSelf(self) -> "ListNode" | None:
        _node = None
        if self.prev is not None:
            self.prev.next = self.next
            if self.next is not None:
                _node = self.next
            else:
                _node = self.prev
        else:
            if self.next is not None:
                self.next.prev = None
            _node = self.next
        del self
        return _node

    def toList(self) -> list:
        next = self.next
        vals = list(self.val)
        while next:
            vals.append(next.val)
        return vals

    @classmethod
    def create(
        cls, node_num: int, values: list = list(), *, default=None
    ) -> "ListNode":  # TEST
        while len(values) < node_num:
            values.append(default)
        first_node = ListNode(values[0])
        prev_node = first_node
        for val in range(1, node_num):
            new_node = ListNode(values[val])
            prev_node.next = new_node
            prev_node = new_node
        return first_node

    @classmethod
    def createByArray(cls, values: list) -> "ListNode":  # TEST
        return ListNode.create(len(values), values)

    def delAfter(self) -> None:
        node = self
        while node.next is not None:
            node = node.next
            del node.prev
        else:
            del node
        return


class TreeNode:
    def __init__(self, value=None) -> None:
        self.val = value
        self.parent: TreeNode | None = None
        self.children: list[TreeNode] = []
        return

    @property
    def childnum(self) -> int:
        return len(self.children)

    def delNode(self, index: int) -> "TreeNode":
        if self.children is not None:
            self.children[index].parent = None
            self.children.pop(index)
        return self

    def __setattr__(self, __name: str, __value: dict["TreeNode", int] | Any) -> None:
        if __name == "next" and len(__value) != 0:
            for node in __value:
                node.parent = self
                self.children.append(node)
        self.__dict__[__name] = __value
        return

    @classmethod
    def create(
        cls,
        levels: int,
        values: list | None = None,
        child: list[int] | None = None,
        *,
        default=None,
    ) -> "TreeNode":  # TEST
        """
        Args:
            levels: The level of new TreeNode
            child: list of node num.
                    Defaults to None.
            values: list of node value.MUST be a two-tier iterable like [HEAD,[level1_node1,level1_node2],[level2_node1,level2_node2]].
                    Defaults to None.
        """
        if child is None:
            child = [0] * levels
        if values is None:
            values = [[default] * child[level] for level in range(levels)]
        first_node = TreeNode(values[0])
        prev_node = first_node
        for level in range(1, levels):
            for node_val in values[level]:
                new_node = TreeNode(node_val)
                prev_node.children.append(new_node)
                if len(prev_node.children) < child[level - 1]:
                    prev_node.children.append(TreeNode())
        return first_node

    @classmethod
    def createByArray(cls, values: list) -> "TreeNode":  # TEST
        return TreeNode.create(len(values), values)

    def __repr__(self):
        return f"TreeNode(value:{self.val} , next:{len(self.children)} children, prev:{self.parent})"

    def delChildren(self) -> None:
        def __delChildren(node: "TreeNode", HEAD: "TreeNode") -> None:
            for node in node.children:
                __delChildren(node, HEAD)
            else:
                if node is not HEAD:
                    del node
                else:
                    node.children = list()

        return __delChildren(self, self) if len(self.children) != 0 else None


class NetNode:
    def __init__(self, val=None, defaultLength=1) -> None:
        self.val = val
        self.next: dict[NetNode, int] = {}
        self.prev: dict[NetNode, int] = {}
        self._defaultLength = defaultLength

    def __setattr__(self, __name: str, __value: dict["NetNode", int] | Any):
        if __name == "next" and __value != {}:
            for node, length in __value.items():
                node.prev[self] = length
        self.__dict__[__name] = __value

    def add(self, Node: "NetNode", length: int | None = None, force=False) -> bool:
        if Node in self.next and not force:
            return False
        length = length if length is not None else self._defaultLength
        self.next[Node] = length
        Node.prev[self] = length
        return True

    def __repr__(self) -> str:
        return f"NetNode(val:{self.val},next:{self.next},prev:{self.prev},defaultLength:{self._defaultLength})"

    @classmethod  # TEST
    def create(
        cls,
        Nodes: int,
        values: list,
        all_next: list,
        lengths: list | None = None,
        defaultLength: int | None = 1,
    ) -> "NetNode":
        if lengths is None:
            lengths = list()
        while len(lengths) < Nodes:
            lengths.append(defaultLength)
        first_node = NetNode(values[0])
        first_node.next = {
            nextNode: length for nextNode, length in zip(all_next[0], lengths[0])
        }
        for node in range(1, Nodes):
            new_node = NetNode()
            new_node.val = values[node]
            new_node._defaultLength = defaultLength
            new_node.next = {
                nextNode: length
                for nextNode, length in zip(all_next[node], lengths[node])
            }
        return first_node

    # TODO createByArray
