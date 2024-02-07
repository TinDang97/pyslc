from fastapi import APIRouter, Depends
from fastapi.exception_handlers import HTTPException
from fastapi.responses import StreamingResponse

from sqlalchemy.orm import Session

from app.schema.chat import (
    ChatCreatePayload,
    ChatResponsePayload,
    AgentChatCreatePayload,
    AgentChatResponse,
)
from app.services.chat import ChatService
from app.services.collection import CollectionService
from app.repository.collection import CollectionRepository
from app.services.knowledge import KnowledgeService
from app.repository.knowledge import KnowledgeRepository
from app.databases.database import database_client

router = APIRouter(prefix="/chat", tags=["chat"])


def get_service(session: Session = Depends(database_client.get_session)) -> ChatService:
    return ChatService(
        collection_service=CollectionService(
            collection_repository=CollectionRepository(),
            knowledge_service=KnowledgeService(
                repository=KnowledgeRepository(), session=session
            ),
            session=session,
        )
    )


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


@router.get("/stream/")
def stream_chat(
    session_id: str, message: str, service: ChatService = Depends(get_service)
):
    response = service.stream_chat(session_id, message)
    return StreamingResponse(response, media_type="text/plain")
