"""
SpotSense - Parking Slot Detection Engine
Core module for analyzing ROI slot occupancy using Computer Vision algorithms.
"""

import json
import os
import cv2
import numpy as np

class ParkingSlotDetector:
    def __init__(self, config_path: str, threshold: int = 900):
        """
        Initialize detector with slot configuration file and pixel threshold.
        """
        self.config_path = config_path
        self.threshold = threshold
        self.slots = self._load_config()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"[WARNING] Slot config file '{self.config_path}' not found.")
            return []
        with open(self.config_path, 'r') as f:
            return json.load(f)

    def process_frame(self, frame):
        """
        Processes a single video frame and determines occupancy for each parking slot.
        Returns:
            processed_frame: Image with visual bounding overlays (Green = Vacant, Red = Occupied)
            stats: Dictionary with total, vacant, and occupied counts.
        """
        if frame is None:
            return None, {"total": 0, "vacant": 0, "occupied": 0}

        # Convert to grayscale and apply adaptive thresholding / blur
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (3, 3), 1)
        thresh = cv2.adaptiveThreshold(
            blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
            cv2.THRESH_BINARY_INV, 25, 16
        )
        median = cv2.medianBlur(thresh, 5)

        vacant_count = 0
        occupied_count = 0
        output_frame = frame.copy()

        for slot in self.slots:
            x, y, w, h = slot["bbox"]
            roi = median[y:y+h, x:x+w]
            count = cv2.countNonZero(roi)

            # Determine occupancy based on non-zero pixel density
            is_occupied = count > self.threshold
            if is_occupied:
                occupied_count += 1
                color = (0, 0, 255) # Red for Occupied
                status = "Occupied"
            else:
                vacant_count += 1
                color = (0, 255, 0) # Green for Vacant
                status = "Vacant"

            # Draw rectangle and status label
            cv2.rectangle(output_frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                output_frame,
                f"{slot['name']}: {status}",
                (x, y - 8),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1
            )

        stats = {
            "total": len(self.slots),
            "vacant": vacant_count,
            "occupied": occupied_count
        }

        return output_frame, stats
