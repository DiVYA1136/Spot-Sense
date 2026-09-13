import cv2
import numpy as np

cap = cv2.VideoCapture('easy1.mp4')
drawing = False
points = []

def draw(event, x, y, flags, param):
    global points, drawing
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))
