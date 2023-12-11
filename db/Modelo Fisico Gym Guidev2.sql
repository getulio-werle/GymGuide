-- BANCO DE DADOS DO SISTEMA GYM GUIDE
-- DDL

-- APAGANDO TABELAS CASO EXISTAM

DROP TABLE IF EXISTS Exercicio_treino;
DROP TABLE IF EXISTS Treino;
DROP TABLE IF EXISTS Lista_treinos;
DROP TABLE IF EXISTS Exercicio_generico CASCADE;
DROP TABLE IF EXISTS Grupo_musculo CASCADE;
DROP TABLE IF EXISTS Endereco;
DROP TABLE IF EXISTS Usuario;

---------------------------------------------

-- CRIANDO AS TABELAS

CREATE TABLE Grupo_musculo (
	cod_grupo_musculo 	SERIAL PRIMARY KEY,
	nome				VARCHAR(60) NOT NULL
);

CREATE TABLE Treino (
	cod_treino 			SERIAL PRIMARY KEY,
	nome 				VARCHAR(60) NOT NULL,
	cod_lista_treinos 	INT NOT NULL
);

CREATE TABLE Usuario (
	cod_usuario 		SERIAL PRIMARY KEY,
	nome 				VARCHAR(255) NOT NULL,
	senha 				VARCHAR(60) NOT NULL,
	cpf 				VARCHAR(20) NOT NULL,
	email 				VARCHAR(255) NOT NULL,
	telefone 			VARCHAR(20) NOT NULL,
	telefone_emergencia	VARCHAR(20),
	status				CHAR(1) NOT NULL,	-- 'A' = Ativo / 'B' = Bloqueado
	vencimento			DATE NOT NULL,		-- Vencimento do plano da academia
	tipo 				CHAR(1) NOT NULL		-- 'I' = Instrutor/ 'A' = Aluno
);

CREATE TABLE Endereco (
	cod_endereco	SERIAL PRIMARY KEY,
	rua				VARCHAR(100) NOT NULL,
	bairro			VARCHAR(100) NOT NULL,
	numero			VARCHAR(20) NOT NULL,
	cep 			VARCHAR(10) NOT NULL,
	complemento		VARCHAR(150),
	cidade 			VARCHAR(100) NOT NULL,
	estado	     	CHAR(2) NOT NULL,
	cod_usuario		INT NOT NULL
);

CREATE TABLE Exercicio_treino (
	cod_exercicio_treino 	SERIAL PRIMARY KEY,
	series 					INT,
	repeticoes				INT,
	observacao 				VARCHAR(255),
	cod_treino 				INT NOT NULL,
	cod_exercicio 			INT NOT NULL
);

CREATE TABLE Lista_Treinos (
	cod_lista_treinos 		SERIAL PRIMARY KEY,
	nome 					VARCHAR(60) NOT NULL,
	cod_usuario 			INT
);

CREATE TABLE Exercicio_generico (
	cod_exercicio 		SERIAL PRIMARY KEY,
	nome 				VARCHAR(60) NOT NULL,
	aparelho 			INT,
	cod_grupo_musculo 	INT	NOT NULL
);

-- ADICIONANDO CHAVES ESTRANGEIRAS

ALTER TABLE Treino ADD CONSTRAINT treino_lista_treino_fk FOREIGN KEY(cod_lista_treinos) REFERENCES Lista_Treinos (cod_lista_treinos) ON DELETE CASCADE;
ALTER TABLE Endereco ADD CONSTRAINT endereco_usuario_fk FOREIGN KEY(cod_usuario) REFERENCES Usuario (cod_usuario) ON DELETE CASCADE;
ALTER TABLE Exercicio_treino ADD CONSTRAINT exercicio_treino_exercicio_generico_fk FOREIGN KEY(cod_exercicio) REFERENCES Exercicio_generico (cod_exercicio) ON DELETE CASCADE;
ALTER TABLE Exercicio_treino ADD CONSTRAINT exercicio_treino_treino_fk FOREIGN KEY(cod_treino) REFERENCES Treino (cod_treino) ON DELETE CASCADE;
ALTER TABLE Lista_Treinos ADD CONSTRAINT lista_treinos_usuario_fk FOREIGN KEY(cod_usuario) REFERENCES Usuario (cod_usuario) ON DELETE CASCADE;
ALTER TABLE Exercicio_generico ADD CONSTRAINT exercicio_generico_grupo_musculo_fk FOREIGN KEY(cod_grupo_musculo) REFERENCES Grupo_Musculo (cod_grupo_musculo) ON DELETE CASCADE;

-----------------------------

-- VERIFICANDO AS TABELAS

SELECT * FROM Treino;
SELECT * FROM Usuario;
SELECT * FROM Exercicio_treino;
SELECT * FROM Exercicio_generico;
SELECT * FROM Endereco;
SELECT * FROM Lista_treinos;
SELECT * FROM Grupo_musculo;

-----------------------------

-- CHECK Exercicio_generico
ALTER TABLE Exercicio_generico 
ADD CONSTRAINT chk_aparelho 
CHECK (aparelho > 0);	-- Verifica o número do aparelho do exercício

-- CHECK Usuario
ALTER TABLE Usuario
ADD CONSTRAINT chk_status
CHECK (status IN ('A', 'B'));	-- 'A' = Ativo / 'B' = Bloqueado

ALTER TABLE Usuario
ADD CONSTRAINT chk_vencimento
CHECK (vencimento > CURRENT_DATE); -- Verifica a data do vencimento do plano da academia

ALTER TABLE Usuario
ADD CONSTRAINT chk_tipo
CHECK (tipo IN ('I', 'A'));	-- 'I' = Instrutor/ 'A' = Aluno

-- CHECK Exercicio_treino
ALTER TABLE Exercicio_treino
ADD CONSTRAINT chk_series
CHECK (series > 0);	-- Verifica se o número de séries é negativo

ALTER TABLE Exercicio_treino
ADD CONSTRAINT chk_repeticoes
CHECK (repeticoes > 0);	-- Verifica se o número de repetições é negativo

-----------------------------

-- VIEW Exercicio_generico
CREATE OR REPLACE VIEW V_Exercicio_generico AS
SELECT cod_exercicio, nome, aparelho, cod_grupo_musculo
FROM Exercicio_generico;

-- VIEW Grupo_musculo
CREATE OR REPLACE VIEW V_Grupo_musculo AS
SELECT cod_grupo_musculo, nome
FROM Grupo_musculo;