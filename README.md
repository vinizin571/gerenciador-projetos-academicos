# Gerenciador de Projetos Acadêmicos

Aplicação web feita com Flask para organizar projetos acadêmicos por disciplina,
com status, prazo e integrantes.

## Funcionalidades

- Lista de projetos na página inicial
- Página de detalhes de cada projeto (`/projeto/<id>`)
- Filtro por disciplina (`/disciplina/<nome>`)
- Páginas fixas: `/sobre` e `/contato`
- Página de erro 404 personalizada

## Tecnologias

- Python 3
- Flask
- Jinja2 (templates com herança: `base.html`)
- HTML e CSS

## Como rodar

```bash
git clone https://github.com/vinizin571/gerenciador-projetos-academicos.git
cd gerenciador-projetos-academicos
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Acesse `http://127.0.0.1:5000` no navegador.

## Estrutura

- `app.py`: rotas e dados de exemplo
- `requirements.txt`: dependências
- `templates/`: páginas Jinja2 (base.html + páginas filhas)
- `static/`: arquivos CSS

## Integrantes

- Vinicius Barbosa Rezende Nogueira - 2607370
- Pedro Herique Lopes Batista - 2604184
- Guilherme Dos Santos Saraiva Virginio - 2612442
- Otávio Luiz Rodrigues Norberto - 2601946