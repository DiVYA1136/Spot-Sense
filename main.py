"""
SpotSense - AI-Powered Smart Parking Slot Detection & Management System
Main Application Entrypoint
"""

import os
import sys
from src.slot_detector import ParkingSlotDetector
from src.utils import draw_header_dashboard

def main():
    print("=========================================================")
    print("               🚗 SpotSense AI Engine                   ")
    print("    Smart Parking Slot Detection & Management System    ")
    print("=========================================================")

    config_path = os.path.join("config", "slots_sample.json")
    print(f"[INFO] Loading slot configuration from: {config_path}")

    detector = ParkingSlotDetector(config_path=config_path)
    print(f"[INFO] Successfully loaded {len(detector.slots)} parking slots.")
    print("[INFO] Computer Vision detection pipeline initialized successfully.")

if __name__ == "__main__":
    main()
