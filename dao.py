#data access object
import sqlite3
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
