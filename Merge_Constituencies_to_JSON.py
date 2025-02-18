import json
import pandas as pd
import os

# ✅ Paths
csv_path = "/Users/supriyarai/Code/ge-o_map/oa_constituency_mapping.csv"
json_dir = "/Users/supriyarai/Code/ge-o_map/Map_JSON/"

# ✅ Load constituency mapping CSV
print("📥 Loading constituency mapping CSV...")
df_constituency = pd.read_csv(csv_path)

# ✅ Ensure proper column names
expected_columns = {"OA_Code", "Constituency"}
if not set(df_constituency.columns).issuperset(expected_columns):
    raise ValueError(f"❌ CSV is missing required columns: {expected_columns}")

# Convert to dictionary for quick lookup
oa_constituency_map = df_constituency.set_index("OA_Code")["Constituency"].to_dict()
print(f"✅ Loaded {len(oa_constituency_map)} OA_Code → Constituency mappings.")

# ✅ Process each JSON file in Map_JSON directory
for filename in os.listdir(json_dir):
    if filename.endswith(".json"):
        json_path = os.path.join(json_dir, filename)
        output_json_path = os.path.join(json_dir, filename.replace(".json", "_Updated.json"))

        print(f"📥 Processing: {filename}...")

        # ✅ Load JSON dataset
        with open(json_path, "r", encoding="utf-8") as file:
            try:
                json_data = json.load(file)
            except json.JSONDecodeError:
                print(f"❌ Error: Failed to parse {filename}, skipping.")
                continue

        # ✅ Merge constituency information
        updated_data = []
        for entry in json_data:
            oa_code = entry.get("OA_Code")

            if not oa_code:
                print(f"⚠️ Missing OA_Code in entry: {entry}")
                continue

            entry["Constituency"] = oa_constituency_map.get(oa_code, "Unknown")
            updated_data.append(entry)

        print(f"✅ Updated {len(updated_data)} entries in {filename}.")

        # ✅ Save updated JSON
        with open(output_json_path, "w", encoding="utf-8") as file:
            json.dump(updated_data, file, indent=4)

        print(f"📁 Saved updated JSON to {output_json_path}")

print("🎉 All JSON files have been processed successfully!")
