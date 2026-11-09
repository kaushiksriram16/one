"""Load the immutable source ledger at application startup."""
import json
from pathlib import Path

LEDGER_PATH = Path(__file__).resolve().parents[2] / "ledger.json"


def load_ledger(path: Path = LEDGER_PATH) -> dict:
    with path.open(encoding="utf-8") as handle:
        return json.load(handle)
