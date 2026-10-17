"""
SpotSense - Real-Time Smart Parking Slot Occupancy Tracker
Leverages YOLOv8 and Point-in-Polygon collision testing to track parking bays.
"""

import os
import sys
import pickle
import cv2
import cvzone
import numpy as np
import pandas as pd
from ultralytics import YOLO

# Configuration
SLOTS_CONFIG_FILE = 'Manasa'
COCO_CLASSES_FILE = 'coco.txt'
MODEL_WEIGHTS = 'yolov8s.pt'
VIDEO_SOURCE = 'easy1.mp4'

# Verify required files exist
for req_file in [SLOTS_CONFIG_FILE, COCO_CLASSES_FILE, MODEL_WEIGHTS, VIDEO_SOURCE]:
    if not os.path.exists(req_file):
        print(f"[ERROR] Required file '{req_file}' not found in current directory.")
        sys.exit(1)

# Load calibrated parking slot boundaries
with open(SLOTS_CONFIG_FILE, 'rb') as f:
    data = pickle.load(f)
    polylines = data.get('polylines', [])
    area_names = data.get('area_names', [])

print(f"[INFO] Loaded {len(polylines)} parking slots from '{SLOTS_CONFIG_FILE}'.")

# Load COCO dataset class labels
with open(COCO_CLASSES_FILE, "r") as f:
    class_list = f.read().splitlines()

# Load YOLOv8 deep learning model
print(f"[INFO] Loading YOLOv8 model from '{MODEL_WEIGHTS}'...")
model = YOLO(MODEL_WEIGHTS)
print("[INFO] Model loaded successfully.")

# Initialize video capture
cap = cv2.VideoCapture(VIDEO_SOURCE)
count = 0

# Target vehicle classes from COCO
TARGET_VEHICLES = {'car', 'truck', 'bus', 'van'}

print("\n==================================================")
print("     🚗 SpotSense - Real-Time Occupancy Tracker   ")
print("==================================================")
print(" Live Detection running...")
print(" Press 'q' or ESC on the video window to quit.")
print("==================================================\n")

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    count += 1
    # Frame skip optimization (process every 3rd frame for speed)
    if count % 3 != 0:
        continue

    frame = cv2.resize(frame, (1020, 500))

    # Run YOLOv8 vehicle detection
    results = model.predict(frame, verbose=False)
    boxes_tensor = results[0].boxes.data

    # Safely convert PyTorch tensor to NumPy array on CPU
    if hasattr(boxes_tensor, 'cpu'):
        boxes_np = boxes_tensor.cpu().numpy()
    else:
        boxes_np = np.array(boxes_tensor)

    px = pd.DataFrame(boxes_np).astype("float")

    vehicle_centers = []
    for _, row in px.iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        class_id = int(row[5])

        if class_id < len(class_list):
            class_name = class_list[class_id].strip().lower()
            if any(v in class_name for v in TARGET_VEHICLES):
                cx = (x1 + x2) // 2
                cy = (y1 + y2) // 2
                vehicle_centers.append((cx, cy))

    # Evaluate occupancy for each slot
    occupied_slots = []
    for i, polyline in enumerate(polylines):
        is_occupied = False
        for cx, cy in vehicle_centers:
            # Check if vehicle center lies inside polygon
            result = cv2.pointPolygonTest(polyline, (cx, cy), False)
            if result >= 0:
                is_occupied = True
                break

        slot_label = area_names[i] if i < len(area_names) else str(i + 1)
        first_point = tuple(polyline[0]) if len(polyline) > 0 else (0, 0)

        if is_occupied:
            occupied_slots.append(i)
            # Red outline for occupied slot
            cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
            cvzone.putTextRect(
                frame,
                f"{slot_label}: Occupied",
                first_point,
                scale=0.8,
                thickness=1,
                colorR=(0, 0, 200),
                colorT=(255, 255, 255)
            )
        else:
            # Green outline for vacant slot
            cv2.polylines(frame, [polyline], True, (0, 255, 0), 2)
            cvzone.putTextRect(
                frame,
                f"{slot_label}: Free",
                first_point,
                scale=0.8,
                thickness=1,
                colorR=(0, 180, 0),
                colorT=(255, 255, 255)
            )

    occupied_count = len(occupied_slots)
    total_slots = len(polylines)
    free_spaces = total_slots - occupied_count

    # Display HUD status indicators
    cvzone.putTextRect(
        frame,
        f'OCCUPIED: {occupied_count}/{total_slots}',
        (50, 60),
        scale=2,
        thickness=2,
        colorR=(0, 0, 200),
        colorT=(255, 255, 255)
    )
    cvzone.putTextRect(
        frame,
        f'AVAILABLE: {free_spaces}',
        (50, 130),
        scale=2,
        thickness=2,
        colorR=(0, 180, 0),
        colorT=(255, 255, 255)
    )

    cv2.imshow('SpotSense - Parking Slot Occupancy', frame)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        print("[INFO] Exiting SpotSense Occupancy Tracker.")
        break

cap.release()
cv2.destroyAllWindows()
# Video capture released and windows destroyed on exit
