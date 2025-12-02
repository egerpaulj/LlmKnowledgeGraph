import logging
import re
from pathlib import Path
from typing import Generator, Tuple
from PyPDF2 import PdfReader
from .document_strategy import DocumentProcessorStrategy

class PdfProcessorStrategy(DocumentProcessorStrategy):
    def process(self, file_path: str) -> Generator[Tuple[str, str], None, None]:
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
                
                title = file.name
                if text:
                    lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
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
                
                yield title, text
        except Exception as e:
            logging.error("Failed to read %s: %s", file.name, e)
