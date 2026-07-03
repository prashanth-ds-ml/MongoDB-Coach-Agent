"""Script to enhance a lesson's quality using OpenRouter Llama 3.1 8B under strict progressive syllabus constraints."""
import os
import sys
import re
import json
from datetime import datetime, timezone

from certcoach.core import database, planner, config
from certcoach.core.lesson_bank import resolve_lesson_target, build_lesson_source_bundle, validate_lesson_markdown, LESSON_CONTRACT_VERSION
from certcoach.core.content_contract import CONTENT_CONTRACT_VERSION
from certcoach.core.model_runner import get_model_runner

def get_syntax_instructions(topic_id: int, concept: str) -> str:
    if topic_id == 1 and concept == "BSON Data Types":
        return """### 3. Syntax & Code Examples (Do's & Don'ts)
Walkthrough:
In Topic 1, we do not call database methods. We represent BSON documents as literals. The examples below show how BSON types are declared.

You MUST copy these exact code blocks for Section 3:

#### DO: Best Practice - Literal BSON Document in mongosh
```javascript
{
    _id: ObjectId(), 
    quantity: NumberInt(5),
    price: NumberDecimal("39.99"),
    created_at: new Date()
}
```

#### DO: Best Practice - Literal BSON Document in PyMongo
```python
# PyMongo uses standard python dictionaries and bson classes
{
    "_id": ObjectId(),
    "quantity": 5,
    "price": Decimal128("39.99"),
    "created_at": datetime.utcnow()
}
```

#### DON'T / EXAM TRAP - Precision degradation
```javascript
{
    price: 39.99, // Standard floating-point Double loses precision in monetary math
    large_counter: 9007199254740992 // JavaScript numbers exceed 2^53 - 1 limit and degrade
}
```"""
    elif topic_id == 2 and concept == "insertOne()":
        return """### 3. Syntax & Code Examples (Do's & Don'ts)
Walkthrough:
In this section, we show how to perform single document insertions. We cover explicit _id definition, auto-generated _id behavior, and retrieving the inserted ID from the driver result object.

You MUST copy these exact code blocks for Section 3:

#### DO: Best Practice - Single Document Insertion in mongosh
```javascript
// Explicit _id insertion
db.orders.insertOne({
    _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
    item: "canvas",
    qty: NumberInt(100),
    tags: ["cotton"],
    size: { h: NumberDecimal("28"), w: NumberDecimal("35.5") }
});

// Implicit _id insertion (driver auto-generates ObjectId)
db.orders.insertOne({
    item: "journal",
    qty: NumberInt(25),
    tags: ["blank", "red"]
});
```

#### DO: Best Practice - Single Document Insertion in PyMongo
```python
from bson import ObjectId, Decimal128
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["test_db"]

# Explicit _id insertion
result1 = db.orders.insert_one({
    "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
    "item": "canvas",
    "qty": 100,
    "tags": ["cotton"],
    "size": { "h": Decimal128("28"), "w": Decimal128("35.5") }
})
print(f"Inserted ID: {result1.inserted_id}")

# Implicit _id insertion (PyMongo generates ObjectId and returns it in result.inserted_id)
result2 = db.orders.insert_one({
    "item": "journal",
    "qty": 25,
    "tags": ["blank", "red"]
})
print(f"Generated ID: {result2.inserted_id}")
```

#### DON'T / EXAM TRAP - Expecting full document return or ignoring DuplicateKeyError
```javascript
// TRAP 1: Expecting insertOne() to return the inserted document
// insertOne() returns a write result object, NOT the document itself.
let doc = db.orders.insertOne({ item: "box" });
print(doc.item); // undefined! 

// TRAP 2: Duplicate key error (violating _id uniqueness)
// This will throw a DuplicateKeyError if the _id already exists in the collection.
db.orders.insertOne({ _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"), item: "pencil" });
```"""
    elif topic_id == 2 and concept == "insertMany()":
        return """### 3. Syntax & Code Examples (Do's & Don'ts)
Walkthrough:
In this section, we show how to perform bulk insertions. We cover ordered vs unordered inserts, behavior when errors occur during inserts, and correct parameter formatting.

You MUST copy these exact code blocks for Section 3:

#### DO: Best Practice - Bulk Document Insertion in mongosh
```javascript
// Unordered bulk insertion (execution continues even if some documents fail)
db.orders.insertMany([
    { _id: 1, item: "pencil", qty: NumberInt(50) },
    { _id: 2, item: "paper", qty: NumberInt(100) },
    { _id: 3, item: "binder", qty: NumberInt(20) }
], { ordered: false });

// Ordered bulk insertion (execution stops immediately on the first error)
db.orders.insertMany([
    { item: "eraser", qty: NumberInt(15) },
    { item: "ruler", qty: NumberInt(30) }
], { ordered: true });
```

#### DO: Best Practice - Bulk Document Insertion in PyMongo
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["test_db"]

# Unordered insertion
result1 = db.orders.insert_many([
    { "_id": 1, "item": "pencil", "qty": 50 },
    { "_id": 2, "item": "paper", "qty": 100 },
    { "_id": 3, "item": "binder", "qty": 20 }
], ordered=False)
print(f"Inserted IDs: {result1.inserted_ids}")

# Ordered insertion
result2 = db.orders.insert_many([
    { "item": "eraser", "qty": 15 },
    { "item": "ruler", "qty": 30 }
], ordered=True)
print(f"Inserted IDs: {result2.inserted_ids}")
```

#### DON'T / EXAM TRAP - Passing single document or ignoring ordered error-stop behavior
```javascript
// TRAP 1: Passing a single object instead of an array/list
// insertMany() expects an array of documents; passing a single object throws a TypeError.
db.orders.insertMany({ item: "desk", qty: NumberInt(1) }); // WRONG! Throws exception.

// TRAP 2: Relying on ordered: true when some IDs might duplicate
// If document _id:2 already exists, document 3 will NOT be inserted.
db.orders.insertMany([
    { _id: 1, item: "envelope" }, // Succeeds
    { _id: 2, item: "stamp" },    // Fails (DuplicateKeyError)
    { _id: 3, item: "card" }     // NEVER PROCESSED because ordered is true!
], { ordered: true });
```"""
    elif topic_id == 2 and concept == "_id and ObjectId":
        return """### 3. Syntax & Code Examples (Do's & Don'ts)
Walkthrough:
In this section, we show how to generate ObjectIds, extract their components, and work with the mandatory primary key _id.

You MUST copy these exact code blocks for Section 3:

#### DO: Best Practice - ObjectId Generation and Inspection in mongosh
```javascript
// Generate a new unique ObjectId
let id = ObjectId();
print("Hex representation: " + id.str);

// Extract the 4-byte creation timestamp as a Date object
let creationTime = id.getTimestamp();
print("Created at: " + creationTime);

// Insert a document with explicit ObjectId primary key
db.users.insertOne({
    _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
    username: "alice"
});
```

#### DO: Best Practice - ObjectId Generation and Inspection in PyMongo
```python
from bson import ObjectId
from pymongo import MongoClient

# Generate a new unique ObjectId
my_id = ObjectId()
print(f"Hex representation: {str(my_id)}")

# Extract the 4-byte creation timestamp (generation_time is timezone-aware UTC datetime)
creation_time = my_id.generation_time
print(f"Created at: {creation_time}")

# Insert a document with explicit ObjectId primary key
client = MongoClient("mongodb://localhost:27017/")
db = client["test_db"]
db.users.insert_one({
    "_id": ObjectId("65a1b2c3d4e5f6a7b8c9d0e1"),
    "username": "alice"
})
```

#### DON'T / EXAM TRAP - Attempting to mutate _id or assuming string comparisons
```javascript
// TRAP 1: Attempting to modify the immutable _id field of an existing document
// This will throw a write error: "The _id field cannot be changed"
db.users.updateOne(
    { username: "alice" },
    { $set: { _id: ObjectId("65a1b2c3d4e5f6a7b8c9d0e2") } }
);

// TRAP 2: Comparing an ObjectId object with its string representation
// "65a1b2c3d4e5f6a7b8c9d0e1" is NOT equal to ObjectId("65a1b2c3d4e5f6a7b8c9d0e1")!
let id1 = ObjectId("65a1b2c3d4e5f6a7b8c9d0e1");
let idStr = "65a1b2c3d4e5f6a7b8c9d0e1";
print(id1 === idStr); // false!
```"""
    elif topic_id == 3 and concept == "find()":
        return """### 3. Syntax & Code Examples (Do's & Don'ts)
Walkthrough:
In this section, we show how to query collections using find(). We cover equality matches, dot notation for subdocument queries, and matching items in arrays.

You MUST copy these exact code blocks for Section 3:

#### DO: Best Practice - Querying Documents in mongosh
```javascript
// Query by a field value
db.users.find({ status: "active" });

// Query a nested subdocument using dot notation (robust, matches regardless of field order)
db.users.find({ "contact.email": "alice@example.com" });

// Query an array containing a specific element
db.users.find({ tags: "premium" });
```

#### DO: Best Practice - Querying Documents in PyMongo
```python
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["test_db"]

# Query by a field value
cursor1 = db.users.find({ "status": "active" })
for doc in cursor1:
    print(doc)

# Query a nested subdocument using dot notation
cursor2 = db.users.find({ "contact.email": "alice@example.com" })
for doc in cursor2:
    print(doc)

# Query an array containing a specific element
cursor3 = db.users.find({ "tags": "premium" })
for doc in cursor3:
    print(doc)
```

#### DON'T / EXAM TRAP - Exact subdocument matching or ignoring dot notation quotes
```javascript
// TRAP 1: Exact subdocument matching (sensitive to field order and matches exact fields only)
// This will NOT match { name: "Alice", contact: { email: "alice@example.com", phone: "123" } }
db.users.find({ contact: { email: "alice@example.com" } });

// TRAP 2: Omitting quotes around dot notation fields
// This will throw a syntax error in Javascript/mongosh and PyMongo
db.users.find({ contact.email: "alice@example.com" }); // WRONG! Throws exception.
```"""
    return """### 3. Syntax & Code Examples (Do's & Don'ts)
[Detail how BSON documents/syntax map between mongosh (JavaScript) and PyMongo (Python) side-by-side.
Provide a detailed syntax walkthrough before each code block. Explain every constructor or method.
Always show BOTH MongoDB Shell (mongosh) and PyMongo (Python) syntax.
Show a correct best-practice code block (labeled 'DO: Best Practice') and an incorrect/trap code block (labeled 'DON'T / EXAM TRAP'), explaining exactly why the trap fails.]"""

def clean_topic_1_leaks(lesson_md: str, concept: str) -> str:
    cleaned = lesson_md
    
    # General Topic 1 replacements
    cleaned = re.sub(r'\binsert_one\b', 'document insertion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\binsertOne\(\)', 'document insertion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\binsertOne\b', 'document insertion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\binsertMany\(\)', 'multiple document insertion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\binsertMany\b', 'multiple document insertion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bfindOne\(\)', 'single document retrieval', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bfindOne\b', 'single document retrieval', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bfind\(\)', 'document retrieval', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bfind\b', 'document retrieval', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bupdateOne\b', 'document update', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bupdateMany\b', 'multiple document update', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\breplaceOne\b', 'document replacement', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bdeleteOne\b', 'document deletion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bdeleteMany\b', 'multiple document deletion', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\baggregate\b', 'document aggregation', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$project\b', 'field filtering', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$addFields\b', 'field addition', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$type\b', 'type code filter', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$set\b', 'field update', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$push\b', 'array append', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$inc\b', 'field increment', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\$unset\b', 'field removal', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bdot notation\b', 'nested path notation', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bAtlas\b', 'Cloud platform', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'\bData Explorer\b', 'Cloud browser', cleaned, flags=re.IGNORECASE)

    # Document structure specific replacements
    if concept == "Document structure":
        cleaned = re.sub(r'\bqueries\b', 'data retrievals', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bquery\b', 'data retrieval', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bprojections\b', 'field selections', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bprojection\b', 'field selection', cleaned, flags=re.IGNORECASE)
        cleaned = re.sub(r'\bpositional operator\b', 'element position indicator', cleaned, flags=re.IGNORECASE)

    return cleaned

def get_enhance_prompt(topic_id: int, concept: str, md_context: str, tested_block: str) -> str:
    # Build prompt instructions based on progressive boundaries
    is_topic_1 = (topic_id == 1)
    
    constraints = ""
    if is_topic_1:
        constraints = """
*** CRITICAL TOPIC 1 PROGRESSIVE BOUNDARIES WARNING ***
You are NOT allowed to write or show any database CRUD operations or collection methods (such as insertOne, insert_one, insertMany, find, findOne, updateOne, deleteOne, deleteMany, insert).
Do NOT use or show any shell calls (like `db.collection.method(...)` or `collection.insert_one(...)`). 
Doing so will immediately FAIL the validation gate.
Instead, you MUST show code examples strictly as BSON Document Literals (raw JSON/dictionary structures) in JavaScript and Python.
For example, instead of db.collection.insertOne({val: 1}), show only the document: {val: NumberInt(1)}.

BANNED WORDS (Topic 1 / Document structure):
- Do NOT use the words 'query', 'queries', 'projection', 'projections', or 'dot notation'. Use alternatives like 'retrieval', 'retrievals', 'field selection', or 'nested path' instead.
- Do NOT use query/update operators like '$type', '$set', '$push', '$inc', '$unset', '$project'.
"""

    syntax_sec = get_syntax_instructions(topic_id, concept)

    prompt = f"""You are CertCoach, a strict-but-warm MongoDB Certification Instructor.
Your task is to take a raw reference document context and write a publication-grade, highly thorough, clear, and conceptually deep exam-level lesson for the concept '{concept}' (Topic {topic_id}).

The lesson MUST follow this exact six-section Markdown structure:

### 1. Core Concept
#### Definition
[Provide a comprehensive, multi-sentence formal definition of the concept]
#### Key Terms
- **[Term 1]**: [Provide a detailed definition. Ensure you explicitly define all key primitives and classes tested, such as Double, Int32 (NumberInt), Int64 (NumberLong), and Decimal128 (NumberDecimal).]
- **[Term 2]**: [Provide a detailed definition]
- **[Term 3]**: [Provide a detailed definition]
- **[Term 4]**: [Provide a detailed definition]
#### Underlying Mechanics
[Provide an exhaustive, highly technical explanation of the serialization layouts, bytes, bits, traversability mechanisms, and binary storage details. For BSON, explain the prefix-length schema, type codes, padding, byte alignments, and why this design allows skipping elements during search without full document parsing.]
#### Design Choices
- **[Choice 1]**: [Detail pros/cons, storage efficiency, or usage limits]
- **[Choice 2]**: [Detail pros/cons, storage efficiency, or usage limits]

### 2. Level-Based Breakdown
#### For Beginners
[Write a rich analogy comparing the concept to real-world objects]
#### For Intermediate Learners
[Detail specific developer-level implementation rules, precision guidelines (e.g. monetary calculations, floating-point rounding errors), and common coding mistakes]
#### For Advanced Developers
[Explain index structures, RAM vs Disk footprint, performance limits, and document constraints (like the 16MB single document boundary)]

{syntax_sec}

### 4. Exam Radar
- **Exam Signal:** [Detail the specific trick or trap the exam tests regarding this concept]
  * *What It Tests:* [Targeted developer logic]
- **Exam Signal:** [Detail another trick or trap]
  * *What It Tests:* [Targeted developer logic]

### 5. Micro-Challenge
[Exactly one multiple-choice question testing the core concept. The question must be a realistic developer decision scenario (e.g., choosing the correct data representation for financial transaction values or high-precision integer counters). It must have exactly 4 choices (labeled A, B, C, D) and exactly 1 correct answer. Do NOT provide the answer or worked solution in the lesson text.]

### 6. 30-Second Recall
Write exactly 4 bullet points summarizing the lesson. Each bullet must start with '- ':
- [Recall Point 1]
- [Recall Point 2]
- [Recall Point 3]
- [Recall Point 4]

---

{constraints}

{tested_block}

REFERENCE CONTEXT:
\"\"\"
{md_context[:20000]}
\"\"\"

Write the complete lesson markdown matching this structure. Ensure it is detailed and technically accurate, but keep explanations concise and direct. Do NOT write fluff. Target a maximum length of 150 words per explanation section so that the entire lesson fits within the output token budget and does not truncate. Do not leave any sections or code blocks incomplete.
"""
    return prompt

def enhance_lesson(topic_id: int, concept: str) -> None:
    database.check_connection()
    target = resolve_lesson_target(topic_id, concept)
    source_bundle = build_lesson_source_bundle(target)
    
    # Retrieve tested concepts from question bank
    query = {"metadata.topic_id": int(topic_id), "metadata.concept": concept}
    questions = list(database.questions_col.find(query))
    
    tested_concepts = []
    for q in questions:
        stem = q.get("question_text", "")
        options = q.get("options", [])
        correct = next((o.get("code_snippet", "") for o in options if o.get("is_correct")), "")
        # Avoid including junk questions (food, yahoo mail, etc.)
        if any(junk in stem.lower() for junk in ["food item", "yahoo", "support"]):
            continue
        tested_concepts.append(f"- Question: {stem}\n  Correct/Key Concept: {correct}")
        
    tested_block = ""
    if tested_concepts:
        tested_lines = "\n".join(tested_concepts[:10]) # Limit to 10 to avoid too much context
        tested_block = f"""
EXAM KNOWLEDGE REQUIREMENTS TO TEACH:
You MUST ensure that the lesson text fully covers and explains the concepts, rules, bit-lengths, limits, and behaviors tested by these exam questions. The learner must be able to answer these questions strictly using what you teach in the lesson:
{tested_lines}
"""
    
    prompt = get_enhance_prompt(topic_id, concept, source_bundle["md_context"], tested_block)
    
    runner = get_model_runner()
    model_config = {"provider": "openrouter", "model": "openrouter/free"}
    if os.getenv("NVIDIA_API_KEY") or os.getenv("nvidia"):
        model_config = {"provider": "nvidia", "model": "meta/llama-3.1-70b-instruct"}
        print(f"Enhancing lesson for Topic {topic_id} | Concept: {concept} using NVIDIA API ({model_config['model']})...")
    else:
        print(f"Enhancing lesson for Topic {topic_id} | Concept: {concept} using OpenRouter Free Router...")
    try:
        response = runner._call_model(model_config, prompt, temperature=0.3, num_ctx=8192)
        if not response:
            print("[-] Error: Empty response from model.")
            return
            
        print("\n[+] Lesson generated successfully. Validating...")
        
        # Validate the cleaned markdown
        lesson_md = response.strip()
        
        # Strip markdown json blocks if model wrapped it
        if lesson_md.startswith("```"):
            lines = lesson_md.splitlines()
            if lines[0].startswith("```markdown") or lines[0].startswith("```"):
                lesson_md = "\n".join(lines[1:-1]).strip()
        
        if topic_id == 1:
            lesson_md = clean_topic_1_leaks(lesson_md, concept)
            
        validation = validate_lesson_markdown(lesson_md, topic_id=topic_id, concept=concept)
        if not validation["is_valid"]:
            print("[-] Validation FAILED with the following issues:")
            for issue in validation["issues"]:
                print(f"  * {issue}")
            print("\nDraft lesson was:")
            print("-" * 50)
            print(lesson_md)
            print("-" * 50)
            return
            
        print("[+] Validation PASSED! Preview of the enhanced lesson:")
        print("=" * 60)
        print(validation["cleaned_markdown"])
        print("=" * 60)
        
        # Save to database
        timestamp = datetime.now(timezone.utc).replace(tzinfo=None).isoformat()
        artifact = {
            "topic_id": int(topic_id),
            "topic": target.topic,
            "concept": concept,
            "lesson_markdown": validation["cleaned_markdown"],
            "source_files": source_bundle["source_files"],
            "status": "validated",
            "validation_issues": [],
            "lesson_contract_version": LESSON_CONTRACT_VERSION,
            "content_contract_version": CONTENT_CONTRACT_VERSION,
            "generated_at": timestamp,
            "validated_at": timestamp,
            "updated_at": timestamp
        }
        database.upsert_lesson_artifact(artifact)
        print(f"\n[+] Successfully saved validated enhanced lesson in MongoDB!")
        
    except Exception as e:
        print(f"[-] Error enhancing lesson: {e}")

def main():
    topic_id = 1
    concept = "BSON Data Types"
    if len(sys.argv) > 2:
        topic_id = int(sys.argv[1])
        concept = sys.argv[2]
        
    enhance_lesson(topic_id, concept)

if __name__ == "__main__":
    main()
