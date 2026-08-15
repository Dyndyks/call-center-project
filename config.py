import os
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
PORT = int(os.environ.get("PORT"))