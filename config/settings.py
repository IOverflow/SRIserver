# Define constants to configure the app

## DATABASE SPECIFIC CONFIG
import os
from pathlib import Path

path = Path(os.getcwd())
db_path = path.parent.absolute()

DATABASE_URL = f'sqlite:///{db_path}/db.sqlite3'
DATABASE_ECHO = True
DATABASE_FUTURE = True
DATABASE_AUTOCOMMIT = False
DATABASE_AUTOFLUSH = False

HOST_IP = "0.0.0.0"
HOST_PORT = 8000

# Configure CORS Middleware
ALLOWED_ORIGINS=[
    "http://localhost:3000",
    "http://localhost:8080",
]

USE_DATABASE_BACKEND = False