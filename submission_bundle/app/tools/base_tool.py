from abc import ABC, abstractmethod


class BaseTool(ABC):

    @property
    @abstractmethod
    def definition(self):
        """
        Metadata exposed to the Planner.
        """
        pass

    @abstractmethod
    def execute(self, **kwargs):
        """
        Executes the tool.
        """
        pass