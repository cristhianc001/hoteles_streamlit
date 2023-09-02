import pandas as pd

df = pd.read_parquet("data/df_transformed.parquet")
df["date"] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')