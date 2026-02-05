import sys
from queue import Queue

from alg_utils.my_token import *

"""
1. Pin text fields to proper tokens.
2. Delete tokens of class 'text'.
3. Pin arrows to their tokens, building the tree.
"""


def divideTokensByTypes(tokens: list[MyToken]) -> list[list[MyToken]]:
    """
    Splits tokens into 3 groups: texts, classics, arrows

    Args:
        tokens: List of MyToken objects to categorize.

    Returns:
        List of 3 lists: [text_tokens, classic_tokens, arrow_tokens]
    """
    res = [[], [], []]
    for token in tokens:
        if token.typename in [MyTokenType.ACTION,
                              MyTokenType.BRANCHING,
                              MyTokenType.START,
                              MyTokenType.END,
                              MyTokenType.TEXT,
                              MyTokenType.MAIL,
                              MyTokenType.DOCUMENT,
                              MyTokenType.EXECUTOR]:
            res[token.typename != MyTokenType.TEXT].append(token)
        elif token.typename in [MyTokenType.ARROW, MyTokenType.ARROW_HEAD]:
            res[2].append(token)
    return res


def pinText(tokens: list[MyToken]):
    """
    Associates text content with appropriate graphical tokens.

    Args:
        tokens: List of all MyToken objects including
            text and graphical tokens.
    """
    texts, classics, arrows = divideTokensByTypes(tokens)
    # print([i for i in classics if i.typename == MyTokenType.EXECUTOR])

    for text in texts:
        if not text.text:
            continue
        if text.text[0].lower() in ["да", "нет", "yes", "no"]:
            text.getClosest(arrows).text.append(text.text[0])
        else:
            got = text.getClosest(classics)
            print(got.typename, file=sys.stderr)
            got.text.append(text.text[0])
            print(got.text, file=sys.stderr)

    special = [token for token in tokens
               if token.typename in [MyTokenType.DOCUMENT, MyTokenType.MAIL,
                                     MyTokenType.START, MyTokenType.END]]
    mapping = {
        MyTokenType.DOCUMENT.value: "Работа с документом",
        MyTokenType.MAIL.value: "Работа с письмом",
        MyTokenType.START.value: "Начало",
        MyTokenType.END.value: "Конец"
    }

    for token in special:
        if not token.text:
            token.text.append(mapping[token.typename.value])


def findExecutor(token: MyToken, executors: list[MyToken]) -> str | None:
    """
    Identifies the executor responsible for a given
     token based on their 'y' coord

    Args:
        token: The token to find an executor for.
        executors: List of executor tokens.

    Returns:
        Executor name string or None if no executor found.
    """
    y = token.rect.leftBottom.y + token.rect.height

    for executor in executors:
        if executor.rect.leftBottom.y < y <= executor.rect.leftBottom.y + executor.rect.height:
            return executor.text[0]

    return None


def pinExecutors(tokens: list[MyToken]):
    """
    Assigns executors' names to other tokens.

    Args:
        tokens: List of all MyToken objects.
    """
    executors = [token for token in tokens if token.typename == MyTokenType.EXECUTOR]
    others = [token for token in tokens
              if token.typename not in [MyTokenType.EXECUTOR, MyTokenType.ARROW, MyTokenType.ARROW_HEAD]]
    for token in others:
        token.executor = findExecutor(token, executors)


def checkHead(arrow: MyToken, tokens: list[MyToken], allArrows: list[MyToken]) -> list:
    """
    Finds a 'head' (terminating element) for an arrow given

    Args:
        arrow: Starting arrow token to trace from.
        tokens: Llist of all tokens.
        allArrows: List of all arrow and arrowhead tokens to search through.

    Returns:
        List containing:
        - Bool value telling if a proper arrowhead exists
        - The found arrowhead or original arrow if none found
    """
    allArrows = allArrows.copy()
    nextArrow = arrow
    while True:
        allArrows.remove(nextArrow)
        nextArrow = nextArrow.getClosest(allArrows)
        # print(nextArrow, file=sys.stderr)
        if nextArrow and nextArrow.typename == MyTokenType.ARROW_HEAD:
            break
        if not nextArrow:
            return [False, arrow]
    return [nextArrow.typename == MyTokenType.ARROW_HEAD, nextArrow]


def pinArrows(tokens: list[MyToken]):
    """
    Organizes info about connections between tokens into
     a specific tree-like object

    Args:
        tokens: List of tokens with text and executors already assigned.

    Returns:
        Tuple containing:
        - List of action nodes with children and parent references
        - List of root node indices
    """
    allArrows = [token for token in tokens if token.typename in
                 [MyTokenType.ARROW, MyTokenType.ARROW_HEAD]]
    outComingArrows = [token for token in tokens if token.typename == MyTokenType.ARROW]
    actions = [tokens[token] for token in range(len(tokens)) if tokens[token].typename not in
               [MyTokenType.TEXT, MyTokenType.ARROW, MyTokenType.ARROW_HEAD]]
    actions = [[actions[token], [], token] for token in range(len(actions))]
    arrowHeads = [token for token in allArrows if token.typename == MyTokenType.ARROW_HEAD]
    invActions: list[None | list] = [None] * len(actions)
    for action in actions:
        invActions[action[2]] = action + [[]]

    for action in actions:
        try:
            tokenAction = action[0]
            arrows = [arrow for arrow in outComingArrows
                      if arrow.rect.distanceTo(tokenAction.rect) <= 10]
            arrows = sorted(arrows, key=lambda x: tokenAction.rect.distanceTo(x.rect))
            # print(f"ACTION: {action}")
            for i in range(len(arrows)):
                try:
                    if i >= len(arrows):
                        break
                    arrow = arrows[i]
                    arrowHead = arrow.getClosest(arrowHeads)
                    if arrowHead and arrowHead.rect.distanceTo(tokenAction.rect) < 10:
                        continue
                    arrowInfo = checkHead(arrow, tokens, allArrows)
                    if not arrowInfo[0]:
                        near = arrowInfo[1].getClosest(actions, f=lambda x: x[0])
                        if near[0].rect.distanceTo(arrowInfo[1].rect) <= 10:
                            near[1].append([action[2], []])

                    # print(f"FIRST ARROW: {arrow}")
                    outComingArrows.remove(arrow)
                    allArrows.remove(arrow)
                    while True:
                        nextArrow = arrow.getClosest(allArrows)
                        if nextArrow and nextArrow.typename == MyTokenType.ARROW_HEAD:
                            break
                        # print(f"NEXT ARROW: {nextArrow}")
                        arrow.text += nextArrow.text
                        allArrows.remove(nextArrow)
                        outComingArrows.remove(nextArrow)
                        if nextArrow in arrows:
                            arrows.remove(nextArrow)
                    # print(f"NEXT ARROW (ENDED): {nextArrow}")
                    arrow.text += nextArrow.text
                    allArrows.remove(nextArrow)
                    if nextArrow in arrows:
                        arrows.remove(nextArrow)
                    action[1].append([nextArrow.getClosest(actions, f=lambda x: x[0])[2], arrow.text])
                except:
                    pass
        except:
            pass
    temp = set()
    for j in range(len(invActions)):
        action = invActions[j]
        for i in action[1]:
            temp.add(i[0])
            invActions[i[0]][3].append(j)
    roots = []
    for i in range(len(invActions)):
        if not i in temp:
            roots.append(i)

    # print(invActions)

    return invActions, roots


def makeTree(tokens: list[MyToken]):
    """
    Constructs a tree of dependencies from tokens given
     combining other functions of the current file

    Args:
        tokens: List of detected MyToken objects.

    Returns:
        List containing:
        - Action nodes with connections
        - Root indices
        - Filtered tokens (without text and executors)
    """
    pinText(tokens)
    pinExecutors(tokens)
    tokens = list(filter(lambda x: x.typename not in [MyTokenType.TEXT, MyTokenType.EXECUTOR], tokens))
    res = [*pinArrows(tokens), tokens]
    return res