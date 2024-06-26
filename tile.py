class Row:
    length: int
    left_border_index: int
    right_border_index: int
    index: int

    def __init__(self, index: int):
        if index < 4:
            self.left_border_index = 0
            self.right_border_index = 3
            self.index = 1
        elif index < 9:
            self.left_border_index = 4
            self.right_border_index = 8
            self.index = 2
        elif index < 15:
            self.left_border_index = 9
            self.right_border_index = 14
            self.index = 3
        elif index < 22:
            self.left_border_index = 15
            self.right_border_index = 21
            self.index = 4
        elif index < 28:
            self.left_border_index = 22
            self.right_border_index = 27
            self.index = 5
        elif index < 33:
            self.left_border_index = 28
            self.right_border_index = 32
            self.index = 6
        else:
            self.left_border_index = 33
            self.right_border_index = 36
            self.index = 7
        self.length = self.right_border_index - self.left_border_index + 1


class NeighboursIndex:
    top: int
    bottom: int
    l1: int
    l2: int
    r1: int
    r2: int
    tile_index: int

    def __init__(self, top, bottom, l1, l2, r1, r2, tile_index):
        self.top = top
        self.bottom = bottom
        self.l1 = l1
        self.l2 = l2
        self.r1 = r1
        self.r2 = r2
        self.tile_index = tile_index

    def get_all_indexes(self) -> list[int]:
        return [index for index in vars(self).values() if index is not None]


class Tile:
    x: int
    y: int
    color: int

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def tap(self, max_color):
        self.color += 1
        self.color %= max_color

    def __repr__(self):
        return f"{self.x} {self.y} {self.color}"


def find_neighbours(tile_index: int) -> NeighboursIndex:
    top, bottom, l1, l2, r1, r2 = [None for _ in range(6)]

    row = Row(tile_index)

    match row.index:
        case 1:
            bottom = tile_index + row.length
            r2 = tile_index + row.length + 1
        case 2 | 3:
            top = tile_index - row.length + 1 if tile_index != row.right_border_index else None
            bottom = tile_index + row.length
            l1 = tile_index - row.length
            r2 = tile_index + row.length + 1
        case 4:
            top = tile_index - row.length + 1 if tile_index != row.right_border_index else None
            bottom = tile_index + row.length - 1 if tile_index != row.left_border_index else None
            l1 = tile_index - row.length
            r2 = tile_index + row.length
        case 5 | 6:
            top = tile_index - row.length
            bottom = tile_index + row.length - 1 if tile_index != row.left_border_index else None
            l1 = tile_index - row.length - 1
            r2 = tile_index + row.length
        case 7:
            top = tile_index - row.length
            l1 = tile_index - row.length - 1

    if tile_index == row.left_border_index and row.index in (1, 2, 3, 4):
        l1 = None
    if tile_index == row.right_border_index and row.index in (4, 5, 6, 7):
        r2 = None

    if tile_index not in (row.right_border_index, row.left_border_index):
        l2 = tile_index - 1
        r1 = tile_index + 1
    elif tile_index == row.left_border_index:
        r1 = tile_index + 1
    elif tile_index == row.right_border_index:
        l2 = tile_index - 1

    return NeighboursIndex(top=top, bottom=bottom, l1=l1, l2=l2, r1=r1, r2=r2, tile_index=tile_index)
