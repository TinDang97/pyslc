from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi.responses import StreamingResponse

from app.core.container import Container
from dependency_injector.wiring import Provide, inject

from app.schema.chat import (
    AgentChatCreatePayload,
    AgentChatResponse,
    ChatCreatePayload,
    ChatResponsePayload,
)
from app.services.chat import ChatService

router = APIRouter(tags=["chat"])
TEST = "test"


@router.post(
    "/agent", response_model=AgentChatResponse, status_code=status.HTTP_201_CREATED
)
@inject
def create_agent_chat(
    payload: AgentChatCreatePayload,
    service: ChatService = Depends(Provide[Container.chat_service]),
) -> AgentChatResponse:
    try:
        return service.create_chat_agent(payload, TEST)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post(
    "/", response_model=ChatResponsePayload, status_code=status.HTTP_201_CREATED
)
@inject
def create_chat(
    payload: ChatCreatePayload,
    service: ChatService = Depends(Provide[Container.chat_service]),
) -> ChatResponsePayload:
    try:
        return service.chat(payload)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/stream/", status_code=status.HTTP_200_OK)
@inject
def stream_chat(
    payload: ChatCreatePayload,
    service: ChatService = Depends(Provide[Container.chat_service]),
):
    response = service.stream_chat(payload)
    return StreamingResponse(response, media_type="text/plain")
