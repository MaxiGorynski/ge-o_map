import json
import pandas as pd

# ✅ Paths to source files
csv_path = "/Users/supriyarai/Code/ge-o_map/oa_constituency_mapping.csv"
json_path = "/Users/supriyarai/Code/ge-o_map/Map_JSON/19. British Sign Language (BSL) Skills by Age.json"
output_json_path = "/Users/supriyarai/Code/ge-o_map/Map_JSON/19. British Sign Language (BSL) Skills by Age_Updated.json"

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

# ✅ Load JSON dataset
print("📥 Loading dataset JSON...")
with open(json_path, "r", encoding="utf-8") as file:
    json_data = json.load(file)

# ✅ Merge constituency information into each entry
updated_data = []
for entry in json_data:
    oa_code = entry.get("OA_Code")

    if not oa_code:
        print(f"⚠️ Missing OA_Code in entry: {entry}")
        continue

    # Assign the constituency name
    entry["Constituency"] = oa_constituency_map.get(oa_code, "Unknown")
    updated_data.append(entry)

print(f"✅ Merged constituency names into {len(updated_data)} dataset entries.")

# ✅ Save updated JSON
with open(output_json_path, "w", encoding="utf-8") as file:
    json.dump(updated_data, file, indent=4)

print(f"📁 Saved updated JSON to {output_json_path}")
