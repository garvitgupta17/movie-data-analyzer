-- Calculate total movie ratings and average movie ratings 
SELECT
    m.movieid,
    m.title,
    AVG(r.rating) AS avg_rating,
    COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r
    ON m.movieid = r.movieid
GROUP BY m.movieid, m.title
HAVING COUNT(r.rating) >= 50
ORDER BY avg_rating DESC, total_ratings DESC
LIMIT 10;


-- All distinct genres
SELECT DISTINCT(genres) AS genre
FROM movies
ORDER BY genre;


-- Extract individual genres
SELECT STRING_TO_ARRAY(genres, '|') AS genre
FROM movies
LIMIT 10;


-- Expand arrays into individual rows
SELECT UNNEST(
    STRING_TO_ARRAY(genres, '|')
) AS genre
FROM movies
LIMIT 10;


-- Count movies by individual genre
SELECT UNNEST(
    STRING_TO_ARRAY(genres, '|')
) AS genre, COUNT(*) AS movie_count
FROM movies
WHERE genres <> '(no genres listed)'
GROUP BY genre
ORDER BY movie_count DESC;


-- Analyze average rating by genre
SELECT g.genre,
    AVG(r.rating) AS avg_rating,
    COUNT(r.rating) AS total_ratings
FROM movies m
JOIN ratings r 
    ON m.movieid = r.movieid
CROSS JOIN LATERAL UNNEST(
    STRING_TO_ARRAY(m.genres, '|')
) AS g(genre)
WHERE m.genres <> '(no genres listed)'
GROUP BY g.genre
HAVING COUNT(r.rating) >= 500
ORDER BY avg_rating DESC;


-- Find the most active users
SELECT 
    userid,
    COUNT(*) AS total_ratings,
    AVG(rating) AS avg_rating
FROM ratings
GROUP BY userid
ORDER BY total_ratings DESC
LIMIT 10;


-- Analyse rating distribution
SELECT rating, COUNT(*) AS total_ratings
FROM ratings
GROUP BY rating
ORDER BY rating;


-- Calculate each user's rating behaviour
-- Find users whose average rating is above the overall average rating.
SELECT
    userid,
    AVG(rating) AS avg_rating,
    COUNT(*) AS total_ratings
FROM ratings
GROUP BY userid
HAVING
    COUNT(rating) >= 50
    AND AVG(rating) > (SELECT AVG(rating) FROM ratings)
ORDER BY avg_rating DESC
LIMIT 10;


-- Find the most popular movies by rating volume
-- Which movies have received the most user ratings, and what is their average rating?
SELECT 
    m.movieid,
    m.title,
    COUNT(*) AS total_ratings,
    AVG(r.rating) AS avg_rating
FROM movies m
JOIN ratings r
    ON m.movieid = r.movieid
GROUP BY m.movieid, m.title
HAVING COUNT(*) >= 100
ORDER BY total_ratings DESC
LIMIT 15;


-- Data quality and integrity checks
-- Check 1 — Total records
-- movies
SELECT COUNT(*) AS total_movies
FROM movies;
-- ratings
SELECT COUNT(*) AS total_ratings
FROM ratings;

-- Check 2 — Duplicate records
-- Check whether duplicate movie IDs exist in movies.
SELECT COUNT(*)
FROM movies
GROUP BY movieid
HAVING COUNT(*) > 1;

-- Check 3 — Referential integrity
-- Find ratings whose movieid does not exist in movies.
SELECT *
FROM ratings r
WHERE movieid NOT EXISTS (SELECT 1 FROM movies M WHERE m.movieid = r.movieid);

-- Check 4 — Invalid ratings
-- Find ratings outside the valid MovieLens range of 0.5 to 5.0, in increments of 0.5.
SELECT * 
FROM ratings 
WHERE rating < 0.5 OR rating > 5.0 OR CAST(rating AS NUMERIC) % 0.5 <> 0;

SELECT
    (SELECT COUNT(*) FROM movies) AS total_movies,
    (SELECT COUNT(*) FROM ratings) AS total_ratings,
    (SELECT COUNT(*) FROM (SELECT movieid FROM movies GROUP BY movieid HAVING COUNT(*) > 1) AS duplicates) AS duplicate_movie_ids,
    (SELECT COUNT(*) FROM ratings r WHERE NOT EXISTS (SELECT 1 FROM movies m WHERE m.movieid = r.movieid)) AS orphan_ratings,
    (SELECT COUNT(*) FROM ratings WHERE rating < 0.5 OR rating > 5.0 OR CAST(rating AS NUMERIC) % 0.5 <> 0) AS invalid_ratings;