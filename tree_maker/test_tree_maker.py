from my_token import MyToken, MyBaseShape, MyPoint, MyTokenType


tokens = [
    MyToken(
        MyBaseShape(MyPoint(1, 0), MyPoint(3, 2)),
        MyTokenType.ACTION,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(6, 1), MyPoint(7, 4)),
        MyTokenType.ACTION,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(3, 4), MyPoint(5, 6)),
        MyTokenType.ACTION,
        None
    ),
    MyToken(
        MyBaseShape(MyPoint(6, 6), MyPoint(10, 8)),
        MyTokenType.ACTION,
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
import matplotlib.pyplot as plt
import matplotlib.patches as patches

# Данные прямоугольников: [(x, y, width, height, цвет, название)]
rectangles = [
    (2, 2, 4, 3, 'red', 'Дом'),
    (8, 5, 3, 5, 'blue', 'Офис'),
    (13, 1, 5, 4, 'green', 'Склад'),
    (3, 9, 6, 2, 'orange', 'Гараж'),
    (11, 9, 4, 3, 'purple', 'Магазин')
]

fig, ax = plt.subplots(figsize=(12, 10))
ax.grid(True, linestyle='--', alpha=0.6)
ax.set_xlim(0, 20)
ax.set_ylim(0, 15)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_title('Множество прямоугольников на сетке', fontsize=14)

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
            color='dark' + color if color != 'red' else 'darkred')

    # Показываем координаты
    ax.text(x, y, f'({x},{y})', fontsize=8, ha='right', va='top')
    ax.text(x + w, y + h, f'({x + w},{y + h})', fontsize=8, ha='left', va='bottom')

# Легенда
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper right')

ax.set_aspect('equal')
plt.tight_layout()
plt.show()

def testDivideTokensByTypes(self):
    pass
