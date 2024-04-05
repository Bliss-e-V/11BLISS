import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

MAPS_API_KEY = os.getenv("MAPS_API_KEY")
