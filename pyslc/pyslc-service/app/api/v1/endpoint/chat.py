from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from app.core.container import Container
from app.schema.chat import (
    ChatCreatePayload,
    ChatCreateResponse,
    ChatListResponsePayload,
)
from app.schema.message import MessageResponsePayload, MessageSendPayload
from app.schema.query import QueryParams
from app.services.chat import ChatService

router = APIRouter(tags=["chat"])
TEST = "test"


@router.get("/", response_model=ChatListResponsePayload, status_code=status.HTTP_200_OK)
@inject
def get_chats(
    service: ChatService = Depends(Provide[Container.chat_service]),
    query: QueryParams = Depends(QueryParams),
) -> ChatListResponsePayload:
    return service.get_chats_by_user(TEST, query)


@router.post("/", status_code=status.HTTP_201_CREATED)
@inject
def create_agent_chat(
    payload: ChatCreatePayload,
    service: ChatService = Depends(Provide[Container.chat_service]),
) -> ChatCreateResponse:
    try:
        return service.create_chat(payload, TEST)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/chat",
    status_code=status.HTTP_201_CREATED,
    description="Send a message to a chat agent",
)
@inject
def chat(
    payload: MessageSendPayload,
    service: ChatService = Depends(Provide[Container.chat_service]),
) -> MessageResponsePayload:
    try:
        return service.chat(payload, TEST)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post(
    "/stream/",
    status_code=status.HTTP_200_OK,
    description="Stream a message to a chat agent",
)
@inject
def stream_chat(
    payload: MessageSendPayload,
    service: ChatService = Depends(Provide[Container.chat_service]),
):
    response = service.stream_chat(payload, TEST)
    return StreamingResponse(response, media_type="text/plain")
