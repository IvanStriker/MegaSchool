from enum import Enum


class MyPoint:
    """
    Represents 2 coordinates: x and y.

    Attributes:
        x: Horizontal coordinate.
        y: Vertical coordinate.
    """

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x} {self.y}"

    def __repr__(self):
        return self.__str__()


class MyBaseShape:
    """
    Defines a rectangle describing some token's position and size.

    Attributes:
        leftBottom: Lower-left corner point of the rectangle.
        width: Horizontal length of the rectangle.
        height: Vertical length of the rectangle.
    """

    def __init__(self, p1: MyPoint, p2: MyPoint):
        leftBottom = MyPoint(min(p1.x, p2.x), min(p1.y, p2.y))
        rightTop = MyPoint(max(p1.x, p2.x), max(p1.y, p2.y))

        self.leftBottom = leftBottom
        self.width = rightTop.x - leftBottom.x
        self.height = rightTop.y - leftBottom.y

    def distanceTo(self, other: "MyBaseShape") -> float:
        """
        Calculates the Manhattan distance between two shapes.

        Args:
            other: Another MyBaseShape to calculate distance to

        Returns:
            Manhattan distance
        """
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

    def getSharedPartWith(self, other: "MyBaseShape") -> float:
        """
        Calculates the common area of two shapes.

        Args:
            other: Another MyBaseShape to check overlap with.

        Returns:
            Common area or 0 if shapes don't intersect.
        """
        dist = 0

        # 1. x
        l = min(self, other, key=lambda x: x.leftBottom.x)
        r = max(self, other, key=lambda x: x.leftBottom.x)

        dist = r.leftBottom.x - l.leftBottom.x - l.width

        if dist >= 0:
            return 0

        dist *= -1

        # 1. y
        d = min(self, other, key=lambda x: x.leftBottom.y)
        u = max(self, other, key=lambda x: x.leftBottom.y)

        dist2 = u.leftBottom.y - d.leftBottom.y - d.height

        if dist2 >= 0:
            return 0

        dist2 *= -1

        return dist * dist2

    def __str__(self):
        return f"{self.leftBottom} {self.width} {self.height}"

    def __repr__(self):
        return self.__str__()


class MyTokenType(Enum):
    """
    Keeps all supported token classes.
    """
    DOCUMENT = 0
    END = 1
    MAIL = 2
    ACTION = 3
    EXECUTOR = 4
    BRANCHING = 5
    OTHERS = 9
    START = 7
    TEXT = 8
    ARROW = 10
    ARROW_HEAD = 11

    def __eq__(self, other):
        return self.value == other.value


class MyToken:
    """
    Represents a detected geometrical element of a scheme.

    Attributes:
        rect: Bounding box describing the token's position and size.
        typename: token's class.
        text: List of text strings that belong to the token.
        executor: executor's name
    """

    def __init__(self,
                 rect: MyBaseShape,
                 typename: MyTokenType,
                 text: list[str] | None = None,
                 executor: str | None = None):
        self.rect = rect
        self.typename = typename
        self.text = text
        self.executor = executor
        if not self.text:
            self.text = []

    def getClosest(self, items, f=lambda x: x):
        """
        Finds the geometrically nearest item from a collection.

        Args:
            items: Collection of items to search through.
            f: Optional function to extract MyBaseShape from items.

        Returns:
            The closest item.
        """
        resDist = 10 ** 10
        resItem = None

        # print(items)

        for item in items:
            if f(item) == self:
                continue
            curDist = self.rect.distanceTo(f(item).rect)

            if curDist < resDist or curDist == resDist and \
                    self.rect.getSharedPartWith(f(resItem).rect) < self.rect.getSharedPartWith(f(item).rect):
                resDist = curDist
                resItem = item

        return resItem

    def __str__(self):
        return f"{self.rect} {self.typename} {self.text} {self.executor}"

    def __repr__(self):
        return self.__str__()