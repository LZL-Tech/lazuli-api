CREATE DATABASE LZLtech;
GO
Use LZLtech;
GO
CREATE TABLE Produtos
( 
  Id          smallint identity(1,1)
, Descricao   VARCHAR(255) NOT NULL
, Quantidade  INT NOT NULL
, CONSTRAINT pkProdutos PRIMARY KEY (Id)
);
GO