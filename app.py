from flask import Flask, request, render_template
from dao import *
import datetime

app = Flask(__name__)

@app.route('/')
def home():

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

if __name__ == '__main__':
    init_db()
    app.run(debug=True, port=80, host='0.0.0.0')
