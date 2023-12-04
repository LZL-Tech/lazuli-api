#from config.env import sgbd, server, user, password, database, port
from app import app
import os

SECRET_KEY =  "LZLtech"


host = os.getenv('DB_HOST') if os.getenv('DB_HOST') else 'lazuli-db'
port = os.getenv('DB_PORT') if os.getenv('DB_PORT') else '1433'
user = os.getenv('DB_USER') if os.getenv('DB_USER') else 'sa'
password = os.getenv('DB_PASSWORD') if os.getenv('DB_PASSWORD') else '123_Mudar'
database = os.getenv('DB_DATABASE') if os.getenv('DB_DATABASE') else 'lazuli'

SQLALCHEMY_DATABASE_URI = f"mssql+pyodbc://{user}:{password}@{host}:{port}/{database}?driver=ODBC+Driver+17+for+SQL+Server"

"""
#Docker config

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}:{porta}/{database}?charset=utf8mb4".format(
    SGBD=sgbd,
    usuario=user,
    senha=password,
    servidor=server,
    porta=port,
    database=database
)
"""