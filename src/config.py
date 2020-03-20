import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(BASE_DIR, "..")

DB_URL = os.getenv("DB_URL", f"sqlite:///{DB_DIR}/database.db")
GITHUB_API_URL = "https://api.github.com/repositories?since={since}"
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")