import logging
from pathlib import Path
from typing import Generator, Tuple
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from .document_strategy import DocumentProcessorStrategy

class EpubProcessorStrategy(DocumentProcessorStrategy):
    def process(self, file_path: str) -> Generator[Tuple[str, str], None, None]:
        file = Path(file_path)
        try:
            book = epub.read_epub(str(file))
            logging.info(f"reading file: {file.name}")
            
            # Try to get title from metadata
            title = file.name
            if book.get_metadata('DC', 'title'):
                title = book.get_metadata('DC', 'title')[0][0]

            for item in book.get_items():
                if item.get_type() == ebooklib.ITEM_DOCUMENT:
                    try:
                        content = item.get_content()
                        soup = BeautifulSoup(content, 'html.parser')
                        text = soup.get_text()
                        if text.strip():
                            yield title, text
                    except Exception as e:
                        logging.warning("Failed to extract text from %s item %s: %s", file.name, item.get_name(), e)
        except Exception as e:
            logging.error("Failed to read %s: %s", file.name, e)
