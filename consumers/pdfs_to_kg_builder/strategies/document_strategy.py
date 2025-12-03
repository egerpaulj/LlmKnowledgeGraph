from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Generator, Optional
import re

@dataclass
class DocumentPage:
    title: str
    text: str
    page_index: Optional[int] = None

class DocumentProcessorStrategyBase(ABC):
    @abstractmethod
    def process(self, file_path: str) -> Generator[DocumentPage, None, None]:
        raise NotImplementedError
    
    CHUNK_WORD_SIZE = 1000
    
    def parse_title(self, text: str, file_name: str) -> str:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        
        title = file_name
        for ln in lines[:6]:
            if re.search(r'chapter\s+\d+', ln, re.I):
                title = ln
                break
            if re.search(r'^\s*title[:\-\s]', ln, re.I):
                title = ln
                break
            if ln.isupper() and 3 <= len(ln) <= 200 and len(ln.split()) <= 12:
                title = ln
                break
            if ln.istitle() and len(ln.split()) <= 10:
                title = ln
                break
            
        return title
