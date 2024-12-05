from flask import Flask, session, request, render_template, redirect, url_for, jsonify
import qrcode
import os
import ssl

app = Flask(__name__)
app.secret_key = 'charadas_senai'

# Listas de grupos e charadas
grupos = []
charadas = {
    1: {"texto": "Qual é o animal que anda com os pés na cabeça?", "resposta": "cabelo", "avanco": 2},
    2: {"texto": "O que é cheio de buracos, mas ainda consegue segurar água?", "resposta": "esponja", "avanco": 3},
    3: {"texto": "O que é invisível e faz o mundo girar?", "resposta": "vento", "avanco": 1},
}

# Variável para controlar qual charada está em andamento

charada_atual = 1  # Exemplo: começando com a charada 1

# Função para gerar QR Code
def gerar_qrcode(charada_id):
    static_folder = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    url = f'http://localhost:5000/charada/{charada_id}'
    qr = qrcode.make(url)
    qr.save(os.path.join(static_folder, f'qrcode_{charada_id}.png')) 

def ranking():
    ordenados = sorted(grupos, key=lambda x: x['pontos'], reverse=True)
    return render_template('ranking.html', grupos=ordenados)

@app.route('/')
def index():
    # Verifica se o grupo já está registrado na sessão
    grupo_id = session.get('grupo_id')
    
    if grupo_id:
        # Redireciona para a página inicial (home) se o grupo já estiver cadastrado
        return redirect(url_for('home'))
    
    # Caso contrário, redireciona para a página de cadastro do grupo
    return redirect(url_for('cadastrar_grupo'))

@app.route('/home')
def home():

    grupo_id = session.get('grupo_id')
    if not grupo_id:
        return redirect(url_for('cadastrar_grupo'))

    grupo = next((g for g in grupos if g['id'] == int(grupo_id)), None)
    if not grupo:
        return 'Grupo não encontrado!', 404
    ordenados = sorted(grupos, key=lambda x: x['pontos'], reverse=True)
    return render_template('home.html', grupos=ordenados)

@app.route('/login', methods=['POST'])
def login():
    grupo_id = request.form.get('grupo_id')
    session['grupo_id'] = grupo_id
    return redirect(url_for('home'))

@app.route('/cadastrar_grupo', methods=['GET', 'POST'])
def cadastrar_grupo():
    if request.method == 'POST':
        nome_grupo = request.form.get('nome_grupo')
        if not nome_grupo:
            return render_template('cadastrar_grupo.html', erro='O nome do grupo é obrigatório!')

        # Criar um ID único para o grupo
        novo_grupo_id = len(grupos) + 1
        novo_grupo = {'id': novo_grupo_id, 'nome': nome_grupo, 'pontos': 0}
        grupos.append(novo_grupo)

        # Armazenar o grupo na sessão
        session['grupo_id'] = novo_grupo_id
        session['grupo_nome'] = nome_grupo

        return redirect(url_for('home'))

    return render_template('cadastrar_grupo.html')

@app.route('/charada/<int:id>', methods=['GET', 'POST'])
def charada(id):
    charada_info = charadas.get(id)
    if not charada_info:
        return 'Charada não encontrada.', 404
    
    grupo_id = session.get('grupo_id')
    if not grupo_id:
        return 'Grupo não identificado! Faça login novamente.', 403
    
    grupo = next((g for g in grupos if g['id'] == int(grupo_id)), None)
    if not grupo:
        return 'Grupo não encontrado.', 404
    
    if request.method == 'POST':
        resposta = request.form.get('resposta', '').lower()
        if resposta == charada_info['resposta'].lower():
            grupo['pontos'] += charada_info['avanco']
            return redirect(url_for('home'))
        else:
            return render_template('charada.html', charada=charada_info, erro='Resposta incorreta! Tente novamente.', grupo=grupo, id=id)

    return render_template('charada.html', charada=charada_info, grupo=grupo, id=id)

if __name__ == '__main__':
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #context.load_cert_chain('path/to/cert.pem', 'path/to/key.pem')  # Substitua pelos caminhos reais
    # Gera os QR Codes para todas as charadas
    for charada_id in charadas.keys():
        gerar_qrcode(charada_id)
    
    app.run( debug=True)
