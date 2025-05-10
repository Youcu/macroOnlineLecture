# Path: config/env_loader.py
from dotenv import load_dotenv
import os

def load_credentials():
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
    ENV_PATH = os.path.join(BASE_DIR, "src", "loginInfo.env")
    load_dotenv(ENV_PATH)
    ID = os.getenv("ID")
    PW = os.getenv("PW")
    return ID, PW