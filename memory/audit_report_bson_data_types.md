# Deep Audit Report: Topic 1 | Concept: BSON Data Types
Generated at: 2026-07-03 09:17:29

## 1. Lesson Overview & Micro-Challenge Audit
### Micro-Challenge Question:
```markdown
What is the primary purpose of using `ObjectId` as the `_id` field in MongoDB documents?
```

* **Audit Verdict**: Verified as aligned. The question tests core BSON properties taught directly in the lesson.

## 2. Practice Question Statistics
* **Total Questions in Bank**: 32
* **Lesson-Aligned Questions**: 13
* **Unaligned Questions**: 19
* **Untagged Questions**: 0

## 3. Lesson-Aligned Questions Detail
### Q1. ID: a12458a5-c977-49e6-92a6-2b55de980bde
**Question**: Which of the following BSON data types represents a unique identifier for documents in MongoDB?
**Options**:
  - A) Double
  * B) ObjectId
  - C) String
  - D) Array
**Alignment Logic**: The question directly tests the concept of 'ObjectId' as a unique identifier, which is explicitly mentioned in sections 2 (Advanced Developers), 4 (Exam Radar), and 6 (30-Second Recall) of the lesson.

### Q2. ID: 0744110d-eaaf-48f3-bd68-4caa5db97012
**Question**: Which BSON data type represents a universally unique identifier, commonly used as a primary key in MongoDB documents?
**Options**:
  - A) String
  * B) ObjectId
  - C) Integer
  - D) Date
**Alignment Logic**: The question directly tests the 'ObjectId' concept described in sections 2 (Advanced Developers), 4 (Exam Radar), and 6 (30-Second Recall), which all highlight ObjectId as a unique identifier used for the _id field.

### Q3. ID: c5d93629-18b1-44f4-b521-e5905e5c7481
**Question**: Which BSON numeric type is best suited for storing high-precision decimal values such as money?
**Options**:
  - String
  * Decimal128
  - Boolean
  - Array
**Alignment Logic**: The question is aligned because the 'Exam Radar' section specifically mentions the distinction between 'double' and 'decimal128' for precise calculations (e.g., money), which allows the student to identify Decimal128 as the correct choice.

### Q4. ID: b727f4f2-0036-4ed3-aeb4-ec38ddfb41a6
**Question**: Which BSON data type can be used to store an array of documents within a single document?
**Options**:
  - A) Integer
  - B) String
  * C) Array
  - D) ObjectId
**Alignment Logic**: The lesson explicitly mentions 'array' as a BSON type and discusses how documents can contain various types (including nested structures) and have flexible shapes. The question tests the identification of the correct BSON type for storing multiple items/documents within one document, which is covered in the 'BSON Types', 'Document Structure', and 'Exam Radar' sections.

### Q5. ID: 077b192d-7495-497b-a9b2-a7a4db806f6b
**Question**: Which BSON data type would you use to store a list of integers in MongoDB?
**Options**:
  - A) String
  * B) Array
  - C) Integer
  - D) ObjectId
**Alignment Logic**: The question tests the student's ability to identify correct BSON types. The lesson explicitly mentions 'array' as a BSON type and discusses the importance of choosing the correct BSON type for performance and structure.

### Q6. ID: 000a72b5-52c5-426e-8dcf-1b1c0cf066b1
**Question**: Which of the following statements about BSON data types in MongoDB is true?
**Options**:
  - A) Documents within a single collection must have the same set of fields.
  * B) A field's data type can differ between documents within a collection.
  - C) All documents in a collection must be stored as arrays.
  - D) BSON only supports string and numeric data types.
**Alignment Logic**: The question tests the core concepts of BSON flexibility and data types. Option A contradicts the 'Flexibility' and 'Document Structure' sections; Option B is directly supported by the 'Intermediate Learners' section (documents don't need to be the same shape); Option C and D are contradicted by the 'BSON Types' and 'Design Choices' sections which mention various types like object, array, and ObjectId.

### Q7. ID: 4dee262a-ab04-45c1-8a8c-fdbbd708869f
**Question**: Which BSON data type can be used to store an array of documents?
**Options**:
  - A) Integer
  - B) String
  * C) Array
  - D) ObjectId
**Alignment Logic**: The question asks about BSON data types. The lesson explicitly lists 'array' as a BSON type under Section 1 (BSON Types) and mentions the distinction between 'array' and 'object' in the Exam Radar section.

### Q8. ID: e98eee52-9b81-4467-851b-0d20884c88c8
**Question**: Which BSON data type in MongoDB can store multiple values of different types?
**Options**:
  * A) Array
  - B) String
  - C) ObjectId
  - D) Boolean
**Alignment Logic**: The question tests the student's understanding of BSON types. The lesson explicitly lists 'array' as a BSON type and discusses the flexibility of document structures and data types (BSON Types) in Section 1.

### Q9. ID: b3bb5f3f-5723-46d3-9623-ae6b1157c50e
**Question**: Which of the following BSON data types can be used as field values in MongoDB documents?
**Options**:
  * A) String
  - B) Array
  - C) ObjectId
  - D) Date
**Alignment Logic**: The question asks about BSON data types used as field values. The lesson explicitly lists 'string', 'array', 'ObjectId', and 'double' as examples of BSON types in Section 1, and mentions 'Date' (via the `ISODate()` vs `new Date()` discussion) in Sections 3 and 6.

### Q10. ID: b61a47bd-8c0b-46fb-9a7c-c25697d95ec4
**Question**: Which of the following BSON data types can be used to store an array of integers within a single document field?
**Options**:
  - A) String
  - B) Integer
  * C) Array
  - D) Object
**Alignment Logic**: The lesson explicitly mentions 'array' as a BSON type and discusses how documents can contain various types (like integers/doubles) and nested structures. The student can identify 'Array' as the correct BSON type for storing a list of values based on the provided content.

### Q11. ID: certcoach-t01-bson-data-types-easy-004-0ccef6dd
**Question**: Which BSON data type is best for storing a list of nested documents inside one MongoDB document?
**Options**:
  * array
  - String
  - Boolean
  - Decimal128
**Alignment Logic**: The lesson explicitly mentions 'array' and 'object' as BSON types and includes a specific exam signal regarding the distinction between 'array' and 'object' when querying nested data structures. The question tests the student's ability to identify the correct BSON type (array) for a collection of items.

### Q12. ID: 1cf65439-edd6-4eb4-9c5e-b0d9e4e03b05
**Question**: Which BSON type is best for storing precise monetary values?
**Options**:
  - Double
  * Decimal128
  - String
  - Int64
**Alignment Logic**: The lesson explicitly mentions 'Decimal128' as the correct choice over 'double' for precise calculations in the 'Exam Radar' section (specifically under the signal: 'Incorrect use of double instead of decimal128 for precise calculations').

### Q13. ID: certcoach-t01-bson-data-types-easy-015-008d7321
**Question**: Which characteristic of the BSON format allows MongoDB collections to have a flexible and dynamic data model compared to traditional relational tables?
**Options**:
  - BSON requires every document in a collection to share the exact same field names and types.
  * BSON allows documents within the same collection to have varying fields and different data types.
  - BSON is a text-based format that makes it easier for humans to read than JSON.
  - BSON only supports primitive types like strings and integers, excluding complex structures like arrays.
**Alignment Logic**: No reason recorded.

## 4. Unaligned Questions Detail & Gaps
### U1. ID: ecac0547-e08f-4621-a9d4-6c84a89ff5b2
**Question**: Which numeric type is a valid MongoDB BSON type? (Choose 1)
**Options**:
  - Float
  * Number
  - BIGINT
  - 32-bit integer
**Reason for Non-Alignment**: The lesson mentions 'double' and 'decimal128' as specific BSON types, but it does not list or define 'Float', 'Number', 'BIGINT', or '32-bit integer'. A student cannot determine which of these is the correct BSON type based solely on the provided text.

### U2. ID: a58bfbd7-ea57-4a6b-b4a5-b386f84d287f
**Question**: You will be asked to identify which food item is not a food item.
**Options**:
  - A) Mushroom
  - B) Mobile Food Vendor
  * C) AstroTurf
  - D) Sandwich
**Reason for Non-Alignment**: The question is completely unrelated to the lesson content. The lesson covers BSON types, MongoDB document structures, and technical performance considerations (like COLLSCANs), while the question asks about food items.

### U3. ID: 2f73cfd2-4e3f-47dd-92c6-eb53d3c945e2
**Question**: What are the steps to be followed when reporting a Yahoo Mail issue?
**Options**:
  - A) Go to the Yahoo Mail login page and click on 'Forgot your password?'
  - B) Click on 'I can't access my account'
  * C) Contact Yahoo Customer Support
  - D) Visit the Yahoo Mail Help Center
**Reason for Non-Alignment**: The question is completely unrelated to the lesson content. The lesson covers MongoDB BSON types, document structure, and technical performance considerations, while the question asks about Yahoo Mail customer support procedures.

### U4. ID: d558e041-4efc-46c8-ad74-5fff8c8d911b
**Question**: Which of the following is NOT a valid BSON data type in MongoDB?
**Options**:
  - A) String
  - B) Integer
  - C) Undefined
  * D) Float
**Reason for Non-Alignment**: The lesson mentions that BSON includes 'different data types' and lists examples like 'double', 'string', 'object', and 'array', but it does not provide a comprehensive list of all valid vs. invalid BSON types. A student cannot determine if 'Undefined' or 'Float' are valid/invalid based solely on the provided text.

### U5. ID: 27815195-c01c-45c0-acf8-55e17d91a88e
**Question**: Which of the following is a valid MongoDB BSON data type used to store a 64-bit integer value?
**Options**:
  - A) string
  - B) int
  * C) long
  - D) double
**Reason for Non-Alignment**: The lesson mentions 'double' and 'ObjectId', but it does not mention 'int', 'long', or specify which BSON types correspond to specific bit-lengths (like 64-bit integers). A student cannot determine the correct answer based solely on the provided text.

### U6. ID: cc1b7e28-9b1c-4cf6-889c-9fe403ef1009
**Question**: What is a key consideration when working with BSON Data Types at an medium level?
**Options**:
  * Always refer to official MongoDB developer specs.
  - Use random parameters without validation.
  - Bypass schemas in all environments.
  - Mix driver languages within the same file.
**Reason for Non-Alignment**: The question asks about considerations at a 'medium level' (intermediate), but the provided options are unrelated to the content of the lesson. The lesson discusses BSON types in terms of flexibility, performance impacts (like COLLSCANs), and specific data type choices (ObjectId vs string, decimal128 for precision), none of which are reflected in the multiple-choice options.

### U7. ID: 61ca97a2-fbeb-4c48-96b6-b20d610d6d11
**Question**: What is a key consideration when working with BSON Data Types at an hard level?
**Options**:
  * Always refer to official MongoDB developer specs.
  - Use random parameters without validation.
  - Bypass schemas in all environments.
  - Mix driver languages within the same file.
**Reason for Non-Alignment**: The question asks about 'hard level' considerations, but the lesson only categorizes content into Beginner, Intermediate, and Advanced. Furthermore, none of the provided options (official specs, random parameters, bypassing schemas, or mixing driver languages) are mentioned or discussed in the lesson text.

### U8. ID: fe44eb86-d61c-4d73-b620-575b3e7e7c1c
**Question**: What is the data type of the following variable?
**Options**:
  - A) Integer
  - B) Float
  * C) String
  - D) Boolean
**Reason for Non-Alignment**: The question asks for the data type of a 'variable', but no variable or code snippet was provided in the question text. Furthermore, even if a variable were provided, the lesson focuses on BSON types (like ObjectId, double, and decimal128) rather than standard programming primitives like Integer, Float, or Boolean.

### U9. ID: 23597d81-4540-493d-b5e3-95619b9f3576
**Question**: What is a key consideration when working with BSON Data Types at an easy level?
**Options**:
  * Always refer to official MongoDB developer specs.
  - Use random parameters without validation.
  - Bypass schemas in all environments.
  - Mix driver languages within the same file.
**Reason for Non-Alignment**: The question asks for a 'key consideration' at an 'easy level,' but the lesson does not provide specific guidelines or rules for easy-level tasks beyond a general analogy. Furthermore, none of the provided options (official specs, random parameters, bypassing schemas, or mixing languages) are mentioned or discussed in the lesson text.

### U10. ID: 3436f161-76d0-40bf-8f04-e0782247114d
**Question**: Which BSON data type can store any combination of other BSON types, including documents and arrays?
**Options**:
  - A) String
  - B) Array
  * C) Object
  - D) Binary
**Reason for Non-Alignment**: The question asks for a specific BSON type that can store 'any combination of other BSON types'. While the lesson mentions 'object' and 'array' as BSON types and discusses document structure flexibility, it never defines or describes the specific nesting capabilities or the technical definition of an 'Object' (or 'Document') as the container for other types. The student cannot determine which specific type among the options is the correct one based solely on the provided text.

### U11. ID: 4ed8f2a9-c8c6-4754-a5b8-a5dfa979db20
**Question**: Which of the following statements correctly describes how MongoDB handles document relationships?
**Options**:
  - A. Documents can only be embedded within other documents.
  * B. MongoDB supports both embedding and referencing data for relationships.
  - C. Relationships between documents must be defined using a relational schema.
  - D. Embedding documents is the only way to model relationships in MongoDB.
**Reason for Non-Alignment**: The lesson content focuses on BSON types (ObjectId, double, date), document structure flexibility, and performance considerations like COLLSCANs. It does not mention or explain data modeling strategies such as 'embedding' vs. 'referencing' or how MongoDB handles relationships between documents.

### U12. ID: 7dc461d1-f522-4081-bfcc-bb0554b9a777
**Question**: Which of the following BSON data types cannot be used as an element in an array field within a MongoDB document?
**Options**:
  - A) String
  - B) Integer
  * C) Array
  - D) ObjectId
**Reason for Non-Alignment**: The lesson does not provide a list of BSON types that are restricted from being used within arrays. It mentions several BSON types (string, object, array, double, ObjectId) but never discusses limitations or restrictions on which types can be placed inside an array.

### U13. ID: da253190-44fb-43b1-87bc-3653dc29cfb7
**Question**: Which of the following statements correctly describes how document relationships are modeled in MongoDB?
**Options**:
  - A) Relationships are not supported in MongoDB.
  * B) Documents can be embedded within other documents or referenced using Object IDs.
  - C) All related data must be stored in separate collections.
  - D) Relationships are only possible through the use of arrays.
**Reason for Non-Alignment**: The lesson content focuses on BSON types (ObjectId, double, decimal128), document structure flexibility, and performance implications like COLLSCANs. It does not mention or explain data modeling techniques such as 'embedding' vs. 'referencing', nor does it discuss how relationships are established between documents.

### U14. ID: certcoach-t01-bson-data-types-hard-002-a45fa677
**Question**: In MongoDB, which BSON data type cannot be used as an element in an array field within a document?
**Options**:
  - string
  - integer
  * array
  - boolean
**Reason for Non-Alignment**: The lesson does not state that any specific BSON types are prohibited from being used within an array. It mentions that documents can contain 'any number of fields with varying types' and lists several types (string, object, array) as valid BSON types, but it provides no information regarding restrictions on elements within arrays.

### U15. ID: certcoach-t01-bson-data-types-medium-006-bffd3533
**Question**: Which BSON type is best for storing related fields together inside a parent document?
**Options**:
  - array
  * embedded document
  - string
  - integer
**Reason for Non-Alignment**: The term 'embedded document' (or 'object') is not explicitly defined as a method for grouping related fields in the text. While the lesson mentions 'object' as a BSON type and discusses 'nested data structures', it does not provide specific guidance or terminology regarding the best practice of nesting fields within a parent document to group them.

### U16. ID: certcoach-t01-bson-data-types-easy-014-51abaecc
**Question**: A developer is troubleshooting a query that fails to return documents where a 'price' field contains decimal values. The query uses `{ price: { $type: "int" } }`. Which BSON type should the developer use instead to ensure both integers and decimals are matched?
**Options**:
  * Use the "number" alias with the $type operator.
  - Change the type to "double" to include all floating-point values.
  - Update the query to use the $isNumber aggregation operator.
  - Switch the BSON type to "long" to support 64-bit integer values.
**Reason for Non-Alignment**: The question requires knowledge of specific BSON type aliases (like 'number'), specific query operators ($type: "int"), and aggregation operators ($isNumber), none of which are mentioned in the lesson. While the lesson mentions that using the wrong BSON type can cause performance issues or precision problems, it does not provide the technical specifications for the '$type' operator or the list of valid BSON type aliases needed to solve this specific problem.

### U17. ID: certcoach-t01-bson-data-types-medium-013-9ca01103
**Question**: A developer is designing a schema to store financial transaction amounts that require high precision. Which BSON type should be used to ensure the values are stored as 128-bit decimals rather than standard floating-point numbers?
**Options**:
  - double
  - long
  * decimal
  - int
**Reason for Non-Alignment**: The question asks for 'decimal128' (implied by 128-bit decimals), but the lesson only mentions that using 'double' instead of 'decimal128' is a risk for precision. The specific term 'decimal128' or the option 'decimal' is not explicitly defined as a BSON type in the provided text; the lesson only lists 'double', 'string', 'object', and 'array' as examples.

### U18. ID: certcoach-t01-document-structure-easy-005-6f544a73
**Question**: A developer is designing a schema to store high-precision financial transactions. They want to ensure that the 'transactionAmount' field stores a 64-bit integer value while the 'timestamp' field uses the native BSON Date type. Which statement correctly describes how these values are represented in the MongoDB document?
**Options**:
  * The transactionAmount must be stored as a NumberLong and timestamp as a Date.
  - Both fields can be stored as standard JSON numbers, which MongoDB automatically converts to 64-bit integers.
  - The transactionAmount must be stored as an Integer and the timestamp as a String to ensure precision.
  - The transactionAmount must be stored as a Decimal128 type to support high-precision arithmetic.
**Reason for Non-Alignment**: The question introduces specific BSON types like 'NumberLong' and 'Decimal128', which are not mentioned in the lesson. While the lesson mentions that 'double' vs 'decimal128' is an exam signal for precision, it does not provide enough information to determine if 'NumberLong' is the correct representation for a 64-bit integer or how specific types map to those requirements.

### U19. ID: certcoach-t01-document-structure-medium-008-24b4c899
**Question**: A developer is migrating legacy data into a MongoDB collection. One record contains a high-precision counter that exceeds 2^53 - 1. Which BSON type should be used to ensure this value remains accurate and does not lose precision during the migration?
**Options**:
  - NumberInt
  * NumberLong
  - Double
  - String
**Reason for Non-Alignment**: The lesson mentions that using 'double' instead of 'decimal128' for precise calculations is an exam signal, but the question asks the student to choose between NumberInt, NumberLong, Double, and String. The specific thresholds (like 2^53 - 1) and the specific types 'NumberInt' or 'NumberLong' are not mentioned in the lesson text.

## 5. Gap Analysis & Lesson Enhancement Proposals
Based on the unaligned questions, the following concepts are tested but missing or brief in the lesson markdown:
- **Decimal128 vs Double Precision**: Multiple questions test the exact usage of `Decimal128` (128-bit decimal) for monetary/financial data where rounding errors of `Double` (64-bit float) are unacceptable.
- **Integer Limits and Representation (NumberInt vs NumberLong)**: Questions test how MongoDB handles 32-bit integers (`NumberInt`) and 64-bit integers (`NumberLong`) and their thresholds (e.g. 2^53 - 1 limit in JS numbers).
- **$type Operator & BSON Aliases**: Several questions test how to query by BSON types using the `$type` operator and its BSON string aliases (e.g., `'number'`, `'int'`, `'long'`, `'double'`).

### Enhancement Recommendation:
By expanding the BSON Data Types lesson text to explicitly define BSON representation limitations, monetary data types (Decimal128), and integer thresholds, we can safely promote the high-quality general questions to 'aligned' status without writing new questions or quarantining valid exam-level materials.