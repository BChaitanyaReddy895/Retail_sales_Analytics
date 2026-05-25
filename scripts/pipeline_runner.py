from __future__ import annotations

from pathlib import Path

from config import load_settings
from extract import extract_csv_files
from generate_sample_data import main as generate_sample_data
from load import create_database_engine, load_schema, load_tables
from transform import transform_tables, validate_transformed_tables
from utils import ensure_directory, setup_logger


def run_pipeline() -> int:
    settings = load_settings()
    ensure_directory(settings.raw_data_dir)
    ensure_directory(settings.processed_data_dir)
    ensure_directory(settings.log_dir)

    logger = setup_logger("pipeline", settings.log_dir)
    logger.info("Starting retail sales ETL pipeline")

    if not list(settings.raw_data_dir.glob("*.csv")):
        logger.info("No raw CSV files found. Generating sample dataset.")
        generate_sample_data()

    raw_tables = extract_csv_files(settings.raw_data_dir, logger=logger)
    transform_result = transform_tables(raw_tables, settings.processed_data_dir, logger=logger)

    validation_issues = validate_transformed_tables(transform_result)
    if validation_issues:
        for issue in validation_issues:
            logger.error(issue)
        raise ValueError("Pipeline validation failed")

    engine = create_database_engine(settings.database_url)
    load_schema(engine, Path(__file__).resolve().parents[1] / "sql" / "schema.sql")
    load_tables(engine, transform_result.tables, logger=logger)

    logger.info("Pipeline completed successfully")
    print("Pipeline completed successfully")
    return 0


if __name__ == "__main__":
    raise SystemExit(run_pipeline())
