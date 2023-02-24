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
    { 'descricao': 'Descrição 1', 'quantidade': 10},
    { 'descricao': 'Descrição 2', 'quantidade': 50},
    { 'descricao': 'Descrição 3', 'quantidade': 5},
    { 'descricao': 'Descrição 4', 'quantidade': 20}
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
    print("+------+---------------------+--------------------+")
    print(f"| {'ID': <5}| {'Descrição': <20}| {'Quantidade': <19}|")
    print("|------+---------------------+--------------------|")
    for item in data:
        print(f"| {item['id']: <5}| {item['descricao']: <20}| {item['quantidade']: <19}|")
        print("|------+---------------------+--------------------|")
else:
    print('Erro ao recuperar a lista de itens')

print('')
print("SELECT ID")

response = requests.get(URL_BASE + endpoint + "/2")

if response.status_code == 200:
    data = response.json()
    print("+------+---------------------+--------------------+")
    print(f"| {'ID': <5}| {'Descrição': <20}| {'Quantidade': <19}|")
    print("|------+---------------------+--------------------|")
    print(f"| {item['id']: <5}| {item['descricao']: <20}| {item['quantidade']: <19}|")
    print("|------+---------------------+--------------------|")
else:
    print('Erro ao recuperar a lista de itens')


print("UPDATE")
data = { 
    'descricao': 'Descrição Update', 
    'quantidade': 999
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

