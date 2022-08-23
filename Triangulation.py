# -*- coding: utf-8 -*-
import numpy as np
import cv2
from freetype import *

face = Face("C://Windows//Fonts//Arial.ttf")
face.set_char_size(48*64)
face.load_char('A')
slot = face.glyph

outline = slot.outline
points = np.array(outline.points, dtype=[('x', np.int32), ('y', np.int32)])

red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)

width = 800
height = 600
img = np.zeros((height, width, 3), np.uint8)
# points = np.array([[100, 50], [200, 300], [700, 200],[500, 100], [400, 150]], np.int32)


def calc_rect(points):
    min_x = points[:, 0].min()
    min_y = points[:, 1].min()

    max_x = points[:, 0].max()
    max_y = points[:, 1].max()

    return (min_x, min_y, max_x, max_y)


def rect_contains(rect, point):
    if point[0] < rect[0]:
        return False
    elif point[1] < rect[1]:
        return False
    elif point[0] > rect[2]:
        return False
    elif point[1] > rect[3]:
        return False
    return True


def contains(polygon, point):
    return False


def draw_triangeles(img, rect, points):
    subdiv = cv2.Subdiv2D()
    subdiv.initDelaunay(rect)

    for p in points:
        subdiv.insert((p[0], p[1]))

    triangles = subdiv.getTriangleList()

    for t in triangles:
        pt1 = (t[0], t[1])
        pt2 = (t[2], t[3])
        pt3 = (t[4], t[5])

        if rect_contains(rect, pt1) and rect_contains(rect, pt2) and rect_contains(rect, pt3):
            cv2.line(img, pt1, pt2, blue, 2)
            cv2.line(img, pt2, pt3, blue, 2)
            cv2.line(img, pt3, pt1, blue, 2)

            centroid = (int((pt1[0] + pt2[0] + pt3[0])//3),
                        int((pt1[1] + pt2[1] + pt3[1])//3))
            cv2.circle(img, centroid, 4, white)


def draw_points(img, points):
    for p in points:
        cv2.circle(img, (p[0], p[1]), 2, white, 2)


# Calculate bounding box around polygon
#rect = calc_rect(points)

# Draw bounding box
#cv2.rectangle(img, rect[0: 2], rect[2: 4], red, 2)

# Draw polygon
#cv2.fillPoly(img, [points], green)

# Draw result of triangulation
#draw_triangeles(img, rect, points)

# Draw vertices on top
draw_points(img, points)

# cv2.fillPoly(img, [A.astype(np.int32)], blue)
# cv2.polylines(img, [A.astype(np.int32)], True, blue)
# draw_points(img, A)

# hull = cv2.convexHull(pts)
# cv2.polylines(img, [hull], True, (0, 255, 0))

cv2.imshow("image", img)

while cv2.getWindowProperty("image", 0) >= 0:
    keyCode = cv2.waitKey(50)

cv2.destroyAllWindows()
