from flask import Flask, request, render_template, redirect, url_for, jsonify
import qrcode
import os

app = Flask(__name__)

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
def home():
    ordenados = sorted(grupos, key=lambda x: x['pontos'], reverse=True)
    return render_template('home.html', grupos=ordenados)

@app.route('/cadastrar_grupo.html', methods=['GET', 'POST'])
def cadastrar_grupo():
    if request.method == 'POST':
        nome_grupo = request.form.get('nome_grupo')
        if nome_grupo:
            novo_grupo = {'id': len(grupos) + 1, 'nome': nome_grupo, 'pontos': 0}
            grupos.append(novo_grupo)
           
            return redirect(url_for('home'))
    return render_template('cadastrar_grupo.html')

@app.route('/charada/<int:id>', methods=['GET', 'POST'])
def charada(id):
    charada_info = charadas.get(id)
    if not charada_info:
        return 'Charada não encontrada.', 404

    if request.method == 'POST':
        resposta = request.form.get('resposta', '').lower()
        grupo_id = int(request.form.get('grupo_id'))
        grupo = next((g for g in grupos if g['id'] == grupo_id), None)

        if not grupo:
            return 'Grupo não encontrado.', 404
        
        if resposta == charada_info['resposta'].lower():
            grupo['pontos'] += charada_info['avanco']
            return redirect(url_for('home'))
        else:
            return render_template('charada.html', charada=charada_info, erro='Resposta incorreta! Tente novamente.', grupos=grupos)
    
    return render_template('charada.html', charada=charada_info, grupos=grupos)


if __name__ == '__main__':
  
    # Gerar QR Codes para todas as charadas ao iniciar
    for charada_id in charadas.keys():
        gerar_qrcode(charada_id)
    
    app.run(debug=True)