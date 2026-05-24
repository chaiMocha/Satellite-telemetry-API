import psycopg2
import os
from dotenv import load_dotenv


DATABASE_HOST = os.getenv("DATABASE_HOST")
DATABASE_USER = os.getenv("DATEBASE_USER")
DATABASE_PASS = os.getenv("DATABASE_PASS")
DATABASE_PORT = os.getenv("DATABASE_PORT")

try:
    conn = psycopg2.connect(
        host=DATABASE_HOST,
        database="postgres",
        user=DATABASE_USER,
        password=DATABASE_PASS,
        port=DATABASE_PORT
    )
    print("Connection successful! Your IP rule is working.")
    conn.close()
except Exception as e:
    print(f"Connection failed:\n{e}")