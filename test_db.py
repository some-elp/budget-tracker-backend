from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

database_url = os.getenv("DATABASE_URL")
engine = create_engine(database_url)

with engine.connect() as conn:
    print("Connected successfully!")