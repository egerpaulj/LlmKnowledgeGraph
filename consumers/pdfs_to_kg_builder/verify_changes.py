import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add the parent directory to sys.path to import the modules
sys.path.append('/home/user/src/LlmKnowledgeGraph/consumers/pdfs_to_kg_builder')

from strategies.pdf_strategy import PdfProcessorStrategy
from strategies.epub_strategy import EpubProcessorStrategy
from pdf_consumer import PdfConsumer

class TestDocumentStrategies(unittest.TestCase):

    @patch('strategies.pdf_strategy.PdfReader')
    def test_pdf_strategy(self, mock_pdf_reader):
        # Setup mock
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Chapter 1\nThis is some text."
        mock_pdf_reader.return_value.pages = [mock_page]

        strategy = PdfProcessorStrategy()
        results = list(strategy.process("test.pdf"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "Chapter 1")
        self.assertEqual(results[0][1], "Chapter 1\nThis is some text.")

    @patch('strategies.epub_strategy.epub.read_epub')
    def test_epub_strategy(self, mock_read_epub):
        # Setup mock
        mock_book = MagicMock()
        mock_book.get_metadata.return_value = [[('Test Book',)]]
        
        mock_item = MagicMock()
        mock_item.get_type.return_value = 9 # ITEM_DOCUMENT
        mock_item.get_content.return_value = b"<html><body><p>Some content</p></body></html>"
        mock_item.get_name.return_value = "chapter1.html"
        
        mock_book.get_items.return_value = [mock_item]
        mock_read_epub.return_value = mock_book

        strategy = EpubProcessorStrategy()
        results = list(strategy.process("test.epub"))

        self.assertEqual(len(results), 1)
        self.assertEqual(results[0][0], "Test Book")
        self.assertEqual(results[0][1], "Some content")

    @patch('pdf_consumer.RelationshipInferenceProvider')
    @patch('pdf_consumer.KnowledgeGraph')
    @patch('strategies.pdf_strategy.PdfReader')
    def test_pdf_consumer_integration(self, mock_pdf_reader, mock_kg, mock_rip):
        # Setup mocks
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Chapter 1\nThis is some text."
        mock_pdf_reader.return_value.pages = [mock_page]
        
        consumer = PdfConsumer("host", "model", "mlflow", "sys", "user")
        
        # Mock file system
        with patch('pathlib.Path.exists', return_value=True), \
             patch('pathlib.Path.iterdir') as mock_iterdir:
            
            mock_file = MagicMock()
            mock_file.is_file.return_value = True
            mock_file.name = "test.pdf"
            mock_file.suffix = ".pdf"
            mock_file.__str__.return_value = "test.pdf"
            
            mock_iterdir.return_value = [mock_file]
            
            consumer.start("dummy_folder")
            
            # Verify that relationships were extracted and added to graph
            mock_rip.return_value.get_relationships.assert_called()
            consumer.graph.add_or_merge_relationships.assert_called()

if __name__ == '__main__':
    unittest.main()
