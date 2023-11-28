INSERT INTO tipo_produto (descricao)
VALUES ('Tipo 1')
	   ,('Tipo 2')
	   ,('Tipo 3')
	   ,('Ingrediente')
       ,('Produto Final')

INSERT INTO unidade_medida (descricao, simbolo)
VALUES ('Unidade', 'UN'),
       ('Quilograma', 'kg'),
       ('Grama', 'g'),
       ('Dúzia', 'dz'),
       ('Litro', 'L');

INSERT INTO produto (descricao, id_tipo_produto, marca, qtd_estoque, id_unidade_medida, preco)
VALUES ('Bolo de Chocolate', 1, NULL, 10, 1, 45.00),
       ('Brigadeiro', 2, NULL, 100, 1, 1.50),
       ('Biscoito Amanteigado', 3, NULL, 50, 2, 8.00),
       ('Cupcake de Morango', 1, NULL, 20, 1, 3.00),
       ('Pão Francês', 2, NULL, 200, 1, 0.50);

INSERT INTO venda (nm_cliente, dt_venda)
VALUES ('Ana Santos', '2023-08-10'),
       ('Carlos Oliveira', '2023-08-15'),
       ('José Souza', '2023-09-25');

INSERT INTO compra (fornecedor, dt_compra)
VALUES ('Distribuidora de Ingredientes ABC', '2023-08-05'),
       ('Supermercado Ingredientes XYZ', '2023-08-12'),
       ('Supermercado Seu Zé', '2023-09-10');

INSERT INTO venda_produto (id_produto, id_venda, quantidade, preco_unidade)
VALUES (1, 1, 1, 45.00),
       (3, 2, 2, 8.00);

INSERT INTO compra_produto (id_compra, id_produto, quantidade, vl_unidade, vl_total)
VALUES (1, 3, 5, 2.00, 10.00),
       (2, 5, 50, 0.30, 15.00);
