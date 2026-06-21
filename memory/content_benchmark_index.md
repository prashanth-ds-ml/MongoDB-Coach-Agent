# Content Benchmark Index

Related: [[Memory Home]], [[content_benchmark_schema|Content Benchmark Schema]], [[topic_01_benchmark|Topic 1 Benchmark Record]], [[reference_repo_adoption|Reference Repo Adoption]]

Captured on 2026-06-17.

## Purpose

Track the combined benchmark in canonical syllabus order so every topic and concept can be expanded sequentially without losing CertCoach's workflow shape.

This index is the rollout map. The detailed record shape is defined in [[content_benchmark_schema|Content Benchmark Schema]].

## Order

1. Topic 1 - MongoDB Overview & The Document Model
   - Status: recorded
   - Concepts:
     - BSON Data Types
     - Document structure
     - Collections vs Tables
   - Record: [[topic_01_benchmark|Topic 1 Benchmark Record]]

2. Topic 2 - CRUD Operations - Create
   - Status: recorded
   - Concepts:
     - insertOne()
     - insertMany()
     - _id and ObjectId
   - Record: [[topic_02_benchmark|Topic 2 Benchmark Record]]

3. Topic 3 - CRUD Operations - Read
   - Status: recorded
   - Concepts:
     - find()
     - findOne()
     - Projections
     - Cursors
     - sort/limit/skip
     - countDocuments()
   - Record: [[topic_03_benchmark|Topic 3 Benchmark Record]]

4. Topic 4 - CRUD Operations - Update
   - Status: recorded
   - Concepts:
     - replaceOne()
     - updateOne()
     - updateMany()
     - $set
     - $push
     - $inc
     - $unset
     - upsert
     - findAndModify
   - Record: [[topic_04_benchmark|Topic 4 Benchmark Record]]

5. Topic 5 - CRUD Operations - Delete
   - Status: recorded
   - Concepts:
     - deleteOne()
     - deleteMany()
     - write concern impacts
   - Record: [[topic_05_benchmark|Topic 5 Benchmark Record]]

6. Topic 6 - Query Operators & MQL
   - Status: recorded
   - Concepts:
     - query operators
     - comparison operators
     - logical operators
     - element and evaluation operators
     - Atlas Search query basics
   - Record: [[topic_06_benchmark|Topic 6 Benchmark Record]]

7. Topic 7 - Querying Arrays & Embedded Documents
   - Status: recorded
   - Concepts:
     - array matching
     - embedded document queries
     - $elemMatch
     - dot notation
   - Record: [[topic_07_benchmark|Topic 7 Benchmark Record]]

8. Topic 8 - Aggregation Framework
   - Status: recorded
   - Concepts:
     - $match
     - $project
     - $group
     - $sort
     - $limit
     - pipeline order
   - Record: [[topic_08_benchmark|Topic 8 Benchmark Record]]

9. Topic 9 - Indexes & Performance
   - Status: recorded
   - Concepts:
     - single-field indexes
     - compound indexes
     - unique indexes
     - covered queries
     - performance tradeoffs
   - Record: [[topic_09_benchmark|Topic 9 Benchmark Record]]

10. Topic 10 - Data Modeling
    - Status: recorded
    - Concepts:
      - embedding
      - referencing
      - schema design tradeoffs
      - document growth
      - denormalization
    - Record: [[topic_10_benchmark|Topic 10 Benchmark Record]]

11. Topic 11 - MongoDB Drivers & PyMongo
    - Status: recorded
    - Concepts:
      - client/database/collection access
      - CRUD with PyMongo
      - aggregation with PyMongo
      - ObjectId handling
      - driver basics
    - Record: [[topic_11_benchmark|Topic 11 Benchmark Record]]

12. Topic 12 - Tools, Tooling & Atlas Search
    - Status: recorded
    - Concepts:
      - Atlas overview
      - Atlas sample datasets
      - Atlas Search indexes
      - Atlas Search queries
      - tooling and operational basics
    - Record: [[topic_12_benchmark|Topic 12 Benchmark Record]]

## Expansion Rule

Expand topics in order. For each topic:

1. create the benchmark record
2. validate official-doc coverage
3. attach the reference objective cluster
4. create lesson and repair prompt notes
5. move to the next topic only after the previous one is recorded
