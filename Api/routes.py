from flask import request, abort, jsonify, Response
from app import app
from models import Produto
from repositories import ProdutoRepository, TipoProdutoRepository

produtoRepository = ProdutoRepository()
tipoProdutoRepository = TipoProdutoRepository()

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produtoEncontrado = produtoRepository.find(id)
    if produtoEncontrado is not None:
        produto = {
            'id_produto': produtoEncontrado.id,
            'descricao': produtoEncontrado.descricao,
            'marca':produtoEncontrado.marca,
            'qtd_estoque':produtoEncontrado.qtd_estoque,
            'preco':produtoEncontrado.preco,
            'id_unidade_medida':produtoEncontrado.id_unidade_medida,
            'id_tipo_produto':produtoEncontrado.id_tipo_produto
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
    #Entrada de dados
    descricao = request.json['descricao']
    marca = request.json['marca']
    qtd_estoque = request.json['qtd_estoque']
    preco = request.json['preco']
    id_unidade_medida = request.json['id_unidade_medida']
    id_tipo_produto = request.json['id_tipo_produto']
    
    novo_produto = Produto()

    #Criando objeto
    tipoProdutoEncontrado = tipoProdutoRepository.find(id_tipo_produto)
    if tipoProdutoEncontrado is not None:
        if tipoProdutoEncontrado.descricao == 'Ingrediente':
            novo_produto.descricao = descricao    
            novo_produto.qtd_estoque = qtd_estoque      
            novo_produto.id_unidade_medida = id_unidade_medida
            novo_produto.id_tipo_produto = id_tipo_produto
            novo_produto.marca = marca
        else:
            novo_produto.descricao = descricao    
            novo_produto.qtd_estoque = qtd_estoque      
            novo_produto.id_unidade_medida = id_unidade_medida
            novo_produto.id_tipo_produto = id_tipo_produto
            novo_produto.preco = preco

    #Inserindo dado no banco de dados
    result = produtoRepository.create(novo_produto)

    #Validando se deu certo a operação
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