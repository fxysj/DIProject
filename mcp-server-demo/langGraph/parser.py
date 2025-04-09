import re
from typing import Dict

def parse_bmi_params(query: str) -> Dict:
    weight_match = re.search(r"体重\s*([0-9.]+)\s*(公斤|kg|KG)?", query)
    height_match = re.search(r"身高\s*([0-9.]+)\s*(米|m|M)?", query)

    weight = float(weight_match.group(1)) if weight_match else 70.0
    height = float(height_match.group(1)) if height_match else 1.75

    return {"weight_kg": weight, "height_m": height}
