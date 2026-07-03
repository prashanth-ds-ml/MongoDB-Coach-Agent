### 1. Core Concept
#### Definition
The `$exists` and `$type` operators are query predicates that filter documents based on field presence or BSON data type. `$exists` checks if a field exists (regardless of value), while `$type` validates a field’s BSON type (e.g., string, integer). These operators are critical for schema validation, data quality checks, and type-specific queries.

#### Key Terms
- **$exists**: Operator that matches documents where a field is present. Returns `true` if the field exists, `false` if absent.
- **$type**: Operator that matches documents where a field’s BSON type matches a specified type code (e.g., `1` for `String`, `16` for `Date`).
- **BSON Type Codes**: Numeric identifiers for BSON types (e.g., `10` for `Object`, `12` for `Boolean`).
- **Field Traversal**: Mechanism for navigating BSON documents without full parsing, using prefix-length encoding.

#### Underlying Mechanics
BSON uses a prefix-length schema: each element starts with a 1-byte type code (e.g., `0x0A` for `Object`), followed by a 4-byte length for the field name. The value’s type code and length follow. This allows MongoDB to skip elements during traversal without parsing entire documents, optimizing query performance.

#### Design Choices
- **Prefix-Length Schema**: Enables efficient element skipping but requires strict byte alignment (e.g., 4-byte padding for odd-length strings).
- **Type Code Restrictions**: `$type` only accepts valid BSON type codes (1–127), rejecting invalid values.

### 2. Level-Based Breakdown
#### For Beginners
Think of `$exists` as a "presence check" and `$type` as a "type labeler." Like labeling storage boxes (e.g., "books" vs. "tools"), `$type` ensures data is stored correctly, while `$exists` confirms a box exists.

#### For Intermediate Learners
- **Precision**: Use `$type` for exact type matches (e.g., `{"age": {"$type": "int"}}`). Avoid mixing with `$eq` for type checks (e.g., `{"age": 30}` vs. `{"age": {"$type": "int"}}`).
- **Floating-Point Pitfalls**: `$type` for `Double` (type `1`) includes both integers and decimals. Use `NumberDecimal` (type `13`) for precise monetary values.

#### For Advanced Developers
- **Indexing**: `$type` queries cannot use indexes unless combined with `$exists`. Indexes on `Double` fields (type `1`) support range queries but not `$type` alone.
- **Document Size**: `$type` checks on large fields (e.g., `Binary` data) may impact performance due to 16MB document limits.

### 3. Syntax & Code Examples (Do's & Don'ts)
#### DO: Best Practice
```javascript
// mongosh
db.users.find({ "age": { "$exists": true, "$type": "int" } });
// PyMongo
collection.find({"age": {"$exists": True, "$type": "int"}})
```
**Explanation**: Combines `$exists` and `$type` to ensure the `age` field is an integer.

#### DON’T / EXAM TRAP
```javascript
// Incorrect: Uses $eq instead of $type
db.users.find({ "age": { "$exists": true, "$eq": "int" } });
```
**Failure**: `$eq` checks value equality, not type. This query would fail if `age` is an integer.

### 4. Exam Radar
**Exam Signal**: `$type` requires valid BSON type codes (e.g., `16` for `Date`), not string names.
*What It Tests*: Confusion between type codes and human-readable names.
**Exam Signal**: `$exists` and `$type` cannot be used together in compound queries without explicit syntax.
*What It Tests*: Misunderstanding of operator precedence or syntax rules.

### 5. Micro-Challenge
A developer needs to find documents where the `price` field is a decimal (e.g., `19.99`). Which query is correct?
A) `{ "price": { "$type": "double" } }`
B) `{ "price": { "$type": "13" } }`
C) `{ "price": { "$exists": true, "$type": "12" } }`
D) `{ "price": { "$type": "NumberDecimal" } }`

### 6. 30-Second Recall
- `$exists` checks field presence; `$type` validates BSON type codes.
- `$type` uses numeric codes (e.g., `13` for `NumberDecimal`), not strings.
- `$exists` and `$type` can be combined to enforce schema rules.
- `$type` queries bypass indexes unless paired with `$exists`.