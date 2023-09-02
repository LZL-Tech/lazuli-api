CREATE DATABASE lazuli;
USE lazuli;

CREATE TABLE compra (
    id_compra INT AUTO_INCREMENT NOT NULL,
    fornecedor VARCHAR(255) NULL,
    dt_compra DATE NULL,
    PRIMARY KEY (id_compra)
);

CREATE TABLE tipo_produto (
    id_tipo_produto INT AUTO_INCREMENT NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    PRIMARY KEY (id_tipo_produto)
);

CREATE TABLE unidade_medida (
    id_unidade_medida INT AUTO_INCREMENT NOT NULL,
    descricao VARCHAR(100) NOT NULL,
    simbolo VARCHAR(10) NULL,
    PRIMARY KEY (id_unidade_medida)
);

CREATE TABLE venda (
    id_venda INT AUTO_INCREMENT NOT NULL,
    nm_cliente VARCHAR(255) NULL,
    dt_venda DATE NULL,
    PRIMARY KEY (id_venda)
);

CREATE TABLE produto (
    id_produto INT AUTO_INCREMENT NOT NULL,
    descricao VARCHAR(150) NOT NULL,
    id_tipo_produto INT NOT NULL,
    marca VARCHAR(100) NULL,
    qtd_estoque FLOAT NULL,
    id_unidade_medida INT NOT NULL,
    preco DECIMAL(10,2) NULL,
    PRIMARY KEY (id_produto),
    FOREIGN KEY (id_tipo_produto) REFERENCES tipo_produto(id_tipo_produto),
    FOREIGN KEY (id_unidade_medida) REFERENCES unidade_medida(id_unidade_medida)
);

CREATE TABLE venda_produto (
    id_venda_produto INT AUTO_INCREMENT NOT NULL,
    id_produto INT NOT NULL,
    id_venda INT NOT NULL,
    quantidade FLOAT NULL,
    preco_unidade DECIMAL(10,2) NOT NULL,
    PRIMARY KEY (id_venda_produto),
    FOREIGN KEY (id_venda) REFERENCES venda(id_venda),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto)
);

CREATE TABLE compra_produto (
    id_compra_produto INT AUTO_INCREMENT NOT NULL,
    id_compra INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade FLOAT NULL,
    vl_unidade DECIMAL(10,2) NULL,
    vl_total DECIMAL(10,2) NULL,
    PRIMARY KEY (id_compra_produto),
    UNIQUE KEY (id_compra, id_produto),
    FOREIGN KEY (id_produto) REFERENCES produto(id_produto),
    FOREIGN KEY (id_compra) REFERENCES compra(id_compra)
);