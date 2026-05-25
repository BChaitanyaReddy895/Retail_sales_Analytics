from __future__ import annotations

import logging
import re
from pathlib import Path
from typing import Iterable

import pandas as pd


def ensure_directory(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def setup_logger(name: str, log_dir: Path) -> logging.Logger:
    ensure_directory(log_dir)
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_dir / "pipeline.log", encoding="utf-8")
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger


def normalize_column_name(column: str) -> str:
    column = column.strip().lower()
    column = re.sub(r"[^a-z0-9]+", "_", column)
    return re.sub(r"_+", "_", column).strip("_")


def normalize_dataframe_columns(frame: pd.DataFrame) -> pd.DataFrame:
    renamed = {column: normalize_column_name(column) for column in frame.columns}
    return frame.rename(columns=renamed)


def standardize_string_series(series: pd.Series) -> pd.Series:
    return series.astype("string").str.strip().replace({"": pd.NA})


def coerce_numeric(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    for column in columns:
        if column in frame.columns:
            frame[column] = pd.to_numeric(frame[column], errors="coerce")
    return frame


def coerce_datetime(frame: pd.DataFrame, columns: Iterable[str]) -> pd.DataFrame:
    for column in columns:
        if column in frame.columns:
            frame[column] = pd.to_datetime(frame[column], errors="coerce", utc=False)
    return frame


def fill_text(frame: pd.DataFrame, columns: Iterable[str], value: str = "unknown") -> pd.DataFrame:
    for column in columns:
        if column in frame.columns:
            frame[column] = frame[column].fillna(value)
    return frame


def fill_numeric(frame: pd.DataFrame, columns: Iterable[str], value: float = 0.0) -> pd.DataFrame:
    for column in columns:
        if column in frame.columns:
            frame[column] = frame[column].fillna(value)
    return frame


def write_dataframe(frame: pd.DataFrame, output_path: Path) -> None:
    ensure_directory(output_path.parent)
    frame.to_csv(output_path, index=False)
