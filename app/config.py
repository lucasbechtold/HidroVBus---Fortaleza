import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-dev-key-hidrovbus")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///hidrovbus.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GEOCODING_API_URL = os.getenv("GEOCODING_API_URL", "https://nominatim.openstreetmap.org")
    TRANSPORT_DATA_ZIP = os.path.join(os.path.dirname(__file__), "..", os.getenv("TRANSPORT_DATA_ZIP", "data/arquivos_google.zip"))
    DEMO_MODE = os.getenv("DEMO_MODE", "true").lower() == "true"