from abc import ABC, abstractmethod

class IRepository(ABC):
    @abstractmethod
    def find(self, id):
        pass
    @abstractmethod
    def findAll(self):
        pass
    @abstractmethod
    def create(self, obj):
        pass
    @abstractmethod
    def update(self, id, obj):
        pass
    @abstractmethod
    def destroy(self, id):
        pass
