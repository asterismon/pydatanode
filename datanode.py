from typing import Any, List, Union  # using for pylint

__version__ = "3.5.1"


class ListNode:
    def __init__(self, value: Any = None) -> None:
        self.val: Any = value
        self.next: Union[ListNode, None] = None
        self.up: Union[ListNode, None] = None

    def __iter__(self):
        class __ListNode_Iter:
            def __init__(self, value: Union[ListNode, None]):
                self.current_value = value

            def __next__(self):
                if self.current_value is None:
                    raise StopIteration
                value, self.current_value = self.current_value, self.current_value.next
                return value

            def __iter__(self):
                return self
        return __ListNode_Iter(self)

    def __setattr__(self, __name, __value) -> None:
        if __name == 'next' and __value is not None:
            try:
                __value.up = self
            except:
                raise TypeError(f'{type(__value)} is not supported')
        self.__dict__[__name] = __value

    def __str__(self):
        next_doc = f"<ListNode id={id(self.next)}>" if self.next is not None else "None"
        up_doc = f"<ListNode id={id(self.up)}>" if self.up is not None else "None"
        return f'ListNode(value:{self.val} , next:{next_doc} , up:{up_doc})'

    def __add__(self, other):
        __l1 = ListNode.tolist(self)
        __l2 = ListNode.tolist(other)
        return ListNode.createByList(__l1+__l2)

    def __sub__(self, other):
        __l1 = ListNode.tolist(self)
        __l2 = ListNode.tolist(other)
        return ListNode.createByList([x for x in list({*__l1} ^ {*__l2}) if x not in __l2])

    def tolist(self) -> list:
        next = self.next
        vals = [self.val]
        while next:
            vals.append(next.val)
        return vals

    @staticmethod
    def create(node_num: int, values: list = []) -> "ListNode":
        while len(values) < node_num:
            values.append(None)
        first_node = ListNode(values[0])
        up_node = first_node
        for val in range(1, node_num):
            new_node = ListNode(values[val])
            up_node.next = new_node
            up_node = new_node
        return first_node

    @staticmethod
    def createByList(values: list) -> "ListNode":
        return ListNode.create(len(values), values)

class TreeNode:
    def __init__(self, value=None):
        self.val = value
        self.next: list[TreeNode] = []
        self.up: Union[TreeNode, None] = None

    @property
    def nodes(self):
        return len(self.next)

    def delNode(self, index: int):
        self.next[index].up = None
        self.next = self.next[:index]+self.next[index+1:]

    def __setattr__(self, __name, __value) -> None:
        if __name == 'next' and __value != []:
            try:
                for node in __value:
                    try:
                        node.up = self
                        self.next.append(node)
                    except:
                        raise TypeError(f'{type(__value)} is not supported')
            except:
                try:
                    __value.up = self
                    self.next.append(__value)
                except:
                    raise TypeError(f'{type(__value)} is not supported')
            self._nodes = len(self.next)
        self.__dict__[__name] = __value

    @staticmethod
    def create(levels: int, values: Union[list, None] = None, child: Union[List[int], None] = None) -> "TreeNode":
        '''
        Args:
            levels: The level of new TreeNode
            child: list of node num.
                    Defaults to None.
            values: list of node value.MUST be a two-tier iterable like [HEAD,[level1_node1,level1_node2],[level2_node1,level2_node2]].
                    Defaults to None.
        '''
        if child is None:
            child = [0 for _ in range(levels)]
        if values is None:
            values = [[None for _ in range(child[level])]
                      for level in range(levels)]
        first_node = TreeNode(values[0])
        up_node = first_node
        for level in range(1, levels):
            for node_val in values[level]:
                new_node = TreeNode(node_val)
                up_node.next.append(new_node)
                if len(up_node.next) < child[level-1]:
                    up_node.next.append(TreeNode())
        return first_node

    @staticmethod
    def createByList(values: list):
        return TreeNode.create(len(values), values)

    def __str__(self):
        up_doc = f"<TreeNode id={id(self.up)}>" if self.up is not None else "None"
        return f'TreeNode(value:{self.val} , next:{self.nodes} node(s) , up:{up_doc})'

    @staticmethod
    def depth_priority(Node: "TreeNode", value: Any, max_depth: Union[int, None]) -> Union["TreeNode", None]:
        if Node.val == value:
            return Node

        def __depth_priority(Node, value, max_depth, __now_depth):
            for node in Node.next:
                if node.val == value:
                    return node
                if node.next:
                    rst = __depth_priority(node, value, max_depth, __now_depth)
                    if rst is not None:
                        return rst
            else:
                return None
        return __depth_priority(Node, value, max_depth, 0)

    @staticmethod
    def breadth_priority(Node: "TreeNode", value: Any, max_depth: Union[int, None] = None) -> Union["TreeNode", None]:
        if Node.val == value:
            return Node

        def __breadth_priority(node_list: List[TreeNode], value, max_depth, __now_depth):
            if max_depth is not None:
                if __now_depth >= max_depth:
                    return None
            child: list[TreeNode] = []
            if node_list == []:
                return None
            for node in node_list:
                if node.val == value:
                    return node
                else:
                    child += node.next
                    continue
            else:
                return __breadth_priority(child, value, max_depth, __now_depth := __now_depth+1)
        return __breadth_priority(Node.next, value, max_depth, 0)


class NetNode:
    def __init__(self, val=None, defaultLength=1) -> None:
        self.val = val
        self.next: dict[NetNode, int] = {}
        self.up: dict[NetNode, int] = {}
        self._defaultLength = defaultLength

    def __setattr__(self, __name, __value):
        if __name == "next" and __value != {}:
            for node, length in __value.items():
                node.up[self] = length
        self.__dict__[__name] = __value

    def add(self, Node, length: Union[int, None] = None, force=False) -> bool:
        if Node in self.next and not force:
            return False
        length = length if length is not None else self._defaultLength
        self.next[Node] = length
        Node.up[self] = length
        return True

    def __str__(self) -> str:
        return f"NetNode(val:{self.val},next:{self.next},up:{self.up},defaultLength:{self._defaultLength})"

    @staticmethod
    def create(Nodes: int, values: list, all_next: list, lengths: Union[list, None] = None, defaultLength: Union[int, None] = 1) -> "NetNode":
        if lengths is None:
            lengths = list()
        while len(lengths) < Nodes:
            lengths.append(defaultLength)
        first_node = NetNode(values[0])
        first_node.next = {nextNode: length for nextNode,
                           length in zip(all_next[0], lengths[0])}
        for node in range(1, Nodes):
            new_node = NetNode()
            new_node.val = values[node]
            new_node._defaultLength = defaultLength
            new_node.next = {nextNode: length for nextNode,
                             length in zip(all_next[node], lengths[node])}
        return first_node