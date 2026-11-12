from flask import Flask, render_template, abort

app = Flask(__name__)

PROJETOS = {
    1: {
        "titulo": "Sistema de Biblioteca",
        "disciplina": "Programação",
        "integrantes": ["Ana", "Bruno", "Carla"],
        "status": "Em andamento",
        "prazo": "15/12/2026",
        "descricao": "Aplicação para cadastro e empréstimo de livros.",
    },
    2: {
        "titulo": "App de Agendamento de Consultas",
        "disciplina": "UX",
        "integrantes": ["Diego", "Elisa"],
        "status": "Concluído",
        "prazo": "30/11/2026",
        "descricao": "Protótipo com persona, jornada e wireframes.",
    },
    3: {
        "titulo": "Loja Virtual com Flask",
        "disciplina": "Programação",
        "integrantes": ["Fábio", "Gabi"],
        "status": "Planejamento",
        "prazo": "20/01/2027",
        "descricao": "Catálogo de produtos com rotas dinâmicas.",
    },
}


@app.route("/")
def index():
    return render_template("index.html", projetos=PROJETOS)


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/contato")
def contato():
    return render_template("contato.html")


@app.route("/projeto/<int:id>")
def projeto(id):
    item = PROJETOS.get(id)
    if not item:
        abort(404)
    return render_template("projeto.html", id=id, projeto=item)


@app.route("/disciplina/<nome>")
def disciplina(nome):
    filtrados = {
        pid: p for pid, p in PROJETOS.items()
        if p["disciplina"].lower() == nome.lower()
    }
    return render_template("disciplina.html", nome=nome, projetos=filtrados)


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)