#from env import host, user, password, database
from app import app

SECRET_KEY =  "LZLtech"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}?driver=ODBC+Driver+17+for+SQL+Server".format(
    SGBD = 'mssql+pyodbc',
    usuario = 'SA',
    senha = '123_Mudar',
    servidor = 'localhost,1433',
    database = 'lazuli'
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