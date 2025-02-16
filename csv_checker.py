##For checking the contents and structure of CSVs that are too large to import to a CSV tool


import pandas as pd

# ✅ File Path
CSV_FILE = "/Users/supriyarai/Code/ge-o_map/westminster-parliamentary-constituencies.csv"

# ✅ Load only first 10 rows to inspect structure
print("📌 Loading CSV (First 10 rows only)...")
df = pd.read_csv(CSV_FILE, nrows=10)

# ✅ Display column names
print("\n🔍 Column Names:", df.columns.tolist())

# ✅ Display first few rows
print("\n📝 Sample Data:\n", df.head())

# ✅ Check total row count (without loading full file)
total_rows = sum(1 for row in open(CSV_FILE)) - 1  # Subtract header row
print(f"\n📊 Total Rows in File: {total_rows}")
