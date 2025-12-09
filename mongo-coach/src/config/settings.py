import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

RAW_DATA_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DATA_DIR = BASE_DIR / "data" / "processed"
CATALOG_DIR = BASE_DIR / "data" / "catalog"

MONGODB_URI = os.environ.get("MONGODB_URI")
HF_TOKEN = os.environ.get("HF_TOKEN")
