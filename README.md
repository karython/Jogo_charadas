---

# **Sistema de Charadas com Ranking**

Bem-vindo ao **Sistema de Charadas!** Um jogo interativo onde grupos competem para responder a charadas e acumular pontos. Este projeto foi desenvolvido utilizando **Flask**, **Python**, **QR Codes** e **HTML/CSS**, com o objetivo de oferecer uma experiência divertida e envolvente.

## **Funcionalidades**

🎮 **Jogo de Charadas:**  
Grupos competem respondendo a charadas. Cada charada tem uma resposta e, se correta, o grupo ganha pontos.

📈 **Ranking Dinâmico:**  
Acompanhe a pontuação dos grupos em tempo real! O ranking é atualizado conforme os grupos respondem corretamente às charadas.

🔐 **Cadastro de Grupos:**  
Os participantes podem cadastrar seus grupos e começar a competir assim que registrados.

📱 **QR Code para Charadas:**  
Para cada charada, um QR Code é gerado. Ao escanear, o grupo é direcionado à página da charada correspondente para tentar a resposta.

---

## **Como Usar**

### 1. **Clonando o Repositório**

Clone o repositório para o seu computador:

```bash
git clone https://github.com/seu-usuario/sistema-charadas.git
```

### 2. **Instalação de Dependências**

Entre na pasta do projeto e instale as dependências com o `pip`:

```bash
cd sistema-charadas
pip install -r requirements.txt
```

### 3. **Executando o Projeto**

Para rodar o sistema, basta executar:

```bash
python app.py
```

Isso iniciará o servidor localmente. Acesse `http://localhost:5000` no seu navegador para começar a jogar!

### 4. **Gerar QR Codes**

Ao iniciar o servidor, os QR Codes são gerados automaticamente para cada charada. Cada grupo pode escanear o QR Code para acessar a página da charada e tentar responder.

---

## **Estrutura do Projeto**

```plaintext
├── app.py              # Arquivo principal do servidor Flask
├── static/             # Arquivos estáticos (como imagens e CSS)
│   ├── css/            # Estilos CSS
│   ├── qrcodes/        # QR Codes gerados para cada charada
├── templates/          # Arquivos HTML (home, cadastro, charadas, etc)
├── requirements.txt    # Dependências do projeto
└── README.md           # Este arquivo
```

---

## **Tecnologias Utilizadas**

- **Flask**: Framework web para Python, usado para criar a API e páginas dinâmicas.
- **QR Code**: Biblioteca Python utilizada para gerar os QR Codes das charadas.
- **HTML/CSS**: Utilizado para construir as páginas da interface web.
- **Python**: Linguagem de programação utilizada para a lógica do sistema.

---

## **Melhorias Futuras**

🔧 **Adicionar mais charadas:** Ampliar o banco de charadas para aumentar a complexidade do jogo.

📊 **Melhorar o Ranking:** Adicionar mais detalhes ao ranking, como mostrar o tempo de resposta de cada grupo.

📱 **Versão Mobile:** Tornar a interface responsiva para dispositivos móveis, permitindo que o jogo seja jogado em qualquer lugar.

---

## **Contribuições**

Contribuições são sempre bem-vindas! Se você encontrar um bug, tiver uma sugestão de melhoria ou quiser adicionar novas funcionalidades, fique à vontade para abrir uma _issue_ ou enviar um _pull request_.

---

## **Licença**

Este projeto está licenciado sob a Licença MIT - veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## **Contato**

Se tiver dúvidas ou sugestões, entre em contato comigo através do e-mail: **karython.unai@gmail.com**

---

### **Capturas de Tela**

**Página Inicial**  
![home](/static/img/home.PNG)

**Cadastro de Grupos**  
![cadastro](/static/img/cadastro%20equipes.PNG)

---
