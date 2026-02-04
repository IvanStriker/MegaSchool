from my_token import MyToken


class TreeNode:
    def __init__(self,
                 value: MyToken,
                 parent: "TreeNode|None" = None,
                 children: list["TreeNode"]|None = None):
        self.value = value
        self.parent = parent
        self.children = children
        if not self.children:
            self.children = []


class Tree:
    def __init__(self):
        self.root = None
        self.current = self.root

    def addChild(self, node: TreeNode, parent: TreeNode|None = None):
        node.parent = parent
        if not parent:
            parent = self.current
        if parent:
            parent.children.append(node)
        elif not self.root:
            self.root = node
        self.current = node
