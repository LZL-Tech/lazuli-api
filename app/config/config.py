#from env import host, user, password, database

SECRET_KEY =  "LZLtech"

SQLALCHEMY_DATABASE_URI = "{SGBD}://{usuario}:{senha}@{servidor}/{database}?driver=ODBC+Driver+17+for+SQL+Server".format(
    SGBD = 'mssql+pyodbc',
    usuario = 'sa',
    senha = '123_Mudar',
    servidor = '127.0.0.1',
    porta = '1433',
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