"""

1. Abrir o docker
2. Baixar Imagem/Criar container
     docker run -e "ACCEPT_EULA=Y" -e "SA_PASSWORD=Numsey#2022" -p 1450:1433 --name sqlserverdb -d mcr.microsoft.com/mssql/server:2019-latest
3. Criar banco e tabelas no sql server
4. Executar o script da api
5. Executar esse script

"""

import requests

URL_BASE = "http://localhost:5000/"


endpoint = "produto"

print("INSERT")
lista_add_produtos = [
    {
      'descricao': 'Pão de Mel',
      'id_tipo_produto': 1,
      'marca': 'Confeitaria Delícia',
      'qtd_estoque': 20,
      'id_unidade_medida' : 1,
      'preco': 4.50
    },
    {
      'descricao': 'Brigadeiro',
      'id_tipo_produto': 2,
      'marca': 'Confeitaria Doce Sabor',
      'qtd_estoque': 100,
      'id_unidade_medida' : 2,
      'preco': 3.50
    },
    {
      'descricao': 'Torta de Morango',
      'id_tipo_produto': 1,
      'marca': 'Confeitaria Saborosa',
      'qtd_estoque': 5,
      'id_unidade_medida' : 1,
      'preco': 35.00
    },
    {
      'descricao': 'Bolo de chocolate',
      'id_tipo_produto': 1,
      'marca': 'Confeitaria Delícia',
      'qtd_estoque': 10,
      'id_unidade_medida' : 1,
      'preco': 50.00
    }
]

for data in lista_add_produtos:
    response = requests.post(URL_BASE + endpoint, json=data)

    if response.status_code == 201:
        print('Item criado com sucesso')
    else:
        print('Erro ao criar o item')

print("SELECT ALL")
response = requests.get(URL_BASE + endpoint,)

if response.status_code == 200:
    data = response.json()
    print(f"+{'-'*6}+{'-'*25}+{'-'*22}+{'-'*12}+{'-'*13}+{'-'*13}+{'-'*11}+")
    print(f"| {'ID': <5}| {'Descrição': <24}| {'Marca': <21}| {'Qtd Estoque': <10}| {'Unidade': <12}| {'Tipo Produto': <12}| {'Preço': <10}|")
    print(f"+{'-'*6}+{'-'*25}+{'-'*22}+{'-'*12}+{'-'*13}+{'-'*13}+{'-'*11}+")
    for item in data:
        id_produto = item['id_produto']
        id_produto = 'NULL' if id_produto is None else str(id_produto)
        descricao = item['descricao']
        descricao = 'NULL' if descricao is None else str(descricao)
        marca = item['marca']
        marca = 'NULL' if marca is None else str(marca)
        qtd_estoque = item['qtd_estoque']
        qtd_estoque = 'NULL' if qtd_estoque is None else str(qtd_estoque)
        preco = item['preco']
        preco = 'NULL' if preco is None else str(preco)
        unidade_medida = item['unidade_medida']['descricao']
        unidade_medida = 'NULL' if unidade_medida is None else str(unidade_medida)
        tipo_produto = item['tipo_produto']['descricao']
        tipo_produto = 'NULL' if tipo_produto is None else str(tipo_produto)

        print(f"| {id_produto: <5}| {descricao: <24}| {marca : <21}| {qtd_estoque: <11}| {unidade_medida: <12}| {tipo_produto: <12}| {preco: <10}|")
        print(f"+{'-'*6}+{'-'*25}+{'-'*22}+{'-'*12}+{'-'*13}+{'-'*13}+{'-'*11}+")
else:
    print('Erro ao recuperar a lista de itens')

print('')
print("SELECT ID")

response = requests.get(URL_BASE + endpoint + "/2")

if response.status_code == 200:
    data = response.json()

    id_produto = data['id_produto']
    id_produto = 'NULL' if id_produto is None else str(id_produto)
    descricao = data['descricao']
    descricao = 'NULL' if descricao is None else str(descricao)
    marca = data['marca']
    marca = 'NULL' if marca is None else str(marca)
    qtd_estoque = data['qtd_estoque']
    qtd_estoque = 'NULL' if qtd_estoque is None else str(qtd_estoque)
    preco = data['preco']
    preco = 'NULL' if preco is None else str(preco)
    id_unidade_medida = data['id_unidade_medida']
    id_unidade_medida = 'NULL' if id_unidade_medida is None else str(id_unidade_medida)
    id_tipo_produto = data['id_tipo_produto']
    id_tipo_produto = 'NULL' if id_tipo_produto is None else str(id_tipo_produto)

    print(f"+{'-'*6}+{'-'*25}+{'-'*22}+{'-'*12}+{'-'*13}+{'-'*11}+")
    print(f"| {'ID': <5}| {'Descrição': <24}| {'Marca': <21}| {'Qtd Estoque': <10}| {'Unidade': <12}| {'Preço': <10}|")
    print(f"+{'-'*6}+{'-'*25}+{'-'*22}+{'-'*12}+{'-'*13}+{'-'*11}+")
    print(f"| {id_produto: <5}| {descricao: <24}| {marca : <21}| {qtd_estoque: <11}| {id_unidade_medida: <12}| {preco: <10}|")
    print(f"+{'-'*6}+{'-'*25}+{'-'*22}+{'-'*12}+{'-'*13}+{'-'*11}+")
else:
    print('Erro ao recuperar a lista de itens')


print("UPDATE")
data = {
      'descricao': 'Update Up',
      'id_tipo_produto': 1,
      'marca': 'Confeitaria Update',
      'qtd_estoque': 5,
      'id_unidade_medida' : 1,
      'preco': 12.00
}

response = requests.put(URL_BASE + endpoint + "/2", json=data)

if response.status_code == 204:
    print('Item atualizado com sucesso')
else:
    print('Erro ao atualizar o item')

print("DELETE")
response = requests.delete(URL_BASE + endpoint + "/3")

if response.status_code == 204:
    print('Item excluído com sucesso')
else:
    print('Erro ao excluir o item')

