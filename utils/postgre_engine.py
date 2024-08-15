import os

from sqlalchemy import create_engine
from dotenv import load_dotenv


def get_engine():
    load_dotenv()
    
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_database = os.getenv("DB_DATABASE")

    connection_string = f"postgresql://{db_username}:{db_password}@{db_host}:{db_port}/{db_database}"

    engine = create_engine(connection_string)
    
    return engine