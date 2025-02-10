import json
import os

# 🔹 Define input JSON file path (modify as needed)
input_file = "static/epsg27700_boundaries.json"
output_dir = "Boundaries_JSON"

# 🔹 Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# 🔹 Load the large JSON file
print(f"📥 Loading JSON file: {input_file}")
try:
    with open(input_file, "r", encoding="utf-8") as file:
        data = json.load(file)
except Exception as e:
    print(f"❌ Error loading JSON: {e}")
    exit()

# 🔹 Ensure the data has the expected structure
if "features" not in data:
    print("❌ Error: JSON file does not contain 'features' key!")
    exit()

# 🔹 Process and split boundaries
print(f"🔄 Splitting {len(data['features'])} boundaries into separate files...")
file_count = 0

for feature in data["features"]:
    try:
        # Extract unit ID (modify based on actual JSON structure)
        unit_id = feature.get("properties", {}).get("unit_id", f"unknown_{file_count}")

        # Define output file path
        output_file = os.path.join(output_dir, f"boundary_{unit_id}.json")

        # Write single boundary data to new JSON file
        with open(output_file, "w", encoding="utf-8") as out_file:
            json.dump(feature, out_file, indent=4)

        file_count += 1
        if file_count % 500 == 0:
            print(f"✅ {file_count} boundary files created...")

    except Exception as e:
        print(f"❌ Error processing unit_id {unit_id}: {e}")

print(f"🎉 Done! {file_count} boundary files saved in '{output_dir}'")
