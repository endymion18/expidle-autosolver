import cv2

from anroid_connector import get_screenshot, image_path, tap_screen, restart_game
from image_processing import find_circles, sort_circles_to_grid, get_grid_with_colors
from tile import Tile, find_neighbours

neighbours_list = [find_neighbours(i) for i in range(0, 37)]

pagination_indexes = [7, 12, 18, 24, 29, 33]

taps_list = []


def paginate(grid: list[Tile], max_color):
    for index in pagination_indexes:
        current_index = index
        while current_index is not None:
            counter = 0
            while grid[neighbours_list[current_index].top].color != 0:
                counter += 1
                for i in neighbours_list[current_index].get_all_indexes():
                    grid[i].tap(max_color)
            taps_list.append((grid[current_index].x, grid[current_index].y, counter))
            current_index = neighbours_list[current_index].l2

        current_index = neighbours_list[index].r2
        while current_index is not None:
            counter = 0
            while grid[neighbours_list[current_index].top].color != 0:
                counter += 1
                for i in neighbours_list[current_index].get_all_indexes():
                    grid[i].tap(max_color)
            taps_list.append((grid[current_index].x, grid[current_index].y, counter))
            current_index = neighbours_list[current_index].r2

    return grid


def solve_puzzle(grid: list[Tile], max_color: int):
    grid = paginate(grid, max_color)
    a, b, c, d = grid[33:37]
    # step 2.1
    counter = 0
    while grid[3].color != c.color:
        counter += 1
        for i in neighbours_list[3].get_all_indexes():
            grid[i].tap(max_color)
    taps_list.append((grid[3].x, grid[3].y, counter))
    # step 2.2
    c_taps = max_color - c.color
    for i in range(c_taps):
        for j in neighbours_list[8].get_all_indexes():
            grid[j].tap(max_color)
        for j in neighbours_list[21].get_all_indexes():
            grid[j].tap(max_color)
    taps_list.append((grid[8].x, grid[8].y, c_taps))
    taps_list.append((grid[21].x, grid[21].y, c_taps))
    # step 2.3
    d_taps = max_color - d.color
    for i in range(d_taps):
        for j in neighbours_list[3].get_all_indexes():
            grid[j].tap(max_color)
    taps_list.append((grid[3].x, grid[3].y, d_taps))
    # step 2.4
    if (b.color + d.color) % 2 != 0:
        for i in range(3):
            for j in neighbours_list[14].get_all_indexes():
                grid[j].tap(max_color)
        taps_list.append((grid[14].x, grid[14].y, 3))

    grid = paginate(grid, max_color)

    return grid


def solve_puzzle_on_phone(max_color: int, times: int):
    for i in range(1, times + 1):
        get_screenshot()
        photo = cv2.imread(image_path)

        formatted_image, circles_list = find_circles(photo)
        sorted_circles_list = sort_circles_to_grid(circles_list)
        tile_grid = get_grid_with_colors(formatted_image, sorted_circles_list, max_color)

        solve_puzzle(tile_grid, max_color)
        print(f"solved {i} puzzle!")
        for tap in taps_list:
            for count in range(tap[2]):
                tap_screen(tap[0], tap[1])
        taps_list.clear()
        restart_game()


if __name__ == "__main__":
    solve_puzzle_on_phone(6, 1)
