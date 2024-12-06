from flask import Flask, session, request, render_template, redirect, url_for, jsonify
import qrcode
import os
import ssl

app = Flask(__name__)
app.secret_key = 'charadas_senai'

# Listas de grupos e charadas
grupos = []
charadas = {
    1: {"texto": "Forças internas, fraquezas escondidas, Oportunidades ao alcance, ameaças que nos cercam. Eu sou?", "resposta": "ANÁLISE SWOT", "avanco": 10},
    2: {"texto": "Quatro quadrantes, prioridades claras, urgente versus importante, decisões precisas. Eu sou?", "resposta": "MATRIZ EISENHOWER", "avanco": 8},
    3: {"texto": "Seis perguntas, um plano perfeito, Quem, quando, onde, o quê, por quê e como, útil e versátil eu sou?", "resposta": "5W2H", "avanco": 8},
    4: {"texto": "Registro detalhado, cronológico e preciso, decisões, ações e resultados, tudo anotado. Um documento indispensável no ambiente empresarial, por ser um resumo ou registro escrito dos fatos e das decisões, ocorrências ou resoluções de uma reunião. Trata-se da?", "resposta": "ATA", "avanco": 8},
    5: {"texto": "Solicitação clara, objetiva e respeitosa, para obter algo, precisa ser feita. O que sou?", "resposta": "PEDIDO", "avanco": 8},
    6: {"texto": "Fatos, dados e conclusões, apresentados com clareza, para informar e orientar, é minha finalidade. O que sou?", "resposta": "RELATÓRIO", "avanco": 8},
    7: {"texto": "Documentação precisa, organizada e acessível, para consultas futuras, é fundamental. O que sou?", "resposta": "ARQUIVO", "avanco": 8},
    8: {"texto": "Comunicação eficaz, clara e objetiva, para evitar mal-entendidos, é essencial. O que sou?", "resposta": "OFÍCIO", "avanco": 8},
    9: {"texto": "Análise crítica, reflexão e ajustes, para melhorar processos, é minha função. O que sou?", "resposta": "ANÁLISE DE PROCESSOS", "avanco": 8}
    

}

# Variável para controlar qual charada está em andamento

charada_atual = 1  # Exemplo: começando com a charada 1

# Função para gerar QR Code
def gerar_qrcode(charada_id):
    static_folder = os.path.join(app.root_path, 'static')
    if not os.path.exists(static_folder):
        os.makedirs(static_folder)

    # Altere 'seu-dominio.com' para o domínio ou IP do seu servidor
    url = f'https://karythongomes.pythonanywhere.com/charada/{charada_id}'
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
        
        # Verifica se já existe um grupo com o mesmo nome (case-insensitive)
        if any(grupo['nome'].lower() == nome_grupo.lower() for grupo in grupos):
            return render_template('cadastrar_grupo.html', erro='Já existe um grupo com esse nome!')


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
        return render_template('erro.html', mensagem="Charada não encontrada."), 404
    
    grupo_id = session.get('grupo_id')
    if not grupo_id:
        return redirect(url_for('cadastrar_grupo'))
    
    grupo = next((g for g in grupos if g['id'] == int(grupo_id)), None)
    if not grupo:
        return render_template('erro.html', mensagem="Grupo não encontrado!"), 404
    
    # Inicializar lista de charadas respondidas caso não exista
    if 'respondidas' not in grupo:
        grupo['respondidas'] = []
    
    # Verificar se a charada já foi respondida
    ja_respondida = id in grupo['respondidas']
    
    if ja_respondida:
        return render_template(
            'charada.html', 
            ja_respondida=True, 
            grupo=grupo
        )
    
    if request.method == 'POST':
        resposta = request.form.get('resposta', '').strip().lower()  # Remove espaços antes e depois da resposta
        if resposta == charada_info['resposta'].lower():
            grupo['pontos'] += charada_info['avanco']
            grupo['respondidas'].append(id)  # Marca a charada como respondida
            return redirect(url_for('home'))
        else:
            return render_template(
                'charada.html', 
                charada=charada_info, 
                erro="Resposta incorreta! Tente novamente.", 
                grupo=grupo, 
                ja_respondida=False
            )
    
    return render_template(
        'charada.html', 
        charada=charada_info, 
        grupo=grupo, 
        ja_respondida=False
    )

if __name__ == '__main__':
    #context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    #context.load_cert_chain('path/to/cert.pem', 'path/to/key.pem')  # Substitua pelos caminhos reais
    # Gera os QR Codes para todas as charadas
    for charada_id in charadas.keys():
        gerar_qrcode(charada_id)
    
    app.run( debug=True)
