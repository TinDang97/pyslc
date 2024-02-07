from fastapi import APIRouter, Depends
from fastapi.exception_handlers import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.databases.database import database_client
from app.schema.chat import (
    AgentChatCreatePayload,
    AgentChatResponse,
    ChatCreatePayload,
    ChatResponsePayload,
)
from app.services.chat import ChatService

router = APIRouter(tags=["chat"])


def get_service(session: Session = Depends(database_client.get_session)) -> ChatService:
    return ChatService(session=session)


@router.post("/agent", response_model=AgentChatResponse, status_code=201)
def create_agent_chat(
    payload: AgentChatCreatePayload, service: ChatService = Depends(get_service)
):
    try:
        return service.create_chat_agent(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/", response_model=ChatResponsePayload, status_code=201)
def create_chat(
    payload: ChatCreatePayload, service: ChatService = Depends(get_service)
):
    try:
        return service.chat(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/stream/")
def stream_chat(
    payload: ChatCreatePayload, service: ChatService = Depends(get_service)
):
    response = service.stream_chat(payload)
    return StreamingResponse(response, media_type="text/plain")
