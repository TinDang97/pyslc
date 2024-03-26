from app.core.container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status

from app.schema.knowledge import (
    KnowledgeBaseCreatePayload,
    KnowledgeBaseUpdatePayload,
    CollectionKnowledgesResponse,
    KnowledgeBaseResponse,
)
from app.schema.query import ListResponse, QueryParams
from app.services.knowledge import KnowledgeService

router = APIRouter()
TEST_USER = "test-user"


@router.post(
    "/", response_model=KnowledgeBaseResponse, status_code=status.HTTP_201_CREATED
)
@inject
def create_knowledge_base(
    payload: KnowledgeBaseCreatePayload,
    service: KnowledgeService = Depends(Provide[Container.knowledge_service]),
):
    return service.create_knowledge_base(payload, TEST_USER)


@router.get(
    "/{uid}", response_model=KnowledgeBaseResponse, status_code=status.HTTP_200_OK
)
@inject
def get_knowledge_base(
    uid: str, service: KnowledgeService = Depends(Provide[Container.knowledge_service])
):
    return service.get_knowledge(uid)


@router.get(
    "/",
    response_model=ListResponse[KnowledgeBaseResponse],
    status_code=status.HTTP_200_OK,
)
@inject
def get_knowledge_bases(
    query: QueryParams = Depends(QueryParams),
    service: KnowledgeService = Depends(Provide[Container.knowledge_service]),
):
    return service.get_knowledges(query)


@router.get(
    "/collection/{collection_id}",
    response_model=CollectionKnowledgesResponse,
    status_code=status.HTTP_200_OK,
)
@inject
def get_knowledge_bases_by_collection(
    collection_id: str,
    query: QueryParams = Depends(QueryParams),
    service: KnowledgeService = Depends(Provide[Container.knowledge_service]),
):
    return service.get_knowledge_bases_by_collection(collection_id, query)


@router.put("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def update_knowledge_base(
    uid: str,
    payload: KnowledgeBaseUpdatePayload,
    service: KnowledgeService = Depends(Provide[Container.knowledge_service]),
):
    return service.update_knowledge_base(uid, payload, TEST_USER)


@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT)
@inject
def delete_knowledge_base(
    uid: str,
    service: KnowledgeService = Depends(Provide[Container.knowledge_service]),
):
    return service.delete_knowledge_base(uid, TEST_USER)
