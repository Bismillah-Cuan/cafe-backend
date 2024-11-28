from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

db_username = os.getenv("DB_USERNAME")
db_password = os.getenv("DB_PASSWORD")
db_server = os.getenv("DB_SERVER")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")

print("connecting to db...")
engine = create_engine(f"postgresql+psycopg2://{db_username}:{db_password}@{db_server}:{db_port}/{db_name}")

connection = engine.connect()
print("connected to db")

Session = sessionmaker(connection)