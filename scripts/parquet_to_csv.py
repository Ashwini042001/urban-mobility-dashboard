import pandas as pd

parquet_file = r"C:\Users\Ashwini\urban-mobility-dashboard\data\raw\2025-01-yellow.parquet"
csv_file = r"C:\Users\Ashwini\urban-mobility-dashboard\data\raw\2025-01-yellow.csv"

df = pd.read_parquet(parquet_file)
df.to_csv(csv_file, index=False)

print(f"✅ Converted Parquet to CSV: {csv_file}")