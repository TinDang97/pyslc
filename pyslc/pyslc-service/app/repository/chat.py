from app.repository.base import BaseRepository
from app.model.chat import Chat


class ChatRepository(BaseRepository[Chat]):
    """
    Chat repository class.
    """

    entity = Chat

    def get_by_session_id(self, session_id: str) -> Chat:
        """
        Get a single chat by its session ID.

        :param session_id: session ID
        :return: chat
        """
        return (
            self.session.query(self.entity)
            .filter(self.entity.session_id == session_id)
            .one()
        )
