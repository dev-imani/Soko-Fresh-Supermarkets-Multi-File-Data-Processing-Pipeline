import csv
import argparse
from pathlib import Path


def discover_files(folder: Path, pattern: str = "transactions_*.csv") -> list:
    """Return matching files sorted by name/date."""
    return sorted(folder.glob(pattern))


# Pass the current working directory as the required folder argument
current_directory = Path(".")
y = discover_files(current_directory)
print(y)
