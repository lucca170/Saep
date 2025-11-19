-- Script de Criação e População do Banco de Dados (saep_db)
-- Baseado na estrutura de gestao_estoque/models.py
-- Nota: A tabela auth_user é simplificada para a inserção do usuário 'luca'.

-- 1. Criação da Tabela Produto (gestao_estoque_produto)
CREATE TABLE gestao_estoque_produto (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    nome VARCHAR(100) NOT NULL UNIQUE,
    descricao TEXT NULL,
    estoque_atual INTEGER NOT NULL,
    estoque_minimo INTEGER NOT NULL
);

-- 2. Criação da Tabela MovimentacaoEstoque (gestao_estoque_movimentacaoestoque)
CREATE TABLE gestao_estoque_movimentacaoestoque (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    tipo_movimentacao VARCHAR(1) NOT NULL,
    quantidade INTEGER NOT NULL,
    data_movimentacao DATE NOT NULL,
    usuario_id INTEGER NULL,
    produto_id BIGINT NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES auth_user (id) ON DELETE SET NULL,
    FOREIGN KEY (produto_id) REFERENCES gestao_estoque_produto (id) ON DELETE CASCADE
);

-- 3. Criação e População da Tabela auth_user
-- A senha é um placeholder, na prática deve ser um hash gerado pelo Django.
CREATE TABLE auth_user (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined DATETIME NOT NULL
);

-- População de Dados (Pelo menos três registros por tabela)

-- Inserção do usuário 'luca' (id=1)
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) 
VALUES (1, 'placeholder_hash_para_senha', '2025-11-19 13:22:26', 1, 'luca', 'Luca', 'Silva', 'luca@saep.com', 1, 1, '2025-11-19 13:15:47');
-- Inserção de mais dois usuários
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) 
VALUES (2, 'placeholder_hash_senha_user2', NULL, 0, 'operador1', 'Op', 'Um', 'op1@saep.com', 0, 1, '2025-11-19 13:30:00');
INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) 
VALUES (3, 'placeholder_hash_senha_user3', NULL, 0, 'operador2', 'Op', 'Dois', 'op2@saep.com', 0, 1, '2025-11-19 13:30:00');


-- Inserção de Produtos (RF3.2: Pelo menos três registros)
INSERT INTO gestao_estoque_produto (id, nome, descricao, estoque_atual, estoque_minimo) VALUES 
(1, 'Mouse Óptico', 'Mouse básico USB', 2, 5),
(2, 'Webcam HD', 'Webcam 720p', 0, 5),
(3, 'Hub USB 4 Portas', 'Extensor de portas', 3, 5);


-- Inserção de Movimentações (RF3.2: Pelo menos três registros)
-- Estas movimentações levam o estoque aos valores atuais (2, 0, 3)
INSERT INTO gestao_estoque_movimentacaoestoque (produto_id, tipo_movimentacao, quantidade, data_movimentacao, usuario_id) VALUES 
(1, 'E', 10, '2025-11-18', 1), -- Entrada inicial de 10 Mouses
(2, 'E', 5, '2025-11-18', 1),  -- Entrada inicial de 5 Webcams
(3, 'E', 5, '2025-11-18', 1),  -- Entrada inicial de 5 Hubs
(1, 'S', 8, '2025-11-19', 2),  -- Saída de 8 Mouses (10-8 = 2)
(2, 'S', 5, '2025-11-19', 3),  -- Saída de 5 Webcams (5-5 = 0)
(3, 'S', 2, '2025-11-19', 2);  -- Saída de 2 Hubs (5-2 = 3)