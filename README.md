# Retail Sales ETL Pipeline & Analytics System

## Project Summary

- Built an end-to-end ETL pipeline using Python, SQL, and Power BI for processing retail sales datasets.
- Automated data extraction, cleaning, transformation, and loading workflows for structured datasets.
- Designed relational database schemas and optimized SQL queries for analytics and reporting.
- Created interactive Power BI dashboards to visualize sales trends, customer insights, and inventory analytics.

## Project Scope

The repository contains the code and support files for a retail ETL workflow that ingests CSV files, transforms them with Pandas, loads normalized tables into a relational database, and supports reporting in SQL and Power BI.

## Core Pipeline

1. Extract raw retail CSV files.
2. Clean and transform the structured data.
3. Validate the processed output.
4. Load curated tables into the SQL database.

## Database Layer

The schema includes normalized tables for customers, products, sales, inventory, and regions. The SQL files include joins, aggregations, filtering, and indexing examples for analytics and reporting.

## Power BI Dashboard

The dashboard focuses on:

- sales trends
- customer insights
- inventory analytics

## Local Run

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/generate_sample_data.py
python scripts/pipeline_runner.py
```

For PostgreSQL, start the container with `docker compose up -d` and set `DATABASE_URL` in `.env`.

## Notes

- `DATABASE_URL` defaults to SQLite for local execution.
- PostgreSQL is supported as the primary database option.
- The project is intentionally kept focused on these core ETL and analytics tasks.
