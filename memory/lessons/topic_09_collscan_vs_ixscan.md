### 1. Core Concept
#### Definition
COLLSCAN and IXSCAN are two types of scan operations used by MongoDB to retrieve data from collections. COLLSCAN is a collection scan, where MongoDB scans every document in a collection to find the documents that match a query. IXSCAN, on the other hand, is an index scan, where MongoDB uses an index to limit the number of documents it must inspect.

#### Key Terms
- **COLLSCAN**: A collection scan operation where MongoDB scans every document in a collection to find the documents that match a query.
- **IXSCAN**: An index scan operation where MongoDB uses an index to limit the number of documents it must inspect.
- **Index**: A data structure that improves the speed of data retrieval by providing a quick way to locate specific data.
- **Collection**: A group of documents stored in a MongoDB database.

#### Underlying Mechanics
When MongoDB performs a COLLSCAN, it must scan every document in the collection, which can be slow and resource-intensive. On the other hand, when MongoDB performs an IXSCAN, it can use the index to quickly locate the documents that match the query, which can significantly improve performance.

#### Design Choices
- **Using an index**: Creating an index on a field can improve query performance by allowing MongoDB to use an IXSCAN instead of a COLLSCAN.
- **Choosing the right index type**: MongoDB provides several types of indexes, including single field indexes, compound indexes, and text indexes. Choosing the right index type depends on the specific use case and query patterns.

### 2. Level-Based Breakdown
#### For Beginners
Think of a COLLSCAN like looking through a phonebook to find a specific name. You have to scan every entry in the phonebook to find the one you're looking for. On the other hand, an IXSCAN is like using the index at the back of the phonebook to quickly find the page where the name is listed.

#### For Intermediate Learners
When designing indexes, consider the query patterns and the frequency of updates. For example, if you have a query that filters on multiple fields, a compound index may be more efficient than separate single field indexes.

#### For Advanced Developers
Consider the storage and memory requirements of indexes. Indexes can consume significant disk space and memory, especially for large collections. Additionally, consider the impact of indexing on write performance, as updating an index can slow down write operations.

### 3. Syntax & Code Examples (Do's & Don'ts)
**DO: Best Practice**
```javascript
// Create a single field index on the "name" field
db.collection.createIndex({ name: 1 })

// Create a compound index on the "name" and "age" fields
db.collection.createIndex({ name: 1, age: 1 })
```

**DON'T / EXAM TRAP**
```javascript
// Creating an index on a field that is not used in queries
db.collection.createIndex({ unusedField: 1 })
```
Explanation: Creating an index on a field that is not used in queries can waste disk space and memory.

### 4. Exam Radar
- **Exam Signal:** A query that filters on multiple fields.
* *What It Tests:* The ability to choose the right index type, such as a compound index, to improve query performance.
- **Exam Signal:** A query that uses a wildcard index.
* *What It Tests:* The ability to understand the limitations and use cases of wildcard indexes.

### 5. Micro-Challenge
Which of the following index types would be most efficient for a query that filters on multiple fields?

A) Single field index
B) Compound index
C) Text index
D) Wildcard index

### 6. 30-Second Recall
- COLLSCAN is a collection scan operation where MongoDB scans every document in a collection.
- IXSCAN is an index scan operation where MongoDB uses an index to limit the number of documents it must inspect.
- Indexes can improve query performance by allowing MongoDB to use an IXSCAN instead of a COLLSCAN.
- Choosing the right index type depends on the specific use case and query patterns.