from fastapi import APIRouter

from app.core.chat.chat import ChatHandler
from app.core.schema.chat import ChatRequest, ChatResponse
from app.settings import settings


router = APIRouter(prefix="/chat", tags=["chat"])

chat_handler = ChatHandler(api_key=settings.openai_api_key, model=settings.openai_model)


@router.post("/", response_model=ChatResponse)
def create_chat(chat: ChatRequest):
    if chat.session_id:
        session_id = chat.session_id
    else:
        session_id = chat_handler.create_chat(chat.message)

    response = chat_handler.get_response(session_id=session_id, message=chat.message)
    response = ChatResponse(
        session_id=response["session_id"], response=response["response"]
    )
    return response
