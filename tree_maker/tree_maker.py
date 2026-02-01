from my_token import *
from tree import *

"""
1. Pin text fields to proper tokens.
2. Delete tokens of class 'text'.
3. Pin arrows to their tokens, building the tree.
"""


def divideTokensByTypes(tokens: list[MyToken]) -> list[list[MyToken]]:
    res = [[], []]
    for token in tokens:
        if token.typename in [MyTokenType.ACTION,
                              MyTokenType.BRANCHING,
                              MyTokenType.START,
                              MyTokenType.END,
                              MyTokenType.TEXT]:
            res[token.typename != MyTokenType.TEXT].append(token)
    return res


def pinText(tokens: list[MyToken]):
    texts, classics = divideTokensByTypes(tokens)
    print(texts, classics)

    for text in texts:
        text.getClosest(classics).text.append(text.text[0])


def pinArrows(tokens: list[MyToken]) -> Tree:
    allArrows = {token for token in tokens if token.typename in
                 [MyTokenType.ARROW, MyTokenType.ARROW_HEAD]}
    arrowHeads = [token for token in tokens
                  if token.typename == MyTokenType.ARROW_HEAD]
    actions = [token for token in tokens if token.typename in
                 [MyTokenType.START, MyTokenType.END, MyTokenType.ACTION,
                  MyTokenType.BRANCHING]]

    start = [token for token in tokens
                  if token.typename == MyTokenType.START][0]
    end = [token for token in tokens
                  if token.typename == MyTokenType.END][0]
    currentWielder = start

    tree = Tree()
    tree.addChild(TreeNode(start))

    while True:
        currentArrow = currentWielder.getClosest(allArrows)
        while currentArrow.typename != MyTokenType.ARROW_HEAD:
            allArrows.remove(currentArrow)
            currentArrow = currentArrow.getClosest(allArrows)
        nextWielder = currentArrow.getClosest(actions)
        allArrows.remove(currentArrow)
        tree.addChild(TreeNode(nextWielder))

        if currentWielder == end:
            break



def make(tokens: list[MyToken]) -> Tree:
    pinText(tokens)
    tokens = list(filter(lambda x: x.typename != MyTokenType.TEXT, tokens))
    pinArrows(tokens)
    pass
