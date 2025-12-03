import logging
from pathlib import Path
from typing import Generator
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from strategies.document_strategy import DocumentPage, DocumentProcessorStrategyBase

class EpubProcessorStrategy(DocumentProcessorStrategyBase):
    def process(self, file_path: str) -> Generator[DocumentPage, None, None]:
        file = Path(file_path)
        try:
            book = epub.read_epub(str(file))
            logging.info(f"reading file: {file.name}")
            
            title = None
            if book.get_metadata('DC', 'title'):
                title = book.get_metadata('DC', 'title')[0][0]
                
            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    try:
                        content = item.get_content()
                        soup = BeautifulSoup(content, 'html.parser')
                        text = soup.get_text()
                        
                        if not title:
                            title = self.parse_title(text=text, file_name=file.name)
                            
                        words = text.split()
                        chunk_size = 500
                        for i in range(0, len(words), DocumentProcessorStrategyBase.CHUNK_WORD_SIZE):
                            text = ' '.join(words[i:i + DocumentProcessorStrategyBase.CHUNK_WORD_SIZE])
                            if text.strip():
                                yield DocumentPage(title=title, text=text)
                    except Exception as e:
                        logging.warning("Failed to extract text from %s item %s: %s", file.name, item.get_name(), e)
        except Exception as e:
            logging.error("Failed to read %s: %s", file.name, e)
