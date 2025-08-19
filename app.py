from flask import Flask, request, render_template
import sqlite3
import datetime

app = Flask(__name__)
DB_NAME = 'esp_data.db'

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS leituras (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dispositivo TEXT NOT NULL,
            mensagem TEXT,
            valor REAL,
            horario TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def salvar_dado(dispositivo, mensagem=None, valor=None):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO leituras (dispositivo, mensagem, valor) VALUES (?, ?, ?)",
        (dispositivo, mensagem, valor)
    )
    conn.commit()
    conn.close()

def carregar_dados(dispositivo):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT horario, mensagem, valor FROM leituras WHERE dispositivo=? ORDER BY horario DESC",
        (dispositivo,)
    )
    linhas = cursor.fetchall()
    conn.close()
    if not linhas:
        return ["Nenhum dado registrado."]
    return [f"{linha[0]} - {linha[1] or linha[2]}" for linha in linhas]

@app.route('/')
def home():
    print('ok')
    return render_template('homepage.html')

@app.route('/botao')
def botao_page():
    dados = carregar_dados('botao')
    return render_template('botao.html', dados=dados)

@app.route('/sensor1')
def sensor1_page():
    dados = carregar_dados('sensor1')
    return render_template('sensor1.html', dados=dados)

@app.route('/distancia')
def receber_distancia():
    valor = request.args.get('valor')
    if not valor:
        return {'erro': 'Parâmetro valor não fornecido'}, 400

    salvar_dado('sensor1', valor=float(valor))
    return {'status': 'ok'}

@app.route('/enviar/<dispositivo>', methods=['POST'])
def receber_post(dispositivo):
    conteudo = request.get_json()
    if not conteudo or 'mensagem' not in conteudo:
        return {'erro': 'Formato inválido'}, 400

    mensagem = conteudo['mensagem']
    salvar_dado(dispositivo, mensagem=mensagem)
    return {'status': 'ok'}

# --- Inicializa banco e roda app ---
if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=80, host='0.0.0.0')
