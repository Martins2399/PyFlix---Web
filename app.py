from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3
from datetime import timedelta

app = Flask(__name__)
app.secret_key = 'pyflix_chave_secreta_super_segura'

@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)

def init_db():
    conn = sqlite3.connect('pyflix.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        conn = sqlite3.connect('pyflix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT nome FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
        user = cursor.fetchone()
        conn.close()
        
        if user:
            session['usuario'] = user[0]
            return redirect(url_for('index'))
        else:
            return render_template('login.html', erro="E-mail ou senha incorretos.")
            
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        try:
            conn = sqlite3.connect('pyflix.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
            conn.commit()
            conn.close()
            
            session['usuario'] = nome
            return redirect(url_for('index'))
        except sqlite3.IntegrityError:
            return render_template('cadastro.html', erro="Este e-mail já está cadastrado.")
        
    return render_template('cadastro.html')

@app.route('/recuperar', methods=['GET', 'POST'])
def recuperar():
    if request.method == 'POST':
        email = request.form.get('email')
        nova_senha = request.form.get('nova_senha')
        
        conn = sqlite3.connect('pyflix.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
        user = cursor.fetchone()
        
        if user:
            cursor.execute('UPDATE usuarios SET senha = ? WHERE email = ?', (nova_senha, email))
            conn.commit()
            conn.close()
            return render_template('login.html', erro="Senha alterada com sucesso! Faça login.")
        else:
            conn.close()
            return render_template('recuperar.html', erro="E-mail não encontrado no sistema.")
            
    return render_template('recuperar.html')

@app.route('/player')
def player():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('player.html')

@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)