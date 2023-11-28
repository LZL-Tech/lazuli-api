import pytest
import requests

base_url = 'http://localhost:5000'

@pytest.fixture
def novo_produto():
    return {
        'descricao': 'Brigadeiro Pytest', 
        'marca': 'Confeitaria Doce Sabor',
        'qtd_estoque': 100,
        'preco': 3.50,
        'tipoProduto':   { 'id_tipo_produto': 2},
        'unidadeMedida': {'id_unidade_medida': 2}   
    }

@pytest.fixture
def atualizacao_produto():
    return {
        'descricao': 'Outro Produto', 
        'marca': 'Marca Teste',
        'qtd_estoque': 50,
        'preco': 5.0,
        'tipoProduto':   { 'id_tipo_produto': 1},
        'unidadeMedida': {'id_unidade_medida': 1}   
    }

def test_get_product_by_id():
    response = requests.get(f'{base_url}/produto/1')
    assert response.status_code == 200
    assert 'descricao' in response.json()

def test_get_all_products():
    response = requests.get(f'{base_url}/produto')
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_add_product(novo_produto):
    response = requests.post(f'{base_url}/produto', json=novo_produto)
    assert response.status_code == 201
    assert 'id_produto' in response.json()

def test_update_product(atualizacao_produto):
    response = requests.put(f'{base_url}/produto/1', json=atualizacao_produto)
    assert response.status_code == 204

def test_delete_product():
    response = requests.delete(f'{base_url}/produto/2')
    assert response.status_code == 204

def test_filter_products():
    params = {'descricao': 'Brigadeiro'}
    response = requests.get(f'{base_url}/produto/filter', params=params)
    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_get_tipo_produtos():
    response = requests.get(f'{base_url}/tipo_produto')
    assert response.status_code == 200
    assert isinstance(response.json(), list)



def test_get_unidades_medidas():
    response = requests.get(f'{base_url}/unidade_medida')
    assert response.status_code == 200
    assert isinstance(response.json(), list)



@pytest.fixture
def nova_compra():
    return {
        "fornecedor": "Mercadinho Novo",
        "dt_compra": "2023-11-04 00:00:00.000",
        "compra_produto":
        [
            {
                "produto": {
                    "id_produto": 1
                },
                "quantidade": 5.50,
                "vl_unidade": 4.50,
                "vl_total": 24.75
            },
            {
                "produto": {
                    "id_produto": 4
                },
                "quantidade": 5.50,
                "vl_unidade": 4.50,
                "vl_total": 24.75
            }
        ]
    }


@pytest.fixture
def update_compra():
    return {
        "fornecedor": "Mercadinho Update",
        "dt_compra": "2024-05-04 00:00:00.000",
        "compra_produto":
        [
            {
                "produto": {
                    "id_produto": 1
                },
                "quantidade": 5.50,
                "vl_unidade": 4.50,
                "vl_total": 24.75
            },
            {
                "produto": {
                    "id_produto": 3
                },
                "quantidade": 5.50,
                "vl_unidade": 4.50,
                "vl_total": 24.75
            }
        ]
    }


def test_get_compra():
    response = requests.get(f'{base_url}/compra/1')
    assert response.status_code == 200
    assert 'fornecedor' in response.json()

def test_get_compras():
    response = requests.get(f'{base_url}/compra')
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_add_compra(nova_compra):
    response = requests.post(f'{base_url}/compra', json=nova_compra)
    assert response.status_code == 201
    assert 'id_compra' in response.json()


def test_update_compra(update_compra):
    response = requests.put(f'{base_url}/compra/1', json=update_compra)
    assert response.status_code == 204


def test_delete_compra():
    response = requests.delete(f'{base_url}/compra/3')
    assert response.status_code == 204

def test_searchCompraProductId():
    response = requests.get(f'{base_url}/compra/produto/1')
    assert response.status_code == 200
    assert isinstance(response.json(), list)



