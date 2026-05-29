import os
import pytest
from unittest.mock import patch, MagicMock

import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
from src.scripts.utils.knowledge_base_indexer import index_markdown_files

@patch("src.scripts.utils.knowledge_base_indexer.Chroma", autospec=True)
@patch("src.scripts.utils.knowledge_base_indexer.SentenceTransformerEmbeddings", autospec=True)
def test_index_markdown_files(mock_embed, mock_chroma, tmp_path):
    # Setup dummy data dir
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    
    # Create a test markdown file
    md_content = """# Test Title
This is some test content under a header.
## Subtitle
And this is subtitle content. We will make it quite long. """ + ("bla " * 300)
    
    md_file = data_dir / "test.md"
    md_file.write_text(md_content, encoding="utf-8")
    
    db_path = str(tmp_path / "chroma_db")
    
    # Run the indexer function
    index_markdown_files(str(data_dir), db_path)
    
    # Assertions
    mock_embed.assert_called_once_with(model_name="all-MiniLM-L6-v2")
    
    # Retrieve the documents passed to from_documents
    call_args = mock_chroma.from_documents.call_args
    assert call_args is not None, "Chroma.from_documents was not called"
    
    docs, embedding_fn = call_args[0]
    kwargs = call_args[1]
    
    assert kwargs.get("persist_directory") == db_path
    
    # Verify documents were correctly chunked with metadata
    assert len(docs) > 0
    # Because of recursion size 1000 and the huge "bla" block, it should be > 1 chunk
    
    # Verify metadata fields injected
    for doc in docs:
        assert "source_file" in doc.metadata
        assert doc.metadata["source_file"] == "test.md"
        # Since it splits by header, either Header 1 or Header 2 should be in some metadata
        assert "Header 1" in doc.metadata or "Header 2" in doc.metadata or "Header 3" in doc.metadata
