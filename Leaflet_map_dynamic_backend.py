import pandas as pd
import json
import os

csv_file = "/Users/supriyarai/Code/ge-o_map/Scotland_Census-2022-Output-Area-Full/UV102b - Age (20) by sex (Full Geo).csv"
data = pd.read_csv(csv_file)

# Convert NaN to None (handles missing values properly)
data = data.where(pd.notna(data), None)

# Convert DataFrame to a dictionary list
data_list = data.to_dict(orient="records")

# Extra safeguard: Replace any remaining "NaN" strings before dumping JSON
json_string = json.dumps(data_list, indent=4, ensure_ascii=False).replace(": NaN", ": null")

# Output folder
output_folder = "/Users/supriyarai/Code/ge-o_map/Map_JSON"
os.makedirs(output_folder, exist_ok=True)

# Specify JSON filename and destination
json_file = os.path.join(output_folder, f"output.UV102b_Age_by_Sex.json")

# Save cleaned JSON data to file
with open(json_file, "w", encoding="utf-8") as f:
    f.write(json_string)

print(f"✅ Cleaned JSON saved to {json_file}")
