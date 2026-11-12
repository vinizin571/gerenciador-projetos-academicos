DROP TABLE IF EXISTS integrantes;
DROP TABLE IF EXISTS projetos;
DROP TABLE IF EXISTS disciplinas;

CREATE TABLE disciplinas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE
);

CREATE TABLE projetos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    descricao TEXT,
    status TEXT NOT NULL DEFAULT 'Planejamento',
    prazo TEXT,
    disciplina_id INTEGER,
    FOREIGN KEY (disciplina_id) REFERENCES disciplinas (id) ON DELETE SET NULL
);

CREATE TABLE integrantes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    projeto_id INTEGER NOT NULL,
    FOREIGN KEY (projeto_id) REFERENCES projetos (id) ON DELETE CASCADE
);

INSERT INTO disciplinas (nome) VALUES ('Programação'), ('UX');

INSERT INTO projetos (titulo, descricao, status, prazo, disciplina_id) VALUES
    ('Sistema de Biblioteca', 'Cadastro e empréstimo de livros.', 'Em andamento', '2026-12-15', 1),
    ('App de Agendamento de Consultas', 'Protótipo com persona, jornada e wireframes.', 'Concluído', '2026-11-30', 2);

INSERT INTO integrantes (nome, projeto_id) VALUES
    ('Vinicius', 1), ('Otavio', 1), ('Guilherme', 2), ('Pedro', 2);