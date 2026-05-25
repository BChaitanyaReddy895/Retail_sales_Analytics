# Data Notes

The repository is built to run in two modes:

1. Use the generated sample retail CSVs in `data/raw/` for local demo runs.
2. Replace the raw files with a public retail dataset, then rerun the same pipeline.

## Why synthetic data is included

The workspace does not ship with a licensed retail dataset, so the repository generates a realistic but synthetic source layer. The generator mimics the kinds of problems the ETL pipeline is supposed to solve:

- mixed date formats
- duplicate source rows
- missing customer and product fields
- uneven order sizes and discount rates
- seasonal sales patterns across the year

## Raw tables

- `regions.csv` maps region ids to business regions.
- `customers.csv` contains customer identity and segmentation data.
- `products.csv` contains product catalog details and pricing.
- `inventory.csv` tracks stock levels and reorder thresholds.
- `sales.csv` contains transactional order data used by the analytics layer.

## Swapping in another dataset

If you want to use a Kaggle or public retail dataset, keep the same table names where possible or update the column mapping in `scripts/transform.py`.
