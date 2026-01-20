import pandas as pd
import glob

# Load demographic data
print("=== DEMOGRAPHIC DATA ===")
files = glob.glob('data/raw/demographic/*.csv')
df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)

# Clean state names
df['state_clean'] = df['state'].str.lower().str.strip()

# Show columns
print(f"\nColumns: {df.columns.tolist()}")

# Aggregate by state for demo_age columns
demo_cols = [c for c in df.columns if c.startswith('demo_age')]
print(f"\nDemo age columns: {demo_cols}")

for col in demo_cols:
    print(f"\n=== Top 10 states by {col} ===")
    agg = df.groupby('state_clean')[col].sum().sort_values(ascending=False)
    print(agg.head(10))
