#from env import host, user, password, database
from app import app

SECRET_KEY =  "LZLtech"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}?driver=ODBC+Driver+17+for+SQL+Server".format(
    SGBD = 'mssql+pyodbc',
    usuario = 'SA',
    senha = 'Numsey#2022',
    servidor = 'localhost,1450',
    database = 'LZLtech'
)

"""
#Docker config

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}?driver=ODBC+Driver+17+for+SQL+Server".format(
    SGBD = 'mssql+pyodbc',
    usuario = user,
    senha = password,
    servidor = host,
    database = database
)
"""