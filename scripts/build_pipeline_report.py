import json
import os

with open("reports/movies_metrics.json", "r") as file:
    movies_metrics = json.load(file)

with open("reports/ratings_metrics.json", "r") as file:
    ratings_metrics = json.load(file)

with open("reports/validation_metrics.json", "r") as file:
    validation_metrics = json.load(file)

total_rows_read = (
    movies_metrics["rows_read"] +
    ratings_metrics["rows_read"]
)

total_rows_affected = (
    movies_metrics["rows_affected"] +
    ratings_metrics["rows_affected"]
)

summary = {
    "total_rows_read": total_rows_read,
    "total_rows_affected": total_rows_affected
}

pipeline_status = (
    "SUCCESS"
    if validation_metrics["status"] == "PASSED"
    else "FAILED"
)

pipeline_start_time = os.environ["PIPELINE_START_TIME"]

pipeline_completed_time = os.environ["PIPELINE_COMPLETED_TIME"]

execution_time_seconds = int(os.environ["PIPELINE_DURATION"])

print("Start time:", pipeline_start_time)
print("Completed time:", pipeline_completed_time)
print("Execution time:", execution_time_seconds)

pipeline_report ={
    "pipeline_name": "movie_analyzer",
    "movies": movies_metrics,
    "ratings": ratings_metrics,
    "validation": validation_metrics,
    "summary": summary,
    "execution": {
        "started_at": pipeline_start_time,
        "completed_at": pipeline_completed_time,
        "duration_seconds": execution_time_seconds
    },
    "status": pipeline_status,
}

with open("reports/pipeline_metrics.json", "w") as file:
    json.dump(pipeline_report, file, indent=4)

print("Combined pipeline report generated successfully!")