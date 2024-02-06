# Created by tindang at 04/02/2024
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.databases.database import database_client
from app.repository.collection import CollectionRepository
from app.repository.knowledge import KnowledgeRepository
from app.schema.collection import (
    CollectionCreatePayload,
    CollectionWithKnowledgeResponse,
    UpdateCollectionPayload,
    CollectionResponse,
)
from app.schema.query import QueryParams
from app.services.collection import CollectionService
from app.services.knowledge import KnowledgeService

router = APIRouter()


def get_service(
    db: Session = Depends(database_client.get_session),
) -> CollectionService:
    return CollectionService(
        session=db,
        collection_repository=CollectionRepository(),
        knowledge_service=KnowledgeService(
            session=db, repository=KnowledgeRepository()
        ),
    )


@router.post("/", status_code=201)
def create_collection(
    payload: CollectionCreatePayload, service: CollectionService = Depends(get_service)
):
    return service.create(payload)


@router.get("/", response_model=List[CollectionResponse], status_code=200)
def list_collections(
    query: QueryParams = Depends(QueryParams),
    service: CollectionService = Depends(get_service),
):
    return service.list(query.limit, query.offset)


@router.get("/{id}", response_model=CollectionResponse, status_code=200)
def get_collection(id: str, service: CollectionService = Depends(get_service)):
    return service.get(id)


@router.get("/name/{name}", response_model=CollectionResponse, status_code=200)
def get_collection_by_name(
    name: str, service: CollectionService = Depends(get_service)
):
    return service.get_by_name(name)


@router.put("/{id}", response_model=CollectionResponse, status_code=200)
def update_collection(
    id: str,
    payload: UpdateCollectionPayload,
    service: CollectionService = Depends(get_service),
):
    return service.update(id, payload)


@router.delete("/{id}", status_code=204)
def delete_collection(id: str, service: CollectionService = Depends(get_service)):
    return service.delete(id)


@router.get(
    "/{collection_name}/knowledge",
    response_model=CollectionWithKnowledgeResponse,
    status_code=200,
)
def create_engine(
    collection_name: str, service: CollectionService = Depends(get_service)
):
    collection = service.get_by_name(collection_name)
    if not collection:
        raise HTTPException(status_code=404, detail="Collection not found")

    knowledge_parts = service.knowledge_service.get_knowledge_bases_by_collection(
        collection_name
    )
    return CollectionWithKnowledgeResponse(
        id=collection.id,
        name=collection.name,
        knowledge_content=knowledge_parts.data,
    )
