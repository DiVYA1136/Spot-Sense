"""
SpotSense Utility Functions
Helper functions for overlay rendering, metrics display, and logger formatting.
"""

import cv2

def draw_header_dashboard(image, stats):
    """
    Renders an overlay banner displaying live vacancy and occupancy metrics.
    """
    if image is None:
        return image

    h, w, _ = image.shape
    banner_height = 50
    overlay = image.copy()
    cv2.rectangle(overlay, (0, 0), (w, banner_height), (20, 20, 20), -1)
    cv2.addWeighted(overlay, 0.7, image, 0.3, 0, image)

    text = f"SpotSense Live | Total Slots: {stats.get('total', 0)} | Vacant: {stats.get('vacant', 0)} 🟢 | Occupied: {stats.get('occupied', 0)} 🔴"
    cv2.putText(
        image,
        text,
        (20, 32),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )
    return image
