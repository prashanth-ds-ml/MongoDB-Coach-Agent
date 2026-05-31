# MongoDB Exam Blueprint (Source: Local PDF Cross-Check)

This document outlines the definitive examinable structure for the CertCoach platform, cross-checked against `data/Resources/UpdatedMongodDBAssociateDeveloperExamGuide.docx3.pdf` and the extracted `data/Primary_Exam_Guide.md`. This structure dictates content extraction, question generation, and module grouping for the MongoDB Associate Developer exam, with Python-specific driver material for Section 6.

## Core Domains & Content Mapping

**1. MongoDB Overview and the Document Model (8%)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Key Topics:** BSON value types, document shape flexibility, collections containing differently shaped documents.

**2. CRUD (51%)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Operations:** insert commands, full-document replacement, `$set`, upsert, multi-document update, `findAndModify`, delete expressions.
*   **Query Coverage:** equality constraints, equality on array fields, relational operators, `$in`, `$elemMatch`, logical operators, sort and limit, projection, cursor iteration, count operations.
*   **Search and Aggregation Coverage:** search index command, search query, aggregation with `$match`, `$group`, `$lookup`, and `$out`.

**3. Indexes (17%)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Topics:** choosing indexes for collection scans, array-field indexes, compound indexes for sort, counting existing indexes, index trade-offs, explain plan outputs such as collection scan versus index scan.

**4. Data Modeling (4%)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Topics:** embedded versus linked relationships, identifying anti-patterns.

**5. Tools and Tooling (2%)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Topics:** loading Atlas Sample Dataset and using Data Explorer to find a document.

**6. Drivers - Python / PyMongo (18%)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Topics:** PyMongo driver purpose, application connection flow, MongoClient URI components, connection pooling, Python syntax for insert/update/delete/find operations, aggregation pipeline syntax, differences between MQL syntax and Aggregation Framework syntax.

## Exam Structure Summary
*   **Total Questions:** ~53
*   **Time Limit:** 75 minutes
*   **Format:** Multiple Choice and Multiple Response
*   **Main Focus Areas:** CRUD, Indexing, Drivers/PyMongo, Document Model, Data Modeling, Tools/Data Explorer.

**Action Item:** This blueprint must guide all future content generation. Transactions should not be treated as a standalone Associate Developer exam domain unless a newer guide explicitly adds them.
