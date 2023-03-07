CREATE DATABASE lazuli;

USE lazuli;

-- DROP SCHEMA dbo;

CREATE SCHEMA dbo;
-- lazuli.dbo.compra definition

-- Drop table

-- DROP TABLE lazuli.dbo.compra;

CREATE TABLE lazuli.dbo.compra (
	id_compra int IDENTITY(0,1) NOT NULL,
	fornecedor varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dt_compra date NULL,
	CONSTRAINT compra_PK PRIMARY KEY (id_compra)
);


-- lazuli.dbo.tipo_produto definition

-- Drop table

-- DROP TABLE lazuli.dbo.tipo_produto;

CREATE TABLE lazuli.dbo.tipo_produto (
	id_tipo_produto int IDENTITY(0,1) NOT NULL,
	descricao varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	CONSTRAINT tipo_produto_PK PRIMARY KEY (id_tipo_produto)
);


-- lazuli.dbo.unidade_medida definition

-- Drop table

-- DROP TABLE lazuli.dbo.unidade_medida;

CREATE TABLE lazuli.dbo.unidade_medida (
	id_unidade_medida int IDENTITY(0,1) NOT NULL,
	descricao varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	simbolo varchar(10) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	CONSTRAINT unidade_medida_PK PRIMARY KEY (id_unidade_medida)
);


-- lazuli.dbo.venda definition

-- Drop table

-- DROP TABLE lazuli.dbo.venda;

CREATE TABLE lazuli.dbo.venda (
	id_venda int IDENTITY(0,1) NOT NULL,
	nm_cliente varchar(255) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	dt_venda date NULL,
	CONSTRAINT venda_PK PRIMARY KEY (id_venda)
);


-- lazuli.dbo.produto definition

-- Drop table

-- DROP TABLE lazuli.dbo.produto;

CREATE TABLE lazuli.dbo.produto (
	id_produto int IDENTITY(1,1) NOT NULL,
	descricao varchar(150) COLLATE SQL_Latin1_General_CP1_CI_AS NOT NULL,
	id_tipo_produto int NOT NULL,
	marca varchar(100) COLLATE SQL_Latin1_General_CP1_CI_AS NULL,
	qtd_estoque float NULL,
	id_unidade_medida int NOT NULL,
	preco decimal(38,0) NULL,
	CONSTRAINT produto_PK PRIMARY KEY (id_produto),
	CONSTRAINT produto_FK FOREIGN KEY (id_tipo_produto) REFERENCES lazuli.dbo.tipo_produto(id_tipo_produto),
	CONSTRAINT produto_FK_1 FOREIGN KEY (id_unidade_medida) REFERENCES lazuli.dbo.unidade_medida(id_unidade_medida)
);


-- lazuli.dbo.venda_produto definition

-- Drop table

-- DROP TABLE lazuli.dbo.venda_produto;

CREATE TABLE lazuli.dbo.venda_produto (
	id_venda_produto int IDENTITY(0,1) NOT NULL,
	id_produto int NOT NULL,
	id_venda int NOT NULL,
	quantidade float NULL,
	preco_unidade decimal(38,0) NOT NULL,
	CONSTRAINT venda_produto_PK PRIMARY KEY (id_venda_produto),
	CONSTRAINT venda_produto_FK FOREIGN KEY (id_venda) REFERENCES lazuli.dbo.venda(id_venda),
	CONSTRAINT venda_produto_FK_1 FOREIGN KEY (id_produto) REFERENCES lazuli.dbo.produto(id_produto)
);


-- lazuli.dbo.compra_produto definition

-- Drop table

-- DROP TABLE lazuli.dbo.compra_produto;

CREATE TABLE lazuli.dbo.compra_produto (
	id_compra_produto int IDENTITY(0,1) NOT NULL,
	id_compra int NOT NULL,
	id_produto int NOT NULL,
	quantidade float NULL,
	vl_unidade decimal(38,0) NULL,
	vl_total decimal(38,0) NULL,
	CONSTRAINT compra_produto_PK PRIMARY KEY (id_compra_produto),
	CONSTRAINT compra_produto_UN UNIQUE (id_compra,id_produto),
	CONSTRAINT compra_produto_FK FOREIGN KEY (id_produto) REFERENCES lazuli.dbo.produto(id_produto),
	CONSTRAINT compra_produto_FK_2 FOREIGN KEY (id_compra) REFERENCES lazuli.dbo.compra(id_compra)
);


