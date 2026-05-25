from __future__ import annotations

from pathlib import Path
from typing import Dict

import pandas as pd

from utils import setup_logger


def extract_csv_files(raw_data_dir: Path, logger=None) -> Dict[str, pd.DataFrame]:
    logger = logger or setup_logger("extract", raw_data_dir.parent.parent / "logs")
    extracted_frames: Dict[str, pd.DataFrame] = {}

    csv_files = sorted(raw_data_dir.glob("*.csv"))
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {raw_data_dir}")

    for file_path in csv_files:
        try:
            frame = pd.read_csv(file_path)
            extracted_frames[file_path.stem.lower()] = frame
            logger.info("Loaded %s with %s rows", file_path.name, len(frame))
        except Exception as exc:
            logger.exception("Failed to extract %s: %s", file_path.name, exc)
            raise

    return extracted_frames
