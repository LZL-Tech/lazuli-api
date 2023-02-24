import os
from abc import ABC, abstractmethod
from flask import Flask, request, abort, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

host=os.getenv('DB_HOST')
user=os.getenv('DB_USER')
password=os.getenv('DB_PASSWORD')
database=os.getenv('DB_NAME')

app = Flask(__name__)
app.secret_key = "LZLtech"

app.config['SQLALCHEMY_DATABASE_URI'] = "{SGBD}://{usuario}:{senha}@{servidor}/{database}?driver=ODBC+Driver+17+for+SQL+Server".format(
    SGBD = 'mssql+pyodbc',
    usuario = 'SA',
    senha = 'Numsey#2022',
    servidor = 'localhost,1450',
    database = 'LZLtech'
)

"""
Docker config

app.config['SQLALCHEMY_DATABASE_URI'] = "{SGBD}://{usuario}:{senha}@{servidor}/{database}?driver=ODBC+Driver+17+for+SQL+Server".format(
    SGBD = 'mssql+pyodbc',
    usuario = user,
    senha = password,
    servidor = host,
    database = database
)
"""
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

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
        item = self.classe.query.get(id)            
        return item         

    def findAll(self):
        list = self.classe.query.order_by(self.classe.id)
        return list

    def create(self, obj):
        try:
            db.session.add(obj) 
            db.session.commit()
            return True
        except:
            db.session.rollback()
            return False

    def update(self, id, obj):
        item = self.find(id)  
        if item is not None:
            for key, value in obj.__dict__.items():
                if key != '_sa_instance_state':
                    setattr(item, key, value)
            db.session.commit()
            return True
        return False

    def destroy(self, id):
        item = self.find(id) 
        if item is not None:        
            try:
                db.session.delete(item)
                db.session.commit()
                return True
            except:
                return False
        return False

class Produto(db.Model):
    __tablename__ = 'Produtos'
    id = db.Column('Id', db.Integer, primary_key=True, autoincrement=True)
    descricao = db.Column('Descricao', db.String(255), nullable=False)
    quantidade = db.Column('Quantidade', db.Integer, nullable=False)

    def __init__(self, descricao, quantidade):
        self.descricao = descricao
        self.quantidade = quantidade

    def __repr__(self):
        return '<Descricao %r>' % self.descricao
    
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
    result = produtoRepository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)