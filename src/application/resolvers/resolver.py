from abc import ABC, abstractmethod

from src.domen.models.task import Task


class ResolverInterface(ABC):

    @abstractmethod
    def resolve(self, task: Task):
        pass
