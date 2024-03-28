# Created by tindang at 04/02/2024

from app.core.container import Container
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException

from app.schema.collection import (
    CollectionCreatePayload,
    CollectionResponse,
    UpdateCollectionPayload,
)
from app.schema.query import ListResponse, QueryParams
from app.services.collection import CollectionService

router = APIRouter()
TEST_USER = "test-user"


@router.post("/", response_model=CollectionResponse, status_code=201)
@inject
def create_collection(
    payload: CollectionCreatePayload,
    service: CollectionService = Depends(Provide[Container.collection_service]),
):
    try:
        return service.create(payload, TEST_USER)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/", response_model=ListResponse[CollectionResponse], status_code=200)
@inject
def list_collections(
    query: QueryParams = Depends(QueryParams),
    service: CollectionService = Depends(Provide[Container.collection_service]),
):
    return service.list(query)


@router.get("/{uid}", response_model=CollectionResponse, status_code=200)
@inject
def get_collection(
    uid: str,
    service: CollectionService = Depends(Provide[Container.collection_service]),
):
    return service.get(uid)


@router.get("/name/{name}", response_model=CollectionResponse, status_code=200)
@inject
def find_collection_by_name(
    name: str,
    service: CollectionService = Depends(Provide[Container.collection_service]),
):
    return service.find_by_name(name)


@router.put("/{uid}", response_model=CollectionResponse, status_code=200)
@inject
def update_collection(
    uid: str,
    payload: UpdateCollectionPayload,
    service: CollectionService = Depends(Provide[Container.collection_service]),
):
    return service.update(uid, payload, TEST_USER)


@router.delete("/{uid}", status_code=204)
@inject
def delete_collection(
    uid: str,
    service: CollectionService = Depends(Provide[Container.collection_service]),
):
    return service.delete(uid, TEST_USER)
