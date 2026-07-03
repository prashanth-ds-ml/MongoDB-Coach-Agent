import os
import pymupdf4llm

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def main():
    pdf_path = os.path.join(PROJECT_ROOT, "data", "Resources", "UpdatedMongodDBAssociateDeveloperExamGuide.docx3.pdf")
    output_path = os.path.join(PROJECT_ROOT, "data", "Primary_Exam_Guide.md")

    print(f"Extracting {pdf_path}...")
    try:
        md_text = pymupdf4llm.to_markdown(pdf_path)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(md_text)
        print(f"Successfully extracted PDF to {output_path}")
    except Exception as e:
        print(f"Error extracting PDF: {e}")

if __name__ == "__main__":
    main()
