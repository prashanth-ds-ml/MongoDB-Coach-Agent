import unittest
from unittest.mock import MagicMock, patch
from certcoach.gemma_flashcards import DOMAINS, PROMPT_TEMPLATE, FlashcardsApp

class TestGemmaFlashcards(unittest.TestCase):
    def test_domains_contains_mandatory_categories(self):
        self.assertIn("All Domains Combined (Default)", DOMAINS)
        self.assertIn("CRUD Operations & PyMongo Syntax", DOMAINS)
        self.assertIn("Indexing & Performance (ESR, COLLSCAN vs IXSCAN)", DOMAINS)
        self.assertIn("Aggregation Framework Pipelines", DOMAINS)
        self.assertIn("Data Modeling Patterns & Limits", DOMAINS)

    def test_prompt_template_formatting(self):
        formatted = PROMPT_TEMPLATE.format(
            domain_focus="CRUD Operations",
            domain_desc="PyMongo connection details"
        )
        self.assertIn("CRUD Operations", formatted)
        self.assertIn("PyMongo connection details", formatted)
        self.assertIn("C100DEV", formatted)

    @patch("tkinter.Tk")
    @patch("certcoach.gemma_flashcards.FlashcardsApp.detect_ollama_and_models")
    def test_app_initialization(self, mock_detect, mock_tk):
        mock_root = MagicMock()
        mock_tk.return_value = mock_root
        
        # Instantiate App with mocked Tk root
        app = FlashcardsApp(mock_root)
        
        self.assertEqual(app.root, mock_root)
        self.assertFalse(app.loading)
        mock_detect.assert_called_once()
