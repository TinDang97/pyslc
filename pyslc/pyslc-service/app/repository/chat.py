from app.repository.base import BaseRepository
from app.model.chat import Chat


class ChatRepository(BaseRepository[Chat]):
    """
    Chat repository class.
    """

    def __init__(self):
        """
        Constructor.
        """
        super().__init__(Chat)

    def get_by_session_id(self, session, session_id: str) -> Chat:
        """
        Get a single chat by its session ID.

        :param session:
        :type session:
        :param session_id: session ID
        :return: chat
        """
        return (
            session.query(self.entity)
            .filter(self.entity.session_id == session_id)
            .one()
        )
