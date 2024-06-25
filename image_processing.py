import cv2
import numpy as np

from tile import Tile

photo = cv2.imread("images/hard.jpg")

hard_colors = {
    (30.0, 30.0, 30.0): 0,
    (90.0, 90.0, 90.0): 1}

expert_colors = {
    (30.0, 30.0, 30.0): 0,
    (40.0, 40.0, 40.0): 1,
    (50.0, 50.0, 50.0): 2,
    (70.0, 70.0, 70.0): 3,
    (80.0, 80.0, 80.0): 4,
    (90.0, 90.0, 90.0): 5
}


def find_circles(image: np.ndarray) -> (np.ndarray, list[list]):
    y, x, _ = image.shape
    print(x, y)

    image = cv2.medianBlur(image, 1)

    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 25, param1=10, param2=29, minRadius=36, maxRadius=36)
    circles = np.uint16(np.around(circles))[0].tolist()

    return image, circles


def sort_circles_to_grid(circles: list[list]) -> list[list]:
    # sorting points to right indexes
    start_point = min(circles, key=lambda x: (round(x[0], -1), x[1]))

    start_x = start_point[0]
    start_y = start_point[1]

    sorted_circles = [start_point]
    circles.remove(start_point)
    index = 0

    while len(circles) != 0:
        if round(start_y - circles[index][1], -1) in (30, 40) and round(circles[index][0] - start_x, -1) in (60, 70):
            start_y = circles[index][1]
            start_x = circles[index][0]
            sorted_circles.append(circles[index])
            circles.remove(circles[index])
        if len(sorted_circles) in (4, 9, 15, 22, 28, 33):
            start_x, start_y, _ = min(circles, key=lambda x: (round(x[0], -1), x[1]))
            sorted_circles.append([start_x, start_y, _])
            circles.remove([start_x, start_y, _])
        index += 1
        if index >= len(circles):
            index = 0

    return sorted_circles


def get_grid_with_colors(image, circles: list[list], mode: int) -> list[Tile]:
    grid = []

    colors = hard_colors if mode == 2 else expert_colors

    for i in range(len(circles)):
        circle = circles[i]
        # draw the outer circle
        circle_img = np.zeros((image.shape[0], image.shape[1]), np.uint8)
        cv2.circle(circle_img, (circle[0], circle[1]), circle[2], (255, 255, 255), -1)
        # get average color
        color = cv2.mean(image, mask=circle_img)[:3]
        color = tuple([round(i, -1) for i in color])
        color = (70.0, 70.0, 70.0) if color == (60.0, 60.0, 60.0) else color
        grid.append(Tile(circle[0], circle[1], colors[color]))
        cv2.circle(image, (circle[0], circle[1]), circle[2], (0, 255, 0), 2)
        cv2.putText(image, f"{i}", (circle[0] - 13, circle[1] + 10), 2, 1, (255, 255, 255))

    # cv2.imshow('detected circles', image)
    # cv2.waitKey(0)

    return grid


if __name__ == "__main__":
    formatted_image, circles_list = find_circles(photo)
    sorted_circles_list = sort_circles_to_grid(circles_list)
    colors_list = get_grid_with_colors(formatted_image, sorted_circles_list, 2)
    print(colors_list)

