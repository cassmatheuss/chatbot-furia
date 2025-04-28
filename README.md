# 🦊🔥 Furia Fan Chat – Back-End

Bem-vindo ao **Furia Fan Chat**! Este é o back-end de um chatbot de IA feito para a torcida da FURIA, integrando detecção de intenção, consultas em tempo real à API do PandaScore e persistência de mensagens com MongoDB. 🚀

---

## ✨ Acesso a aplicação hospedada:
 - https://furia.cassmatheus.site

## ✨ Visão Geral

O **Furia Fan Chat** é um servidor Flask que:

- Usa IA (via OpenRouter) para entender a intenção do usuário e responder de forma contextualizada.
- Consulta a [API do PandaScore](https://developers.pandascore.co/reference/) para trazer informações em tempo real.
- Armazena histórico de mensagens e sessões no MongoDB.
- Oferece endpoints simples e práticos para integração com front-ends e outras aplicações.

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Flask** – Framework web leve ⚡
- **OpenRouter** – Gateway de IA para processamento de linguagem natural 🤖
- **PandaScore API** – Dados esportivos em tempo real 🎮
- **MongoDB** – Armazenamento de mensagens e sessões 💾
- **Langchain** – Biblioteca para a integração com IA
---

## 📦 Instalação

1. **Clone o repositório:**
   ```bash
   git clone https://github.com/cassmatheuss/chatbot-furia
   cd chatbot-furia
   ```

2. **Crie e configure o `.env`:**
   ```env
   OPENROUTER_API_KEY=
   OPENROUTER_BASE_URL=
   PANDASCORE_API_KEY=
   DB_NAME=
   MONGO_DB_URL=
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```
   **ou use o Poetry!**

5. **Execute o servidor:**
   ```bash
   python main.py
   ```
   **ou:**
   ```bash
   poetry run python main.py
   ```

---

## 🚦 Endpoints da API

### 1. `/chat` – Interação com o Chatbot

- **Método:** `POST`
- **Body (JSON):**
  ```json
  {
    "message": "Qual foi o último jogo da FURIA?",
    "session_id": "125c3817-4c9f-4d95-a83b-9d414c4745a6"
  }
  ```
- **Resposta (JSON):**
  ```json
  {
    "created_at": "2025-04-27T22:00:41.720128-03:00",
    "message": "O último jogo da FURIA foi contra o TheMongolz no campeonato PGL Bucharest - Group Stage. Aqui estão os detalhes:\n\n- **Times**: FURIA x TheMongolz\n- **Vencedor**: TheMongolz\n- **Início**: 09/04/2025 às 09:55 (Horário de Brasília)\n- **Fim**: 09/04/2025 às 11:48 (Horário de Brasília)\n\nVamos torcer para que a FURIA se recupere nas próximas partidas! 🐾🔥",
    "session_id": "125c3817-4c9f-4d95-a83b-9d414c4745a6",
    "type": "AI"
  }
  ```

---

### 2. `/history/` – Histórico da Sessão

- **Método:** `GET`
- **Resposta (JSON):**
  ```json
  {
    "history": [
      {
        "_id": "680d3770193a169a0ea76cb9",
        "created_at": "2025-04-26T16:43:44.802677-03:00",
        "message": "oi, tudo bem?",
        "session_id": "125c3817-4c9f-4d95-a83b-9d414c4745a6",
        "type": "HUMAN"
      },
      {
        "_id": "680d3773193a169a0ea76cba",
        "created_at": "2025-04-26T16:43:47.883596-03:00",
        "message": "E aí, meu parça! Tô na vibe, e você? Pronto pra torcer pela FURIA e quebrar tudo no CS2? VAMO FURIA! 🦊🔥",
        "session_id": "125c3817-4c9f-4d95-a83b-9d414c4745a6",
        "type": "AI"
      }
      // ...demais mensagens
    ]
  }
  ```

---

## 🔑 Variáveis de Ambiente

Configure o arquivo `.env` com as seguintes variáveis:

| Variável               | Descrição                                           |
|------------------------|----------------------------------------------------|
| OPENROUTER_API_KEY     | Chave de API do OpenRouter                         |
| OPENROUTER_BASE_URL    | URL base do OpenRouter                             |
| PANDASCORE_API_KEY     | Chave de API do PandaScore                         |
| DB_NAME                | Nome do banco de dados MongoDB                     |
| MONGO_DB_URL           | URL de conexão MongoDB Atlas/local                 |

---

## 🧠 Como Funciona?

1. **Usuário envia mensagem** ➡️
2. **Back-end detecta intenção** via OpenRouter ➡️
3. **Consulta a PandaScore API** se necessário ➡️
4. **Responde com contexto esportivo e como se fosse um torcedor** ➡️
5. **Salva tudo no MongoDB** para histórico e análise.

---

## 🏆 Exemplos de Uso

- **Perguntar sobre o último jogo:**  
  “Quando foi o último jogo da FURIA?”

- **Consultar histórico:**  
  `GET /history/125c3817-4c9f-4d95-a83b-9d414c4745a6`

---


## 📣 Feito por Matheus Castilho! 🦊🔥
