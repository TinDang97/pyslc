from fastapi import APIRouter, Depends
from fastapi.exception_handlers import HTTPException
from sqlalchemy.orm import Session

from app.schema.chat import ChatCreatePayload, ChatResponsePayload
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


@router.post("/", response_model=ChatResponsePayload, status_code=201)
def create_chat(
    payload: ChatCreatePayload, service: ChatService = Depends(get_service)
):
    try:
        return service.chat(payload)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/engine/{collection_id}", status_code=200)
def create_engine(collection_id: str, service: ChatService = Depends(get_service)):
    try:
        service.create_engine(collection_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
