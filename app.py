import sqlite3
import csv
import io
from flask import Flask, jsonify, request, Response
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATABASE = 'financas.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transacoes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            descricao TEXT NOT NULL,
            valor REAL NOT NULL,
            tipo TEXT CHECK(tipo IN ('receita', 'despesa')) NOT NULL,
            categoria TEXT NOT NULL,
            data TEXT NOT NULL,
            criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

init_db()


# ROTAS DA API REST
@app.route('/api/transacoes', methods=['GET'])
def listar_transacoes():
    mes = request.args.get('mes')
    ano = request.args.get('ano')
    
    conn = get_db_connection()
    query = 'SELECT * FROM transacoes WHERE 1=1'
    params = []

    if mes and ano:
        # Formata mes para ter dois digitos (ex: '05')
        mes_str = f"{int(mes):02d}"
        query += " AND strftime('%m', data) = ? AND strftime('%Y', data) = ?"
        params.extend([mes_str, str(ano)])

    query += ' ORDER BY data DESC, id DESC'
    transacoes = conn.execute(query, params).fetchall()
    conn.close()

    return jsonify([dict(t) for t in transacoes]), 200

@app.route('/api/transacoes', methods=['POST'])
def criar_transacao():
    dados = request.get_json()
    descricao = dados.get('descricao')
    valor = dados.get('valor')
    tipo = dados.get('tipo')
    categoria = dados.get('categoria')
    data = dados.get('data')

    if not descricao or valor is None or not tipo or not categoria or not data:
        return jsonify({'erro': 'Todos os campos são obrigatórios!'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO transacoes (descricao, valor, tipo, categoria, data)
        VALUES (?, ?, ?, ?, ?)
    ''', (descricao, float(valor), tipo, categoria, data))
    conn.commit()
    novo_id = cursor.lastrowid
    conn.close()

    return jsonify({'id': novo_id, 'mensagem': 'Transação adicionada!'}), 201

@app.route('/api/resumo', methods=['GET'])
def obter_resumo():
    mes = request.args.get('mes')
    ano = request.args.get('ano')

    conn = get_db_connection()
    
    filtro = ""
    params = []
    if mes and ano:
        mes_str = f"{int(mes):02d}"
        filtro = " AND strftime('%m', data) = ? AND strftime('%Y', data) = ?"
        params = [mes_str, str(ano)]

    receitas = conn.execute(f"SELECT SUM(valor) FROM transacoes WHERE tipo = 'receita'{filtro}", params).fetchone()[0] or 0.0
    despesas = conn.execute(f"SELECT SUM(valor) FROM transacoes WHERE tipo = 'despesa'{filtro}", params).fetchone()[0] or 0.0
    saldo = receitas - despesas

    categorias = conn.execute(f'''
        SELECT categoria, SUM(valor) as total 
        FROM transacoes 
        WHERE tipo = 'despesa'{filtro} 
        GROUP BY categoria
    ''', params).fetchall()
    
    conn.close()

    return jsonify({
        'total_receitas': receitas,
        'total_despesas': despesas,
        'saldo': saldo,
        'despesas_por_categoria': [dict(c) for c in categorias]
    }), 200

@app.route('/api/transacoes/<int:id>', methods=['DELETE'])
def deletar_transacao(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM transacoes WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return jsonify({'mensagem': 'Transação removida!'}), 200

@app.route('/api/exportar/csv', methods=['GET'])
def exportar_csv():
    """Gera e faz o download de um relatório em CSV com acentuação correta (UTF-8 com BOM)."""
    conn = get_db_connection()
    transacoes = conn.execute('SELECT data, descricao, categoria, tipo, valor FROM transacoes ORDER BY data DESC').fetchall()
    conn.close()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Data', 'Descrição', 'Categoria', 'Tipo', 'Valor (R$)'])

    for t in transacoes:
        writer.writerow([t['data'], t['descricao'], t['categoria'], t['tipo'], t['valor']])

    # O 'utf-8-sig' adiciona o BOM que obriga o Excel a reconhecer a acentuação corretamente
    conteudo_csv = output.getvalue().encode('utf-8-sig')

    response = Response(conteudo_csv, mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=relatorio_financas.csv'
    return response

if __name__ == '__main__':
    app.run(debug=True, port=5000)