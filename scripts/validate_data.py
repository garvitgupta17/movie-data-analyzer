import psycopg
import logging
import sys
import json
import os
from dotenv import load_dotenv

logger = logging.getLogger("movie_analyzer")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    "logs/validation.log",
    mode="a"
)

console_handler = logging.StreamHandler()

formatter = logging.Formatter(
    "%(asctime)s - %(levelname)s - %(message)s"
)

file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)

conn = None
cur = None

try:
    load_dotenv()

    logger.info("Validation started")

    conn = psycopg.connect(
        host=os.getenv("DB_HOST"),
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        port=int(os.getenv("DB_PORT", "5432"))
    )

    logger.info("Database connection successful")

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM movies;")
    total_movies = cur.fetchone()
    logger.info(f"Total movies: {total_movies[0]}")

    cur.execute("SELECT COUNT(*) FROM ratings;")
    total_ratings = cur.fetchone()
    logger.info(f"Total ratings: {total_ratings[0]}")

    cur.execute("SELECT COUNT(*) FROM (SELECT movieid FROM movies GROUP BY movieid HAVING COUNT(*) > 1) AS duplicates;")
    duplicate_movie_ids = cur.fetchone()
    logger.info(f"Duplicated movie ids: {duplicate_movie_ids[0]}")

    cur.execute("SELECT COUNT(*) FROM ratings r WHERE NOT EXISTS (SELECT 1 FROM movies m WHERE m.movieid = r.movieid);")
    orphan_ratings = cur.fetchone()
    logger.info(f"Orphan ratings: {orphan_ratings[0]}")

    cur.execute("SELECT COUNT(*) FROM ratings WHERE rating > 5.0 OR rating < 0.5 OR CAST(rating AS NUMERIC) % 0.5 <> 0;")
    invalid_ratings = cur.fetchone()
    logger.info(f"Invalid ratings: {invalid_ratings[0]}")

    validation_status = "PASSED" if (
        duplicate_movie_ids[0] == 0 
        and orphan_ratings[0] == 0 
        and invalid_ratings[0] == 0
    ) else "FAILED"

    validation_metrics = {
        "total_movies": total_movies[0],
        "total_ratings": total_ratings[0],
        "duplicate_movie_ids": duplicate_movie_ids[0],
        "orphan_ratings": orphan_ratings[0],
        "invalid_ratings": invalid_ratings[0],
        "status": validation_status
    }

    with open("reports/validation_metrics.json", "w") as file:
        json.dump(validation_metrics, file, indent=4)
    
    print("Validation metrics saved successfully!")

    if validation_status == "PASSED":
        logger.info("PASSED")
        sys.exit(0)
    else:
        logger.error("FAILED")
        sys.exit(1)

except psycopg.OperationalError:
    logger.exception("Database connection failed")
    sys.exit(1)

finally:
    if cur is not None:
        cur.close()
    if conn is not None:
        conn.close()
    logger.info("Validation completed")
    