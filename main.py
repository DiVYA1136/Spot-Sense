"""
SpotSense - AI-Powered Smart Parking Slot Detection & Management System
Main Entrypoint Application
"""

import argparse
import sys
import os

def run_annotator():
    """Launch the interactive slot annotation tool."""
    print("\n[INFO] Launching SpotSense Parking Slot Annotation Tool (test1.py)...")
    try:
        import test1
    except Exception as e:
        print(f"[ERROR] Failed to run test1.py: {e}")

def run_detector():
    """Launch the real-time YOLOv8 vehicle detection and occupancy tracker."""
    print("\n[INFO] Launching SpotSense Real-Time Occupancy Tracker (test2.py)...")
    try:
        import test2
    except Exception as e:
        print(f"[ERROR] Failed to run test2.py: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="SpotSense - AI-Powered Smart Parking Slot Detection System"
    )
    parser.add_argument(
        "-a", "--annotate",
        action="store_true",
        help="Launch the interactive slot annotation tool to draw and label parking bays."
    )
    parser.add_argument(
        "-d", "--detect",
        action="store_true",
        help="Launch the real-time YOLOv8 vehicle detection and slot occupancy tracker (default)."
    )

    args = parser.parse_args()

    print("=========================================================")
    print("               🚗 SpotSense AI Engine                   ")
    print("    Smart Parking Slot Detection & Management System    ")
    print("=========================================================")

    if args.annotate:
        run_annotator()
    else:
        run_detector()

if __name__ == "__main__":
    main()
