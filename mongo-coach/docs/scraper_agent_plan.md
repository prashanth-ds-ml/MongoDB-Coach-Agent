# Scraper Agent – Design (v1)

Goal: Given a MongoDB docs URL, fetch the page, extract the main
documentation content (title, sections, subsections, code blocks)
into a structured JSON file under `data/raw/`.

Modes (planned):
- `single_url`: scrape one URL (e.g. db.collection.insertOne).
- `associate_python_full`: use a catalog + seed config to scrape
  all relevant URLs for the Associate Dev (Python) exam.

Output schema (high-level):

```jsonc
{
  "url": "...",
  "doc_type": "mongodb_docs_method",
  "method_name": "db.collection.insertOne",
  "title": "db.collection.insertOne() (mongosh method)",
  "version": "8.2",
  "breadcrumbs": [...],
  "sections": [
    {
      "section_id": "definition",
      "heading": "Definition",
      "heading_level": 2,
      "content": "Text...",
      "code_blocks": [],
      "subsections": []
    }
  ],
  "fetched_at": "ISO-8601 timestamp"
}
```
