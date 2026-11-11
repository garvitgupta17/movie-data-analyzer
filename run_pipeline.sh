#!/bin/bash
set -e

exec > >(tee -a logs/pipeline.log) 2>&1

SECONDS=0

pipeline_start_time=$(date -Iseconds)

rm -f reports/movies_metrics.json
rm -f reports/ratings_metrics.json
rm -f reports/validation_metrics.json
rm -f reports/pipeline_metrics.json

pipeline_exit() {
    exit_code=$?

    if [ $exit_code -eq 0 ]; then
        echo "Pipeline Status: SUCCESS"
    else
        echo "Pipeline Status: FAILED"
        echo "Exit Code: $exit_code"
    fi
}
trap pipeline_exit EXIT

echo "================================"
echo "Movie Data Pipeline Started"
date
echo "================================"

echo "Step 1: Loading Movies..."
python3 scripts/load_movies.py

echo "Step 2: Loading Ratings..."
python3 scripts/load_ratings.py

echo "Step 3: Running Data Validation..."
python3 scripts/validate_data.py

pipeline_completed_time=$(date -Iseconds)

echo "Step 4: Building Pipeline Report..."
PIPELINE_START_TIME="$pipeline_start_time" \
PIPELINE_COMPLETED_TIME="$pipeline_completed_time" \
PIPELINE_DURATION="$SECONDS" \
python3 scripts/build_pipeline_report.py

echo "Execution Time: ${SECONDS} seconds"

validation_status=$(python3 -c "import json; print(json.load(open('reports/pipeline_metrics.json'))['validation']['status'])")

pipeline_status=$(python3 -c "import json; print(json.load(open('reports/pipeline_metrics.json'))['status'])")

echo " "
echo "========== ETL SUMMARY =========="
echo "Movies source: data/movies.csv"
echo "Ratings source: data/ratings.csv"
echo "Database: movie_analyzer"
echo "Validation: $validation_status"
echo "Execution Time: ${SECONDS} seconds"
echo "Pipeline Status: $pipeline_status"
echo "================================="

echo "================================"
echo "Movie Data Pipeline Finished"
echo "================================"