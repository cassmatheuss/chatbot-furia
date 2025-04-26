import os
from src.shared.utils.mongo_connect import connect_mongodb


class HistoryRepository:
    def __init__(self):
        self.mongodb_url = os.getenv("MONGO_DB_URL")
        self.db_name = os.getenv("DB_NAME")
        self.db = connect_mongodb(self.mongodb_url, self.db_name)

    def get_messages_by_session_id(self, session_id: str):
        try:
            messages_collection = self.db["messages"]
            messages = list(messages_collection.find({"session_id": session_id}))

            for msg in messages:
                msg['_id'] = str(msg['_id'])

            return messages
        except Exception as e:
            raise Exception(f"Erro ao buscar mensagens: {str(e)}")
