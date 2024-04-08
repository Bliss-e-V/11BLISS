import os
from pathlib import Path

from dotenv import load_dotenv

dotenv_path = Path(".env")
load_dotenv(dotenv_path=dotenv_path)

GMAPS_API_KEY = os.getenv("GMAPS_API_KEY")
GMAPS_CHUNK_SIZE = os.getenv("GMAPS_CHUNK_SIZE")
