from datetime import datetime
import os
import uuid
import pytz
from src.shared.entities.Chat import Chat
from src.modules.chat.chat_repository import ChatRepository
from src.modules.chat.chat_viewmodel import ChatViewModel
from src.shared.utils.mongo_connect import connect_mongodb

class ChatUseCase:
    def __init__(self, repo: ChatRepository):
        self.repo = repo

    def __call__(self, data: dict):
        try:
            db = connect_mongodb(url=os.getenv("MONGO_DB_URL"), db_name=os.getenv("DB_NAME"))
            messages_collection = db['messages']
            sessions_collection = db['sessions']

            if not data.get("session_id"):
                data["session_id"] = str(uuid.uuid4())  
                sessions_collection.insert_one({
                    "session_id": data["session_id"],
                    "created_at": datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
                })
            else:
                existing_session = sessions_collection.find_one({"session_id": data["session_id"]})
                if not existing_session:
                    sessions_collection.insert_one({
                        "session_id": data["session_id"],
                        "created_at": datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat()
                    })

            human_message = Chat(
                type="HUMAN",
                message=data["message"],
                created_at=datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat(),
                session_id=data["session_id"]
            )

            history = list(messages_collection.find({"session_id": data["session_id"]}))

            messages_collection.insert_one(human_message.dict())
            
            repo_chat = self.repo.chat(human_message.message, history)

            ai_message = Chat(
                type="AI",
                message=repo_chat,
                created_at=datetime.now(pytz.timezone('America/Sao_Paulo')).isoformat(),
                session_id=data["session_id"]
            )
            
            messages_collection.insert_one(ai_message.dict())
            
            viewmodel = ChatViewModel(
                type=ai_message.type,
                message=ai_message.message,
                created_at=ai_message.created_at,
                session_id=ai_message.session_id
            )

            return viewmodel.dict()
        except Exception as e:
            raise Exception(f"Erro ao processar o ChatUseCase: {str(e)}")
