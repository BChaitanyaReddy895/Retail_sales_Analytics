from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd
from sqlalchemy import create_engine, text

from utils import setup_logger


TABLE_ORDER = ["regions", "customers", "products", "inventory", "sales"]


def create_database_engine(database_url: str):
    return create_engine(database_url, future=True)


def load_schema(engine, schema_file: Path) -> None:
    schema_sql = schema_file.read_text(encoding="utf-8")
    statements = [statement.strip() for statement in schema_sql.split(";") if statement.strip()]
    with engine.begin() as connection:
        for statement in statements:
            connection.execute(text(statement))


def truncate_tables(engine, tables: list[str]) -> None:
    if not tables:
        return

    with engine.begin() as connection:
        if engine.dialect.name == "sqlite":
            connection.execute(text("PRAGMA foreign_keys = OFF"))
            for table_name in reversed(tables):
                connection.execute(text(f"DELETE FROM {table_name}"))
            connection.execute(text("PRAGMA foreign_keys = ON"))
        else:
            connection.execute(text(f"TRUNCATE TABLE {', '.join(tables)} RESTART IDENTITY CASCADE"))


def load_tables(engine, tables: Dict[str, pd.DataFrame], logger=None) -> None:
    logger = logger or setup_logger("load", Path("logs"))
    truncate_tables(engine, [table for table in TABLE_ORDER if table in tables])

    with engine.begin() as connection:
        for table_name in TABLE_ORDER:
            frame = tables.get(table_name)
            if frame is None or frame.empty:
                logger.warning("Skipping empty table %s", table_name)
                continue
            frame.to_sql(table_name, con=connection, if_exists="append", index=False, method="multi", chunksize=500)
            logger.info("Loaded %s rows into %s", len(frame), table_name)
