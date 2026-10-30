from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'pyflix_secret_key_segura'  # Necessário para gerir sessões

# Banco de dados simulado em memória para demonstração
usuarios_db = {}

@app.route('/')
def index():
    # Se o utilizador não estiver logado, redireciona para a página de login/landing
    if 'usuario' not in session:
        return redirect(url_for('login'))
    return render_template('index.html', usuario=session['usuario'])

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        senha = request.form.get('senha')
        
        # Validação simples
        if email in usuarios_db and usuarios_db[email]['senha'] == senha:
            session['usuario'] = usuarios_db[email]['nome']
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
        
        if email in usuarios_db:
            return render_template('cadastro.html', erro="Este e-mail já está cadastrado.")
            
        usuarios_db[email] = {'nome': nome, 'senha': senha}
        session['usuario'] = nome
        return redirect(url_for('index'))
        
    return render_template('cadastro.html')

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