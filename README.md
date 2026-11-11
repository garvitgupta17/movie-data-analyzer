# Movie Data Analyzer

A Python and PostgreSQL-based ETL pipeline that processes the MovieLens dataset, performs data quality validation, and generates structured JSON execution reports.

## Project Overview

Movie Data Analyzer is a hands-on Data Engineering project demonstrating a basic but complete batch data pipeline.

The project extracts movie and rating records from CSV files, transforms them into database-compatible records, loads them into PostgreSQL, validates data integrity, and generates pipeline execution metrics.

### Key Features

- CSV ingestion using Python and Pandas.
- PostgreSQL integration using Psycopg 3.
- Idempotent data loading using conditional UPSERT operations.
- Primary key and foreign key constraints.
- SQL-based analytics using JOINs, aggregations, subqueries, and window-independent relational queries.
- Data quality checks for duplicate movie IDs, orphan ratings, and invalid ratings.
- Structured logging and exception handling.
- Environment-based database configuration using `.env`.
- Automated pipeline orchestration using Bash.
- JSON reports for individual ETL stages and overall pipeline execution.

## Technology Stack

| Technology | Purpose |
|---|---|
| Python 3.10 | ETL development |
| Pandas | CSV processing |
| PostgreSQL 16 | Relational database |
| Psycopg 3 | Python–PostgreSQL connectivity |
| SQL | Data analysis and validation |
| Bash | Pipeline orchestration |
| python-dotenv | Environment configuration |
| JSON | Pipeline metrics and reporting |
| Git | Version control |

## Project Architecture

```text
MovieLens CSV Dataset
        |
        v
   Python / Pandas
        |
        v
   Data Processing
        |
        v
   PostgreSQL Database
     /          \
    v            v
Movies Table   Ratings Table
     \          /
      v        v
    Data Validation
          |
          v
    JSON Reporting
          |
          v
   Pipeline Summary
```

## Project Structure

```text
movie-data-analyzer/
│
├── data/
│   ├── movies.csv
│   ├── ratings.csv
│   ├── links.csv
│   ├── tags.csv
│   └── README.txt
│
├── reports/
│   ├── movies_metrics.json
│   ├── ratings_metrics.json
│   ├── validation_metrics.json
│   └── pipeline_metrics.json
│
├── scripts/
│   ├── explore_data.py
│   ├── load_movies.py
│   ├── load_ratings.py
│   ├── validate_data.py
│   └── build_pipeline_report.py
│
├── sql/
│   └── analytics.sql
│
├── .env.example
├── .gitignore
├── requirements.txt
├── run_pipeline.sh
└── README.md
```

## Dataset

The project uses the MovieLens dataset.

| Dataset | Records |
|---|---:|
| Movies | 9,125 |
| Ratings | 100,004 |
| Unique users | 671 |
| Unique rated movies | 9,066 |

The pipeline primarily processes `movies.csv` and `ratings.csv`. The other CSV files are retained as part of the source dataset.

## Database Design

The project uses two relational tables.

### Movies

| Column | Data Type | Constraint |
|---|---|---|
| movieid | INTEGER | PRIMARY KEY |
| title | TEXT | NOT NULL |
| genres | TEXT | |

### Ratings

| Column | Data Type | Constraint |
|---|---|---|
| userid | INTEGER | PRIMARY KEY (composite) |
| movieid | INTEGER | PRIMARY KEY (composite), FOREIGN KEY |
| rating | REAL | NOT NULL |
| timestamp | BIGINT | NOT NULL |

The composite primary key on `(userid, movieid)` prevents duplicate ratings for the same user and movie.

### Create the Database

```bash
createdb movie_analyzer
```

Connect to PostgreSQL:

```bash
psql -d movie_analyzer
```

Create the tables:

```sql
CREATE TABLE movies (
    movieid INTEGER PRIMARY KEY,
    title TEXT NOT NULL,
    genres TEXT
);

CREATE TABLE ratings (
    userid INTEGER NOT NULL,
    movieid INTEGER NOT NULL,
    rating REAL NOT NULL,
    timestamp BIGINT NOT NULL,
    PRIMARY KEY (userid, movieid),
    FOREIGN KEY (movieid) REFERENCES movies(movieid)
);
```

## Getting Started

### 1. Prerequisites

Install the following:

- Python 3.10
- PostgreSQL 16 or a compatible PostgreSQL version
- Git

Ensure PostgreSQL is running before executing the pipeline.

### 2. Clone the Repository

```bash
git clone https://github.com/garvitgupta17/movie-data-analyzer.git

cd movie-data-analyzer
```

### 3. Create a Virtual Environment

```bash
python3 -m venv .venv

source .venv/bin/activate
```

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a local `.env` file using the example:

```bash
cp .env.example .env
```

Update the values according to your PostgreSQL configuration:

```dotenv
DB_HOST=localhost
DB_NAME=movie_analyzer
DB_USER=your_postgres_username
DB_PORT=5432
```

The `.env` file is excluded from version control to prevent accidental exposure of local configuration.

### 6. Create the Database and Tables

Follow the database setup instructions in the Database Design section above.

## Running the Pipeline

Execute the complete pipeline from the project root:

```bash
chmod +x run_pipeline.sh

./run_pipeline.sh
```

The pipeline executes the following stages:

1. **Load Movies:** Reads movie records from CSV and loads them into PostgreSQL.
2. **Load Ratings:** Reads rating records and loads them into PostgreSQL.
3. **Data Validation:** Checks database integrity and rating validity.
4. **Pipeline Reporting:** Combines execution metrics into a JSON report.

### Idempotent Loading

The ETL scripts use PostgreSQL `INSERT ... ON CONFLICT DO UPDATE` statements with conditional update clauses.

This allows the pipeline to be executed repeatedly without unnecessarily updating unchanged records.

## Data Quality Validation

The validation script performs the following checks:

| Validation | Description |
|---|---|
| Duplicate movie IDs | Checks uniqueness of movie identifiers |
| Orphan ratings | Identifies ratings referencing nonexistent movies |
| Invalid ratings | Checks rating range and increments |

Expected rating values range from 0.5 to 5.0 in increments of 0.5.

## Pipeline Reports

The pipeline generates four JSON reports inside the `reports/` directory.

| Report | Description |
|---|---|
| `movies_metrics.json` | Movie loading metrics |
| `ratings_metrics.json` | Rating loading metrics |
| `validation_metrics.json` | Data quality results |
| `pipeline_metrics.json` | Combined pipeline execution summary |

### Latest Execution Results

| Metric | Result |
|---|---:|
| Total movies processed | 9,125 |
| Total ratings processed | 100,004 |
| Total rows read | 109,129 |
| Duplicate movie IDs | 0 |
| Orphan ratings | 0 |
| Invalid ratings | 0 |
| Pipeline status | SUCCESS |
| ETL processing duration | 5 seconds |

*These results represent one successful execution and may vary across machines and subsequent runs.*

## SQL Analytics

The `sql/analytics.sql` file contains SQL queries for exploring the dataset, including:

- Movie rating counts.
- Average movie ratings.
- Genre-wise analysis.
- Top-rated movies.
- User rating activity.
- Rating distribution.
- Data quality checks.

## Future Improvements

- Implement automated unit and integration tests.
- Add incremental data loading.
- Introduce a proper database configuration module.
- Add workflow scheduling using Apache Airflow.
- Containerize the pipeline using Docker.
- Implement CI/CD with GitHub Actions.
- Add dashboard-based visualization of pipeline metrics.

## Learning Outcomes

This project demonstrates practical experience with:

- ETL pipeline development.
- Relational database design.
- Python and SQL integration.
- Data validation and quality checks.
- Transaction management and error handling.
- Logging and monitoring fundamentals.
- Bash automation.
- Environment configuration and dependency management.
- Git-based project organization.

---

**Project:** Movie Data Analyzer  
**Category:** Data Engineering / ETL / SQL Analytics