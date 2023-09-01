import pandas as pd

df_reviews = pd.read_csv("data/reviews.csv", sep=";", parse_dates=["date"])
df_lodgings = pd.read_csv("data/lodgings.csv", sep=";")

df = df_reviews.merge(df_lodgings, on="lodging_id")