import os
import sqlite3

from flask import Flask, abort, redirect, render_template, request, url_for

import db_sql

app = Flask(__name__)
os.makedirs(app.instance_path, exist_ok=True)
app.config["DATABASE"] = os.path.join(app.instance_path, "projetos.db")
db_sql.init_app(app)

STATUS = ["Planejamento", "Em andamento", "Concluído"]


@app.route("/")
def index():
    return render_template("index.html", projetos=db_sql.listar_projetos())


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


# ----- Projetos -----
@app.route("/projeto/<int:id>")
def projeto(id):
    item = db_sql.buscar_projeto(id)
    if item is None:
        abort(404)
    return render_template(
        "projeto.html",
        projeto=item,
        integrantes=db_sql.listar_integrantes(id),
    )


@app.route("/projeto/novo", methods=["GET", "POST"])
def projeto_novo():
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        if titulo:
            db_sql.criar_projeto(
                titulo,
                request.form["descricao"].strip(),
                request.form["status"],
                request.form["prazo"],
                request.form.get("disciplina_id") or None,
            )
            return redirect(url_for("index"))
    return render_template(
        "form_projeto.html",
        projeto=None,
        disciplinas=db_sql.listar_disciplinas(),
        status_opcoes=STATUS,
    )


@app.route("/projeto/<int:id>/editar", methods=["GET", "POST"])
def projeto_editar(id):
    item = db_sql.buscar_projeto(id)
    if item is None:
        abort(404)
    if request.method == "POST":
        titulo = request.form["titulo"].strip()
        if titulo:
            db_sql.atualizar_projeto(
                id,
                titulo,
                request.form["descricao"].strip(),
                request.form["status"],
                request.form["prazo"],
                request.form.get("disciplina_id") or None,
            )
            return redirect(url_for("projeto", id=id))
    return render_template(
        "form_projeto.html",
        projeto=item,
        disciplinas=db_sql.listar_disciplinas(),
        status_opcoes=STATUS,
    )


@app.route("/projeto/<int:id>/excluir", methods=["POST"])
def projeto_excluir(id):
    db_sql.excluir_projeto(id)
    return redirect(url_for("index"))


# ----- Integrantes -----
@app.route("/projeto/<int:id>/integrantes", methods=["POST"])
def integrante_novo(id):
    if db_sql.buscar_projeto(id) is None:
        abort(404)
    nome = request.form["nome"].strip()
    if nome:
        db_sql.criar_integrante(nome, id)
    return redirect(url_for("projeto", id=id))


@app.route("/projeto/<int:pid>/integrante/<int:iid>/excluir", methods=["POST"])
def integrante_excluir(pid, iid):
    db_sql.excluir_integrante(iid, pid)
    return redirect(url_for("projeto", id=pid))


# ----- Disciplinas -----
@app.route("/disciplinas", methods=["GET", "POST"])
def disciplinas():
    erro = None
    if request.method == "POST":
        nome = request.form["nome"].strip()
        if nome:
            try:
                db_sql.criar_disciplina(nome)
                return redirect(url_for("disciplinas"))
            except sqlite3.IntegrityError:
                erro = "Já existe uma disciplina com esse nome."
    return render_template(
        "disciplinas.html", disciplinas=db_sql.listar_disciplinas(), erro=erro
    )


@app.route("/disciplina/<int:id>/excluir", methods=["POST"])
def disciplina_excluir(id):
    db_sql.excluir_disciplina(id)
    return redirect(url_for("disciplinas"))


@app.route("/disciplina/<nome>")
def disciplina(nome):
    return render_template(
        "disciplina.html",
        nome=nome,
        projetos=db_sql.listar_projetos_por_disciplina(nome),
    )


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)