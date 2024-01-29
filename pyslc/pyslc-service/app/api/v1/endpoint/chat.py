from fastapi import APIRouter, Depends
from fastapi.exception_handlers import HTTPException

from app.core.schema.chat import ChatCreate, ChatResponse, CreateQueryRequestPayload
from app.core.llm.zep import ZepEngine
from app.core.chat.storage import ChatStorage


router = APIRouter(prefix="/chat", tags=["chat"])
storage = ChatStorage[ZepEngine]()


@router.post("/", response_model=ChatResponse)
def create_chat(chat: CreateQueryRequestPayload):
    doc = chat.document
    name = chat.name

    if name in storage:
        return

    storage.add(name, ZepEngine(name, doc))


@router.post("/{name}", response_model=ChatResponse)
def chat(name: str, chat: ChatCreate = Depends()):
    engine: ZepEngine = storage.get(name)
    if not engine:
        raise HTTPException(status_code=404, detail="Chat not found")
    response = engine.query(chat.message)
    return response
