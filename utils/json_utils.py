import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent
TESTDATA_DIR = PROJECT_ROOT / "testdata"


def load_json_data(filename: str) -> Any:
    """Loads a JSON file from testdata/, independent of the current working directory."""
    file_path = TESTDATA_DIR / filename
    with file_path.open("r", encoding="utf-8") as file:
        return json.load(file)
