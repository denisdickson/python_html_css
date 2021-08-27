import sqlite3
from flask import Flask, request, url_for, session, g, redirect, abort, render_template, flash

# configuração
DATABASE = "blog.db"
SECRET_KEY = 'pudim'


app = Flask(__name__)
app.config.from_object(__name__)


def conectar_bd():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def antes_requisicao():
    g.bd = conectar_bd()


@app.teardown_request
def depois_request(exc):
    g.bd.close()


@app.route('/')
@app.route('/entradas')
def exibir_entradas():
    sql = "SELECT titulo, text FROM entradas ORDER BY id DESC"
    cur = g.bd.execute(sql)
    entradas = []
    for titulo, text in cur.fetchall():
        entradas.append({'titulo': titulo, 'text': text})
    return render_template('exibir_entradas.html', entradas=entradas)


@app.route('/inserir')
def inserir_entrada():
    if not session.get('logado'):
        abort(401)
    sql = "INSERT INTO entradas(titulo, text) VALUES (?,?)"
    g.bd.execute(sql, request.form['campoTitulo'], request.form['campoTexto'])
    g.bd.commit()
    return redirect(url_for('exibir_entradas'))


@app.route('/logout')
def logout():
    session.pop('logado', None)
    return redirect(url_for('exibr_entradas'))


@app.route('/login', methods=["GET", "POST"])
def login():
    erro = None
    if request.method == "POST":
        if request.form['campoUsuario'] != 'admin' \
                or request.form['campoSenha'] != 'admin':
            erro = "Senha ou usuário inválidos !"
        else:
            session['logado'] = True
        print("Foi post")
        return redirect(url_for('exibir_entradas'))
    return render_template('login.html', erro=erro)
