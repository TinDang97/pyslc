from abc import ABC, abstractmethod


class ServiceBase(ABC):
    @abstractmethod
    def get(self, uid):
        pass

    @abstractmethod
    def list(self, limit, offset):
        pass

    @abstractmethod
    def create(self, data, created_by):
        pass

    @abstractmethod
    def update(self, uid, data, updated_by):
        pass

    @abstractmethod
    def delete(self, uid, deleted_by):
        pass
