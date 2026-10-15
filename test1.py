"""
SpotSense - Interactive Parking Slot Annotation Tool
Allows users to define custom parking slot polygonal regions on video footage.
"""

import os
import pickle
import cv2
import cvzone
import numpy as np

# Configuration
VIDEO_SOURCE = 'easy1.mp4'
SLOTS_CONFIG_FILE = 'Manasa'

# Initialize video capture
cap = cv2.VideoCapture(VIDEO_SOURCE)

drawing = False
area_names = []
polylines = []
points = []

# Load existing parking slots if available
if os.path.exists(SLOTS_CONFIG_FILE):
    try:
        with open(SLOTS_CONFIG_FILE, 'rb') as f:
            data = pickle.load(f)
            polylines = data.get('polylines', [])
            area_names = data.get('area_names', [])
        print(f"[INFO] Loaded {len(polylines)} existing parking slots from '{SLOTS_CONFIG_FILE}'.")
    except Exception as e:
        print(f"[WARNING] Could not read existing '{SLOTS_CONFIG_FILE}': {e}. Starting fresh.")
        polylines = []
        area_names = []
else:
    print(f"[INFO] No existing slot file found at '{SLOTS_CONFIG_FILE}'. Starting with empty slots.")

def draw(event, x, y, flags, param):
    """Mouse callback handler to draw polygon coordinates for a parking spot."""
    global points, drawing, polylines, area_names

    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        points = [(x, y)]

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            points.append((x, y))

    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        if len(points) > 2:
            print("\n--------------------------------------------------")
            slot_name = input("Enter Area / Slot Name (e.g. 1, A1, Bay-3): ").strip()
            if slot_name:
                area_names.append(slot_name)
                polylines.append(np.array(points, np.int32))
                print(f"[SUCCESS] Slot '{slot_name}' defined with {len(points)} vertices.")
            else:
                print("[CANCELLED] Empty name entered. Slot discarded.")
            print("--------------------------------------------------\n")


def print_controls():
    print("==================================================")
    print("     🚗 SpotSense - Parking Slot Annotator        ")
    print("==================================================")
    print(" Controls:")
    print("  • Left Mouse Button: Click and drag to outline a parking bay")
    print("  • Release Mouse: Enter slot name in console")
    print("  • Press 's': Save all slot boundaries to file ('Manasa')")
    print("  • Press 'u' or 'z': Undo / remove last added slot")
    print("  • Press 'c': Clear all current slots")
    print("  • Press 'q' or ESC: Exit annotator")
    print("==================================================\n")

print_controls()

cv2.namedWindow('SpotSense - Slot Annotation')
cv2.setMouseCallback('SpotSense - Slot Annotation', draw)

while True:
    ret, frame = cap.read()
    if not ret:
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        continue

    frame = cv2.resize(frame, (1020, 500))

    # Draw existing saved polylines
    for i, polyline in enumerate(polylines):
        cv2.polylines(frame, [polyline], True, (0, 0, 255), 2)
        if i < len(area_names) and len(polyline) > 0:
            cvzone.putTextRect(
                frame,
                f'{area_names[i]}',
                tuple(polyline[0]),
                scale=1,
                thickness=1,
                colorR=(0, 0, 200),
                colorT=(255, 255, 255)
            )

    # Draw current drawing polyline in progress
    if drawing and len(points) > 1:
        current_poly = np.array(points, np.int32)
        cv2.polylines(frame, [current_poly], False, (255, 255, 0), 2)

    cv2.imshow('SpotSense - Slot Annotation', frame)

    key = cv2.waitKey(100) & 0xFF

    # Save to binary pickle file
    if key == ord('s'):
        with open(SLOTS_CONFIG_FILE, 'wb') as f:
            data = {'polylines': polylines, 'area_names': area_names}
            pickle.dump(data, f)
        print(f"[SAVED] Successfully saved {len(polylines)} slots to '{SLOTS_CONFIG_FILE}'.")

    # Undo last added slot
    elif key == ord('u') or key == ord('z'):
        if polylines and area_names:
            removed_name = area_names.pop()
            polylines.pop()
            print(f"[UNDO] Removed slot '{removed_name}'. Remaining: {len(polylines)}.")
        else:
            print("[INFO] No slots available to remove.")

    # Clear all slots
    elif key == ord('c'):
        polylines = []
        area_names = []
        print("[CLEAR] Cleared all parking slots.")

    # Quit
    elif key == ord('q') or key == 27:
        print("[INFO] Exiting SpotSense Slot Annotation Tool.")
        break

cap.release()
cv2.destroyAllWindows()
# Supports slot undo operations via 'u' and 'z' hotkeys

# Supports clearing all bays via 'c' hotkey

# Interactive command line guide printed on startup
