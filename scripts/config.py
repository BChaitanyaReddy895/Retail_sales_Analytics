from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Settings:
    database_url: str
    raw_data_dir: Path
    processed_data_dir: Path
    log_dir: Path
    batch_size: int = 1000


def load_settings() -> Settings:
    database_url = os.getenv(
        "DATABASE_URL",
        "sqlite:///retail_sales.db",
    )
    raw_data_dir = Path(os.getenv("RAW_DATA_DIR", PROJECT_ROOT / "data" / "raw"))
    processed_data_dir = Path(
        os.getenv("PROCESSED_DATA_DIR", PROJECT_ROOT / "data" / "processed")
    )
    log_dir = Path(os.getenv("LOG_DIR", PROJECT_ROOT / "logs"))
    batch_size = int(os.getenv("BATCH_SIZE", "1000"))

    return Settings(
        database_url=database_url,
        raw_data_dir=raw_data_dir,
        processed_data_dir=processed_data_dir,
        log_dir=log_dir,
        batch_size=batch_size,
    )
