from alg_utils.my_token import MyTokenType, MyToken
from alg_utils.tree_maker import make

"""
TreeNode:
[token, [childNodes: [node, texts]], id, [parent_ids]]
"""


def constructFromTree(tree: list, roots: list, path: str):
    file = open(path, "w")
    used = [False] * len(tree)
    actionNum = 1
    offset = 0

    def dfs(node: int):
        nonlocal actionNum, offset
        used[node] = True
        token = tree[node]
        if token[0].typename == MyTokenType.BRANCHING and \
            len(token[1]) > 0 and \
            len(token[1][0][1]):
            file.write(" " * offset + f"{actionNum}. ЕСЛИ " + ";".join(token[0].text) + " ТО {" + f" | {token[0].executor}\n")
            actionNum += 1
            offset += 2

            dfs(token[1][0][0])

            offset -= 2
            file.write(" " * offset + "} ИНАЧЕ {\n")
            offset += 2

            dfs(token[1][1][0])

            offset -= 2
            file.write(" " * offset + "}\n")
        else:
            file.write(" " * offset + f"{actionNum}. " + ";".join(token[0].text) + f" | {token[0].executor}\n")
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


def constructFromTokens(tokens: list[MyToken], path: str):
    constructFromTree(*make(tokens)[:2], path)