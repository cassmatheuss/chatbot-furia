from datetime import datetime
from dotenv import load_dotenv
import os
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
import pytz
import requests

def to_brasilia(iso_utc_str):
    if not iso_utc_str:
        return "Data/Hora indefinida"
    utc_dt = datetime.strptime(iso_utc_str, '%Y-%m-%dT%H:%M:%SZ')
    utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
    brasilia_tz = pytz.timezone('America/Sao_Paulo')
    brasilia_dt = utc_dt.astimezone(brasilia_tz)
    return brasilia_dt.strftime('%d/%m/%Y %H:%M:%S') + " Horário de Brasília"

def format_championship_name(match):
    league_name = match.get('league', {}).get('name', '')
    series_name = match.get('serie', {}).get('name', '')
    tournament_name = match.get('tournament', {}).get('name', '')
    parts = [league_name, series_name]
    base_name = ' '.join([part for part in parts if part])
    if tournament_name:
        championship = f"{base_name} - {tournament_name}"
    else:
        championship = base_name
    return championship

def extract_teams(opponents):
    if len(opponents) >= 2:
        team1 = opponents[0]['opponent']['name']
        team2 = opponents[1]['opponent']['name']
    else:
        team1 = "Time 1 indefinido"
        team2 = "Time 2 indefinido"
    return team1, team2

class ChatRepository:
    def __init__(self):
        self.model_name = "gpt-4o-mini"
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openrouter_url = os.getenv('OPENROUTER_BASE_URL')
        self.temperature = 0.4
        self.pandascore_api_key = os.getenv('PANDASCORE_API_KEY')
        self.pandascore_furia_id = '124530'
        self.pandascore_cs2_id = '3'
        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.openrouter_api_key,
            openai_api_base=self.openrouter_url
        )
        self.intent_prompt = PromptTemplate(
            input_variables=["user_input"],
            template=(
                "Classifique a intenção do usuário a partir da mensagem abaixo, respondendo apenas com uma das opções: "
                "'last_matches', 'next_matches', 'live_matches', 'current_line', 'chat'.\n\n"
                "Alguns exemplos:\n"
                "- \"Qual a lineup da FURIA?\" => current_line\n"
                "- \"Quem são os jogadores da FURIA?\" => current_line\n"
                "- \"Últimos jogos da FURIA\" => last_matches\n"
                "- \"Jogos anteriores da FURIA\" => last_matches\n"
                "- \"Quando é o próximo jogo da FURIA?\" => next_matches\n"
                "- \"Está tendo jogo agora?\" => live_matches\n"
                "- \"Quanto ta o jogo agora?\" => live_matches\n"
                "- Qualquer outra pergunta: => chat\n\n"
                "Mensagem: {user_input}"
            )
        )
        self.intent_chain = self.intent_prompt | self.llm
        self.context_functions = {
            "last_matches": {"context": "Partidas Anteriores", "function": self.get_last_matches},
            "next_matches": {"context": "Próximas Partidas", "function": self.get_next_matches},
            "live_matches": {"context": "Partidas ao Vivo", "function": self.get_live_matches},
            "current_line": {"context": "Lineup Atual", "function": self.get_current_line},
        }

    def _fetch_matches(self, endpoint, params):
        url = f'https://api.pandascore.co/matches/{endpoint}'
        headers = {'Authorization': f'Bearer {self.pandascore_api_key}'}
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        return data if isinstance(data, list) else []

    def get_last_matches(self):
        params = {
            'filter[opponent_id]': self.pandascore_furia_id,
            'page[size]': 10,
            'filter[videogame]': self.pandascore_cs2_id
        }
        data = self._fetch_matches('past', params)
        if not data:
            return "Não foram encontradas partidas anteriores."
        matches = []
        for idx, match in enumerate(data):
            team1, team2 = extract_teams(match.get('opponents', []))
            winner = match.get('winner')
            winner_name = winner['name'] if winner else "Indefinido"
            start_time = to_brasilia(match.get('begin_at'))
            end_time = to_brasilia(match.get('end_at'))
            championship = format_championship_name(match)
            score = f"{match['results'][0]['score'] if match.get('results') else "Indefinido"}  x {match['results'][1]['score']}" if match.get('results') else "Indefinido"
            matches.append(
                f"======================================================\n"
                f"Partida {idx}\n\n"
                f"Times: {team1} x {team2}\n"
                f"Vencedor: {winner_name}\n"
                f"Campeonato: {championship}\n"
                f"Início: {start_time}\n"
                f"Fim: {end_time}\n"
                f"Placar: {score}\n"
                f"======================================================\n\n"
            )
        return (
            "LISTA NUMERADA DE PARTIDAS, QUANTO MENOR O NÚMERO, MAIS RECENTE A PARTIDA (0 FOI A ÚLTIMA PARTIDA DA FURIA):\n\n"
            + ''.join(matches)
        )

    def get_live_matches(self):
        params = {
            'filter[videogame]': self.pandascore_cs2_id,
            'filter[opponent_id]': self.pandascore_furia_id,
        }
        data = self._fetch_matches('running', params)
        if not data:
            return "PARTIDA EM ANDAMENTO:\n\nNão está havendo partida no momento!"
        matches = []
        for match in data:
            team1, team2 = extract_teams(match.get('opponents', []))
            championship = format_championship_name(match)
            matches.append(
                f"======================================================\n"
                f"Partida em Andamento\n\n"
                f"Times: {team1} x {team2}\n"
                f"Campeonato: {championship}\n"
                f"======================================================\n\n"
            )
        return "PARTIDA EM ANDAMENTO:\n\n" + ''.join(matches)

    def get_next_matches(self):
        params = {
            'filter[videogame]': self.pandascore_cs2_id,
            'page[size]': 10,
            'filter[opponent_id]': self.pandascore_furia_id,
        }
        data = self._fetch_matches('upcoming', params)
        if not data:
            return "PRÓXIMAS PARTIDAS:\n\nNenhuma partida agendada no momento."
        matches = []
        for match in data:
            team1, team2 = extract_teams(match.get('opponents', []))
            scheduled_time = to_brasilia(match.get('scheduled_at'))
            championship = format_championship_name(match)
            matches.append(
                f"======================================================\n"
                f"Partida Agendada\n\n"
                f"Times: {team1} x {team2}\n"
                f"Campeonato: {championship}\n"
                f"Horário: {scheduled_time}\n"
                f"======================================================\n\n"
            )
        return "PRÓXIMAS PARTIDAS:\n\n" + ''.join(matches)

    def get_current_line(self):
        url = 'https://api.pandascore.co/players'
        headers = {'Authorization': f'Bearer {self.pandascore_api_key}'}
        params = {
            'filter[videogame_id]': self.pandascore_cs2_id,
            'filter[team_id]': self.pandascore_furia_id,
        }
        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        if not isinstance(data, list) or not data:
            return "ATUAIS JOGADORES (LineUp da equipe de CS2):\n\nNão foi possível encontrar a lineup atual da FURIA."
        players = []
        for idx, player in enumerate(data):
            full_name = f"{player.get('first_name', '')} {player.get('last_name', '')}".strip()
            nickname = player.get('name', 'Apelido não disponível')
            nationality = player.get('nationality', 'Nacionalidade não disponível')
            players.append(
                f"======================================================\n"
                f"Jogador {idx + 1}\n\n"
                f"Nome: {full_name}\n"
                f"Nickname: {nickname}\n"
                f"Nacionalidade: {nationality}\n"
                f"======================================================\n\n"
            )
        return "ATUAIS JOGADORES (LineUp da equipe de CS2):\n\n" + ''.join(players)

    def detect_intent(self, user_input: str) -> str:
        response = self.intent_chain.invoke({"user_input": user_input})
        intent = response.content.strip().lower()
        if intent not in self.context_functions and intent != "chat":
            return "chat"
        return intent

    def chat(self, question: str, history: list = []) -> str:
        intent = self.detect_intent(question)
        context = ""
        if intent in self.context_functions:
            context = self.context_functions[intent]["function"]()

        formatted_history = []
        for msg in history:
            if msg['type'] == "AI":
                formatted_history.append(AIMessage(content=msg['message']))
            else:
                formatted_history.append(HumanMessage(content=msg['message']))

        base_prompt = SystemMessage(content=f"""
            Você é o chatbot oficial e carismático da FURIA Esports, especializado no time de CS2.

            ⚠️ Instruções Importantes:
            - Utilize exclusivamente as informações fornecidas no contexto abaixo, provenientes da API da PandaScore.
            - Em hipótese alguma, invente ou suponha informações que não estejam presentes no contexto.
            - Se uma informação solicitada não estiver disponível no contexto, responda claramente que os dados não estão disponíveis no momento.
            - Nunca afirme que não possui acesso a informações; sempre baseie suas respostas no contexto fornecido.
            - Não utilize markdown para nada, NEM para negrito ou itálico; utilize apenas texto puro.                        
            - O Nicholas Nogueira - guerri não faz mais parte do time; ignore qualquer referência a ele, mesmo que presente no contexto.

            🎯 Diretrizes de Resposta:
            - Adote um tom amigável, divertido e alinhado com a identidade da FURIA.
            - Utilize emojis relacionados a esports e à FURIA para tornar a conversa mais envolvente: 🕹️, 🎮, 🏆, 💪, 🔥, 👾, 🎉, 🤖, 😎, 🐯, 🐆.
            - Apresente informações de forma clara, objetiva e com espaçamento adequado entre parágrafos.
            - Evite o uso de markdown; utilize apenas texto puro.
            - Para listas, como a lineup atual, utilize tópicos numerados com emojis de números.
            - Utilize emojis de números para listas, como: 1️⃣, 2️⃣, 3️⃣, 4️⃣, 5️⃣, 6️⃣.
            - Para separar seções, utilize emojis de separação, como: ➡️, 🔽, 🔼.
            - Utilize emojis de bandeira para nacionalidades, como: 🇧🇷, 🇺🇸, 🇦🇷, etc.
            - Utilize emojis de time para representar a FURIA, como: 🐯, 🐆.
            - Não utilize markdown para nada, nem para negrito ou itálico; utilize apenas texto puro.
            - Não utilize traços ou underscores para separar palavras; prefira espaços normais.

            👤 Informações Adicionais:
            - Caso o usuário pergunte quem criou este chatbot, informe que foi desenvolvido por Matheus Castilho.

            🔗 Redes Sociais e Links Úteis:
            - Site Oficial: https://www.furia.gg/
            - Instagram: @furiagg

            📄 Contexto Disponível:
            {context}
            """)


        messages = [base_prompt] + formatted_history + [HumanMessage(content=question)]
        response = self.llm.invoke(messages)
        return response.content
