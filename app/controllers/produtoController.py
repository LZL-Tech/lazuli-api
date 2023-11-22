from app import app
from flask import Response, abort, jsonify, request, url_for

from models.produto import Produto
from repositories.produtoRepository import ProdutoRepository
from repositories.tipoProdutoRepository import TipoProdutoRepository
from repositories.compraRepository import CompraRepository
from repositories.vendaRepository import VendaRepository


produto_repository = ProdutoRepository()
tipo_produto_repository = TipoProdutoRepository()
compra_repository = CompraRepository()
venda_repository = VendaRepository()

@app.route('/produto/<int:id>', methods=['GET'])
def get_product(id):
    produtoEncontrado = produto_repository.find(id)
    if produtoEncontrado is not None:
        produto = {
            'id_produto': produtoEncontrado.id,
            'descricao': produtoEncontrado.descricao,
            'marca':produtoEncontrado.marca,
            'qtd_estoque':produtoEncontrado.qtd_estoque,
            'preco':produtoEncontrado.preco,
            'unidade_medida': {
                'id_unidade_medida':produtoEncontrado.unidade_medida.id,
                'descricao':produtoEncontrado.unidade_medida.descricao,
                'simbolo':produtoEncontrado.unidade_medida.simbolo,
            },
            'tipo_produto': {
                'id_tipo_produto':produtoEncontrado.tipo_produto.id,
                'descricao':produtoEncontrado.tipo_produto.descricao,
            }
        }

        return jsonify(produto)
    else:
       abort(400, 'Error')

@app.route('/produto', methods=['GET'])
def get_products():
    produtos = produto_repository.findAll()
    serializados = []

    if len(produtos) > 0:
        for produto in produtos:
            produto_serializado = {
                'id_produto': produto.id,
                'descricao': produto.descricao,
                'marca':produto.marca,
                'qtd_estoque':produto.qtd_estoque,
                'preco':produto.preco,
                'id_unidade_medida':produto.id_unidade_medida,
                'id_tipo_produto':produto.id_tipo_produto,
                'tipo_produto': {
                    'id_tipo_produto': produto.tipo_produto.id,
                    'descricao': produto.tipo_produto.descricao
                },
                'unidade_medida': {
                    'id_unidade_medida': produto.unidade_medida.id,
                    'descricao': produto.unidade_medida.descricao,
                    'simbolo': produto.unidade_medida.simbolo
                }
            }

            serializados.append(produto_serializado)

    return jsonify(serializados)

@app.route('/produto', methods=['POST'])
def add_product():
    #Entrada de dados request.json.get('descricao')
    descricao = request.json.get('descricao')
    marca = request.json.get('marca')
    qtd_estoque = request.json.get('qtd_estoque')
    preco = request.json.get('preco')
    unidade_medida = request.json.get('unidadeMedida')
    tipo_produto = request.json.get('tipoProduto')

    novo_produto = Produto()

    #Criando objeto
    tipoProdutoEncontrado: Produto = tipo_produto_repository.find(tipo_produto['idTipoProduto'])
    if tipoProdutoEncontrado is not None:
        if tipoProdutoEncontrado.descricao.upper() == 'INGREDIENTE':
            novo_produto.descricao = descricao
            novo_produto.qtd_estoque = qtd_estoque
            novo_produto.id_unidade_medida = unidade_medida['idUnidadeMedida']
            novo_produto.id_tipo_produto = tipo_produto['idTipoProduto']
            novo_produto.marca = marca
        else:
            novo_produto.descricao = descricao
            novo_produto.qtd_estoque = qtd_estoque
            novo_produto.id_unidade_medida = unidade_medida['idUnidadeMedida']
            novo_produto.id_tipo_produto = tipo_produto['idTipoProduto']
            novo_produto.preco = preco

    #Inserindo dado no banco de dados
    result = produto_repository.create(novo_produto)

    #Validando se deu certo a operação
    if result is not None:
        response = jsonify(None)
        response.status_code = 201
        response.headers['Location'] = url_for('get_product', id=result.id)
        return response
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['PUT'])
def update_product(id):
    produto_encontrado: Produto = produto_repository.find(id)
    descricao = request.json.get('descricao')
    marca = request.json.get('marca')
    qtd_estoque = request.json.get('qtd_estoque')
    preco = request.json.get('preco')
    unidade_medida = request.json.get('unidade_medida')
    tipo_produto = request.json.get('tipo_produto')

    tipoProdutoEncontrado: Produto = tipo_produto_repository.find(tipo_produto['id_tipo_produto'])
    if tipoProdutoEncontrado is not None:
        if tipoProdutoEncontrado.descricao.upper() == 'INGREDIENTE':
            produto_encontrado.descricao = descricao
            produto_encontrado.qtd_estoque = qtd_estoque
            produto_encontrado.id_unidade_medida = unidade_medida['id_unidade_medida']
            produto_encontrado.id_tipo_produto = tipo_produto['id_tipo_produto']
            produto_encontrado.marca = marca
            produto_encontrado.preco = None
        else:
            produto_encontrado.descricao = descricao
            produto_encontrado.qtd_estoque = qtd_estoque
            produto_encontrado.id_unidade_medida = unidade_medida['id_unidade_medida']
            produto_encontrado.id_tipo_produto = tipo_produto['id_tipo_produto']
            produto_encontrado.marca = None
            produto_encontrado.preco = preco

    result = produto_repository.update(id, produto_encontrado)

    if result == True:
        return Response(status=200)
    else:
        abort(400, 'Error')

@app.route('/produto/<int:id>', methods=['DELETE'])
def delete_product(id):
    if compra_repository.checkAssociatedProduct(id) == True:
        return jsonify({"message": "Não é possível excluir o produto, pois está associado a compra."}), 409

    if venda_repository.checkAssociatedProduct(id) == True:
        return jsonify({"message": "Não é possível excluir o produto, pois está associado a venda."}), 409

    result = produto_repository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/produto/filter', methods=['GET'])
def get_filter_produtos():
    id_tipo = request.args.get('id_tipo')
    descricao = request.args.get('descricao')
    serializados = []

    produtos = produto_repository.findAllSearch(id_tipo, descricao)
    if len(produtos) > 0:
        for produto in produtos:
            produto_serializado = {
                'id_produto': produto.id,
                'descricao': produto.descricao,
                'marca':produto.marca,
                'qtd_estoque':produto.qtd_estoque,
                'preco':produto.preco,
                'id_unidade_medida':produto.id_unidade_medida,
                'id_tipo_produto':produto.id_tipo_produto,
                'tipo_produto': {
                    'id_tipo_produto': produto.tipo_produto.id,
                    'descricao': produto.tipo_produto.descricao
                },
                'unidade_medida': {
                    'id_unidade_medida': produto.unidade_medida.id,
                    'descricao': produto.unidade_medida.descricao,
                    'simbolo': produto.unidade_medida.simbolo
                }
            }
            serializados.append(produto_serializado)

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response