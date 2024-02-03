# Created by tindang at 04/02/2024

from app.schema.chat import ChatCreatePayload, ChatResponsePayload
from app.services.base import ServiceBase
from app.services.collection import CollectionService


class ChatService(ServiceBase):
    def get(self, id):
        pass

    def list(self, limit, offset):
        pass

    def create(self, data):
        pass

    def update(self, id, data):
        pass

    def delete(self, id):
        pass

    def __init__(self, collection_service: CollectionService):
        super().__init__()
        self.collection_service: CollectionService = collection_service

    def create_engine(self, collection_id: str):
        """
        :param collection_id:
        :type collection_id:
        :return:
        :rtype:

        :raises:
            ValueError: not found collection or knowledge base
        """
        return self.collection_service.create_engine(collection_id)

    def create_chat(self, payload: ChatCreatePayload) -> ChatResponsePayload:
        collection = self.collection_service.get(payload.collection_id)

        if not collection:
            raise ValueError("Collection not found")

        try:
            self.create_engine(payload.collection_id)
        except Exception as e:
            raise ValueError("Create engine failed. Reason: {}".format(str(e)))

        try:
            message = self.collection_service.query(
                payload.collection_id, payload.message
            )
        except ValueError as e:
            raise ValueError("Query failed. Reason: {}".format(str(e)))

        return ChatResponsePayload(
            message=message,
            collection_id=collection.id,
            collection_name=collection.name,
        )
