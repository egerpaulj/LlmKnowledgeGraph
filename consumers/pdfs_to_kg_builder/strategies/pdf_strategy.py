import logging

from pathlib import Path
from typing import Generator
from PyPDF2 import PdfReader
from strategies.document_strategy import DocumentProcessorStrategyBase, DocumentPage

class PdfProcessorStrategy(DocumentProcessorStrategyBase):
        
    def process(self, file_path: str) -> Generator[DocumentPage, None, None]:
        file = Path(file_path)
        try:
            reader = PdfReader(str(file))
            logging.info(f"reading file: {file.name}")
            for idx, page in enumerate(reader.pages, start=1):
                try:
                    text = page.extract_text() or ""
                except Exception as e:
                    logging.warning("Failed to extract text from %s page %d: %s", file.name, idx, e)
                    text = ""
                    
                if text:
                    title = self.parse_title(text=text, file_name=file.name)
                    words = text.split()
                    
                    for i in range(0, len(words), DocumentProcessorStrategyBase.CHUNK_WORD_SIZE):
                        text = ' '.join(words[i:i + DocumentProcessorStrategyBase.CHUNK_WORD_SIZE])
                        if text.strip():
                            yield DocumentPage(title=title, text=text)
        except Exception as e:
            logging.error("Failed to read %s: %s", file.name, e)
