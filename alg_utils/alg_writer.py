from tree import Tree, TreeNode

"""
TreeNode:
[token, [childNodes: [node, texts]], id, [parent_ids]]
"""


def constructFromTree(tree: list, roots: list, path: str):
    file = open(path, "w")
    used = [False] * len(tree)
    actionNum = 1

    def dfs(node: int):
        nonlocal actionNum
        used[node] = True
        token = tree[node]
        file.write(f"{actionNum}. " + ";".join(token[0].text) + "\n")
        actionNum += 1
        for child in token[1]:
            nextNode = tree[child[0]]
            if any([not used[x] for x in nextNode[3]]):
                roots.append(nextNode)
                continue
            if not used[nextNode[2]]:
                dfs(nextNode[2])

    i = 0
    while i < len(roots):
        dfs(roots[i])
        i += 1
    file.close()