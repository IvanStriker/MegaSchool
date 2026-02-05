from alg_utils.alg_writer import constructFromTokens, constructFromTree
from alg_utils.tree_maker import makeTree
from alg_utils.my_token import MyToken, MyBaseShape, MyPoint, MyTokenType
from model import test_model


tokens = [
    MyToken(
        MyBaseShape(MyPoint(17, 9), MyPoint(18, 18)),
        MyTokenType.EXECUTOR,
        ["IVAN"]
    ),
    MyToken(
        MyBaseShape(MyPoint(17, 9), MyPoint(18, 0)),
        MyTokenType.EXECUTOR,
        ["VLAD"]
    ),
    MyToken(
        MyBaseShape(MyPoint(1, 0), MyPoint(3, 2)),
        MyTokenType.MAIL,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(6, 1), MyPoint(7, 4)),
        MyTokenType.DOCUMENT,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(6, 2), MyPoint(7, 4)),
        MyTokenType.TEXT,
        ["Действие 2"]
    ),
    MyToken(
        MyBaseShape(MyPoint(3, 4), MyPoint(5, 6)),
        MyTokenType.START,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(4, 5), MyPoint(5, 6)),
        MyTokenType.TEXT,
        ["Начало"]
    ),
    MyToken(
        MyBaseShape(MyPoint(6, 6), MyPoint(10, 8)),
        MyTokenType.BRANCHING,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(7, 7), MyPoint(10, 8)),
        MyTokenType.TEXT,
        ["Условие"]
    ),
    MyToken(
        MyBaseShape(MyPoint(15, 6), MyPoint(17, 8)),
        MyTokenType.END,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(15, 6), MyPoint(17, 8)),
        MyTokenType.TEXT,
        ["Конец"]
    ),
    MyToken(
        MyBaseShape(MyPoint(11, 11), MyPoint(13, 13)),
        MyTokenType.ACTION,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(11, 11), MyPoint(12, 12)),
        MyTokenType.TEXT,
        ["Действие 3"]
    ),
    MyToken(
        MyBaseShape(MyPoint(13, 6.5), MyPoint(15, 7)),
        MyTokenType.TEXT,
        ["Да"]
    ),
    MyToken(
        MyBaseShape(MyPoint(8, 9), MyPoint(9, 10)),
        MyTokenType.TEXT,
        ["Нет"]
    ),
    MyToken(
        MyBaseShape(MyPoint(8, 8), MyPoint(10, 10)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(8, 10.2), MyPoint(10.2, 12)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(10.5, 10.2), MyPoint(11, 12)),
        MyTokenType.ARROW_HEAD,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(10, 6), MyPoint(12, 7)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(12, 6), MyPoint(15, 7)),
        MyTokenType.ARROW_HEAD,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(1, 3), MyPoint(2, 7)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(1, 6), MyPoint(4, 7)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(3, 1), MyPoint(5, 2)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(7, 3), MyPoint(10, 4)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(9, 3), MyPoint(10, 5)),
        MyTokenType.ARROW,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(1, 2), MyPoint(2, 3)),
        MyTokenType.ARROW_HEAD,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(5, 1), MyPoint(6, 2)),
        MyTokenType.ARROW_HEAD,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(9, 5), MyPoint(10, 6)),
        MyTokenType.ARROW_HEAD,
        None
    ),
]


for token in tokens:
    token.rect.leftBottom.x *= 10
    token.rect.leftBottom.y *= 10
    token.rect.width *= 10
    token.rect.height *= 10


def draw():
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches

    # Данные прямоугольников: [(x, y, width, height, цвет, название)]
    rectangles = [
        (i.rect.leftBottom.x,
         i.rect.leftBottom.y,
         i.rect.width,
         i.rect.height,
         'red',
         i.typename)
        for i in tokens
    ]

    fig, ax = plt.subplots(figsize=(120, 100))
    ax.grid(True, linestyle='--', alpha=0.6)
    ax.set_xlim(0, 3000)
    ax.set_ylim(0, 2000)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_title('Множество прямоугольников на сетке', fontsize=10)

    # Цвета для заливки
    fill_colors = {
        'red': 'lightcoral',
        'blue': 'lightblue',
        'green': 'lightgreen',
        'orange': 'wheat',
        'purple': 'lavender'
    }

    # Рисуем все прямоугольники
    for x, y, w, h, color, label in rectangles:
        rect = patches.Rectangle((x, y), w, h,
                                 linewidth=2,
                                 edgecolor=color,
                                 facecolor=fill_colors.get(color, 'white'),
                                 alpha=0.7,
                                 label=label)
        ax.add_patch(rect)

        # Подписываем центр прямоугольника
        center_x = x + w / 2
        center_y = y + h / 2
        ax.text(center_x, center_y, label,
                ha='center', va='center',
                fontsize=9, fontweight='bold',
                color='dark' + color if color not in ['red', 'purple'] else 'darkred')

        # Показываем координаты
        ax.text(x, y, f'({x},{y})', fontsize=8, ha='right', va='top')
        ax.text(x + w, y + h, f'({x + w},{y + h})', fontsize=8, ha='left', va='bottom')

    # Легенда
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc='upper right')

    ax.set_aspect('equal')
    plt.tight_layout()
    plt.show()

def testTree():
    global tokens
    # tree, roots, tokens = make(tokens)
    test_model.prepareModel()
    res = test_model.scan("./model/test_images/5.png")
    tokens = []
    for token in res:
        tokens.append(MyToken(
            MyBaseShape(
                MyPoint(*token["coord"][:2]),
                MyPoint(*token["coord"][2:4])
            ),
            MyTokenType(int(token["class"])),
            [token["text"]] if len(token["text"]) else []
        ))
    # tree, roots, tokens = make(tokens)
    # constructFromTree(tree, roots, "output.txt")


testTree()
draw()