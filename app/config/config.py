#from config.env import sgbd, server, user, password, database, port
from app import app

SECRET_KEY =  "LZLtech"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}:{porta}/{database}?charset=utf8mb4".format(
    SGBD='mysql+mysqlconnector',
    usuario='root',
    senha='123_Mudar',
    servidor='localhost',
    porta='1433',
    database='lazuli'
)

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