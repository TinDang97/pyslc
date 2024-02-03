from fastapi import APIRouter
from app.schema.knowledge import KnowledgeBasePayload, KnowledgeBaseResponse

router = APIRouter()


@router.get("", response_model=KnowledgeBaseResponse)
async def get_knowledge():
    return {"knowledge": "This is the knowledge endpoint from the chat module."}


@router.post("", status_code=201)
async def post_knowledge(
    payload: KnowledgeBasePayload,
):
    return {"knowledge": "This is the knowledge endpoint from the chat module."}


@router.put("", status_code=200)
async def put_knowledge(
    payload: KnowledgeBasePayload,
):
    return {"knowledge": "This is the knowledge endpoint from the chat module."}
