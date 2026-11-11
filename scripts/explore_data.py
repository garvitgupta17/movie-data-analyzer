import pandas as pd

# inspect movies.csv file
movies = pd.read_csv("data/movies.csv")

print(movies.head())
print(movies.shape)
print(movies.columns)
movies.info()
print(movies.isnull().sum())
print(movies.duplicated().sum())

print(movies["movieId"].nunique())
print(movies["movieId"].duplicated().sum())

# inspect ratings.csv file
ratings = pd.read_csv("data/ratings.csv")

print(ratings.shape)
print(ratings.isnull().sum())
print(ratings.duplicated().sum())
print(ratings["rating"].describe())

# Check referential integrity
print(ratings["movieId"].nunique())
print(ratings["userId"].nunique())
print((~ratings["movieId"].isin(movies["movieId"])).sum())

# Validate the composite primary-key assumption
print(ratings.duplicated(subset=["userId", "movieId"]).sum())

# Understand the source data
print(movies.head(3).values.tolist())

