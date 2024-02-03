from abc import ABC, abstractmethod


class ServiceBase(ABC):
    @abstractmethod
    def get(self, id):
        pass

    @abstractmethod
    def list(self, limit, offset):
        pass

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def update(self, id, data):
        pass

    @abstractmethod
    def delete(self, id):
        pass
