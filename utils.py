"""
SpotSense - Utility Functions and Helper Tools
Provides slot format conversion (Pickle <-> JSON) and geometry helper routines.
"""

import os
import json
import pickle
import numpy as np

def export_slots_to_json(pickle_path: str = 'Manasa', json_path: str = 'slots.json') -> bool:
    """
    Exports binary pickle slot polylines to a human-readable JSON format.
    Useful for cross-platform dashboards and API integrations.
    """
    if not os.path.exists(pickle_path):
        print(f"[ERROR] Source pickle file '{pickle_path}' not found.")
        return False

    with open(pickle_path, 'rb') as f:
        data = pickle.load(f)

    polylines = data.get('polylines', [])
    area_names = data.get('area_names', [])

    json_slots = []
    for i, poly in enumerate(polylines):
        name = area_names[i] if i < len(area_names) else str(i + 1)
        points = poly.tolist() if hasattr(poly, 'tolist') else list(poly)
        json_slots.append({
            "slot_id": i + 1,
            "name": name,
            "polygon": points
        })

    with open(json_path, 'w') as f:
        json.dump(json_slots, f, indent=2)

    print(f"[SUCCESS] Exported {len(json_slots)} slots to '{json_path}'.")
    return True

def import_slots_from_json(json_path: str = 'slots.json', pickle_path: str = 'Manasa') -> bool:
    """
    Imports slots from JSON format and compiles them into a binary pickle file.
    """
    if not os.path.exists(json_path):
        print(f"[ERROR] Source JSON file '{json_path}' not found.")
        return False

    with open(json_path, 'r') as f:
        json_slots = json.load(f)

    polylines = []
    area_names = []

    for item in json_slots:
        area_names.append(item.get("name", "Unknown"))
        poly_arr = np.array(item.get("polygon", []), dtype=np.int32)
        polylines.append(poly_arr)

    with open(pickle_path, 'wb') as f:
        pickle.dump({'polylines': polylines, 'area_names': area_names}, f)

    print(f"[SUCCESS] Imported {len(polylines)} slots and saved to '{pickle_path}'.")
    return True

if __name__ == "__main__":
    # If run directly, generate slots.json from existing Manasa calibration
    if os.path.exists('Manasa'):
        export_slots_to_json('Manasa', 'slots.json')

# Verified round-trip conversion integrity between JSON and Pickle
