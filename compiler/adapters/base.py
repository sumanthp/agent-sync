from abc import ABC, abstractmethod
from ..models import AgentRule

class BaseAdapter(ABC):
    @abstractmethod
    def translate(self, rule: AgentRule) -> dict:
        """
        Translates a universal rule into a dictionary of {file_path: content}
        """
        pass
