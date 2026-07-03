# MongoDB Certification Lesson: findAndModify (Topic 4)

### 1. Core Concept

#### Definition

#### Key Terms
- **query**: A filter document specifying selection criteria using query operators. Only one document is modified even if multiple match. Defaults to empty document `{}`.
- **update**: Either an update operator document (`$set`, `$inc`, `$push`) performing modification, a replacement document replacing the entire document, or an aggregation pipeline (MongoDB 5.0+).
- **new**: Boolean flag determining return value. `false` (default) returns pre-modification document; `true` returns post-modification document.
- **upsert**: Boolean that creates a new document when no match is found. Requires unique index on query fields to prevent duplicates in concurrent scenarios.

#### Underlying Mechanics
The operation executes as a single atomic unit within MongoDB's write lock, preventing race conditions. For retryable writes, the entire document is copied to an internal side collection before modification, impacting performance with large documents. The operation uses the same query execution engine as `find()`, supporting indexes for efficient document location.

#### Design Choices
- **Legacy Status**: Deprecated in favor of `findOneAndUpdate()`, `findOneAndDelete()`, `findOneAndReplace()`. Use modern methods for new development.

### 2. Level-Based Breakdown

#### For Beginners
Think of `findAndModify()` as a bank teller who simultaneously checks your account balance AND processes a withdrawal in one seamless action—you see the updated balance immediately, preventing others from seeing inconsistent states.

#### For Intermediate Learners
Use `$set` for field updates, `$inc` for numeric increments, and `$push` for array additions. Avoid replacement documents `{}` unless intentionally overwriting all fields. Be cautious with floating-point arithmetic—use `NumberDecimal` for monetary values to prevent rounding errors.

#### For Advanced Developers

### 3. Syntax & Code Examples (Do's & Don'ts)

**MongoDB Shell (mongosh):**
```javascript
// DO: Best Practice - Update with return
db.users.findAndModify({
    query: { name: "Alice" },
    update: { $inc: { score: 1 } },
    new: true
});

// DON'T / EXAM TRAP - Missing new flag
db.users.findAndModify({
    query: { name: "Alice" },
    update: { $inc: { score: 1 } }
});
// Returns original document, not updated one
```

**PyMongo (Python):**
```python
# DO: Best Practice
result = collection.find_one_and_update(
    {"name": "Alice"},
    {"$inc": {"score": 1}},
    return_document=ReturnDocument.AFTER
)

# DON'T / EXAM TRAP - Wrong return handling
result = collection.find_and_modify(
    query={"name": "Alice"},
    update={"$inc": {"score": 1}}
)
# Returns original document; new parameter defaults to False
```

### 4. Exam Radar

- **Exam Signal:** Confusing `findAndModify()` with `updateOne()` return values
* *What It Tests:* Understanding that `findAndModify()` returns documents while `updateOne()` returns `WriteResult` objects.

- **Exam Signal:** Upsert without unique index causing duplicates
* *What It Tests:* Knowledge of race conditions and the requirement for unique indexes to prevent multiple document creation.

### 5. Micro-Challenge
A developer is designing a schema and needs to select the most appropriate representation. Which BSON type is the correct choice?



A) `db.write operations.updateOne({type: "transfer"}, {$inc: {count: 1}})`
B) `db.write operations.findAndModify({query: {type: "transfer"}, update: {$inc: {count: 1}}})`
C) `db.write operations.findAndModify({query: {type: "transfer"}, update: {$inc: {count: 1}}, new: true})`
D) `db.write operations.findOneAndUpdate({type: "transfer"}, {$inc: {count: 1}})`

### 6. 30-Second Recall

- `findAndModify()` is legacy; use `findOneAndUpdate()` for new code
- Returns original document by default; use `new: true` to return updated version
- Atomic single-document operation with built-in race condition protection
- Upsert requires unique index to prevent duplicate document creation