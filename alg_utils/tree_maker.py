import sys
from queue import Queue

from my_token import *
from tree import *

"""
1. Pin text fields to proper tokens.
2. Delete tokens of class 'text'.
3. Pin arrows to their tokens, building the tree.
"""


def divideTokensByTypes(tokens: list[MyToken]) -> list[list[MyToken]]:
    res = [[], [], []]
    for token in tokens:
        if token.typename in [MyTokenType.ACTION,
                              MyTokenType.BRANCHING,
                              MyTokenType.START,
                              MyTokenType.END,
                              MyTokenType.TEXT,
                              MyTokenType.MAIL,
                              MyTokenType.DOCUMENT]:
            res[token.typename != MyTokenType.TEXT].append(token)
        elif token.typename in [MyTokenType.ARROW, MyTokenType.ARROW_HEAD]:
            res[2].append(token)
    return res


def pinText(tokens: list[MyToken]):
    texts, classics, arrows = divideTokensByTypes(tokens)

    for text in texts:
        if text.text[0].lower() in ["да", "нет", "yes", "no"]:
            text.getClosest(arrows).text.append(text.text[0])
        else:
            text.getClosest(classics).text.append(text.text[0])

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


def findExecutor(token: MyToken, executors: list[MyToken]) -> str|None:
    y = token.rect.leftBottom.y + token.rect.height

    for executor in executors:
        if executor.rect.leftBottom.y < y <= executor.rect.leftBottom.y + executor.rect.height:
            return executor.text[0]

    return None


def pinExecutors(tokens: list[MyToken]):
    executors = [token for token in tokens if token.typename == MyTokenType.EXECUTOR]
    others = [token for token in tokens
              if token.typename not in [MyTokenType.EXECUTOR, MyTokenType.ARROW, MyTokenType.ARROW_HEAD]]
    for token in others:
        token.executor = findExecutor(token, executors)


def pinArrows(tokens: list[MyToken]):
    allArrows = [token for token in tokens if token.typename in
                 [MyTokenType.ARROW, MyTokenType.ARROW_HEAD]]
    outComingArrows = [token for token in tokens if token.typename == MyTokenType.ARROW]
    actions = [tokens[token] for token in range(len(tokens)) if tokens[token].typename not in
                  [MyTokenType.TEXT, MyTokenType.ARROW, MyTokenType.ARROW_HEAD]]
    actions = [[actions[token], [], token] for token in range(len(actions))]
    invActions: list[None|list] = [None] * len(actions)
    for action in actions:
        invActions[action[2]] = action + [[]]

    for action in actions:
        tokenAction = action[0]
        arrows = [arrow for arrow in outComingArrows
                  if arrow.rect.distanceTo(tokenAction.rect) <= 5]
        arrows = sorted(arrows, key=lambda x: tokenAction.rect.distanceTo(x.rect))
        # print(f"ACTION: {action}")
        for i in range(len(arrows)):
            if i >= len(arrows):
                break
            arrow = arrows[i]
            # print(f"FIRST ARROW: {arrow}")
            outComingArrows.remove(arrow)
            allArrows.remove(arrow)
            while (nextArrow := arrow.getClosest(allArrows)).typename != MyTokenType.ARROW_HEAD:
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


def make(tokens: list[MyToken]):
    pinText(tokens)
    pinExecutors(tokens)
    tokens = list(filter(lambda x: x.typename not in [MyTokenType.TEXT, MyTokenType.EXECUTOR], tokens))
    res = [*pinArrows(tokens), tokens]
    return res

