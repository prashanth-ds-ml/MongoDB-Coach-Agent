### 1. Core Concept
#### Definition
The `$group` stage aggregates documents by a specified key expression, applying accumulator operators (e.g., `$sum`, `$addToSet`, `$max`) to produce one output document per distinct group key. It can also perform computed fields, conditional grouping, and nested grouping via nested pipelines.

#### Key Terms
- **Double**: 64‑bit IEEE‑754 floating‑point number; used for numeric values that require fractional precision.
- **Int32 (NumberInt)**: 32‑bit signed integer; stored as `NumberInt` in BSON.
- **Int64 (NumberLong)**: 64‑bit signed integer; stored as `NumberLong` in BSON.
- **Decimal128 (NumberDecimal)**: Fixed‑point 128‑bit decimal; provides exact decimal arithmetic for monetary data.

#### Underlying Mechanics
BSON encodes each field with a type code followed by a length prefix; the server can skip over fields by reading the length and moving the cursor forward, enabling selective parsing. Padding bytes align documents to 4‑byte boundaries, and the maximum document size is 16 MiB, which constrains the combined output of `$group` accumulators.

#### Design Choices
- **Choice 1** – *Accumulator efficiency*: `$sum` is O(1) per group, while `$push` stores every element, increasing memory use.
- **Choice 2** – *Group key complexity*: Arbitrary expressions are allowed, but complex expressions may exceed the 16 MiB output limit and force disk use.

### 2. Level-Based Breakdown
#### For Beginners
Think of `$group` as a classroom roll‑call: each student (document) is counted under their class (group key), and the teacher tallies how many are in each class.

#### For Intermediate Learners
Use `$match` before `$group` to limit input size, apply `$project` only after grouping to avoid unnecessary field passes, and remember that `$group` cannot use indexes directly—pre‑filtering is essential for performance.

#### For Advanced Developers
`$group` writes intermediate results to a temporary collection; RAM‑based processing caps at 100 MiB, after which it spills to disk. The 16 MiB document limit applies to each output document, and large `$addToSet` or `$push` accumulators may trigger pagination, affecting throughput.

### 3. Syntax & Code Examples (Do's & Don'ts)
**Syntax mapping**: In the MongoDB shell you write `{ "$group": { "_id": "$field", "total": { "$sum": 1 } } }`. In PyMongo the same stage is a Python dict: `{"$group": {"_id": "$field", "total": {"$sum": 1}}}`. Both languages accept the stage as an element of the pipeline list.

**DO: Best Practice**
```javascript
// mongosh
db.orders.aggregate([
  { "$match": { "status": "shipped" } },
  { "$group": { "_id": "$customer", "revenue": { "$sum": "$amount" } } }
]);
```

```python
# PyMongo
pipeline = [
    {"$match": {"status": "shipped"}},
    {"$group": {"_id": "$customer", "revenue": {"$sum": "$amount"}}}
]
cursor = db.orders.aggregate(pipeline)
```

**DON'T / EXAM TRAP**
```javascript
// Incorrect: using $project before $group to compute a sum
db.orders.aggregate([
  { "$project": { "total": { "$add": ["$amount", 5] } } },
  { "$group": { "_id": "$customer", "sumTotal": { "$sum": "$total" } } }
]);
```
*Why it fails*: `$project` runs on each document before grouping, so the constant `5` is summed for every document, inflating the result. The correct approach is to sum only the original field (`$amount`) inside `$group`.

### 4. Exam Radar
- **Exam Signal:** Placing a `$project` that computes a sum **before** `$group`. *What It Tests:* Understanding of stage order and accumulator scope.
- **Exam Signal:** Using `$sum: 1` on a field that may be missing or `null`. *What It Tests:* Handling of absent fields and implicit null‑to‑zero conversion.

### 5. Micro-Challenge
Which pipeline correctly calculates the **average** order value per customer while ensuring the result is a precise `Decimal128`?

A) `{ "$group": { "_id": "$customer", "avgValue": { "$avg": "$amount" } } }`
B) `{ "$group": { "_id": "$customer", "avgValue": { "$divide": ["$amount", 1] } } }`
C) `{ "$group": { "_id": "$customer", "avgValue": { "$avg": { "$toDecimal": "$amount" } } } }`
D) `{ "$group": { "_id": "$customer", "avgValue": { "$sum": "$amount" } } }`

### 6. 30-Second Recall
- `$group` creates one output document per distinct group key.
- Accumulators (`$sum`, `$avg`, `$max`, …) compute values across grouped documents.
- Pre‑filter with `$match` to limit processed data and stay within the 16 MiB output limit.
- Complex group keys or large accumulators may force disk‑based processing.