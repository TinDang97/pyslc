from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.databases.database import database_client
from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
    KnowledgeBaseListPayloadResponse,
    KnowledgeBaseResponse,
)
from app.schema.query import QueryParams
from app.services.knowledge import KnowledgeService

router = APIRouter()


def get_service(db: Session = Depends(database_client.get_session)) -> KnowledgeService:
    return KnowledgeService(session=db)


@router.post("/", response_model=KnowledgeBaseResponse, status_code=201)
def create_knowledge_base(
    payload: KnowledgeBaseCreatePayload,
    service: KnowledgeService = Depends(get_service),
):
    return service.create_knowledge_base(payload)


@router.get("/{id}", response_model=KnowledgeBaseResponse, status_code=200)
def get_knowledge_base(id: str, service: KnowledgeService = Depends(get_service)):
    return service.get_knowledge_base(id)


@router.get("/", response_model=List[KnowledgeBaseResponse], status_code=200)
def get_knowledge_bases(
    query: QueryParams = Depends(QueryParams),
    service: KnowledgeService = Depends(get_service),
):
    return service.get_knowledge_bases(query.limit, query.offset)


@router.get(
    "/collection/{collection_id}",
    response_model=KnowledgeBaseListPayloadResponse,
    status_code=200,
)
def get_knowledge_bases_by_collection(
    collection_id: str,
    query: QueryParams = Depends(QueryParams),
    service: KnowledgeService = Depends(get_service),
):
    return service.get_knowledge_bases_by_collection(
        collection_id, query.limit, query.offset
    )
