from typing import List
from domain.models import Produto, UnidadeMedida, TipoProduto
from flask import Response, abort, jsonify, request, url_for
from flask_cors import cross_origin
from repository.repositories import *
from itertools import groupby


from app import app

produto_repository = ProdutoRepository()
tipo_produto_repository = TipoProdutoRepository()
unidade_medida_repository = UnidadeMedidaRepository()
compra_repository = CompraRepository()
compra_produto_repository = CompraProdutoRepository()
venda_repository = VendaRepository()
venda_produto_repository = VendaProdutoRepository()

@app.route('/')
@app.route('/home')
def index():
    return "Hello, World!"

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

@app.route('/tipo_produto', methods=['GET'])
def get_tipo_produtos():
    tipo_produtos = tipo_produto_repository.findAll()
    serializados = []

    if len(tipo_produtos) > 0:
        for tipo_produto in tipo_produtos:
            tipo_produto_serializado = {
                'id_tipo_produto': tipo_produto.id,
                'descricao': tipo_produto.descricao
            }
            serializados.append(tipo_produto_serializado)

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/unidade_medida', methods=['GET'])
def get_unidades_medidas():
    unidades_medida: List[UnidadeMedida] = unidade_medida_repository.findAll()
    response = []
    for unidade_medida in unidades_medida:
        response.append({
            'id_unidade_medida': unidade_medida.id,
            'descricao': unidade_medida.descricao,
            'simbolo': unidade_medida.simbolo
        })
    return jsonify(response)

@app.route('/compra/<int:id>', methods=['GET'])
def get_compra(id):
    compraEncontrado: Compra = compra_repository.find(id)
    result = []
    for key, group in groupby(compraEncontrado, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%Y-%m-%d'),
            "produto": []
        }
        for item in group:
            compra["produto"].append({
                "id_produto": item[2].id,
                "descricao": item[2].descricao,
                "quantidade": float(item[1].quantidade),
                "vl_unidade": float(item[1].vl_unidade),
                "vl_total": float(item[1].vl_total)
            })
        result.append(compra)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/compra', methods=['GET'])
def get_compras():
    compras = compra_repository.findAll()
    result = []
    for key, group in groupby(compras, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%Y-%m-%d'),
            "produto": []
        }
        for item in group:
            compra["produto"].append({
                "id_produto": item[2].id,
                "descricao": item[2].descricao,
                "quantidade": float(item[1].quantidade),
                "vl_unidade": float(item[1].vl_unidade),
                "vl_total": float(item[1].vl_total)
            })
        result.append(compra)
    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/compra', methods=['POST'])
def add_compra():
    fornecedor = request.json.get('fornecedor')
    dt_compra = request.json.get('dt_compra')
    compra_produto = request.json.get('compra_produto')

    if not fornecedor or not dt_compra or not compra_produto:
        abort(400, message="'Dados incompletos.")

    nova_compra = Compra()
    nova_compra.fornecedor = fornecedor
    nova_compra.dt_compra = dt_compra

    result_compra: Compra = compra_repository.create(nova_compra)

    if result_compra is None:
        abort(400, 'Error ao cadastrar compra')

    for item in compra_produto:
        id_produto = item['produto']['id_produto']
        descricao = item['produto']['descricao']

        quantidade = item['quantidade']
        vl_unidade = item['vl_unidade']
        vl_total = item['vl_total']

        if not quantidade:
            abort(400, message="O campo 'quantidade' é obrigatório.")

        if vl_total is not None and vl_unidade is None:
            vl_unidade = vl_total / quantidade

        if vl_unidade is not None and vl_total is None:
            vl_total = vl_unidade * quantidade

        nova_compra_produto = CompraProduto()
        nova_compra_produto.id_compra = result_compra.id
        nova_compra_produto.id_produto = id_produto
        nova_compra_produto.quantidade = quantidade
        nova_compra_produto.vl_unidade = vl_unidade
        nova_compra_produto.vl_total = vl_total

        result:CompraProduto = compra_produto_repository.create(nova_compra_produto)

        #Validando se deu certo a operação
        if result is None:
            abort(400, 'Error ao cadastrar compra x produto')

    response = jsonify(None)
    response.status_code = 201
    response.headers['Location'] = url_for('get_compra', id=result_compra.id)
    return response

@app.route('/compra/<int:id>', methods=['PUT'])
def update_compra(id):
    compra_encontrado: Compra = compra_repository.find(id)

    if compra_encontrado is None:
         abort(404, message="'Not Found")

    fornecedor = request.json.get('fornecedor')
    dt_compra = request.json.get('dt_compra')
    compra_produto = request.json.get('compra_produto')

    if not fornecedor or not dt_compra or not compra_produto:
            abort(400, message="'Dados incompletos.")

    compra_encontrado.fornecedor = fornecedor
    compra_encontrado.dt_compra = dt_compra

    result = compra_repository.update(id, compra_encontrado)

    if result == True:
        for item in compra_produto:
            id_produto = item['produto']['id_produto']
            descricao = item['produto']['descricao']

            quantidade = item['quantidade']
            vl_unidade = item['vl_unidade']
            vl_total = item['vl_total']

            if not quantidade:
                abort(400, message="O campo 'quantidade' é obrigatório.")

            if vl_total is not None and vl_unidade is None:
                vl_unidade = vl_total / quantidade

            if vl_unidade is not None and vl_total is None:
                vl_total = vl_unidade * quantidade

            nova_compra_produto = CompraProduto()
            nova_compra_produto.id_compra = id
            nova_compra_produto.id_produto = id_produto
            nova_compra_produto.quantidade = quantidade
            nova_compra_produto.vl_unidade = vl_unidade
            nova_compra_produto.vl_total = vl_total

            result:CompraProduto = compra_produto_repository.create(nova_compra_produto)

            #Validando se deu certo a operação
            if result is None:
                abort(400, 'Error ao cadastrar compra x produto')
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/compra/<int:id>', methods=['DELETE'])
def delete_compra(id):
    result = compra_repository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/compra/produto/<int:id>', methods=['GET'])
def searchCompraProductId(id):
    compras = compra_repository.searchCompraProductId(id)
    result = []
    for key, group in groupby(compras, lambda x: x[0]):
        compra = {
            "id_compra": key.id,
            "fornecedor": key.fornecedor,
            "dt_compra": key.dt_compra.strftime('%Y-%m-%d'),
            "produto": []
        }
        for item in group:
            compra["produto"].append({
                "id_produto": item[2].id,
                "descricao": item[2].descricao,
                "quantidade": float(item[1].quantidade),
                "vl_unidade": float(item[1].vl_unidade),
                "vl_total": float(item[1].vl_total)
            })
        result.append(compra)

    response = jsonify(result)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/venda/<int:id>', methods=['GET'])
def get_venda(id):
    vendaEncontrado: Venda = venda_repository.find(id)
    if vendaEncontrado is not None:
        venda_serializado = {
            'id_venda': vendaEncontrado.id,
            'nm_cliente': vendaEncontrado.nm_cliente,
            'dt_venda': vendaEncontrado.dt_venda.strftime('%Y-%m-%d'),
            "venda_produto": []
        }
        for vendaProdutos in vendaEncontrado.vendaProdutos:
            venda_serializado["venda_produto"].append({
                "id_venda_produto": vendaProdutos.id,
                "id_produto": vendaProdutos.id_produto,
                "id_venda": vendaProdutos.id_venda,
                "preco_unidade": float(vendaProdutos.preco_unidade),
                "produto": {
                    'id_produto': vendaProdutos.produto.id,
                    'descricao': vendaProdutos.produto.descricao,
                    'marca': vendaProdutos.produto.marca,
                    'qtd_estoque': vendaProdutos.produto.qtd_estoque,
                    'preco': vendaProdutos.produto.preco,
                    'id_unidade_medida': vendaProdutos.produto.id_unidade_medida,
                    'id_tipo_produto': vendaProdutos.produto.id_tipo_produto,
                    'tipo_produto': {
                        'id_tipo_produto': vendaProdutos.produto.tipo_produto.id,
                        'descricao': vendaProdutos.produto.tipo_produto.descricao
                    },
                    'unidade_medida': {
                        'id_unidade_medida': vendaProdutos.produto.unidade_medida.id,
                        'descricao': vendaProdutos.produto.unidade_medida.descricao,
                        'simbolo': vendaProdutos.produto.unidade_medida.simbolo
                    }
                }
            })

        response = jsonify(venda_serializado)
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response
    else:
       abort(400, 'Error')

@app.route('/venda', methods=['GET'])
def get_vendas():
    vendas: Venda = venda_repository.findAll()
    serializados = []

    if len(vendas) > 0:
        for venda in vendas:
            venda_serializado = {
                'id_venda': venda.id,
                'nm_cliente': venda.nm_cliente,
                'dt_venda': venda.dt_venda.strftime('%Y-%m-%d'),
                "venda_produto": []
            }
            for vendaProdutos in venda.vendaProdutos:
                venda_serializado["venda_produto"].append({
                    "id_venda_produto": vendaProdutos.id,
                    "id_produto": vendaProdutos.id_produto,
                    "id_venda": vendaProdutos.id_venda,
                    "preco_unidade": float(vendaProdutos.preco_unidade),
                    "quantidade": vendaProdutos.quantidade,
                    "produto": {
                        'id_produto': vendaProdutos.produto.id,
                        'descricao': vendaProdutos.produto.descricao,
                        'marca': vendaProdutos.produto.marca,
                        'qtd_estoque': vendaProdutos.produto.qtd_estoque,
                        'preco': vendaProdutos.produto.preco,
                        'id_unidade_medida': vendaProdutos.produto.id_unidade_medida,
                        'id_tipo_produto': vendaProdutos.produto.id_tipo_produto,
                        'tipo_produto': {
                            'id_tipo_produto': vendaProdutos.produto.tipo_produto.id,
                            'descricao': vendaProdutos.produto.tipo_produto.descricao
                        },
                        'unidade_medida': {
                            'id_unidade_medida': vendaProdutos.produto.unidade_medida.id,
                            'descricao': vendaProdutos.produto.unidade_medida.descricao,
                            'simbolo': vendaProdutos.produto.unidade_medida.simbolo
                        }
                    }
                })
            serializados.append(venda_serializado)

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/venda', methods=['POST'])
def add_venda():
    nm_cliente: str = request.json.get('nm_cliente')
    dt_venda: datetime = request.json.get('dt_venda')
    venda_produto = request.json.get('venda_produto')

    nova_venda = Venda()
    nova_venda.nm_cliente = nm_cliente
    nova_venda.dt_venda = dt_venda

    result_venda: Venda = venda_repository.create(nova_venda)

    if result_venda is None:
        abort(400, 'Error ao cadastrar venda')

    for item in venda_produto:
        id_produto = item['id_produto']
        quantidade = item['quantidade']
        preco_unidade = item['preco_unidade']

        nova_venda_produto = VendaProduto()
        nova_venda_produto.id_venda = result_venda.id
        nova_venda_produto.id_produto = id_produto
        nova_venda_produto.quantidade = quantidade
        nova_venda_produto.preco_unidade = preco_unidade

        result: VendaProduto = venda_produto_repository.create(nova_venda_produto)

        #Validando se deu certo a operação
        if result is None:
            abort(400, 'Error ao cadastrar venda x produto')

    response = jsonify(None)
    response.status_code = 201
    response.headers['Location'] = url_for('get_venda', id=result_venda.id)
    return response

@app.route('/venda/<int:id>', methods=['PUT'])
def update_venda(id):
    venda_encontrado: Venda = venda_repository.find(id)

    if venda_encontrado is None:
         abort(404, message="'Not Found")

    nm_cliente: str = request.json.get('nm_cliente')
    dt_venda: datetime = request.json.get('dt_venda')
    venda_produto: VendaProduto = request.json.get('venda_produto')

    venda_encontrado.nm_cliente = nm_cliente
    venda_encontrado.dt_venda = dt_venda

    result = venda_repository.update(id, venda_encontrado)

    venda_produto_encontrado: VendaProduto = venda_produto_repository.findByVendaId(id)

    if result == True:

        itens_para_remover = [item for item in venda_produto_encontrado if item not in venda_produto]
        for item in itens_para_remover:
           venda_produto_repository.destroy(item.id)

        for item in venda_produto:
            vpe_item = next((item2 for item2 in venda_produto_encontrado if item['id_produto'] == item2.id_produto
            and item['quantidade'] == item2.quantidade and item['preco_unidade'] == item2.preco_unidade), None)
            if vpe_item:
                vpe_item.id_produto = item['id_produto']
                vpe_item.quantidade =  item['quantidade']
                vpe_item.preco_unidade = item['preco_unidade']

                result = venda_produto_repository.update(vpe_item.id, vpe_item)
            else:
                nova_venda_produto = VendaProduto()
                nova_venda_produto.id_venda = id
                nova_venda_produto.id_produto = item['id_produto']
                nova_venda_produto.quantidade = item['quantidade']
                nova_venda_produto.preco_unidade = item['preco_unidade']

                result_venda_produto: VendaProduto = venda_produto_repository.create(nova_venda_produto)

        return Response(status=204)
    else:
        abort(400, 'Error ao atualizar venda x produto')

@app.route('/venda/<int:id>', methods=['DELETE'])
def delete_venda(id):
    result = venda_repository.destroy(id)
    if result == True:
        return Response(status=204)
    else:
        abort(400, 'Error')

@app.route('/venda/produto/<int:id>', methods=['GET'])
def searchVendaProductId(id):
    vendas = venda_repository.searchVendaProductId(id)
    serializados = []

    if len(vendas) > 0:
        for key, group in groupby(vendas, lambda x: x[0]):
            venda_serializado = {
                'id_venda': key.id,
                'nm_cliente': key.nm_cliente,
                'dt_venda': key.dt_venda.strftime('%Y-%m-%d'),
                "venda_produto": []
            }
            for item in group: #venda.vendaProdutos:
                venda_serializado["venda_produto"].append({
                    "id_venda_produto": item[1].id,
                    "id_produto": item[1].id_produto,
                    "id_venda": item[1].id_venda,
                    "preco_unidade": float(item[1].preco_unidade),
                    "quantidade": item[1].quantidade,
                    "produto": {
                        'id_produto': item[2].id,
                        'descricao': item[2].descricao,
                        'marca': item[2].marca,
                        'qtd_estoque': item[2].qtd_estoque,
                        'preco': item[2].preco,
                        'id_unidade_medida': item[2].id_unidade_medida,
                        'id_tipo_produto': item[2].id_tipo_produto,
                        'tipo_produto': {
                            'id_tipo_produto': item[2].tipo_produto.id,
                            'descricao': item[2].tipo_produto.descricao
                        },
                        'unidade_medida': {
                            'id_unidade_medida':item[2].unidade_medida.id,
                            'descricao': item[2].unidade_medida.descricao,
                            'simbolo': item[2].unidade_medida.simbolo
                        }
                    }
                })
            serializados.append(venda_serializado)

    response = jsonify(serializados)
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response