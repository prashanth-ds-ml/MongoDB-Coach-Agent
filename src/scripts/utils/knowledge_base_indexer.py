import os
import glob
from pathlib import Path

# Langchain imports
from langchain_text_splitters import MarkdownHeaderTextSplitter, RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings

def index_markdown_files(data_dir: str, db_path: str):
    print(f"--- Starting Document Indexing from {data_dir} ---")
    
    # 1. Define markdown headers to split on
    headers_to_split_on = [
        ("#", "Header 1"),
        ("##", "Header 2"),
        ("###", "Header 3"),
    ]
    markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
    
    # 2. We use a secondary text splitter to ensure no chunk is too large for the embedding window
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000, 
        chunk_overlap=150
    )

    documents = []
    files = glob.glob(os.path.join(data_dir, "**/*.md"), recursive=True)
    
    for file_path in files:
        file_name = os.path.basename(file_path)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                
            # Split by headers
            md_header_splits = markdown_splitter.split_text(content)
            
            # Further split by chunk size
            splits = text_splitter.split_documents(md_header_splits)
            
            # Add source metadata tracking
            for split in splits:
                if "source_file" not in split.metadata:
                    split.metadata["source_file"] = file_name
                documents.append(split)
                
        except Exception as e:
            print(f"Failed to process {file_name}: {e}")

    if not documents:
        print("No documents found or splitting failed.")
        return

    print(f"Created {len(documents)} chunks from {len(files)} files.")
    
    # 3. Embedding definition (Must match retriever)
    print("Generating embeddings using all-MiniLM-L6-v2...")
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Insert into ChromaDB
    print(f"Storing chunks in ChromaDB at {db_path}...")
    db = Chroma.from_documents(
        documents, 
        embedding_function, 
        persist_directory=db_path
    )
    # Chroma persists automatically upon addition in recent versions, though persist() can be called manually.
    if hasattr(db, "persist"):
        db.persist()
    print("Indexing complete and persisted to disk!")


if __name__ == "__main__":
    # Ensure correct paths regardless of cwd
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
    data_dir = os.path.join(project_root, "data", "cleaned_markdowns")
    db_path = os.path.join(project_root, "chroma_db")
    
    index_markdown_files(data_dir, db_path)
