import pandas as pd

# Read the 3 CSV files
df1 = pd.read_csv('file1.csv')
df2 = pd.read_csv('file2.csv')
df3 = pd.read_csv('file3.csv')

# Merge with full outer joins
merged_df = df1.merge(df2, on='id', how='outer').merge(df3, on='id', how='outer')

# Save result
merged_df.to_csv('merged_all_ids.csv', index=False)
print("✅ Merged all CSVs (all IDs included).")


