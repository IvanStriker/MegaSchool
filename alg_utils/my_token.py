from enum import Enum


class MyPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"

    def __repr__(self):
        return self.__str__()


class MyBaseShape:
    def __init__(self, p1: MyPoint, p2: MyPoint):
        leftBottom = MyPoint(min(p1.x, p2.x), min(p1.y, p2.y))
        rightTop = MyPoint(max(p1.x, p2.x), max(p1.y, p2.y))

        self.leftBottom = leftBottom
        self.width = rightTop.x - leftBottom.x
        self.height = rightTop.y - leftBottom.y

    def distanceTo(self, other: "MyBaseShape") -> float:
        dist = 0

        # 1. x
        l = min(self, other, key=lambda x: x.leftBottom.x)
        r = max(self, other, key=lambda x: x.leftBottom.x)

        dist += max(0.0, r.leftBottom.x - l.leftBottom.x - l.width)

        # 1. y
        d = min(self, other, key=lambda x: x.leftBottom.y)
        u = max(self, other, key=lambda x: x.leftBottom.y)

        dist += max(0.0, u.leftBottom.y - d.leftBottom.y - d.height)

        return dist

    def __str__(self):
        return f"{self.leftBottom} {self.width} {self.height}"

    def __repr__(self):
        return self.__str__()


class MyTokenType(Enum):
    ARROW = 1
    ARROW_HEAD = 2
    START = 3
    END = 4
    EXECUTOR = 5
    ACTION = 6
    BRANCHING = 7 # triangles
    DOCUMENT = 8
    MAIL = 9
    MAIL_ACTION = 10
    TEXT = 11
    OTHERS = 12


class MyToken:
    def __init__(self,
                 rect: MyBaseShape,
                 typename: MyTokenType,
                 text: list[str]|None):
        self.rect = rect
        self.typename = typename
        self.text = text
        if not self.text:
            self.text = []

    def getClosest(self, items, f=lambda x: x):
        resDist = 10 ** 10
        resItem = None

        print(items)

        for item in items:
            if f(item) == self:
                continue
            curDist = self.rect.distanceTo(f(item).rect)

            if curDist < resDist:
                resDist = curDist
                resItem = item

        return resItem

    def __str__(self):
        return f"{self.rect} {self.typename} {self.text}"

    def __repr__(self):
        return self.__str__()