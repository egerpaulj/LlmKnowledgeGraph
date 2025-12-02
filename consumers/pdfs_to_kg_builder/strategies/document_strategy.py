from abc import ABC, abstractmethod
from typing import Any

class DocumentProcessorStrategy(ABC):
    @abstractmethod
    def process(self, file_path: str) -> Any:
        pass
