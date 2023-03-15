CREATE DATABASE lazuli;
GO
USE lazuli;
GO
CREATE TABLE compra 
(
	id_compra int IDENTITY(1,1) NOT NULL
	,fornecedor varchar(255) NULL
	,dt_compra date NULL
	,CONSTRAINT compra_PK PRIMARY KEY (id_compra)
);
GO
CREATE TABLE tipo_produto 
(
	id_tipo_produto int IDENTITY(1,1) NOT NULL
	,descricao varchar(100) NOT NULL
	,CONSTRAINT tipo_produto_PK PRIMARY KEY (id_tipo_produto)
);
GO
CREATE TABLE unidade_medida 
(
	id_unidade_medida int IDENTITY(1,1) NOT NULL
	,descricao varchar(100) NOT NULL
	,simbolo varchar(10) NULL
	,CONSTRAINT unidade_medida_PK PRIMARY KEY (id_unidade_medida)
);
GO
CREATE TABLE venda 
(
	id_venda int IDENTITY(1,1) NOT NULL
	,nm_cliente varchar(255) NULL
	,dt_venda date NULL
	,CONSTRAINT venda_PK PRIMARY KEY (id_venda)
);
GO
CREATE TABLE produto 
(
	id_produto int IDENTITY(1,1) NOT NULL
	,descricao varchar(150) NOT NULL
	,id_tipo_produto int NOT NULL
	,marca varchar(100) NULL
	,qtd_estoque float NULL
	,id_unidade_medida int NOT NULL
	,preco decimal(10,2) NULL
	,CONSTRAINT produto_PK PRIMARY KEY (id_produto)
	,CONSTRAINT produto_FK FOREIGN KEY (id_tipo_produto) REFERENCES lazuli.dbo.tipo_produto(id_tipo_produto)
	,CONSTRAINT produto_FK_1 FOREIGN KEY (id_unidade_medida) REFERENCES lazuli.dbo.unidade_medida(id_unidade_medida)
);
GO
CREATE TABLE venda_produto (
	id_venda_produto int IDENTITY(1,1) NOT NULL
	,id_produto int NOT NULL
	,id_venda int NOT NULL
	,quantidade float NULL
	,preco_unidade decimal(10,2) NOT NULL
	,CONSTRAINT venda_produto_PK PRIMARY KEY (id_venda_produto)
	,CONSTRAINT venda_produto_FK FOREIGN KEY (id_venda) REFERENCES lazuli.dbo.venda(id_venda)
	,CONSTRAINT venda_produto_FK_1 FOREIGN KEY (id_produto) REFERENCES lazuli.dbo.produto(id_produto)
);
GO
CREATE TABLE compra_produto (
	id_compra_produto int IDENTITY(1,1) NOT NULL
	,id_compra int NOT NULL
	,id_produto int NOT NULL
	,quantidade float NULL
	,vl_unidade decimal(10,2) NULL
	,vl_total decimal(10,2) NULL
	,CONSTRAINT compra_produto_PK PRIMARY KEY (id_compra_produto)
	,CONSTRAINT compra_produto_UN UNIQUE (id_compra,id_produto)
	,CONSTRAINT compra_produto_FK FOREIGN KEY (id_produto) REFERENCES lazuli.dbo.produto(id_produto)
	,CONSTRAINT compra_produto_FK_2 FOREIGN KEY (id_compra) REFERENCES lazuli.dbo.compra(id_compra)
);
