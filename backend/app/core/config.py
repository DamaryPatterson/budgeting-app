from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[3]
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "budget_data.json"
FRONTEND_DIR = BASE_DIR / "frontend" / "static"
