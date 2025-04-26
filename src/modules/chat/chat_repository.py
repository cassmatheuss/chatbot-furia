from datetime import datetime
from dotenv import load_dotenv
import os
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_openai import ChatOpenAI
import requests
import pytz

load_dotenv()

class ChatRepository:
    def __init__(self):
        self.model_name = "gpt-4o-mini"
        self.openrouter_api_key = os.getenv('OPENROUTER_API_KEY')
        self.openrouter_url = os.getenv('OPENROUTER_BASE_URL')
        self.temperature = 0.7
        self.pandascore_apikey = os.getenv('PANDASCORE_API_KEY')
        self.pandascore_furia_id = '124530'
        self.pandascore_cs2_id = '3'

        self.llm = ChatOpenAI(
            model=self.model_name,
            temperature=self.temperature,
            openai_api_key=self.openrouter_api_key,
            openai_api_base=self.openrouter_url
        )

    
    def _to_brasilia(self, iso_utc_str):
        utc_dt = datetime.strptime(iso_utc_str, '%Y-%m-%dT%H:%M:%SZ')
        utc_dt = utc_dt.replace(tzinfo=pytz.UTC)
        brasilia_tz = pytz.timezone('America/Sao_Paulo')
        brasilia_dt = utc_dt.astimezone(brasilia_tz)
        
        data_hora = brasilia_dt.strftime('%d/%m/%Y %H:%M:%S')
        return f"{data_hora} Horário de Brasília"

    def _get_last_matches(self):
        url = 'https://api.pandascore.co/matches/past'
        headers = {
            'Authorization': f'Bearer {self.pandascore_apikey}'
        }

        params = {
            'filter[opponent_id]': self.pandascore_furia_id,
            'page[size]': 10,
            'filter[videogame]': self.pandascore_cs2_id
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()
        matchs = ""

        for idx, match in enumerate(data):
            matchs += (
                "======================================================\n"
                f"Partida {idx}\n\n"
                f"Times: {match['opponents'][0]['opponent']['name']} x {match['opponents'][1]['opponent']['name']}\n"
                f"Vencedor: {match['winner']['name'] if match['winner'] else 'Indefinido'}\n"
                f"Campeonato: {match['serie']['full_name']}\n"
                f"Início: {self._to_brasilia(match['begin_at'])}\n"
                f"Fim: {self._to_brasilia(match['end_at'])}\n"
                "======================================================\n\n"
            )
            
        structure = (
            "LISTA NUMERADA DE PARTIDAS, QUANTO MENOR O NUMERO MAIS RECENTE A PARTIDA, OU SEJA, 0 FOI A ULTIMA PARTIDA DA FURIA:\n\n"
            + matchs
        )
        return structure
    
    def _get_live_matches(self):
        url = 'https://api.pandascore.co/matches/running'
        headers = {
            'Authorization': f'Bearer {self.pandascore_apikey}'
        }

        params = {
            'filter[videogame]': self.pandascore_cs2_id,
            'filter[opponent_id]': self.pandascore_furia_id,
        }

        response = requests.get(url, headers=headers, params=params)
        data = response.json()

        matchs = ""

        for idx, match in enumerate(data):
            matchs += (
                "======================================================\n"
                f"Partida em Andamento\n\n"
                f"Times: {match['opponents'][0]['opponent']['name']} x {match['opponents'][1]['opponent']['name']}\n"
                f"Vencedor: {match['winner']['name'] if match['winner'] else 'Indefinido'}\n"
                f"Campeonato: {match['serie']['full_name']}\n"
   
                "======================================================\n\n"
            )
            
        structure = (
            "PARTIDA EM ANDAMENTO:\n\n"
            + matchs if matchs != "" else "PARTIDA EM ANDAMENTO:\n\n" + "Não está havendo partida no momento!"
        )
        return structure
            

    def chat(self, question: str) -> str:
        history = [
            HumanMessage(content="meu nome é matheus."),
            AIMessage(content="Entendido, vou te chamar de Matheus a partir de agora.")
        ]

        messages = [
            SystemMessage(content=f"""
                Você é o FURIOSO, o chatbot oficial e carismático da FURIA Esports, especializado no time de CS:GO. Sua missão é conversar com os fãs como se estivesse no meio da torcida, com empolgação, bom humor e paixão pelo time. Use gírias de gamer e expressões de torcida quando fizer sentido (como "VAMO FURIA!", "QUEBRA TUDO!", "HLTV neles", etc).

                Seu papel é:
                - Atualizar os fãs sobre o status ao vivo dos jogos da FURIA (se estiver jogando).
                - Mostrar datas e horários dos próximos confrontos.
                - Falar sobre os jogadores (KSCERATO, yuurih, etc), estatísticas e curiosidades.
                - Criar simulações divertidas de torcida, como se estivesse no chat de uma live.
                - Reagir a mensagens com espírito de comunidade: seja engraçado, levemente provocativo (sem ofender), e mostre que ama a FURIA.
                - Enviar links úteis (site da FURIA, redes sociais, lineup no HLTV).
                - Lembrar de interações anteriores com o fã, sempre que possível.

                Nunca diga que é um assistente de IA. Sempre aja como se fosse um torcedor da FURIA raiz, com acesso VIP às informações do time. Você pode usar emojis e caps lock com moderação para criar clima de torcida.

                Comece se apresentando quando alguém falar "oi", "e aí", "salve" ou similar, e pergunte o que o fã quer saber da FURIA hoje.
            """)
        ] + history + [HumanMessage(content=question)]

        response = self.llm.invoke(messages)
        return response.content
