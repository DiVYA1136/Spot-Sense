"""
SpotSense - Utility Functions
"""
import os
import json
import pickle
import numpy as np

def export_slots_to_json(pickle_path: str = 'Manasa', json_path: str = 'slots.json') -> bool:
    if not os.path.exists(pickle_path):
        return False
    with open(pickle_path, 'rb') as f:
        data = pickle.load(f)
    polylines = data.get('polylines', [])
    area_names = data.get('area_names', [])
    json_slots = []
    for i, poly in enumerate(polylines):
        name = area_names[i] if i < len(area_names) else str(i + 1)
        json_slots.append({'slot_id': i + 1, 'name': name, 'polygon': poly.tolist()})
    with open(json_path, 'w') as f:
        json.dump(json_slots, f, indent=2)
    return True
