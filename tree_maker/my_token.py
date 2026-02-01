from enum import Enum


class MyPoint:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y


class MyBaseShape:
    def __init__(self, p1: MyPoint, p2: MyPoint):
        leftBottom = MyPoint(min(p1.x, p2.x), min(p1.y, p2.y))
        rightTop = MyPoint(max(p1.x, p2.x), max(p1.y, p2.y))

        self.leftBottom = leftBottom
        self.width = rightTop.x - leftBottom.x
        self.height = rightTop.y - leftBottom.y

    def distanceTo(self, other: "MyBaseShape") -> float:
        xArr1 = [self.leftBottom.x, self.leftBottom.x + self.width]
        xArr2 = [other.leftBottom.x, other.leftBottom.x + other.width]

        yArr1 = [self.leftBottom.y, self.leftBottom.y + self.height]
        yArr2 = [other.leftBottom.y, other.leftBottom.y + other.height]

        dist = 10**10

        for x1 in xArr1:
            for x2 in xArr2:
                dist = min(dist, abs(x1 - x2))

        for y1 in yArr1:
            for y2 in yArr2:
                dist = min(dist, abs(y1 - y2))

        return dist


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

    def getClosest(self, items) -> "MyToken":
        resDist = 10 ** 10
        resItem = None

        for item in items:
            if item == self:
                continue
            curDist = self.rect.distanceTo(item.rect)

            if curDist < resDist:
                resDist = curDist
                resItem = item

        return resItem