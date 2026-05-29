**Definitive Source Ingestion Pipeline (Best Practice)**

The most reliable method for building the knowledge base is to clone the official repository and process its source files systematically. This avoids the pitfalls of web scraping and provides atomic access to the source Markdown/MDX files.

**Procedure:**
1.  **Clone Repository:** Use `git clone https://github.com/mongodb/docs.git` to get the entire source structure locally.
2.  **Extraction:** Navigate into the `content/` directory (or appropriate subdirectories) and focus on extracting all files with `.mdx` or `.md` extensions.
3.  **Conversion:** Systematically convert all extracted `.mdx` files to standard Markdown (`.md`) format.
4.  **Final Processing:** Process the resulting `.md` files through the existing Chunking $\rightarrow$ Embedding $\rightarrow$ Indexing pipeline.

**Impact:** This method ensures we capture the *intended* documentation, rather than the *rendered* documentation, which is far more robust for LLM training and RAG.
