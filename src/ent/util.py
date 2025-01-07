import csv
from pathlib import Path


def get_rows(csv_filepath: Path) -> list[dict]:
    with csv_filepath.open() as f:
        reader = csv.DictReader(f)
        return [row for row in reader]
