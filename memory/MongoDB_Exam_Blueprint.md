# MongoDB Exam Blueprint (Source: User Input)

This document outlines the definitive, examinable structure for the CertCoach platform, derived from an official study guide and supplemented by the user's explicit curriculum mapping. This structure dictates content extraction, question generation, and module grouping.

## 📚 Core Domains & Content Mapping

**1. MongoDB Basics / Document Model**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Key Topics:** BSON vs JSON, `_id` field, Embedded documents, Arrays, Dot notation, Document size limits.

**2. CRUD Operations**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Operators:** `$set`, `$unset`, `$inc`, `$push`, `$pull`
*   **Query Operators:** `$eq`, `$gt`, `$lt`, `$in`, `$and`, `$or`, `$exists`

**3. Querying Arrays and Embedded Documents**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Key Concepts:** Dot notation, `$elemMatch`, Array indexes.

**4. Projection**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Concepts:** Including fields, excluding fields, projection rules.

**5. Sorting, Limiting, Counting**
*   **Source Paths:** `data/Primary_Exam_Guide.md`

**6. Indexes**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Topics:** single field index, compound index, multikey index, index usage.

**7. Aggregation Framework**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Common Pipeline Stages:** `$match`, `$group`, `$project`, `$sort`, `$limit`, `$unwind`, `$lookup`

**8. Transactions**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Key Concepts:** ACID, multi-document transactions, session usage.

**9. Python Driver (PyMongo)**
*   **Source Paths:** `data/Primary_Exam_Guide.md`
*   **Important Topics:** `MongoClient`, `insert_one()`, `insert_many()`, `find()`, `update_one()`, `delete_one()`, `aggregation` with `aggregate()`.

## 📝 Exam Structure Summary
*   **Total Questions:** ~53
*   **Time Limit:** 75 minutes
*   **Format:** Multiple Choice
*   **Main Focus Areas (Weighting Guide):** CRUD, Indexing, Aggregation, Data Modeling, PyMongo usage.

**Action Item:** This blueprint must guide all future content generation, ensuring every piece of material generated targets one of these specific areas.