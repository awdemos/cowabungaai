import os
from pathlib import Path

TXT_FILE_NAME = "test_with_data.txt"
PPTX_FILE_NAME = "test.pptx"
WAV_FILE_NAME = "0min12sec.wav"
XLSX_FILE_NAME = "test.xlsx"


def data_path(filename: str | None = None) -> Path:
    """Return the path to a file in the test data directory."""
    path = Path(os.path.dirname(__file__)) / ".." / "data" / filename
    if not path.exists():
        raise FileNotFoundError(f"File not found in data directory: {path}")
    return path
