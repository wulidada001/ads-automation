from abc import ABC, abstractmethod
from core.context import TaskContext

class BaseTask(ABC):
    @abstractmethod
    def run(self, ctx: TaskContext):
        pass