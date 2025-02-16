#One-time use for testing completeness of boundary data that is now superfluous.

import os
import json
import numpy as np
from scipy.spatial import distance

# ✅ Directory containing all boundary JSON files
BOUNDARY_DIR = "/Users/supriyarai/Code/ge-o_map/Boundaries_JSON"


# ✅ Function to calculate nearest point in a set
def find_nearest_coordinate(start_point, coordinates):
    distances = [distance.euclidean(start_point, point) for point in coordinates]
    nearest_idx = np.argmin(distances)
    return coordinates[nearest_idx]


# ✅ Iterate over all JSON boundary files
def check_boundary_closure():
    files = [f for f in os.listdir(BOUNDARY_DIR) if f.endswith(".json")]

    for file in files:
        file_path = os.path.join(BOUNDARY_DIR, file)

        try:
            with open(file_path, "r") as f:
                data = json.load(f)

            # Extract polygon coordinates
            if "geometry" in data and "coordinates" in data["geometry"]:
                coords = data["geometry"]["coordinates"][0]  # First polygon ring
                first_coord = tuple(coords[0])
                last_coord = tuple(coords[-1])

                # Case 1: Check if the polygon is already closed
                if first_coord == last_coord:
                    print(f"✅ {file}: Already closed.")
                    continue  # Move to next file

                # Case 2: Find the nearest coordinate to the first one
                nearest_coord = find_nearest_coordinate(first_coord, coords)

                print(f"⚠️ {file}: First ≠ Last ({first_coord} ≠ {last_coord})")
                print(f"   🔍 Nearest to First: {nearest_coord}")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")


# ✅ Run the check
check_boundary_closure()