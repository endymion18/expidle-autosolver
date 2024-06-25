import cv2

from image_processing import find_circles, sort_circles_to_grid, get_grid_with_colors
from tile import Tile, find_neighbours

photo = cv2.imread("images/expert.jpg")

MAX_COLOR = 6

formatted_image, circles_list = find_circles(photo)
sorted_circles_list = sort_circles_to_grid(circles_list)
tile_grid = get_grid_with_colors(formatted_image, sorted_circles_list, MAX_COLOR)

neighbours_list = [find_neighbours(i) for i in range(0, 37)]

pagination_indexes = [7, 12, 18, 24, 29, 33]


def paginate(grid: list[Tile]):
    for index in pagination_indexes:
        current_index = index
        while current_index is not None:
            while grid[neighbours_list[current_index].top].color != 0:
                for i in neighbours_list[current_index].get_all_indexes():
                    grid[i].tap()
            current_index = neighbours_list[current_index].l2

        current_index = neighbours_list[index].r2
        while current_index is not None:
            while grid[neighbours_list[current_index].top].color != 0:
                for i in neighbours_list[current_index].get_all_indexes():
                    grid[i].tap()
            current_index = neighbours_list[current_index].r2

    return grid


def solve_puzzle(grid: list[Tile]):
    grid = paginate(grid)
    a, b, c, d = grid[33:37]
    # step 2.1
    while grid[3].color != c.color:
        for i in neighbours_list[3].get_all_indexes():
            grid[i].tap()
    # step 2.2
    c_taps = MAX_COLOR - c.color
    for i in range(c_taps):
        for j in neighbours_list[8].get_all_indexes():
            grid[j].tap()
        for j in neighbours_list[21].get_all_indexes():
            grid[j].tap()
    # step 2.3
    d_taps = MAX_COLOR - d.color
    for i in range(d_taps):
        for j in neighbours_list[3].get_all_indexes():
            grid[j].tap()
    # step 2.4
    if (b.color + d.color) % 2 != 0:
        for i in range(3):
            for j in neighbours_list[14].get_all_indexes():
                grid[j].tap()

    grid = paginate(grid)

    return grid


print(solve_puzzle(tile_grid))

