import cv2

from image_processing import find_circles, sort_circles_to_grid, get_grid_with_colors

photo = cv2.imread("images/hard.jpg")

formatted_image, circles_list = find_circles(photo)
sorted_circles_list = sort_circles_to_grid(circles_list)
hard_grid = get_grid_with_colors(formatted_image, sorted_circles_list, "hard")

mode = "hard"
match mode:
    case "hard":
        max_value = 2
    case "expert":
        max_value = 6


def get_neighbouring_indexes(index: int) -> list[int]:
    if index < 4:
        indexes = [index + 4, index + 5]
        match index:
            case 0:
                indexes.append(index + 1)
            case 3:
                indexes.append(index - 1)
            case _:
                indexes.extend([index + 1, index - 1])
    elif index < 9:
        indexes = [index + 5, index + 6]
        match index:
            case 4:
                indexes.extend([index - 4, index + 1])
            case 8:
                indexes.extend([index - 5, index - 1])
            case _:
                indexes.extend([index - 4, index - 5, index + 1, index - 1])
    elif index < 15:
        indexes = [index + 6, index + 7]
        match index:
            case 9:
                indexes.extend([index - 5, index + 1])
            case 14:
                indexes.extend([index - 6, index - 1])
            case _:
                indexes.extend([index - 5, index - 6, index + 1, index - 1])
    elif index < 22:
        indexes = []
        match index:
            case 15:
                indexes.extend([index + 7, index - 6, index + 1])
            case 21:
                indexes.extend([index - 7, index - 1, index + 6])
            case _:
                indexes.extend([index - 6, index - 7, index + 1, index - 1, index + 6, index + 7])
    elif index < 28:
        indexes = [index - 6, index - 7]
        match index:
            case 22:
                indexes.extend([index + 6, index + 1])
            case 27:
                indexes.extend([index - 1, index + 5])
            case _:
                indexes.extend([index + 1, index - 1, index + 5, index + 6])
    elif index < 33:
        indexes = [index - 5, index - 6]
        match index:
            case 28:
                indexes.extend([index + 5, index + 1])
            case 32:
                indexes.extend([index - 1, index + 4])
            case _:
                indexes.extend([index + 1, index - 1, index + 4, index + 5])
    else:
        indexes = [index - 4, index - 5]
        match index:
            case 33:
                indexes.append(index + 1)
            case 36:
                indexes.append(index - 1)
            case _:
                indexes.extend([index + 1, index - 1])

    indexes.append(index)

    return indexes


def solve_puzzle(grid: list):
    start_index = 3
    for index in (7, 12, 18):
        while grid[start_index] != 0:
            neighbours = get_neighbouring_indexes(index)
            for i in neighbours:
                grid[i] += 1
                grid[i] %= max_value

    return grid


print(solve_puzzle(hard_grid))
