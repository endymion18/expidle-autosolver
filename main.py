import cv2
import numpy as np

image = cv2.imread("images/expert.jpg")
y, x, _ = image.shape
print(x, y)

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

image = image[450:y - 225]
image = cv2.medianBlur(image, 1)

gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
circles = cv2.HoughCircles(gray_image, cv2.HOUGH_GRADIENT, 1, 25, param1=10, param2=29, minRadius=36, maxRadius=36)
circles = np.uint16(np.around(circles))[0].tolist()
# sorting points to right indexes
start_point = min(circles, key=lambda x: (round(x[0], -1), x[1]))

start_x = start_point[0]
start_y = start_point[1]

circles1 = [start_point]
circles.remove(start_point)
index = 0

while len(circles) != 0:
    if round(start_y - circles[index][1], -1) in (30, 40) and round(circles[index][0] - start_x, -1) in (60, 70):
        start_y = circles[index][1]
        start_x = circles[index][0]
        circles1.append(circles[index])
        circles.remove(circles[index])
    if len(circles1) in (4, 9, 15, 22, 28, 33):
        start_x, start_y, _ = min(circles, key=lambda x: (round(x[0], -1), x[1]))
        circles1.append([start_x, start_y, _])
        circles.remove([start_x, start_y, _])
    index += 1
    if index >= len(circles):
        index = 0

counter = 0
colors = {}
for i in circles1:
    # draw the outer circle
    circle_img = np.zeros((image.shape[0], image.shape[1]), np.uint8)
    cv2.circle(circle_img, (i[0], i[1]), i[2], (255, 255, 255), -1)
    color = cv2.mean(image, mask=circle_img)[:3]
    color = tuple([round(i, -1) for i in color])
    color = (70.0, 70.0, 70.0) if color == (60.0, 60.0, 60.0) else color
    if color in colors:
        colors[color] += 1
    else:
        colors[color] = 1
    cv2.circle(image, (i[0], i[1]), i[2], (0, 255, 0), 2)
    cv2.putText(image, f"{counter}", (i[0] - 13, i[1] + 10), 2, 1, (255, 255, 255))
    counter += 1

print(colors)
cv2.imshow('detected circles', image)
cv2.waitKey(0)
