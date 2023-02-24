import sqlalchemy
from abc import ABC, abstractmethod
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import QueuePool
from threading import local
from flask import Flask, request, jsonify, send_from_directory, url_for, Response

app = Flask(__name__)

# Criar conexão com o SQL Server usando autenticação SQL Server
engine = sqlalchemy.create_engine(
    "mssql+pyodbc://SA:Numsey#2022@localhost,1450/LZLtech?driver=ODBC+Driver+17+for+SQL+Server"
)
connection = engine.connect()

# Criar sessão com o Banco de Dados
Base = declarative_base(engine)
session_factory = sessionmaker(bind=engine)
Session = scoped_session(session_factory)

# criar um objeto de thread local para armazenar a sessão
local_session = local()

# criar uma função para retornar a sessão da thread atual
def get_session():
    if not hasattr(local_session, 'session'):
        local_session.session = Session()
    return local_session.session

class IRepository(ABC):
    @abstractmethod
    def find(self, id):
        pass
    @abstractmethod
    def findAll(self):
        pass
    @abstractmethod
    def create(self, obj):
        pass
    @abstractmethod
    def update(self, id, obj):
        pass
    @abstractmethod
    def destroy(self, id):
        pass

class RepositoryBase(IRepository):
    def __init__(self, classe):
        self.classe = classe

    def find(self, id):
        item = get_session().query(self.classe).get(id)            
        return item         

    def findAll(self):
        list = get_session().query(self.classe)  
        return list

    def create(self, obj):
        try:
            get_session().add(obj) 
            get_session().commit()
            return True
        except:
            get_session().rollback()
            return False

    def update(self, id, obj):
        item = get_session().query(self.classe).get(id)  
        if item is not None:
            for key, value in obj.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(item, key, value)
            get_session().commit()
            return True
        return False

    def destroy(self, id):
        item = get_session().query(self.classe).get(id)
        if item is not None:        
            try:
                get_session().delete(item)
                get_session().commit()
                return True
            except:
                return False
        return False

class Produto(Base):
    __tablename__ = 'Produtos'
    id = Column('Id', Integer, primary_key=True, autoincrement=True)
    descricao = Column('Descricao', String(255), nullable=False)
    quantidade = Column('Quantidade', Integer, nullable=False)

    def __init__(self, descricao, quantidade):
        self.descricao = descricao
        self.quantidade = quantidade

class ProdutoRepository(RepositoryBase):
    def __init__(self):
        super().__init__(Produto)

produtoRepository = ProdutoRepository()

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produtoEncontrado = produtoRepository.find(id)
    if produtoEncontrado is not None:
        produto = {
            'id': produtoEncontrado.id,
            'descricao': produtoEncontrado.descricao,
            'quantidade':produtoEncontrado.quantidade
        }
        return jsonify(produto)
    else:
        abort(400, 'Error')


@app.route('/produto', methods=['GET'])
def get_products():  
    produtos = produtoRepository.findAll()
    lista_produtos = [{'id': produto.id, 'descricao': produto.descricao, 'quantidade': produto.quantidade} for produto in produtos]
    return jsonify(lista_produtos)

@app.route('/produto', methods=['POST'])
def add_product():
    descricao = request.json['descricao']
    quantidade = request.json['quantidade']
    novo_produto = Produto(descricao, quantidade)
    result = produtoRepository.create(novo_produto)
    if result == True:
        return Response(status=201)
    else:
        abort(400, 'Error')


@app.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    produtoEncontrado = produtoRepository.find(id)

    descricao = request.json['descricao']
    quantidade = request.json['quantidade']

    produtoEncontrado.descricao = descricao
    produtoEncontrado.quantidade = quantidade

    result = produtoRepository.update(id, produtoEncontrado)

    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    result = produtoEncontrado = produtoRepository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)