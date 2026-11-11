import pandas as pd
import psycopg
import json
import os
from dotenv import load_dotenv

movies = pd.read_csv("data/movies.csv")

print(movies.shape)

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
    INSERT INTO movies (movieid, title, genres)
    VALUES (%s, %s, %s)
    ON CONFLICT (movieid)
    DO UPDATE SET
        title = EXCLUDED.title,
        genres = EXCLUDED.genres
    WHERE
        movies.title IS DISTINCT FROM EXCLUDED.title
        OR movies.genres IS DISTINCT FROM EXCLUDED.genres;
    """

    movie_records = list(movies.itertuples(index=False, name=None))
    print(len(movie_records))
    print(movie_records[0])
    print(type(movie_records))
    print(type(movie_records[0]))

    cur = conn.cursor()

    cur.executemany(insert_query, movie_records)

    rows_read = len(movie_records)
    print(f"Rows read from CSV: {rows_read}")

    print(f"Rows Affected: {cur.rowcount}")

    movies_metrics = {
        "rows_read": rows_read,
        "rows_affected": cur.rowcount
    }

    conn.commit()

    with open("reports/movies_metrics.json", "w") as file:
        json.dump(movies_metrics, file, indent=4)
    
    print("Movie metrics saved successfully!")

    print("Movie records processed successfully!")

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


