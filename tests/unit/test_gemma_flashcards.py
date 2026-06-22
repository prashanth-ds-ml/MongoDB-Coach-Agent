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

    @patch("certcoach.gemma_flashcards.database")
    @patch("certcoach.gemma_flashcards.messagebox")
    def test_task_load_db_card_handles_connection_error(self, mock_messagebox, mock_database):
        # Configure database error
        mock_database.connection_error = Exception("Connection timed out")
        
        # Instantiate App with mocked Tk root
        mock_root = MagicMock()
        mock_root.after = lambda delay, callback: callback()
        with patch("certcoach.gemma_flashcards.FlashcardsApp.detect_ollama_and_models"):
            app = FlashcardsApp(mock_root)
        
        # Set mock helpers
        app.on_card_failed = MagicMock()
        
        # Run database load
        app.task_load_db_card("All Domains Combined (Default)")
        
        # Verify that messagebox.showerror was called instead of exiting
        mock_messagebox.showerror.assert_called_once()
        self.assertIn("Connection timed out", mock_messagebox.showerror.call_args[0][1])
        app.on_card_failed.assert_called_once()

    @patch("certcoach.gemma_flashcards.database")
    @patch("certcoach.gemma_flashcards.messagebox")
    def test_task_load_db_card_handles_empty_questions(self, mock_messagebox, mock_database):
        # Configure database connection success but empty results
        mock_database.connection_error = None
        mock_database.questions_col.find.return_value = []
        
        mock_root = MagicMock()
        mock_root.after = lambda delay, callback: callback()
        with patch("certcoach.gemma_flashcards.FlashcardsApp.detect_ollama_and_models"):
            app = FlashcardsApp(mock_root)
            
        app.on_card_failed = MagicMock()
        
        app.task_load_db_card("All Domains Combined (Default)")
        
        # Verify showwarning called for empty questions
        mock_messagebox.showwarning.assert_called_once()
        app.on_card_failed.assert_called_once()
