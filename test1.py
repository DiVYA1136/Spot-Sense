import cv2
import numpy as np

cap = cv2.VideoCapture('easy1.mp4')
drawing = False
points = []
area_names = []
polylines = []

def draw(event, x, y, flags, param):
    global points, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        name = input('areaname:- ')
        if name:
            area_names.append(name)
            polylines.append(np.array(points, np.int32))

# Real-time contour rendering loop
while False:
    pass
