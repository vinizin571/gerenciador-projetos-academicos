import sqlite3

import click
from flask import current_app, g


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as f:
        db.executescript(f.read().decode("utf-8"))


@click.command("init-db")
def init_db_command():
    """Cria as tabelas a partir do schema.sql."""
    init_db()
    click.echo("Banco de dados inicializado.")


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)


# ---------- DISCIPLINAS ----------
def listar_disciplinas():
    return get_db().execute(
        "SELECT id, nome FROM disciplinas ORDER BY nome"
    ).fetchall()


def criar_disciplina(nome):
    db = get_db()
    db.execute("INSERT INTO disciplinas (nome) VALUES (?)", (nome,))
    db.commit()


def excluir_disciplina(id):
    db = get_db()
    db.execute("DELETE FROM disciplinas WHERE id = ?", (id,))
    db.commit()


# ---------- PROJETOS ----------
def listar_projetos():
    # LEFT JOIN: projetos sem disciplina também aparecem
    return get_db().execute(
        """
        SELECT p.id, p.titulo, p.status, p.prazo, d.nome AS disciplina
        FROM projetos p
        LEFT JOIN disciplinas d ON d.id = p.disciplina_id
        ORDER BY p.id
        """
    ).fetchall()


def listar_projetos_por_disciplina(nome):
    # INNER JOIN: só projetos que têm disciplina
    return get_db().execute(
        """
        SELECT p.id, p.titulo, p.status
        FROM projetos p
        INNER JOIN disciplinas d ON d.id = p.disciplina_id
        WHERE LOWER(d.nome) = LOWER(?)
        ORDER BY p.id
        """,
        (nome,),
    ).fetchall()


def buscar_projeto(id):
    return get_db().execute(
        """
        SELECT p.*, d.nome AS disciplina
        FROM projetos p
        LEFT JOIN disciplinas d ON d.id = p.disciplina_id
        WHERE p.id = ?
        """,
        (id,),
    ).fetchone()


def criar_projeto(titulo, descricao, status, prazo, disciplina_id):
    db = get_db()
    db.execute(
        """
        INSERT INTO projetos (titulo, descricao, status, prazo, disciplina_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (titulo, descricao, status, prazo, disciplina_id),
    )
    db.commit()


def atualizar_projeto(id, titulo, descricao, status, prazo, disciplina_id):
    db = get_db()
    db.execute(
        """
        UPDATE projetos
        SET titulo = ?, descricao = ?, status = ?, prazo = ?, disciplina_id = ?
        WHERE id = ?
        """,
        (titulo, descricao, status, prazo, disciplina_id, id),
    )
    db.commit()


def excluir_projeto(id):
    db = get_db()
    db.execute("DELETE FROM projetos WHERE id = ?", (id,))
    db.commit()


# ---------- INTEGRANTES ----------
def listar_integrantes(projeto_id):
    return get_db().execute(
        "SELECT id, nome FROM integrantes WHERE projeto_id = ? ORDER BY nome",
        (projeto_id,),
    ).fetchall()


def criar_integrante(nome, projeto_id):
    db = get_db()
    db.execute(
        "INSERT INTO integrantes (nome, projeto_id) VALUES (?, ?)",
        (nome, projeto_id),
    )
    db.commit()


def excluir_integrante(id, projeto_id):
    db = get_db()
    db.execute(
        "DELETE FROM integrantes WHERE id = ? AND projeto_id = ?",
        (id, projeto_id),
    )
    db.commit()