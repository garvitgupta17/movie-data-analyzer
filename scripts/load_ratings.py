import pandas as pd
import psycopg
import json
import os
from dotenv import load_dotenv

ratings = pd.read_csv("data/ratings.csv")

print(ratings.shape)

rating_records = list(ratings.itertuples(index=False, name=None))

print(rating_records[0])
print([type(value) for value in rating_records[0]])
print(len(rating_records))
print(ratings.dtypes)
print(ratings.head())
print(type(rating_records[0]))

conn = None
cur = None

try:
    load_dotenv()

    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        port=int(os.getenv("DB_PORT", "5432"))
    )

    insert_query = """
    INSERT INTO ratings (userid, movieid, rating, timestamp) 
    VALUES (%s, %s, %s, %s)
    ON CONFLICT (userid, movieid)
    DO UPDATE SET
        rating = EXCLUDED.rating,
        timestamp = EXCLUDED.timestamp
    WHERE
        ratings.rating IS DISTINCT FROM EXCLUDED.rating
        OR ratings.timestamp IS DISTINCT FROM EXCLUDED.timestamp;
    """

    cur = conn.cursor()

    cur.executemany(insert_query, rating_records)

    rows_read = len(rating_records)
    print(f"Rows read from CSV: {rows_read}")

    print(f"Rows Affected: {cur.rowcount}")

    ratings_metrics = {
        "rows_read": rows_read,
        "rows_affected": cur.rowcount
    }

    conn.commit()
    
    with open("reports/ratings_metrics.json", "w") as file:
        json.dump(ratings_metrics, file, indent=4)
    
    print("Ratings metrics saved successfully!")

    print("Rating records processed successfully!")

except Exception as e:
    if conn is not None:
        conn.rollback()

    print(f"Failed to insert the records: {e}")
    raise

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
