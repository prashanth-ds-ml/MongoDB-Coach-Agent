# Syllabus Audit Details: Gaps & Unaligned Questions

## Topic 1: MongoDB Overview & The Document Model

### Concept: BSON Data Types
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson context. The text explicitly defines 'ObjectId' as a 12-byte value used as a unique identifier and highlights its importance in the 'Exam Radar' section regarding its role as an optimized type for specific use cases (like identification) versus other BSON types.)
* **Total Questions**: 32 (Aligned: 13, General: 19)
* **Unaligned Gaps Detail**:
  - **Q ID**: `ecac0547-e08f-4621-a9d4-6c84a89ff5b2`
    * **Text**: Which numeric type is a valid MongoDB BSON type? (Choose 1)
    * **Reason**: The lesson mentions 'double' and 'decimal128' as specific BSON types, but it does not list or define 'Float', 'Number', 'BIGINT', or '32-bit integer'. A student cannot determine which of these is the correct BSON type based solely on the provided text.

  - **Q ID**: `a58bfbd7-ea57-4a6b-b4a5-b386f84d287f`
    * **Text**: You will be asked to identify which food item is not a food item.
    * **Reason**: The question is completely unrelated to the lesson content. The lesson covers BSON types, MongoDB document structures, and technical performance considerations (like COLLSCANs), while the question asks about food items.

  - **Q ID**: `2f73cfd2-4e3f-47dd-92c6-eb53d3c945e2`
    * **Text**: What are the steps to be followed when reporting a Yahoo Mail issue?
    * **Reason**: The question is completely unrelated to the lesson content. The lesson covers MongoDB BSON types, document structure, and technical performance considerations, while the question asks about Yahoo Mail customer support procedures.

  - **Q ID**: `d558e041-4efc-46c8-ad74-5fff8c8d911b`
    * **Text**: Which of the following is NOT a valid BSON data type in MongoDB?
    * **Reason**: The lesson mentions that BSON includes 'different data types' and lists examples like 'double', 'string', 'object', and 'array', but it does not provide a comprehensive list of all valid vs. invalid BSON types. A student cannot determine if 'Undefined' or 'Float' are valid/invalid based solely on the provided text.

  - **Q ID**: `27815195-c01c-45c0-acf8-55e17d91a88e`
    * **Text**: Which of the following is a valid MongoDB BSON data type used to store a 64-bit integer value?
    * **Reason**: The lesson mentions 'double' and 'ObjectId', but it does not mention 'int', 'long', or specify which BSON types correspond to specific bit-lengths (like 64-bit integers). A student cannot determine the correct answer based solely on the provided text.

  - **Q ID**: `cc1b7e28-9b1c-4cf6-889c-9fe403ef1009`
    * **Text**: What is a key consideration when working with BSON Data Types at an medium level?
    * **Reason**: The question asks about considerations at a 'medium level' (intermediate), but the provided options are unrelated to the content of the lesson. The lesson discusses BSON types in terms of flexibility, performance impacts (like COLLSCANs), and specific data type choices (ObjectId vs string, decimal128 for precision), none of which are reflected in the multiple-choice options.

  - **Q ID**: `61ca97a2-fbeb-4c48-96b6-b20d610d6d11`
    * **Text**: What is a key consideration when working with BSON Data Types at an hard level?
    * **Reason**: The question asks about 'hard level' considerations, but the lesson only categorizes content into Beginner, Intermediate, and Advanced. Furthermore, none of the provided options (official specs, random parameters, bypassing schemas, or mixing driver languages) are mentioned or discussed in the lesson text.

  - **Q ID**: `fe44eb86-d61c-4d73-b620-575b3e7e7c1c`
    * **Text**: What is the data type of the following variable?
    * **Reason**: The question asks for the data type of a 'variable', but no variable or code snippet was provided in the question text. Furthermore, even if a variable were provided, the lesson focuses on BSON types (like ObjectId, double, and decimal128) rather than standard programming primitives like Integer, Float, or Boolean.

  - **Q ID**: `23597d81-4540-493d-b5e3-95619b9f3576`
    * **Text**: What is a key consideration when working with BSON Data Types at an easy level?
    * **Reason**: The question asks for a 'key consideration' at an 'easy level,' but the lesson does not provide specific guidelines or rules for easy-level tasks beyond a general analogy. Furthermore, none of the provided options (official specs, random parameters, bypassing schemas, or mixing languages) are mentioned or discussed in the lesson text.

  - **Q ID**: `3436f161-76d0-40bf-8f04-e0782247114d`
    * **Text**: Which BSON data type can store any combination of other BSON types, including documents and arrays?
    * **Reason**: The question asks for a specific BSON type that can store 'any combination of other BSON types'. While the lesson mentions 'object' and 'array' as BSON types and discusses document structure flexibility, it never defines or describes the specific nesting capabilities or the technical definition of an 'Object' (or 'Document') as the container for other types. The student cannot determine which specific type among the options is the correct one based solely on the provided text.

  - **Q ID**: `4ed8f2a9-c8c6-4754-a5b8-a5dfa979db20`
    * **Text**: Which of the following statements correctly describes how MongoDB handles document relationships?
    * **Reason**: The lesson content focuses on BSON types (ObjectId, double, date), document structure flexibility, and performance considerations like COLLSCANs. It does not mention or explain data modeling strategies such as 'embedding' vs. 'referencing' or how MongoDB handles relationships between documents.

  - **Q ID**: `7dc461d1-f522-4081-bfcc-bb0554b9a777`
    * **Text**: Which of the following BSON data types cannot be used as an element in an array field within a MongoDB document?
    * **Reason**: The lesson does not provide a list of BSON types that are restricted from being used within arrays. It mentions several BSON types (string, object, array, double, ObjectId) but never discusses limitations or restrictions on which types can be placed inside an array.

  - **Q ID**: `da253190-44fb-43b1-87bc-3653dc29cfb7`
    * **Text**: Which of the following statements correctly describes how document relationships are modeled in MongoDB?
    * **Reason**: The lesson content focuses on BSON types (ObjectId, double, decimal128), document structure flexibility, and performance implications like COLLSCANs. It does not mention or explain data modeling techniques such as 'embedding' vs. 'referencing', nor does it discuss how relationships are established between documents.

  - **Q ID**: `certcoach-t01-bson-data-types-hard-002-a45fa677`
    * **Text**: In MongoDB, which BSON data type cannot be used as an element in an array field within a document?
    * **Reason**: The lesson does not state that any specific BSON types are prohibited from being used within an array. It mentions that documents can contain 'any number of fields with varying types' and lists several types (string, object, array) as valid BSON types, but it provides no information regarding restrictions on elements within arrays.

  - **Q ID**: `certcoach-t01-bson-data-types-medium-006-bffd3533`
    * **Text**: Which BSON type is best for storing related fields together inside a parent document?
    * **Reason**: The term 'embedded document' (or 'object') is not explicitly defined as a method for grouping related fields in the text. While the lesson mentions 'object' as a BSON type and discusses 'nested data structures', it does not provide specific guidance or terminology regarding the best practice of nesting fields within a parent document to group them.

  - **Q ID**: `certcoach-t01-bson-data-types-easy-014-51abaecc`
    * **Text**: A developer is troubleshooting a query that fails to return documents where a 'price' field contains decimal values. The query uses `{ price: { $type: "int" } }`. Which BSON type should the developer use instead to ensure both integers and decimals are matched?
    * **Reason**: The question requires knowledge of specific BSON type aliases (like 'number'), specific query operators ($type: "int"), and aggregation operators ($isNumber), none of which are mentioned in the lesson. While the lesson mentions that using the wrong BSON type can cause performance issues or precision problems, it does not provide the technical specifications for the '$type' operator or the list of valid BSON type aliases needed to solve this specific problem.

  - **Q ID**: `certcoach-t01-bson-data-types-medium-013-9ca01103`
    * **Text**: A developer is designing a schema to store financial transaction amounts that require high precision. Which BSON type should be used to ensure the values are stored as 128-bit decimals rather than standard floating-point numbers?
    * **Reason**: The question asks for 'decimal128' (implied by 128-bit decimals), but the lesson only mentions that using 'double' instead of 'decimal128' is a risk for precision. The specific term 'decimal128' or the option 'decimal' is not explicitly defined as a BSON type in the provided text; the lesson only lists 'double', 'string', 'object', and 'array' as examples.

  - **Q ID**: `certcoach-t01-document-structure-easy-005-6f544a73`
    * **Text**: A developer is designing a schema to store high-precision financial transactions. They want to ensure that the 'transactionAmount' field stores a 64-bit integer value while the 'timestamp' field uses the native BSON Date type. Which statement correctly describes how these values are represented in the MongoDB document?
    * **Reason**: The question introduces specific BSON types like 'NumberLong' and 'Decimal128', which are not mentioned in the lesson. While the lesson mentions that 'double' vs 'decimal128' is an exam signal for precision, it does not provide enough information to determine if 'NumberLong' is the correct representation for a 64-bit integer or how specific types map to those requirements.

  - **Q ID**: `certcoach-t01-document-structure-medium-008-24b4c899`
    * **Text**: A developer is migrating legacy data into a MongoDB collection. One record contains a high-precision counter that exceeds 2^53 - 1. Which BSON type should be used to ensure this value remains accurate and does not lose precision during the migration?
    * **Reason**: The lesson mentions that using 'double' instead of 'decimal128' for precise calculations is an exam signal, but the question asks the student to choose between NumberInt, NumberLong, Double, and String. The specific thresholds (like 2^53 - 1) and the specific types 'NumberInt' or 'NumberLong' are not mentioned in the lesson text.


### Concept: Document structure
* **Micro-Challenge Status**: Not Aligned (The question fails on two counts: 1. It includes an incomplete option (C), which makes it impossible to answer correctly as a standalone question. 2. Option A contains information not present in the text; while the text mentions `ObjectId` is used if `_id` is omitted, it does not state that `ObjectId` 'guarantees uniqueness across collections automatically'. The focus of the lesson is on document structure and BSON types, not cross-collection logic.)
* **Total Questions**: 11 (Aligned: 7, General: 4)
* **Unaligned Gaps Detail**:
  - **Q ID**: `4fdc02ab-dc51-4986-8dcc-d8c955f16180`
    * **Text**: How many documents are there in the image?
    * **Reason**: The question asks to count documents 'in the image', but there is no image provided in the lesson context. Furthermore, the lesson focuses on BSON types, field constraints, and document structure, not visual identification of objects.

  - **Q ID**: `aba60959-c4e4-4c5a-8964-aadcc708f378`
    * **Text**: Which of the following statements about document structure in MongoDB is true?
    * **Reason**: The question includes options that are not addressed in the lesson. Specifically, 'All collections must be created before inserting any documents' and 'Each document must use a sequential integer as its identifier' are concepts (implicit collection creation and ID types) not mentioned in the text. Furthermore, while the lesson mentions field flexibility, it does not explicitly state that data types can differ between documents; it only states that fields can vary and that BSON types are strict within specific values.

  - **Q ID**: `certcoach-t01-document-structure-hard-003-c1924b6c`
    * **Text**: In MongoDB, when designing a document model, which of the following best demonstrates how to structure data that is frequently accessed together?
    * **Reason**: The question asks about 'how to structure data that is frequently accessed together,' which involves architectural design decisions (Embedding vs. Referencing). The provided lesson only covers the basic definition of Embedded Documents as a way to create nested structures and notes that they allow complex modeling without separate collections, but it does not provide specific guidance or rules on how to decide between embedding versus referencing based on access patterns.

  - **Q ID**: `certcoach-t01-document-structure-easy-002-e99ac5b4`
    * **Text**: A developer is designing a schema for a product catalog. Which of the following statements correctly describes the constraints on field names within a MongoDB document?
    * **Reason**: The question asks about constraints on field names (specifically mentioning dots and dollar signs), but the lesson text explicitly states that field names *can* contain dots (.) and dollar signs ($) as long as they are literal field names. The option 'Field names must be unique and cannot contain dots (.) or dollar signs ($)' contradicts the provided lesson content.


### Concept: Collections vs Tables
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core concept of 'Schema Flexibility vs. Rigidity' and the fact that MongoDB collections do not enforce a fixed set of fields (columns) for every document, whereas relational tables require all rows to conform to a defined schema.)
* **Total Questions**: 26 (Aligned: 25, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `7a62b8f0-1b37-4d45-a9ab-81e62f526ee1`
    * **Text**: What is the relationship between the MongoDB database and MongoDB Atlas?
    * **Reason**: The lesson content focuses exclusively on the structural differences between MongoDB Collections and SQL Tables (schema flexibility, BSON documents, and automatic _id generation). It does not mention or define 'MongoDB Atlas' or its role as a cloud-based service.


## Topic 2: CRUD Operations - Create

### Concept: insertOne()
* **Micro-Challenge Status**: Not Aligned (The question contains two issues regarding alignment. 1) Option D is a fact from the text, but because there are two correct answers (B and D), the question is technically flawed as a single-choice question. 2) Option C introduces 'multiple collections', which is not mentioned in the lesson context and could be interpreted as a leak or an irrelevant distractor.)
* **Total Questions**: 15 (Aligned: 9, General: 6)
* **Unaligned Gaps Detail**:
  - **Q ID**: `37b42d0c-6766-4956-a76c-bc1d3e2ea726`
    * **Text**: Which of the following query documents should you use to ensure that only the documents with the specified zip codes are returned? (Select one.)
    * **Reason**: The question asks about query operators (like $in and $nin) and filtering logic, but the provided lesson context only covers the `insertOne()` method for inserting data. The lesson does not mention query syntax, selection criteria, or any methods used to retrieve documents.

  - **Q ID**: `0bdeb2a6-9f87-426b-bdf1-13341bcf1915`
    * **Text**: What is the correct output of the query?
    * **Reason**: The question asks for the 'correct output of the query', but no query is provided in the prompt. Furthermore, the options provided are full document objects, whereas the lesson states that `insertOne()` returns a result object containing `acknowledged` and `insertedId`, not the original document itself.

  - **Q ID**: `b077a760-c5fb-4073-b267-d8872d228fba`
    * **Text**: Inserting documents into MongoDB collection
    * **Reason**: The question provided ('Inserting documents into MongoDB collection') is not a multiple-choice question; it is a statement/title. Furthermore, the options provided are grammatically similar variations of each other and do not test any specific concepts, mechanics, or 'Exam Signals' (such as result shapes, write concerns, or _id uniqueness) defined in the lesson.

  - **Q ID**: `c1da65a9-3293-4a95-870c-07d959505bfc`
    * **Text**: For what reason do you want to create a new account?
    * **Reason**: The question is completely unrelated to the lesson content. The lesson covers MongoDB's `insertOne()` method, document structure, and write concerns, while the question asks about account creation reasons.

  - **Q ID**: `e5a71ce9-17be-467f-868d-895a47fe728c`
    * **Text**: United Airlines is the only airline that has a route from Denver Airport (DEN) to Northwest Arkansas Airport (XNA). It has decided to cancel this route. Which of the following queries will correctly delete the route?

Note: The data is in the `routes` collection of the `sample_training` database.
    * **Reason**: The question asks about deleting a document using 'deleteOne', but the provided lesson context only covers the 'insertOne()' operation. The concepts of deletion, the 'deleteOne' method, and the specific query syntax for filtering by fields like 'src_airport' or 'dst_airport' are not mentioned in the lesson.

  - **Q ID**: `certcoach-t02-insertone-medium-001-7c6f1eac`
    * **Text**: A developer is using the mongosh shell to insert a new user document into the 'users' collection. Which of the following commands correctly uses the `insertOne()` method to insert a single document while explicitly defining the write concern?
    * **Reason**: The question asks the student to identify the 'correct' way to define a write concern. While the lesson includes an example of a valid write concern (w: 'majority'), it does not provide enough information to determine why one specific syntax is correct over another (e.g., why {writeConcern: { w: 1}} is correct vs {writeConcern: 1}). Furthermore, the question asks for 'the' correct command among four options where two of them are technically valid MongoDB syntaxes ({w: 1} and {w: 'majority'}), making it impossible to distinguish between them based solely on the provided text.


### Concept: insertMany()
* **Micro-Challenge Status**: Not Aligned (The question contains two major issues regarding alignment: 1. It introduces 'PyMongo' and a Python script context; the lesson text specifies that while drivers have limits, the content provided focuses on the MongoDB Shell and general driver behavior without providing specific Python syntax or library-specific details. 2. The code snippet uses `insert_one()` (Python/PyMongo style) instead of `insertOne()` (MongoDB Shell style). Since the lesson specifically covers `insertMany()` and `insertOne()` in the context of the MongoDB Shell, introducing a different language's API violates the rule against leaking outside content or using non-standard syntax.)
* **Total Questions**: 16 (Aligned: 15, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t02-insertmany-medium-001-204b30cd`
    * **Text**: A developer is using the mongosh shell to perform a bulk insert of multiple documents into a collection and needs to capture the resulting IDs.
    * **Reason**: The question asks for the correct way to 'capture' the result, but the options provided are syntactically inconsistent with the lesson. The lesson specifies that insertMany() returns an array of IDs in a field called `insertedIds` (plural). One option uses `inserted_ids` (snake_case), which is not mentioned; another suggests accessing it as a property on the result object, but the question doesn't specify if the user wants the raw response or just the specific field. Most importantly, the options provided are slightly ambiguous regarding whether they are checking for the correct key name or the correct method of access.


### Concept: _id and ObjectId
* **Micro-Challenge Status**: Not Aligned (The question is not strictly aligned because option C is a 'double' truth. While both A and C are correct based on the text, the question format (multiple choice) implies only one answer is correct. Furthermore, the lesson states that if you provide an _id, it must be unique; Option B says it can be duplicates, which is false, but because there are two true statements (A and C), the question is technically flawed as a single-choice quiz.)
* **Total Questions**: 17 (Aligned: 14, General: 3)
* **Unaligned Gaps Detail**:
  - **Q ID**: `3ae187a9-1942-4530-bc5c-fe7ce7ca36da`
    * **Text**: Which of the following commands correctly inserts multiple documents into a collection using `insertMany()` in MongoDB Shell (mongosh)?
    * **Reason**: The question asks about the `insertMany()` method and its specific syntax for multiple documents. While the 'Exam Radar' section mentions that students might get confused between `insertOne()` and `insertMany()`, the lesson text does not provide any code examples, syntax rules, or explanations for the `insertMany()` method itself; it only provides details for `insertOne()`.

  - **Q ID**: `d1324d3e-f4a2-4c9c-8e98-43530547c7c6`
    * **Text**: Which of the following commands correctly inserts a single document into a MongoDB collection using the `mongosh` shell?
    * **Reason**: The question includes options (B and D) that feature 'writeConcern' parameters. These parameters are not mentioned anywhere in the provided lesson context. While option A is aligned with the lesson's code examples, a student cannot determine if B or D are incorrect based solely on the provided text because the concept of write concerns is never introduced.

  - **Q ID**: `4fdd255c-9ee7-46c4-ac5e-198ad61eccc9`
    * **Text**: Which of the following MongoDB commands correctly inserts a document into a collection and returns an `insertedId` value?
    * **Reason**: The question asks which command returns an 'insertedId' value. While the lesson mentions that insertOne() returns 'insertedId', it does not provide enough information to distinguish between the options provided. Specifically, the lesson does not mention 'writeConcern' or its impact on return values, and it does not specify that insertMany() returns 'insertedIds' (plural) instead of 'insertedId'. A student cannot determine why the third and fourth options are incorrect based solely on the provided text.


## Topic 3: CRUD Operations - Read

### Concept: find()
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A reflects the 'Intermediate' section regarding the difference between find() and findOne(). Option B reflects the 'Core Concept' and 'Design Choices' sections regarding projections. Option C directly addresses the 'Exam Trap' in Section 3 regarding the default behavior of the _id field.)
* **Total Questions**: 5 (Aligned: 1, General: 4)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t03-find-easy-002-584460de`
    * **Text**: A developer is using PyMongo to retrieve all documents where the 'status' field is 'active'. Which of the following code snippets correctly implements this using the `find()` method?
    * **Reason**: The question introduces 'PyMongo' and a specific Python-style syntax (e.g., .all()), which are not mentioned or defined in the lesson. The lesson only provides JavaScript/Shell style examples for MongoDB methods.

  - **Q ID**: `certcoach-t03-find-easy-002-1a6a42a3`
    * **Text**: A developer needs to retrieve all documents from a collection that match a specific filter criteria using the PyMongo driver. Which method should be used to return an iterable result set of all matching documents?
    * **Reason**: The question specifies the 'PyMongo driver', which is not mentioned in the lesson. The lesson focuses on general MongoDB concepts and standard syntax (e.g., db.collection.find()), whereas PyMongo-specific implementation details are outside the provided context.

  - **Q ID**: `certcoach-t03-find-medium-001-d767e2ce`
    * **Text**: A developer needs to retrieve all documents from a 'products' collection where the 'category' is 'electronics'. Which PyMongo method call correctly returns a cursor for these results?
    * **Reason**: The question introduces 'PyMongo' and the specific method syntax `collection.find(query=...)`, which are not mentioned or defined in the lesson. The lesson only provides standard MongoDB shell-style syntax (e.g., `db.collection.find()`). Additionally, the inclusion of `.count()` as an option involves a method not covered in the provided text.

  - **Q ID**: `certcoach-t03-find-easy-003-a0bc4c1f`
    * **Text**: A developer uses the PyMongo `find()` method to query a collection containing 50 documents that match the specified filter. What is the return type of the operation?
    * **Reason**: The question introduces 'PyMongo' and specific Python data types (like 'list of Python dictionaries'), which are not mentioned in the lesson. The lesson focuses on general MongoDB concepts and JavaScript-style syntax; it does not provide information regarding specific language drivers or their specific return type implementations.


### Concept: findOne()
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The text explicitly compares `findOne()` to `find().limit(1)` in the 'Design Choices' and 'DON'T / EXAM TRAP Example' sections, noting that `findOne()` is more efficient and less complex for retrieving a single document.)
* **Total Questions**: 21 (Aligned: 4, General: 17)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t03-find-easy-001-807ee5a6`
    * **Text**: A developer needs to retrieve a single document from the 'products' collection where the category is 'electronics'. Which PyMongo method call correctly returns the result as a Python dictionary?
    * **Reason**: The question asks specifically about 'PyMongo' and a 'Python dictionary'. The provided lesson context does not mention PyMongo, Python, or any specific programming language libraries; it focuses on MongoDB shell/general methods. Furthermore, the lesson mentions that findOne() behaves differently in PyMongo versus the shell (returning a document vs. a cursor), but it does not provide the specific PyMongo syntax or library-specific details required to distinguish between the options provided.

  - **Q ID**: `certcoach-t03-find-easy-002-788fee2a`
    * **Text**: A developer needs to retrieve a single document from the 'inventory' collection where the 'status' is 'available'. Which PyMongo method call correctly returns the result as a Python dictionary?
    * **Reason**: The question asks specifically for a 'PyMongo method' and a result as a 'Python dictionary'. The lesson context does not provide any information regarding PyMongo, Python-specific syntax (like .to_dict()), or the specific behavior of find_one() in the PyMongo library. While it mentions a 'PyMongo vs. Shell' difference in the Exam Radar, it does not provide the actual technical details or code examples required to distinguish between them.

  - **Q ID**: `certcoach-t03-find-medium-001-34f86029`
    * **Text**: A developer is using PyMongo to retrieve a single document from the 'products' collection where the category is 'electronics'. Which of the following code snippets correctly implements this using the appropriate method and query filter?
    * **Reason**: The question introduces 'PyMongo' and specific Python-style syntax (e.g., .first(), .next()), which are not covered in the provided lesson. While the lesson mentions a 'PyMongo vs. Shell' difference in the Exam Radar section, it does not provide any PyMongo code examples or specify that `find_one()` is the correct method for PyMongo; therefore, a student cannot determine the correct answer based solely on the provided text.

  - **Q ID**: `certcoach-t03-find-easy-001-10d75a9c`
    * **Text**: When using the PyMongo driver to retrieve data, what is the primary difference between the return types of the find() and find_one() methods?
    * **Reason**: The question asks about PyMongo-specific behavior (Python dictionary vs. cursor), but the lesson context only mentions 'PyMongo' in a brief note under 'Exam Radar' regarding shell differences. The lesson does not provide any details, code examples, or explanations regarding Python types, dictionaries, or specific PyMongo driver implementation details.

  - **Q ID**: `certcoach-t03-find-easy-001-e332221f`
    * **Text**: Given a collection containing two documents that match the filter `{'type': 'fast_food'}`, what will the PyMongo `find_one()` method return?
    * **Reason**: The question asks about 'PyMongo' and the 'find_one()' method. The provided lesson context focuses on MongoDB shell/general syntax (e.g., findOne(), printjson()) and does not mention PyMongo or its specific implementation differences.

  - **Q ID**: `certcoach-t03-find-easy-001-be5cf33d`
    * **Text**: A developer is using PyMongo to retrieve a specific user profile and wants to ensure that only the 'username' and 'email' fields are returned, while explicitly excluding the '_id' field.
    * **Reason**: The question introduces 'PyMongo' and a specific requirement to exclude the '_id' field. The lesson context does not provide any information regarding PyMongo (it only mentions it in a brief 'Exam Radar' note about differences between shell and PyMongo), nor does it explain how to explicitly exclude fields using 0; it only mentions inclusion rules (1) for projections.

  - **Q ID**: `certcoach-t03-find-medium-001-f6eea02a`
    * **Text**: A developer is using PyMongo to retrieve a single document from the 'products' collection where the category is 'electronics'. Which of the following code snippets correctly implements this using the appropriate method?
    * **Reason**: The question introduces PyMongo-specific methods (such as .one() and .first()) which are not mentioned in the lesson. Furthermore, the 'Exam Radar' section explicitly notes that findOne() behaves differently in PyMongo versus the shell, but the lesson does not provide any specific PyMongo code examples or syntax to help a student distinguish between the options provided.

  - **Q ID**: `certcoach-t03-find-medium-001-def3cf28`
    * **Text**: Given a collection containing two documents matching the query { "status": "active" }, what will the PyMongo `find_one()` method return?
    * **Reason**: The question asks about 'PyMongo' and the `find_one()` method. The lesson context focuses on MongoDB shell/general syntax and specifically mentions in the 'Exam Radar' section that PyMongo behaves differently than the shell (noting that findOne() returns a document in PyMongo vs a cursor in some contexts). However, the lesson does not provide any specific details, code examples, or rules regarding PyMongo or Python-specific implementations to allow a student to answer this accurately based solely on the provided text.

  - **Q ID**: `certcoach-t03-findone-easy-001-0a8860c0`
    * **Text**: A developer needs to retrieve a single document from the 'users' collection where the status is 'active', but only wants to return the 'username' and 'email' fields. Which mongosh command is syntactically correct?
    * **Reason**: The question includes an option using `.one()`, which is not mentioned or defined anywhere in the provided lesson context. Additionally, one of the options includes a third argument `{limit: 1}` for `findOne()`, which is not part of the syntax described in the lesson (the lesson only shows query and projection as arguments).

  - **Q ID**: `certcoach-t03-findone-easy-001-e28b332f`
    * **Text**: A developer needs to retrieve a single document from the 'users' collection where the status is 'active', but only wants to return the 'username' and 'email' fields.
    * **Reason**: The question includes an option using the .one() method (db.users.find(...).one()), which is not mentioned or defined anywhere in the provided lesson context.

  - **Q ID**: `certcoach-t03-findone-easy-001-751babc8`
    * **Text**: When using the `findOne()` method to retrieve a single document, how does the behavior of the projection parameter differ from the `find()` method?
    * **Reason**: The question asks how the behavior of the projection parameter in `findOne()` *differs* from the `find()` method. The lesson context does not provide any information regarding a difference in projection behavior between these two methods; it only explains what projection is and how to use it within both contexts.

  - **Q ID**: `certcoach-t03-findone-easy-001-e5313423`
    * **Text**: A developer is trying to retrieve only the 'title' and 'description' fields from a document using findOne(), but they also included a field exclusion for 'metadata'. What will happen?
    * **Reason**: The question asks about the behavior of 'mixing inclusion and exclusion' (e.g., using both 1 and 0) in a single projection. The lesson mentions that 'Projection Inclusion/Exclusion' is an exam topic, but it does not provide any rules, logic, or examples regarding what happens when both are used together; it only shows simple inclusion examples like { name: 1, age: 1 }.

  - **Q ID**: `certcoach-t03-findone-medium-001-3416d054`
    * **Text**: A developer needs to retrieve a single document from the 'users' collection where the status is 'active', but only wants the 'username' and 'email' fields returned.
    * **Reason**: The question includes an option using the .one() method (db.users.find(...).one()), which is not mentioned or defined anywhere in the provided lesson context.

  - **Q ID**: `certcoach-t03-findone-medium-002-4af59e29`
    * **Text**: A developer wants to retrieve a single document from the 'inventory' collection where the 'sku' is 'ABC-123', but they must exclude the 'internal_notes' field from the result.
    * **Reason**: The question requires knowledge of exclusion rules (using '0' to exclude a field), but the provided lesson text only mentions inclusion ('1') and does not explicitly define or provide examples for exclusion syntax. Additionally, the option using '.next()' is not mentioned in the lesson.

  - **Q ID**: `certcoach-t03-findone-medium-001-c5c3bdd9`
    * **Text**: Given a collection of products, what is the result of executing `db.products.findOne({ category: "electronics" }, { name: 1, price: 0 })` if a matching document exists with fields `{ name: "Phone", price: 500 }`?
    * **Reason**: The question requires knowledge of 'exclusion' rules in projections (using `0` to exclude a field). While the lesson mentions 'Projection Inclusion/Exclusion' in the Exam Radar section, it does not provide any specific rules, code examples, or explanations for how `0` behaves versus `1`. The student cannot determine if `price: 0` results in an excluded field or a null value based solely on the provided text.

  - **Q ID**: `certcoach-t03-find-easy-001-26686a5a`
    * **Text**: You are using the PyMongo driver to retrieve a single document from the 'restaurants' collection where the name is 'Pasta Palace'. Which method call correctly returns the result as a Python dictionary?
    * **Reason**: The question asks about the PyMongo driver and specifically mentions returning a 'Python dictionary'. The lesson context only covers MongoDB shell/general syntax. Furthermore, the 'Exam Radar' section notes that findOne() behaves differently in PyMongo versus the shell, but the lesson does not provide the specific Python-specific implementation details (like the underscore in `find_one()` or the requirement for a dictionary return) needed to distinguish between the provided options.

  - **Q ID**: `certcoach-t03-find-easy-002-3624e42a`
    * **Text**: When using the PyMongo driver to retrieve documents, which method should be used if your application logic requires receiving a single document as a Python dictionary rather than a cursor object?
    * **Reason**: The question asks about PyMongo-specific implementation details (the difference between `findOne()` and `find_one()`). While the 'Exam Radar' section mentions that PyMongo and the shell have different behaviors regarding cursors vs. documents, the lesson text does not provide any information on PyMongo syntax or the specific method names used in the Python driver.


### Concept: Projections
* **Micro-Challenge Status**: Not Aligned (The Micro-Challenge section is empty. No question was provided for evaluation. Please provide the question text to determine if it aligns with the lesson context.)
* **Total Questions**: 13 (Aligned: 8, General: 5)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t03-projections-easy-001-2265fc5f`
    * **Text**: Given a collection of products, what fields will be returned by the following query: db.products.find({}, { name: 1, description: 0 })?
    * **Reason**: The question tests a scenario that violates the 'Design Choice: Inclusion vs. Exclusion Logic' and the 'Exam Trap' sections of the lesson. The lesson states that you cannot mix inclusion (1) and exclusion (0) in the same projection object (except for _id). Specifically, it explains that if you use inclusion syntax like { name: 1 }, MongoDB assumes all other fields are excluded; however, by including 'description: 0' alongside 'name: 1', the query technically violates the logic rules described. Furthermore, the lesson states that '_id' is included by default unless explicitly set to 0. Because the question doesn't specify the status of '_id', a student following the lesson would know that '_id' would be present in the result, making 'Only the name field' an incorrect answer based on the provided text.

  - **Q ID**: `certcoach-t03-projections-medium-001-3d13a2ea`
    * **Text**: A developer wants to retrieve only the 'title' and 'thumbnail' fields from a collection of products using the `find()` method. Which projection document correctly implements this requirement?
    * **Reason**: The question asks for a projection that retrieves 'title' and 'thumbnail', but the provided options include one where 'thumbnail' is set to 0 (exclusion) and another where 'thumbnail' is set to true. While the lesson explains inclusion/exclusion, it does not explicitly state that `true` is an acceptable synonym for `1` in all contexts of the projection object; however, more importantly, the question cannot be answered definitively because two options (the second and fourth) are technically valid ways to include both fields based on the text's definition of inclusion (any non-zero integer or true). The lesson does not provide a specific 'correct' way to choose between `1` and `true` for this specific scenario.

  - **Q ID**: `certcoach-t03-projections-medium-001-ddebcd69`
    * **Text**: A developer attempts to retrieve only the 'title' and 'description' fields from a collection using a projection that explicitly excludes the '_id' field, but they also include a request for the 'author' field.
    * **Reason**: The question describes a scenario involving 'mixed' inclusion and exclusion (requesting specific fields while also excluding _id). The lesson states that you cannot mix inclusion and exclusion except for the '_id' field. However, the provided options do not accurately reflect the logic described in the lesson; specifically, the lesson explains that if any field is included (1), all other fields are excluded by default, but it does not provide a mechanism to 'mix' them as the question implies. Furthermore, the question's premise of 'inclusion taking precedence over exclusion' or 'overriding' is not a concept mentioned in the text.

  - **Q ID**: `certcoach-t03-countdocuments-medium-001-900c7929`
    * **Text**: A developer needs to count how many documents in the 'inventory' collection have a 'status' of 'active', while specifically excluding the 'internal_notes' field from the calculation.
    * **Reason**: The question asks for a 'count' operation. The provided lesson context only covers the `find()` method and its projection parameters. It does not mention or define the `countDocuments()` method or the `.count()` method, nor does it explain how projections affect count operations.

  - **Q ID**: `certcoach-t03-countdocuments-medium-001-b91d7baa`
    * **Text**: When using the `countDocuments()` method to determine the number of documents matching a specific filter, how does the inclusion of a projection document affect the returned count?
    * **Reason**: The question asks about the `countDocuments()` method and how projections affect its result. The provided lesson context only covers the `find()` method and the mechanics of Projections (inclusion/exclusion, memory limits, and the _id exception). There is no mention of the `countDocuments()` method or any discussion on how projection logic interacts with count operations.


### Concept: Cursors
* **Micro-Challenge Status**: Not Aligned (The question contains elements that are not covered in the lesson text and introduces external logic. Specifically: 1) Option B includes a 'for...in' loop over a cursor and an array push/check logic which is not discussed; 2) Option C mentions 'findOne()', which is explicitly excluded from the core concept of cursors (the text notes that findOne() is used instead of find() to avoid returning a cursor); 3) The question asks for the 'correct' approach, but since none of the options provided are actually the recommended 'best practice' described in the lesson (which is using .forEach()), it creates ambiguity. To be strictly aligned, the question should focus on the difference between .toArray() and .forEach().)
* **Total Questions**: 10 (Aligned: 0, General: 10)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t03-cursors-easy-001-8d8a69c6`
    * **Text**: You are using PyMongo to retrieve multiple documents from a collection; which of the following code snippets correctly demonstrates how to iterate over the resulting cursor?
    * **Reason**: The question asks about 'PyMongo' (a Python driver), while the lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax'. Furthermore, the options include methods like .find_all() and .fetch(), which are not mentioned in the lesson.

  - **Q ID**: `certcoach-t03-cursors-easy-001-13776197`
    * **Text**: You are using PyMongo to retrieve multiple documents from a collection; which of the following code snippets correctly demonstrates how to iterate over the results returned by the `find()` method?
    * **Reason**: The question asks about 'PyMongo' (Python driver) syntax and methods like `.to_list()` or `.each()`, whereas the lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh)' syntax. The lesson does not mention Python-specific libraries or PyMongo-specific methods.

  - **Q ID**: `certcoach-t03-cursors-easy-001-e442afb6`
    * **Text**: When using the PyMongo driver to perform a read operation that returns multiple documents, what is the primary architectural reason for the driver returning a cursor instead of a full list of results?
    * **Reason**: The question specifically mentions the 'PyMongo driver', whereas the lesson context explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and warns to avoid 'driver-specific nuances'. Additionally, while the lesson explains why cursors are used (memory/bandwidth), the student cannot answer this specific question because the term 'PyMongo' is never mentioned in the text.

  - **Q ID**: `certcoach-t03-cursors-easy-001-cd8e981a`
    * **Text**: You are using PyMongo to fetch results from a collection. When you execute `results = collection.find()`, what is the nature of the `results` object and how does it handle memory?
    * **Reason**: The question mentions 'PyMongo', which is a Python driver. The lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and warns to avoid 'driver-specific nuances'. Additionally, the option mentioning a 'generator' refers to a Python-specific implementation of an iterator, which is not discussed in the provided text.

  - **Q ID**: `certcoach-t03-cursors-easy-001-b060f309`
    * **Text**: A developer is processing a large result set from a `collection.find()` operation using PyMongo and notices that memory usage remains low even as they iterate through thousands of documents. Why does this occur?
    * **Reason**: The question references 'PyMongo' (a Python driver) and specific internal implementation details like 'batches' and '100 documents per batch'. The lesson context explicitly states it focuses on MongoDB Shell (mongosh) syntax and does not mention PyMongo or the specific technical mechanics of how drivers handle batching.

  - **Q ID**: `certcoach-t03-cursors-medium-001-dbc5b4ce`
    * **Text**: You are using PyMongo to retrieve a list of documents from a collection; which code snippet correctly demonstrates how to iterate over the results returned by the `find()` method?
    * **Reason**: The question asks about 'PyMongo' (a Python driver), whereas the lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax'. Additionally, the options provided include methods like `.to_list()`, which are not mentioned in the lesson.

  - **Q ID**: `certcoach-t03-cursors-medium-001-bea48471`
    * **Text**: You are using PyMongo to fetch a large set of documents from a collection; which approach correctly handles the memory efficiency benefits of a cursor when processing results?
    * **Reason**: The question refers to 'PyMongo', which is a Python driver. The lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and warns against 'driver-specific nuances'. Additionally, the code examples in the options use Python-style syntax (e.g., `list(results)`, `len(results)`), whereas the lesson only provides JavaScript/Shell examples (`toArray()`, `forEach()`).

  - **Q ID**: `certcoach-t03-cursors-medium-001-0914852a`
    * **Text**: When using PyMongo to perform a read operation that returns multiple documents, what is the primary architectural reason for the driver returning a cursor instead of a full list of results?
    * **Reason**: The question mentions 'PyMongo', which is a Python driver. The lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and warns to avoid 'driver-specific nuances'. Additionally, the lesson explains the architectural reason as 'streaming results row-by-row' or 'lazy evaluation,' but the question introduces an external technology (PyMongo) not mentioned in the text.

  - **Q ID**: `certcoach-t03-cursors-medium-001-3af4263f`
    * **Text**: When using PyMongo to perform a read operation that returns multiple documents, what is the primary architectural benefit of the driver returning a cursor instead of a full list?
    * **Reason**: The question references 'PyMongo' and 'Python dictionary objects', which are specific to a Python driver. The lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and warns against 'driver-specific nuances'. Furthermore, the conversion of BSON to Python types is not mentioned in the text.

  - **Q ID**: `certcoach-t03-cursors-medium-001-d292c2c9`
    * **Text**: A developer executes `results = collection.find()` on a collection containing 1,000 documents. How does the PyMongo driver handle these results when the developer iterates over the `results` object using a `for` loop?
    * **Reason**: The question asks specifically about how the 'PyMongo driver' handles results. The lesson context explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and warns to avoid 'driver-specific nuances.' Therefore, a question regarding PyMongo is not aligned with the provided content.


### Concept: sort/limit/skip
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It addresses the 'Stable Sort' and 'In-Memory vs. Index Scan' concepts by requiring a tie-breaker for non-unique fields (like `signupDate`). The requirement to ensure consistency and avoid in-memory sorts directly maps to the 'Best Practice' section of the text, which recommends adding a unique field like `_id` to the sort criteria. It does not require knowledge of any outside topics or advanced features not mentioned in the text.)
* **Total Questions**: 10 (Aligned: 2, General: 8)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t03-sort-limit-skip-easy-001-dcc23e38`
    * **Text**: In a mongosh environment, which of the following commands correctly applies a limit to a query that retrieves only the first 5 documents from the 'products' collection?
    * **Reason**: The question asks about the `.limit()` method and how to retrieve a specific number of documents. However, the provided lesson context focuses exclusively on the `sort()` method, BSON type hierarchy during sorting, and memory limits for unindexed sorts. The lesson does not contain any information regarding the `.limit()` method or its syntax.

  - **Q ID**: `certcoach-t03-sort-limit-skip-easy-001-92c2c193`
    * **Text**: You are using the mongosh shell to retrieve only the first 25 documents from a collection named 'products' that match a specific query; which of the following is the correct syntax?
    * **Reason**: The question asks for the correct syntax to limit results (using .limit()), but the provided lesson context focuses exclusively on the .sort() method and its implications (BSON hierarchy, memory limits, and tie-breaking). The lesson does not provide any information regarding the syntax or parameters of the .limit() method.

  - **Q ID**: `certcoach-t03-sort-limit-skip-easy-001-e865ac54`
    * **Text**: When using the `limit()` method on a cursor to optimize performance, at what point must the limit be applied relative to data retrieval?
    * **Reason**: The question asks about the timing/placement of 'limit()' relative to data retrieval (a performance optimization concept). The lesson only mentions 'limit' in the context of its interaction with 'sort' and 'skip' (specifically that 'skip' is applied before 'limit' regardless of code order), but it does not discuss 'data retrieval' stages or the specific timing of when a limit is applied to optimize performance.

  - **Q ID**: `certcoach-t03-sort-limit-skip-easy-001-54dcfdd8`
    * **Text**: A collection contains 100 documents matching a specific query. What is the result of executing `db.collection.find({status: "active"}).limit(5)`?
    * **Reason**: The question tests the behavior of `.limit()` on a query without an explicit `.sort()`. While the lesson mentions that `SKIP` and `LIMIT` are applied after sorting, it does not provide any information regarding how `.limit()` behaves alone or what 'first' means in the absence of a deterministic sort. The student cannot determine if the result is 'consistent' or 'random' based solely on the provided text.

  - **Q ID**: `certcoach-t03-sort-limit-skip-medium-001-5e97f9f0`
    * **Text**: A developer is using the mongosh shell to retrieve only the first 25 results from a query on the 'products' collection; which of the following syntactically correct statements correctly applies the limit?
    * **Reason**: The question asks about the correct syntax for applying a 'limit' operation. The provided lesson context focuses exclusively on the 'sort()' method, its internal mechanics (IXSCAN vs SORT), BSON type hierarchy, and memory limits. The lesson does not provide any information, syntax rules, or examples regarding the .limit() method or how it interacts with other methods like .toArray() or .count().

  - **Q ID**: `certcoach-t03-sort-limit-skip-medium-001-4d589ff4`
    * **Text**: A developer is using the mongosh shell to retrieve only the first 25 results from a query on the 'products' collection; which of the following syntactically correct statements applies the limit correctly?
    * **Reason**: The question asks about the correct syntax for applying a .limit() method. While the lesson mentions that .limit() is used in conjunction with .sort(), it does not provide any information regarding the specific syntax or placement of the .limit() method itself. The student cannot determine which option is syntactically correct based solely on the provided text.

  - **Q ID**: `certcoach-t03-sort-limit-skip-medium-001-0f97fde2`
    * **Text**: When implementing a pagination feature using the mongosh shell, what is the primary architectural reason for applying the .limit() method to a cursor?
    * **Reason**: The lesson does not discuss the 'architectural reason' for using .limit(), nor does it mention multi-key indexes, findOne() conversions, or the 16MB BSON document size limit. While the lesson mentions that .limit() is used in conjunction with .sort() and .skip(), it does not provide any technical context regarding why .limit() itself is used.

  - **Q ID**: `certcoach-t03-sort-limit-skip-medium-001-4225ad61`
    * **Text**: A developer is implementing a pagination feature and wants to ensure that only the first 25 results are processed by the application logic. Which of the following practices correctly optimizes performance and prevents unnecessary data transfer?
    * **Reason**: The question asks about optimizing performance and preventing unnecessary data transfer by limiting results. While the lesson mentions .limit() and .skip(), it does not provide any information regarding 'data transfer' optimization or the specific mechanics of how .limit() affects network/server overhead compared to manual counting. The lesson focuses on sorting, memory limits for unindexed sorts (100MB), and the order of operations between sort, skip, and limit, but does not provide enough context to determine which method 'optimizes performance' in the way described by the question.


### Concept: countDocuments()
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The text explicitly states in the 'Do's & Don'ts' section that 'db.users.countDocuments({})' is the correct way to count all documents because an empty query filter {} matches all documents. Options A, B, and C are not supported or are identified as incorrect/traps within the context of the provided material.)
* **Total Questions**: 8 (Aligned: 6, General: 2)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t03-countdocuments-easy-001-3b6e6d0e`
    * **Text**: When performing a count of documents that match a specific filter, which method should be used to ensure an accurate count by scanning the collection based on the provided query?
    * **Reason**: The question asks which method should be used for an accurate count by scanning the collection. While the lesson emphasizes `countDocuments()` as the correct method, the options provided include `db.collection.find().count()`, `db.collection.count()`, and `db.collection.find().countDocuments()`. The lesson does not mention or define the `.find()` method or the `.count()` method (which is often deprecated or behaves differently), making it impossible for a student to determine why the other options are incorrect based solely on the provided text.

  - **Q ID**: `certcoach-t03-countdocuments-medium-001-0642afed`
    * **Text**: A developer needs to determine the exact number of documents in a collection that match a specific filter before performing a bulk update; which method should they use to ensure an accurate count based on the query criteria?
    * **Reason**: The question includes options like 'db.collection.estimatedDocumentCount()' and 'db.collection.find(query).count()', which are not mentioned or defined in the lesson context. The lesson focuses exclusively on countDocuments().


## Topic 4: CRUD Operations - Update

### Concept: replaceOne()
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core concept of 'Total Overwrite' (ensuring other fields are removed), uses the correct method (`replaceOne`), and requires the student to construct a replacement document based on specific requirements provided in the prompt without requiring external knowledge or advanced features like transactions or complex indexing.)
* **Total Questions**: 14 (Aligned: 5, General: 9)
* **Unaligned Gaps Detail**:
  - **Q ID**: `ac994245-3c3d-4e71-95cb-cf7e53845ca7`
    * **Text**: You need to update the following documents from POS to SQL Server:

1. 2016_05_POS_Sales_Report.xlsx
2. 2016_05_POS_Inventory_Report.xlsx
3. 2016_05_POS_Employee_Report.xlsx
4. 2016_05_POS_Customer_Report.xlsx

What should you do?
    * **Reason**: The question is completely unrelated to the lesson content. The lesson covers MongoDB's `replaceOne()` operation, including its mechanics, syntax, and differences from update operators. The question asks about migrating Excel files from a POS system to SQL Server, which involves data migration and ETL processes not mentioned in the text.

  - **Q ID**: `056ed890-f428-47ad-8d56-c400dec0f309`
    * **Text**: You must implement a method to update an object in a database. You should be able to update an object by specifying its id and the new values for its properties. The method should return the updated object.
    * **Reason**: The question asks for a Python-style function implementation (using `**kwargs` or similar syntax) and focuses on 'updating' properties. The lesson is specifically about the MongoDB `replaceOne()` method, which replaces an entire document rather than updating specific fields. Furthermore, the lesson does not cover Python programming concepts like keyword arguments (**), nor does it describe a method that returns the updated object (it notes that `replaceOne` returns an UpdateResult containing counts/IDs).

  - **Q ID**: `531b9130-81d5-4be2-a281-f4ceee144b5f`
    * **Text**: What should be done with the following data?
    * **Reason**: The question provided ('What should be done with the following data?') does not include any actual data, code snippets, or scenarios. Furthermore, the options (Add, Remove, Update) are generic and do not test the specific nuances of `replaceOne()` covered in the lesson, such as 'Total Overwrite vs. Partial Modification', 'Upsert Semantics', or '_id Immutability'.

  - **Q ID**: `certcoach-t04-replaceone-easy-001-e993e04c`
    * **Text**: You need to replace an existing document in a collection with a completely new set of fields using the PyMongo `replace_one()` method. Which of the following is the correct syntax for replacing a document where 'status' is 'inactive'?
    * **Reason**: The question asks for the 'PyMongo' `replace_one()` method. The provided lesson context only covers MongoDB Shell syntax (`db.collection.replaceOne()`) and does not mention Python-specific drivers, PyMongo libraries, or their specific naming conventions (e.g., snake_case vs camelCase).

  - **Q ID**: `certcoach-t04-replaceone-easy-001-b4237110`
    * **Text**: A developer needs to replace an entire document's content with a new set of fields using PyMongo. Which method call correctly implements this by replacing all existing fields except for the _id?
    * **Reason**: The question asks for a 'PyMongo' implementation, but the provided lesson context only covers MongoDB Shell syntax and general conceptual logic. The lesson does not mention PyMongo or any other specific programming language drivers/libraries.

  - **Q ID**: `certcoach-t04-replaceone-medium-001-cd7f3bb0`
    * **Text**: A developer wants to replace an existing document in a collection with a new set of fields, ensuring that all original fields (except _id) are removed and replaced by the new ones. Which PyMongo method call is syntactically correct for this operation?
    * **Reason**: The question asks for a 'PyMongo method call', but the lesson context only provides MongoDB Shell syntax (e.g., `db.collection.replaceOne()`). The PyMongo driver uses different naming conventions (snake_case vs camelCase) and is not mentioned or defined in the provided text.

  - **Q ID**: `certcoach-t04-replaceone-medium-001-c265fb39`
    * **Text**: A developer wants to completely replace a document's content with a new set of fields using the PyMongo `replace_one()` method. Which of the following code snippets correctly implements this operation?
    * **Reason**: The question asks for a 'PyMongo' implementation, but the lesson context only provides and discusses MongoDB Shell syntax. While the logic of `replaceOne` is similar, the specific library (PyMongo) and its method naming convention (`replace_one` vs `replaceOne`) are not mentioned in the provided text.

  - **Q ID**: `certcoach-t04-updateone-medium-001-79b5ad99`
    * **Text**: A developer wants to replace an entire document's content (except for the _id) with a new set of fields using the PyMongo driver. Which method call is syntactically correct?
    * **Reason**: The question asks for a 'PyMongo' driver implementation, but the lesson context only provides MongoDB Shell syntax. Additionally, the inclusion of '$replace' in the options introduces an operator not mentioned or defined in the lesson.

  - **Q ID**: `certcoach-t04-updateone-medium-002-52166121`
    * **Text**: A developer needs to replace an existing document's entire content (excluding the _id) with a new set of fields using the PyMongo driver. Which method call is syntactically correct?
    * **Reason**: The question asks for a 'PyMongo driver' implementation, but the lesson context only provides MongoDB Shell syntax and does not mention or define PyMongo-specific methods or Python-style naming conventions (e.g., `replace_one` vs `replaceOne`). A student relying strictly on the provided text would see `db.collection.replaceOne()` as the standard.


### Concept: updateOne()
* **Micro-Challenge Status**: Not Aligned (The question asks the user to use an 'appropriate operator for incrementing numbers' (which would be $inc). However, the provided lesson text only mentions and explains the $set operator. While it lists $inc as an example of a field-level operator in the 'Key Terms & Mechanics' section, it does not provide any details on its syntax, usage, or behavior. Therefore, the student cannot know the correct syntax for incrementing numbers based solely on the provided text.)
* **Total Questions**: 5 (Aligned: 1, General: 4)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t04-updateone-easy-001-62c03aa0`
    * **Text**: A developer wants to update only the 'status' field of a document where 'itemId' is 501 using the PyMongo `update_one()` method. Which of the following syntactically correct calls performs this specific partial update?
    * **Reason**: The question asks for a solution using the PyMongo `update_one()` method. The lesson context explicitly states that it focuses strictly on 'MongoDB Shell (mongosh) syntax' and provides examples in JavaScript/Shell format. Additionally, while the lesson mentions `$inc` as an operator, the specific scenario of updating a status string is only covered via the `$set` example.

  - **Q ID**: `certcoach-t04-updateone-easy-002-a729a807`
    * **Text**: A developer needs to update a single document by incrementing the 'viewCount' field by 5 while simultaneously updating the 'status' field to 'active'. Which approach correctly implements this partial update using PyMongo?
    * **Reason**: The question asks for a solution using 'PyMongo', but the lesson explicitly states that it focuses strictly on 'MongoDB Shell (mongosh)' syntax. Additionally, while the lesson mentions the `$inc` operator in passing within the text and the Micro-Challenge, it does not provide any code examples or detailed instructions for `$inc`, making it impossible to determine the correct multi-operator syntax solely from the provided material.

  - **Q ID**: `certcoach-t04-updateone-medium-001-8a53db00`
    * **Text**: A developer wants to update only the 'status' field of a document where the 'id' is 101 using the PyMongo `update_one()` method. Which of the following syntactically correct calls performs this specific partial update?
    * **Reason**: The question asks for a 'PyMongo' implementation, but the lesson context explicitly states that it focuses strictly on 'MongoDB Shell (mongosh)' syntax. Additionally, while the lesson mentions `$set` and `$inc`, it does not provide enough detail to confirm which specific operator is required for a simple field update versus an increment or push without the student bringing in outside knowledge of MongoDB operators.

  - **Q ID**: `certcoach-t04-updateone-medium-002-7be1ea87`
    * **Text**: A developer needs to update a single document's 'inventory' count by incrementing it by 5, while simultaneously updating its 'status' field to 'in_stock'. Which approach correctly implements this partial update using the `updateOne()` method?
    * **Reason**: The question requires knowledge of the `$inc` operator to perform a numeric increment. While the lesson mentions that `updateOne()` uses operators like `$set` and `$inc`, it never provides any code examples, syntax rules, or explanations for how the `$inc` operator specifically functions.


### Concept: updateMany()
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It requires the use of `updateMany` (implied by 'all matching documents simultaneously'), a query filter (items marked 'out_of_stock'), and an update document using the `$set` operator as described in the text. It explicitly forbids `replaceOne`, which aligns with the 'Don't/Exam Trap' section regarding replacement semantics.)
* **Total Questions**: 5 (Aligned: 2, General: 3)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t04-updatemany-easy-001-d8c1e071`
    * **Text**: A developer needs to update the 'status' field to 'active' for all documents where the 'type' is 'guest' using the PyMongo `update_many()` method. Which of the following syntactically correct calls performs this specific operation?
    * **Reason**: The question asks for a 'PyMongo' implementation (Python driver), whereas the lesson context specifically defines and provides examples for the 'MongoDB Shell' command. Additionally, while the logic of the update is similar, the Python syntax (e.g., `upsert=True` as a keyword argument) is not mentioned or covered in the provided text.

  - **Q ID**: `certcoach-t04-updatemany-easy-003-921d914b`
    * **Text**: A collection contains three documents with 'status': 'pending', 'pending', and 'active'. Which command correctly updates all 'pending' documents by incrementing their 'priority' field by 1?
    * **Reason**: The question requires knowledge of the `$inc` operator to perform an increment operation. While the lesson mentions `$inc` as a valid operator in the 'Update Document' section and the 'Advanced' section, it does not provide any code examples or specific explanations for how `$inc` functions compared to `$set`. A student can only be certain that `$inc` is the correct choice for 'incrementing' based on general MongoDB knowledge, not strictly from the provided text.

  - **Q ID**: `certcoach-t04-updatemany-medium-001-e3ef643f`
    * **Text**: A developer needs to update the 'status' field to 'active' and increment the 'viewCount' by 5 for all documents where the 'category' is 'promotional'. Which PyMongo method call correctly implements this multi-document update?
    * **Reason**: The question asks for a 'PyMongo method call', but the lesson context only covers 'MongoDB Shell' commands. Additionally, while the lesson mentions the '$inc' operator in the text and code examples, it does not explicitly define how to combine multiple operators (like $set and $inc) within a single update document; however, the primary reason for misalignment is the shift from MongoDB Shell syntax to PyMongo library-specific implementation.


### Concept: $set
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the 'Upsert Dependency' and 'Modifier Operator' sections of the text, which specify that $set does not create documents on its own (it only modifies existing fields) and requires an explicit `upsert: true` flag to perform an upsert. Since the scenario specifies no match is found and upsert is false, the student must conclude based on the text that nothing happens/no document is created.)
* **Total Questions**: 5 (Aligned: 2, General: 3)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t04-set-easy-001-27fcf1d6`
    * **Text**: A developer wants to update only the 'status' field of a document where the 'type' is 'active' using PyMongo; which command correctly uses the $set operator for this partial update?
    * **Reason**: The question asks for a solution using 'PyMongo', but the lesson context only covers MongoDB Shell (mongosh) syntax. While the logic of $set is similar, the specific method call structure and parameter naming (e.g., `upsert=True` as a keyword argument) are specific to the Python driver's API, which is not mentioned or defined in the provided text.

  - **Q ID**: `certcoach-t04-set-easy-003-a4dc9bfc`
    * **Text**: A collection contains a document: {"_id": 101, "name": "Cafe A", "status": "open"}. Which PyMongo operation correctly updates only the 'status' field to 'closed' while preserving the 'name' field?
    * **Reason**: The question asks for a 'PyMongo' operation, but the lesson context only covers MongoDB Shell (mongosh) syntax. While the logic of $set is consistent, the specific library implementation (PyMongo) and its method signatures are not mentioned in the provided text.

  - **Q ID**: `certcoach-t04-set-medium-001-d43e2225`
    * **Text**: A developer wants to update only the 'status' field of a document where 'id' is 101, ensuring other fields remain unchanged. Which PyMongo method call correctly implements this partial update?
    * **Reason**: The question asks for a 'PyMongo method call', but the lesson context only provides examples and instructions using MongoDB Shell (mongosh) syntax. The PyMongo library is not mentioned in the lesson.


### Concept: $push
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core concept of $push as an 'array append' operation (adding 'Sushi' to the existing list) and specifically addresses the distinction between modification ($push) and replacement (which would have wiped the other tags). The syntax provided matches the example in the text exactly.)
* **Total Questions**: 5 (Aligned: 4, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t04-push-easy-001-0ba972fb`
    * **Text**: A developer wants to add a new tag 'organic' to the 'tags' array of a document where the name is 'apple'. Which PyMongo update method correctly appends this value without overwriting the existing array?
    * **Reason**: The question introduces 'PyMongo' and its specific method syntax (e.g., .update_one()), which are not mentioned or defined in the lesson. The lesson focuses on MongoDB Shell/general update operations. Additionally, the inclusion of the 'multi' option in one of the choices is a concept not covered in the provided text.


### Concept: $inc
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It requires the use of the `$inc` operator (covered in Section 1 and 3), utilizes a query filter (explained in Section 3), and focuses on numeric field modification as described in the 'Do' example. The requirement for 'precise syntax and casing' directly addresses Trap 1 (Operator Casing Sensitivity) mentioned in the Exam Radar.)
* **Total Questions**: 6 (Aligned: 4, General: 2)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t04-inc-easy-001-1a6c9e8c`
    * **Text**: A developer needs to increment the 'view_count' field by 5 for a document where the 'title' is 'intro_to_mongo'. Which PyMongo update method and argument structure correctly implements this arithmetic operation?
    * **Reason**: The question asks for a 'PyMongo' update method. The provided lesson context only covers 'MongoDB Shell' syntax and examples (e.g., db.collection.updateOne). While the logic of the $inc operator is consistent, the specific Python driver syntax (PyMongo) is not mentioned or defined in the lesson.

  - **Q ID**: `certcoach-t04-inc-medium-001-de293c96`
    * **Text**: A developer needs to increment the 'viewCount' field by 5 for a specific document identified by its 'productId'. Which of the following PyMongo update operations correctly implements this using the $inc operator?
    * **Reason**: The question asks for a 'PyMongo' update operation (Python driver), but the lesson context only provides examples and instructions for the 'MongoDB Shell' (JavaScript/Shell syntax). Specifically, PyMongo uses snake_case methods like `update_one()`, whereas the lesson only covers the standard MongoDB shell method `updateOne()`.


### Concept: $unset
* **Micro-Challenge Status**: Aligned (The question is perfectly aligned with the lesson. It directly tests the 'Exam Signal' of distinguishing between $unset and $set as described in the text. The options provided reflect the specific examples given in the 'Do's & Don't' section, and the answer can be determined solely by following the rules established in the lesson.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: upsert
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The specific scenario regarding 'upsert: true' being used without specifying all fields and the resulting behavior (creating a document with only specified fields) is explicitly listed under 'Exam Signal 2' in the provided text.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: findAndModify
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A relates to the 'Update' and 'Query' components; Option B refers to the core functionality of finding/modifying (which includes deletion in standard MongoDB context, though the text focuses on update); Option C directly addresses the 'Upsert' feature explained in section 1; and Option D refers to the 'Sort' behavior described in section 1. None of the options require knowledge of external topics like transactions, sharding, or specific BSON types not mentioned in the text.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

## Topic 5: CRUD Operations - Delete

### Concept: deleteOne()
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core distinction between `delete_one()` and `delete_many()` as highlighted in both the 'Intermediate Learners' section and the 'Exam Trap' section of the text. The options provided use the exact syntax and examples (e.g., 'Ready Penny Inn') found in the lesson, and do not introduce any outside concepts like BSON types or advanced indexing.)
* **Total Questions**: 2 (Aligned: 0, General: 2)
* **Unaligned Gaps Detail**:
  - **Q ID**: `12bdf256-6ced-46bc-bba3-95ae9e490182`
    * **Text**: Will you help me?
    * **Reason**: The question and its options are completely unrelated to the provided lesson. The lesson covers MongoDB's `deleteOne()` method, query filters, and `DeleteResult` objects, while the question discusses 'pages' and 'moving documents to a new folder', which are not mentioned in the text.

  - **Q ID**: `7c955f66-95af-48f2-80b1-eb05075af6f8`
    * **Text**: Given the following documents, what will be the name of the file that was deleted?
    * **Reason**: The question refers to a set of 'documents' and asks for the name of a file that was deleted, but no code snippet, query filter, or collection of documents was provided in the question. Furthermore, the lesson context does not mention specific data types like 'files' or 'logs'; it only explains the mechanics of `deleteOne()`.


### Concept: deleteMany()
* **Micro-Challenge Status**: Not Aligned (The question contains multiple correct answers (A and C), which violates the standard of a single-choice micro-challenge. Additionally, while 'complex criteria' is mentioned in the text under Design Choices, option A is the primary definition provided in the Core Concept section. To be strictly aligned, the question should only have one clearly correct answer based on the text.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

## Topic 6: Query Operators & MQL

### Concept: Comparison ($eq, $gt, $lt, $in, $nin)
* **Micro-Challenge Status**: Not Aligned (The question is not strictly aligned because it asks for a 'less than or equal to' operation (which would typically use the $lte operator), but the lesson text does not define or mention the $lte operator. The lesson only covers $eq, $gt, $lt, $in, and $nin. Therefore, the correct answer is not provided in the source material.)
* **Total Questions**: 20 (Aligned: 7, General: 13)
* **Unaligned Gaps Detail**:
  - **Q ID**: `7971aab0-e26c-430d-a8fd-89d3e73d4682`
    * **Text**: Which of the following query documents would return all customers with a satisfaction rating of 1 or 2? (Select one.)
    * **Reason**: The question requires identifying a query for '1 or 2', which would logically be solved using the $in operator (e.g., { $in: [1, 2] }). However, the lesson does not mention the $lte operator, and the options provided include $lte, which is not defined in the lesson's list of comparison operators ($eq, $gt, $lt, $in, $nin).

  - **Q ID**: `08098d42-7503-417f-b5a1-04a2b7e6529b`
    * **Text**: Which of the following queries would return documents for all customers 65 or older? (Select all that apply.)
    * **Reason**: The question includes the '$gte' operator (greater than or equal to), which is not mentioned or defined in the lesson context. The lesson only covers $eq, $gt, $lt, $in, and $nin.

  - **Q ID**: `79ff826a-8e90-4ecf-8c89-d8a579a0b0a6`
    * **Text**: What is a key consideration when working with Finding Documents by Using Comparison Operators at an easy level?
    * **Reason**: The question asks about a 'key consideration' for beginners (easy level), but the provided options are unrelated to the content of the lesson. The lesson discusses comparison operators ($gt, $lt, etc.), BSON types, and specific traps like mixing logical/comparison operators or type mismatches, none of which are reflected in the provided multiple-choice options.

  - **Q ID**: `71d63d58-1720-4770-b0cb-d14e8d95e06f`
    * **Text**: Which of the following MongoDB queries correctly finds documents where the 'age' field is greater than 30 and the 'gender' field is 'Male'?
    * **Reason**: The question requires knowledge of how to combine multiple conditions (conjunctions) within a single query. The lesson only covers individual comparison operators ($gt, $lt, $eq, $in, $nin) and mentions logical operators ($and, $or) as a 'trap' to avoid when used incorrectly, but it does not provide instructions or syntax for combining multiple fields in a single find() statement.

  - **Q ID**: `3ea97e08-355d-44c4-9dd2-484df72c80ba`
    * **Text**: What is a key consideration when working with Finding Documents by Using Comparison Operators at an medium level?
    * **Reason**: The question asks about 'medium level' considerations, but the provided options do not relate to the content described in the 'Intermediate Learners' section of the lesson. The lesson mentions avoiding mixing logical operators with comparison operators as a trap for intermediate learners; however, none of the multiple-choice options reflect this information or any other concept mentioned in the text.

  - **Q ID**: `ee418101-0c1e-4b00-b45e-ddb19ce51d05`
    * **Text**: Consider the following MongoDB collection `users` with documents containing fields: `_id`, `name`, `age`, and `location`. You need to find users who are older than 30 years and live in either 'New York' or 'Los Angeles'. Which of the following Python code snippets correctly implements this query using PyMongo?
    * **Reason**: The question requires knowledge of PyMongo (Python) syntax and the .sort() method with constants like DESCENDING/ASCENDING. The lesson context only provides JavaScript-style MongoDB shell examples and does not mention Python, the PyMongo library, or sorting operations.

  - **Q ID**: `411174a7-4a05-44d3-9385-0ebb2c8ba555`
    * **Text**: Consider the following MongoDB collection `users` with documents containing fields: `_id`, `name`, and `scores`. Each `scores` field is an array of objects with `subject` and `score` properties. You need to find users who have scored more than 90 in both Mathematics and Physics. Which of the following queries correctly achieves this using comparison operators in MongoDB's aggregation framework?
    * **Reason**: The question introduces several concepts not covered in the lesson: 1) The Aggregation Framework (e.g., $match, $project), 2. Complex nested array structures (arrays of objects), and 3. The $elemMatch operator. The lesson only covers basic comparison operators ($eq, $gt, $lt, $in, $nin) used within a standard .find() method.

  - **Q ID**: `8ddd0d3f-b43a-42bb-b297-3157e7ad677f`
    * **Text**: Given the following MongoDB collection `products` with documents containing fields such as `name`, `price`, and `stock`, which of the following Python code snippets correctly uses comparison operators to find products where the price is greater than $50 and the stock quantity is less than 10, while also sorting by price in descending order?
    * **Reason**: The question is not aligned because it requires knowledge of Python/PyMongo syntax (e.g., `MongoClient`, `.sort()` method signatures) and the concept of sorting results ('sorting by price in descending order'), none of which are mentioned or explained in the lesson context.

  - **Q ID**: `8c49ddaf-d1de-4e14-9674-27560861f770`
    * **Text**: Consider the following MongoDB collection `orders` with documents containing fields: `_id`, `customer_id`, and `amount`. You need to find orders where the amount is between $100 and $500, but exclude any orders where the customer_id is 'admin'. Which of the following queries correctly implements this logic using comparison operators in MongoDB's Python driver?
    * **Reason**: The question is not aligned because it requires knowledge of operators not included in the lesson. Specifically, the logic 'exclude any orders where the customer_id is admin' would require the use of '$ne' (not equal) or '$nin', neither of which are defined in the lesson. Additionally, the question asks for a solution using the 'Python driver', but the lesson only provides JavaScript-style syntax and does not mention Python or PyMongo.

  - **Q ID**: `certcoach-t06-element-exists-type-medium-001-b0cf275b`
    * **Text**: Which query operator selects documents where a field exists in a specified array?
    * **Reason**: The question asks about the '$exists' operator (or a concept related to field existence), which is not mentioned in the lesson. While the lesson covers '$in', it does not mention '$exists' or '$type'. Therefore, a student cannot determine the correct answer using only the provided material.

  - **Q ID**: `certcoach-t06-element-exists-type-medium-002-becde3ef`
    * **Text**: Which operator selects documents where a field exists or does not exist in MongoDB?
    * **Reason**: The question asks about the '$exists' operator, which is not mentioned, defined, or included in the provided lesson context. The lesson only covers comparison operators ($eq, $gt, $lt, $in, $nin).

  - **Q ID**: `certcoach-t06-element-exists-type-medium-003-89bb3976`
    * **Text**: Which query operator selects documents where a field exists in an array?
    * **Reason**: The question asks about the '$exists' operator (or a concept related to existence), which is not mentioned in the lesson. While the lesson mentions '$in', it defines it as matching values within an array, not checking if a field exists in an array.

  - **Q ID**: `certcoach-t06-element-exists-type-medium-004-7790cee6`
    * **Text**: Which operator selects documents where a field exists or does not exist?
    * **Reason**: The question asks about the '$exists' operator, which is not mentioned, defined, or included in the provided lesson context. The lesson only covers comparison operators ($eq, $gt, $lt, $in, $nin).


### Concept: Logical ($and, $or, $not, $nor)
* **Micro-Challenge Status**: Not Aligned (The question is not strictly aligned because it is a 'prompt' rather than a 'question'. It asks the user to perform an action (find documents) without providing a specific choice or asking for a specific syntax. Furthermore, based on the 'Exam Trap' section in the lesson, this specific phrasing ('age is greater than 20 and status is active') is identified as a trap to test if the student knows they must use the $and operator. A properly aligned Micro-Challenge should ask the user to identify the correct syntax or the correct operator for that specific scenario.)
* **Total Questions**: 2 (Aligned: 1, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t06-logical-and-or-not-nor-medium-002-1f6a04c3`
    * **Text**: Which operator should you use to select documents where the value of a field equals any value in a specified array?
    * **Reason**: The question asks about the '$in' operator (matching a value against an array), which is not mentioned, defined, or included in the lesson context. The lesson only covers logical query operators: $and, $or, $not, and $nor.


### Concept: Element ($exists, $type)
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the specific requirement of ensuring both existence and data type (as shown in the 'Best Practice' example). Option A highlights the 'Exam Trap' mentioned in the text (only checking existence), Option C addresses the 'Exam Signal' regarding mixing up existence with equality, and Option D uses a different type than requested. All concepts used are explicitly defined in the lesson.)
* **Total Questions**: 1 (Aligned: 0, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t06-element-exists-type-medium-005-6e2b91a5`
    * **Text**: Which query operator selects documents where a field exists or has a specific BSON type?
    * **Reason**: The question asks for a single operator that performs both functions ('exists OR has a specific BSON type'), but the lesson defines these as two distinct operators ($exists and $type) used for different purposes. Furthermore, the phrasing 'or' in the question implies a choice between two functionalities that are actually handled by two separate tools in the text.


### Concept: Atlas Search query basics
* **Micro-Challenge Status**: Not Aligned (The question contains a significant conceptual mismatch with the lesson content. The question asks how to perform the query 'using Atlas Search', but the provided code examples and the 'Exam Trap' section describe standard MongoDB Query Language (MQL) using the `.find()` method. In actual MongoDB practice, Atlas Search uses the `$search` aggregation stage, not the `.find()` method shown in the options. Furthermore, option C is syntactically incorrect for MQL, but since the lesson doesn't define the syntax for `$or` (only mentions it as a logical operator), the question tests knowledge outside of the provided text by trying to distinguish between different ways to write an 'OR' condition.)
* **Total Questions**: 1 (Aligned: 0, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `e540e203-bcb9-4e04-b016-074e9568c76c`
    * **Text**: Consider the following MongoDB collection named `products` containing documents with fields: `_id`, `name`, `price`, and `rating`. You need to find products where the price is greater than $50 AND the rating is at least 4. Which of the following Python code snippets correctly performs this query using PyMongo?
    * **Reason**: The question is not aligned because it asks for a solution using 'PyMongo' (Python code), while the lesson context only covers MongoDB Query Language (MQL) syntax and Atlas Search concepts. Additionally, the lesson does not provide any information regarding Python integration or PyMongo library usage.


## Topic 7: Querying Arrays & Embedded Documents

### Concept: $elemMatch
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core distinction between using `$elemMatch` and direct comparison on an array field as described in both the 'Beginners' section and the 'Syntax & Code Examples (Do's & Don'ts)' section. The options provided directly mirror the 'DO' and 'DON'T' examples provided in the text.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: dot notation
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It directly tests the distinction between using dot notation alone versus $elemMatch for arrays of embedded documents, which is explicitly covered in the 'Advanced Developers' section and the 'DON'T / EXAM TRAP' section. The options provided mirror the exact examples given in the text.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: Array size queries
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It directly tests the core concept of using $elemMatch to query nested fields within an array (as shown in the Intermediate Learners and Do's & Don'ts sections) and specifically targets the 'Exam Signal' regarding the distinction between dot notation and $elemMatch for multi-condition array elements.)
* **Total Questions**: 33 (Aligned: 23, General: 10)
* **Unaligned Gaps Detail**:
  - **Q ID**: `f823f55e-4f70-4856-b09f-2abf2a4ad7ed`
    * **Text**: Which of the following MongoDB Python query will correctly find documents where the 'fruits' array contains both 'apple' and 'banana'? 

```python
from pymongo import MongoClient, ASCENDING

client = MongoClient()
db = client.mydatabase
collection = db.mycollection

# Option A
result = collection.find({'fruits': {'$all': ['apple', 'banana']}})

# Option B
result = collection.find({'fruits': {'$elemMatch': {'$in': ['apple', 'banana']}}})

# Option C
result = collection.find({{'fruits.$': 'apple'}, {'fruits.$': 'banana'}})

# Option D
result = collection.find({'fruits': {'$all': ['apple'], '$all': ['banana']}})

    * **Reason**: The question asks about finding an array containing 'apple' AND 'banana', which involves the $all operator. The provided lesson context only covers the $elemMatch operator and does not mention or explain the $all operator, nor does it provide examples of simple string matching within arrays.

  - **Q ID**: `01a6f730-3bd0-4d33-8f2a-5a0cd7e4b6d7`
    * **Text**: Which of the following MongoDB Python queries correctly finds documents where the 'tags' array contains both 'Python' and 'Coding'?
    * **Reason**: The question asks about finding elements containing two different values ('Python' and 'Coding') within an array. The lesson only covers $elemMatch for matching multiple criteria on a single element (e.g., product: 'xyz' AND score: 8). The correct operator for the logic described in the question is $all, which is not mentioned or explained in the provided lesson context.

  - **Q ID**: `8818f3f7-f743-45ba-9054-697d3f123abb`
    * **Text**: Which of the following MongoDB queries correctly filters documents where the 'fruits' array contains both 'apple' and 'banana'?
    * **Reason**: The question asks for a query to find an array containing multiple specific values ('apple' and 'banana'), which would typically require the $all operator. However, the lesson context only covers the $elemMatch operator for matching elements that satisfy multiple conditions within a single object (e.g., product: 'xyz' AND score: 8). The lesson does not mention or explain the $all operator or how to query for multiple independent values in an array.

  - **Q ID**: `06336790-6a73-4d78-9395-21732f198b19`
    * **Text**: Which of the following MongoDB queries correctly finds documents where the 'tags' array contains both 'Python' and 'Coding'?
    * **Reason**: The question asks to find an array containing two different string values ('Python' and 'Coding'). The lesson focuses exclusively on using $elemMatch to match multiple conditions within a single nested object inside an array. The lesson does not cover the $in or $all operators, nor does it provide guidance on how to query simple arrays of strings.

  - **Q ID**: `dff99d77-1968-4434-a51c-32140dbb0447`
    * **Text**: What is a key consideration when working with Querying on Array Elements in MongoDB at an easy level?
    * **Reason**: The question asks about 'key considerations' for a specific difficulty level (easy), but the provided options are unrelated to the lesson content. The lesson focuses on the mechanics, syntax, and performance of $elemMatch; it does not mention official developer specs, random parameters, bypassing schemas, or mixing driver languages.

  - **Q ID**: `9b90af13-76d1-4257-b58c-7d5f5193df7e`
    * **Text**: Which of the following MongoDB queries correctly identifies documents where at least one element in the 'tags' array contains the string 'python', and also returns only the 'title' field of these documents?
    * **Reason**: The question introduces two concepts not covered in the lesson: 1) Regular expressions (the `/python/` syntax), and 2) Projection (selecting only specific fields like 'title' using `{ title: 1, _id: 0 }`). The lesson focuses exclusively on the $elemMatch operator for array filtering.

  - **Q ID**: `c7a70971-f2fc-4852-ac08-e5c1688d4531`
    * **Text**: Consider the following MongoDB collection `inventory` with documents containing an array field `items`. Each item has a `name`, `quantity`, and `price`. Which of the following queries correctly finds products where at least one item's quantity is greater than 100?
    * **Reason**: The question asks for a query where 'at least one item's quantity is greater than 100'. While the lesson explains that $elemMatch is used to match multiple conditions on a single element, it does not state that $elemMatch is required for a single condition (like just 'quantity > 100'). Furthermore, the first option provided in the question uses an invalid syntax ($elemMatch: { items.quantity: ... }) which is not taught; the lesson teaches $elemMatch applied to the array field itself (e.g., { results: { $elemMatch: { ... } } }).

  - **Q ID**: `certcoach-t07-elemmatch-medium-002-d73de9c1`
    * **Text**: Which query will return documents from the `products` collection where the `tags` array contains at least one element that is both a string starting with 'tech' and has a length greater than 4?
    * **Reason**: The question requires knowledge of `$regex`, `$size`, and string length calculations (or a `$length` operator), none of which are mentioned or defined in the lesson. The lesson only covers basic comparison operators ($gte, $lt) and simple equality within the context of $elemMatch.

  - **Q ID**: `certcoach-t07-elemmatch-medium-008-f6bb6bd6`
    * **Text**: Which query will match documents where the `results` array contains at least one element that is both greater than or equal to `80` and less than `90`, but does not include any elements with a score of exactly `85`?
    * **Reason**: The question introduces a specific logic constraint (excluding a value exactly equal to 85) that requires knowledge of the $ne operator. The provided lesson context only covers $elemMatch with basic comparison operators ($gte, $lt) and does not mention or define the $ne operator.

  - **Q ID**: `certcoach-t07-elemmatch-hard-004-f992687b`
    * **Text**: Which query will return documents where the `results` array contains at least one embedded document with a `score` greater than or equal to 80 and a `product` that is either 'abc' or 'xyz'?
    * **Reason**: The question introduces the '$in' operator (or an array as a value for 'product') to handle multiple possible values ('abc' or 'xyz'). The provided lesson context only covers basic equality and range comparisons ($gte, $lt) within $elemMatch and does not mention or explain the '$in' operator.


## Topic 8: Aggregation Framework

### Concept: $match
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core definition of the $match stage as a 'gatekeeper' that filters documents based on conditions. The options provided are standard aggregation stages, but only $match is defined in this specific lesson context as the tool for filtering.)
* **Total Questions**: 4 (Aligned: 1, General: 3)
* **Unaligned Gaps Detail**:
  - **Q ID**: `51af6c51-dc5f-4102-b3a9-ed19899652ab`
    * **Text**: Given the data set and query:

{ "_id" : ObjectId("512bc95fe835e68f199c8686"), "player" : "p1", "score" : 89 }
{ "_id" : ObjectId("512bc962e835e68f199c8687"), "player" : "p2", "score" : 85 }
{ "_id" : ObjectId("55f5a192d4bede9ac365b257"), "player" : "p2", "score" : 65 }
{ "_id" : ObjectId("55f5a192d4bede9ac365b258"), "player" : "p3", "score" : 65 }
{ "_id" : ObjectId("55f5a1d3d4bede9ac365b259"), "player" : "p3", "score" : 75 }
{ "_id" : ObjectId("55f5a1d3d4bede9ac365b25a"), "player" : "p5", "score" : 70 }
{ "_id" : ObjectId("55f5a1d3d4bede9ac365b25b"), "player" : "p6", "score" : 100 }

db.scores.aggregate([
  { $group: {
    _id: '$player',
    score: { $avg: '$score' }
  }},
  { $match: {
    score: { $gt: 70 }
  }}
])

What is the output?
(Choose 1)
    * **Reason**: The question requires the student to perform a calculation using the $avg operator and evaluate a comparison operator ($gt). The provided lesson context only covers the basic definition of $match as a filter and does not include information on aggregation math (like $avg), query operators (like $gt), or how to calculate results from a multi-stage pipeline involving $group.

  - **Q ID**: `6d0928ae-ee1e-473d-91c8-0ece1028a4d9`
    * **Text**: What Python code is a valid aggregation that can be used with collection.aggregate(pipeline)?
    * **Reason**: The question asks for 'Python code', but the lesson context only provides JavaScript/mongosh syntax. Furthermore, the options include a `$group` stage which is not mentioned or defined in the provided lesson text.

  - **Q ID**: `7ff945b6-a697-4ce0-a31c-a9cbff0539a0`
    * **Text**: Which aggregation operator is used to group documents and perform calculations like sum or average?
    * **Reason**: The question asks about the '$group' operator and its functionality (sum/average), but the provided lesson context only covers the '$match' operator. While '$group' is mentioned in passing as a comparison point for performance optimization, its specific functionality or syntax is not taught in this lesson.


### Concept: $group
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The text explicitly states in the 'Intermediate Learners' section that a common mistake is using $project instead of $match for filtering documents before grouping, and it reinforces this in the 'Do's & Don't' section by showing the correct sequence (filtering with $match before $group). The options provided are standard aggregation stages mentioned or contrasted within the text.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: $project
* **Micro-Challenge Status**: Not Aligned (The question contains a contradiction based on the provided text. The 'DON'T / EXAM TRAP' section explicitly states that using `0` is incorrect and that 'In MongoDB, 0 or false should be used to exclude fields.' However, it then immediately follows with: 'What to Watch For: Always use false or 1 when including/excluding fields.' This inconsistency in the source text makes it impossible to determine if A or B is the 'correct' answer based strictly on the provided material. Additionally, the inclusion of '0' as an option creates ambiguity because the lesson text provides conflicting instructions regarding its validity.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: $sort
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The text explicitly states in both the 'Intermediate Learners' and 'Best Practice' sections that using $match before sorting is a way to reduce the number of documents being sorted for better performance.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: $limit
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the 'Exam Signal' regarding the importance of pipeline stage order (specifically why $limit should follow filtering) and uses the exact logic described in the 'DO' and 'DON'T' sections of the text. The options provided directly mirror the scenarios discussed in the lesson without introducing outside concepts like BSON types or complex operators.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: $lookup
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the core mechanics of $lookup (left collection, right collection, localField, foreignField, and as) and specifically addresses 'Exam Signal 2' regarding the correct naming/matching of fields. The options provided force the student to identify the correct mapping between a local field in one collection and its corresponding foreign field in another, which is the primary concept taught.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: $out
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson content. Option A addresses the 'Exam Trap' regarding invalid collection names (spaces), Option B reflects the core definition of the $out stage provided in Section 1 and the Exam Radar, and Option C serves as a distractor based on other common aggregation stages mentioned in the text.)
* **Total Questions**: 1 (Aligned: 0, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `a9b1766d-d1a1-4a59-a483-d69a009781ad`
    * **Text**: After executing the following aggregation pipeline:
db.getSiblingDB("mdb").coll.aggregate([
  { $out: {db: "test", collection: "results"} }
])
What are two expected results? (Choose 2)
    * **Reason**: The question introduces a syntax for the $out stage that is not present in the lesson. The lesson defines $out as taking a string (e.g., { $out: 'bakery_counts' }), whereas the question uses an object with nested fields ({ $out: {db: 'test', collection: 'results'} }). This specific syntax for specifying a different database and collection is not mentioned in the provided text.


### Concept: $unwind
* **Micro-Challenge Status**: Aligned (The question is perfectly aligned with the lesson. It directly tests the core definition of the $unwind stage as provided in the 'Core Concept' section. The distractors (group, match, sort) are standard aggregation stages but are not mentioned in the text, meaning they do not leak future content or complex concepts; they simply serve as clear alternatives to the correct answer defined in the lesson.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: $addFields
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the 'Exam Signal' regarding the distinction between $addFields and $project. The lesson explicitly states that $addFields is used to add new fields (including those based on expressions/values) while $project is for reshaping or filtering, and it specifically identifies the confusion between these two as a common exam trap.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

## Topic 9: Indexes & Performance

### Concept: Single field indexes
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson content. Option B reflects the 'Underlying Mechanics' section (locating documents without scanning the entire collection). Option D reflects the 'Design Choices' and 'Advanced Developers' sections regarding write amplification. Options A and C are incorrect based on the text, but they do not introduce outside concepts; they simply test the student's ability to distinguish single field indexes from other types or functions described in the text.)
* **Total Questions**: 6 (Aligned: 0, General: 6)
* **Unaligned Gaps Detail**:
  - **Q ID**: `33f36add-4691-43b8-a908-de95af5627e7`
    * **Text**: How should the 'autocomplete' index be defined to look for matches at the beginning of a word on the name field? (Choose 1)
    * **Reason**: The question refers to 'autocomplete' indexing and specific tokenization types (edgeGram, nGram, etc.) which are not mentioned or explained in the lesson. The lesson only covers Single Field Indexes, Compound Indexes, and basic `createIndex` syntax.

  - **Q ID**: `cf08301c-166c-42a1-be41-73f39199f375`
    * **Text**: 20. The following query generates a collection scan:

db.people.find({employer : "ABC" }).sort( {last_name:1 , job:1})

Which two indexes will most improve the performance of the query?

(Choose 2)
    * **Reason**: The question requires knowledge of compound indexes and the specific rules for optimizing sort orders within a multi-field index (e.g., matching the direction of 'last_name:1' and 'job:1'). The lesson provided only covers single field indexes and does not explain how multiple fields in an index interact with query sorting or the logic required to choose between the four specific compound options provided.

  - **Q ID**: `6a8d746e-9b3e-4979-ba0e-d74a2d6d9725`
    * **Text**: Given a collection called collection, in which all documents have the following shape:
{
  _id:1,
  objs:[
    {a:1,b:2},{a:2,b:1}
  ]
}
And the query on this collection:
db.collection.find({"objs.a":1})
What index will support this query?
(Choose 1)
    * **Reason**: The question involves nested fields (e.g., 'objs.a') and multi-key indexes, which are not mentioned or explained in the lesson. The lesson only covers single field indexes on top-level fields and does not provide any information on how MongoDB handles indexing for arrays or dot notation.

  - **Q ID**: `f6378bef-3823-438e-b6c5-c96048b65123`
    * **Text**: Given the following query:
db.coll.find({}).sort({"product": 1, "price": 1})
Which two indexes will improve the performance of this query? (Choose 2)
    * **Reason**: The question requires identifying which specific sort orders (ascending/descending) match a given query's sort order. While the lesson mentions that 'ascending and descending sort orders affect query performance differently,' it does not provide the rules or logic required to determine which specific index matches a multi-field sort operation (e.g., matching the [1, 1] pattern). Furthermore, the question involves compound indexes, but the lesson's primary focus is on single field indexes.

  - **Q ID**: `4c4cefe3-66aa-4269-b62f-aa86444ed339`
    * **Text**: Given the following query:
db.coll.find({}).sort({"product": 1, "price": 1})
Which two indexes improve the performance of this query the most?
(Choose 2)
    * **Reason**: The question requires knowledge of 'Compound Indexes' and how specific sort orders (ascending vs. descending) interact with multi-field sorting. The provided lesson only covers 'Single Field Indexes' and does not provide the rules or logic required to determine which compound index matches a multi-field sort query.

  - **Q ID**: `b6a249f9-dee8-48b3-a1c9-137d51f85b9f`
    * **Text**: What mongosh command shows how many indexes are associated with an inventory collection? (Choose 1)
    * **Reason**: The lesson content does not mention any methods for listing or showing indexes (such as getIndexes() or showIndexes()). It only provides the syntax for creating an index using createIndex().


### Concept: Compound indexes
* **Micro-Challenge Status**: Not Aligned (The question contains elements that are not supported by the lesson text. Option D mentions 'array and nested documents', which are not discussed in the provided context. Additionally, while the lesson notes that field order is crucial, it does not state that ascending order is always superior to descending order (Option A); rather, it states that a specific order (e.g., {type: 1, genre: -1}) is more effective for specific queries than its reverse. The question tests knowledge of 'array' and 'nested documents' which are outside the provided scope.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: Multikey indexes
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A reflects the 'Underlying Mechanics' and 'Intermediate Learners' sections (each element is indexed individually). Option B is not supported by the text (the text mentions sorting but doesn't say they are *only* for sorted results). Option C addresses a specific 'Exam Trap' mentioned in the text regarding the incorrect use of unique multikey indexes.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: Atlas Search indexes
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A reflects the definition provided in Section 1 (full-text search). Options B, C, and D are incorrect based on the text: B contradicts the 'Exam Trap' regarding confusing search indexes with other types; C contradicts the requirement to explicitly specify fields; and D is not supported by any part of the text. No outside concepts or future topics were introduced.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: explain()
* **Micro-Challenge Status**: Not Aligned (The question asks 'What does the following explain() output indicate...', but the provided code snippet is just a command to generate an output, not an actual output. The student cannot see any metrics (like IXSCAN, COLLSCAN, or executionTimeMillis) from the code provided; they only see the method call. Furthermore, the answer provided in the prompt contains information ('totalDocsExamined') that is not explicitly mentioned in the lesson text, even though it is implied by 'execution statistics'.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: COLLSCAN vs IXSCAN
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson content. Option C directly reflects the definition provided in Section 1 ('a full collection scan where MongoDB scans every document in the collection'). Options A, B, and D are incorrect based on the text: A is partially true but the text emphasizes COLLSCAN as a fallback when no suitable index exists; B contradicts the 'poor performance' warning; and D introduces an arbitrary number (10,000) not mentioned in the text. No outside concepts or future topics were introduced.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

## Topic 10: Data Modeling

### Concept: Embedding vs Referencing
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The correct answer (A) is directly supported by the 'Underlying Mechanics' section under 'Embedding: Pros', which states that embedding offers a 'Simpler structure, fewer joins, easier queries.' Option B describes a 'Con' of embedding, C attributes write performance to referencing (not embedding), and D is not mentioned as a specific benefit of embedding in the text.)
* **Total Questions**: 4 (Aligned: 0, General: 4)
* **Unaligned Gaps Detail**:
  - **Q ID**: `38aa32bd-579e-4958-829c-dcad418f8d65`
    * **Text**: What schema is the most effective? (Choose 1)
    * **Reason**: The question requires a subjective judgment on which specific data types (Orders vs. Reviews vs. Prices vs. Inventory) are 'most effective' to embed. The lesson provides general principles for choosing between embedding and referencing based on read/write ratios and growth patterns, but it does not provide the specific business logic or rules required to rank these four specific scenarios against each other.

  - **Q ID**: `f4620a42-638c-4cc5-89b4-6d1393b55ae8`
    * **Text**: What type of data structure should be used to store a list of items?
    * **Reason**: The question asks about general data structures (Array, Dictionary, Set) for storing lists. The lesson focuses specifically on MongoDB modeling strategies (Embedding vs. Referencing). While the code example shows an array of objects being embedded, the lesson does not define or discuss 'Dictionaries' or 'Sets' as valid options in this context.

  - **Q ID**: `4a077a2c-50a4-4d7f-a5db-483b5430a683`
    * **Text**: What is the best way to handle user authentication?
    * **Reason**: The question asks about authentication strategies (third-party services, JWTs, bcrypt), which are not mentioned or covered in the lesson. The lesson is strictly focused on data modeling techniques: Embedding vs. Referencing.

  - **Q ID**: `62750a1e-39c4-488b-9598-56f75451202a`
    * **Text**: Which is considered a data modeling anti-pattern in MongoDB?
    * **Reason**: The term 'anti-pattern' is never mentioned or defined in the lesson. While the lesson discusses 'Common mistakes' and 'Exam Traps,' it does not provide a specific list of anti-patterns or enough context to determine which of the provided options constitutes one without outside knowledge.


### Concept: Anti-patterns
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A directly reflects the 'Best Practice' section regarding read-heavy workloads and embedding. Option B reflects the 'Don't/Exam Trap' section regarding write-heavy workloads. Options C and D are incorrect based on the text provided, but they do not introduce outside concepts or leak advanced topics not covered in the lesson.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: One-to-Many relationships
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option B directly mirrors the text in Section 1 ('Referencing is better for large or growing relationships where duplication would be wasteful. It avoids repeated data and allows for more flexible updates'). The other options are either factually incorrect based on the text (A) or introduce concepts not supported by the text (C, D).)
* **Total Questions**: 0 (Aligned: 0, General: 0)

## Topic 11: MongoDB Drivers & PyMongo

### Concept: PyMongo purpose
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the specific 'Exam Signal' regarding the distinction between PyMongo methods and raw MQL syntax (specifically the use of `insert()` vs `insert_one()`). All options provided are based on the code examples and warnings provided in Section 3.)
* **Total Questions**: 15 (Aligned: 1, General: 14)
* **Unaligned Gaps Detail**:
  - **Q ID**: `4fefdb15-8259-4ca4-ab23-47c1bbf65385`
    * **Text**: What is the value of x?
    * **Reason**: The question 'What is the value of x?' does not refer to any concepts, code snippets, or logic provided in the lesson. The lesson focuses on PyMongo syntax, MongoClient, and insert methods; it contains no mathematical problems or variables labeled 'x'.

  - **Q ID**: `certcoach-t11-crud-with-pymongo-medium-001-63fd56e4`
    * **Text**: Which method in PyMongo is used to update multiple documents that match a specific query filter?
    * **Reason**: The lesson content does not mention update operations at all. It only covers connection (MongoClient), database/collection access, and insertion methods (specifically insert_one). The terms 'update_many', 'replace_one', or 'bulk_write' are not mentioned in the text.

  - **Q ID**: `certcoach-t11-mongoclient-medium-001-c4ec05c2`
    * **Text**: Which of the following ways correctly creates a `MongoClient` object in PyMongo?
    * **Reason**: The question introduces multiple options (AsyncMongoClient, host/port keyword arguments, and tz_aware parameters) that are not mentioned or defined in the lesson. While the first option matches the example provided, the student cannot determine if it is the 'correct' way among the others because the lesson does not cover asynchronous drivers or specific keyword argument configurations.

  - **Q ID**: `certcoach-t11-mongoclient-medium-002-f544a4ee`
    * **Text**: Which of the following correctly creates a `MongoClient` object in PyMongo?
    * **Reason**: The question includes options that are not covered in the lesson. Specifically, 'AsyncMongoClient' and the keyword arguments 'host', 'port', 'uri', and 'connect=False' are never mentioned or shown in the provided text. The only valid construction shown in the lesson is `client = MongoClient("mongodb://localhost:27017/")`.

  - **Q ID**: `certcoach-t11-crud-with-pymongo-hard-001-3072ea6b`
    * **Text**: Which PyMongo method should you use if you want to update a single document in a MongoDB collection based on a specific condition and ensure that the operation is acknowledged by the server?
    * **Reason**: The question asks about 'update_one()', 'replace_one()', and 'bulk_write()'. These methods are not mentioned or defined anywhere in the provided lesson context. The only insertion method mentioned is 'insert_one()'. Therefore, a student cannot solve this question using only the provided material.

  - **Q ID**: `certcoach-t11-crud-with-pymongo-medium-002-c96abb7b`
    * **Text**: Which PyMongo method should you use to update multiple documents that match a specific query filter?
    * **Reason**: The lesson content only provides information and code examples for the `insert_one()` method. It does not mention update methods (such as `update_one` or `update_many`), replacement methods, or `bulk_write`. Therefore, a student cannot determine the correct answer using only the provided text.

  - **Q ID**: `certcoach-t11-crud-with-pymongo-medium-001-605bea2a`
    * **Text**: Which PyMongo method should be used to update a single document in a MongoDB collection?
    * **Reason**: The lesson content does not mention update operations (such as 'update_one' or 'update_many') or the 'replace_one' method. It only provides information and code examples regarding connection setup and insertion methods ('insert_one').

  - **Q ID**: `certcoach-t11-crud-with-pymongo-medium-002-380d6b9b`
    * **Text**: Which PyMongo method should be used to update multiple documents in a MongoDB collection?
    * **Reason**: The lesson content does not mention update operations (update_one, update_many) or replace_one. While it mentions insert_one and insert_many in the '30-Second Recall' section, it provides no information regarding update methods.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-hard-003-69ee8e95`
    * **Text**: Which connection option correctly sets the maximum number of connections in a PyMongo connection pool using the `MongoClient` constructor?
    * **Reason**: The question asks about specific connection pool parameters (maxPoolSize, maxConnecting, etc.) and their values. The provided lesson only covers basic `MongoClient` initialization with a connection string and does not mention or define any configuration options for the connection pool.

  - **Q ID**: `certcoach-t11-mongoclient-medium-001-350ab5c1`
    * **Text**: Which of the following is the correct way to create a MongoClient in PyMongo?
    * **Reason**: The question asks to identify the 'correct' way among four variations. While the lesson provides one valid example (`client = MongoClient("mongodb://localhost:27017/")`), it does not provide the necessary context or information to determine why the other three options are incorrect (e.g., it doesn't mention keyword arguments like `host`, `port`, `uri`, or `connect`). A student cannot strictly determine which is 'correct' versus 'incorrect' based solely on the provided text.

  - **Q ID**: `certcoach-t11-crud-with-pymongo-hard-001-134db2cf`
    * **Text**: Which PyMongo method correctly updates a single document in a collection?
    * **Reason**: The lesson context does not mention update operations, the `update_one()` method, or the `$set` operator. While the lesson mentions that PyMongo provides a high-level API for 'updating' in general terms, it never defines specific methods or syntax for updates, making it impossible for a student to determine the correct answer based solely on the provided text.

  - **Q ID**: `certcoach-t11-pymongo-purpose-easy-003-86175ddd`
    * **Text**: What method is used to establish a connection to MongoDB using PyMongo?
    * **Reason**: The question asks for a specific method name (e.g., 'connect') to establish a connection, but the lesson states that the 'MongoClient' class is used for this purpose and provides the code `client = MongoClient("mongodb://localhost:27017/")`. The lesson does not mention or define any methods named 'connect', 'connection', 'establish_connection', or 'create_connection'.

  - **Q ID**: `certcoach-t11-pymongo-purpose-easy-004-6d1141de`
    * **Text**: Which method in PyMongo is used to establish a connection to MongoDB?
    * **Reason**: The question asks for a specific method used to establish a connection (e.g., 'connect' or 'establish_connection'), but the lesson states that the class `MongoClient` is used for this purpose. The correct answer ('MongoClient') is not among the provided options, and the specific methods listed in the options are never mentioned in the text.

  - **Q ID**: `certcoach-t11-crud-with-pymongo-medium-003-f8b406ee`
    * **Text**: Consider the following PyMongo code snippet intended to update multiple documents in a MongoDB collection. Identify the correct syntax for the `update_many` method call.
    * **Reason**: The lesson does not mention or provide any information regarding the `update_many` method, update operations, query filters, or asynchronous programming (await). The only insertion-related methods mentioned are `insert_one()` and `insertMany()`.


### Concept: Connection strings and URI components
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the 'Case Sensitivity' and 'Connection Options in URIs' exam signals specifically mentioned in Section 3 (Do's & Don'ts). The distinction between uppercase 'MS' and lowercase 'ms' is explicitly highlighted as an exam trap in the text, and both options provided are present in the lesson's code examples.)
* **Total Questions**: 13 (Aligned: 1, General: 12)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-001-ac08d623`
    * **Text**: Which component in a MongoDB connection string is used to specify the authentication mechanism?
    * **Reason**: The lesson mentions 'Authentication Options' as a general category within the URI, but it does not define specific components like 'authMechanism', 'user', or 'password'. The student cannot determine which specific term is used for the mechanism based solely on the provided text.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-003-37da8351`
    * **Text**: Which component of a MongoDB connection string specifies the username used to authenticate with the database?
    * **Reason**: The question asks about specific components of a connection string (username, password, authSource, dbname), but the lesson only mentions 'Authentication Options' as a general category and does not define or list these specific sub-components.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-004-f10f2619`
    * **Text**: Which component of a MongoDB connection string is used to specify the database name you want to connect to?
    * **Reason**: The lesson defines 'hostname', 'port', and 'authentication options' as components of a connection string, but it never mentions or explains how to specify a 'database' name within the URI. The question asks for information not provided in the text.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-005-61e25b92`
    * **Text**: Which component of a MongoDB connection string is used to specify the authentication mechanism?
    * **Reason**: The question asks about specific components (like 'authMechanism') within a connection string. While the lesson mentions that URIs contain 'Authentication Options', it never defines or lists specific parameters like 'authMechanism' or 'user/password' as part of the URI structure.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-006-85f41424`
    * **Text**: Which component of a MongoDB connection string specifies the authentication mechanism to use?
    * **Reason**: The lesson mentions 'Authentication Options' as a component of a connection string, but it does not define specific parameters like 'authMechanism', nor does it provide any information regarding the specific keywords or components used to define authentication within the URI.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-hard-001-1d56a154`
    * **Text**: Which component in a MongoDB connection string specifies the database to connect to?
    * **Reason**: The lesson defines 'hostname', 'port', and 'authentication options' as components of a connection string (URI), but it does not mention or define the 'database' component within the URI structure. The student cannot determine which part specifies the database based solely on the provided text.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-easy-001-3be0a7ca`
    * **Text**: Which component of a MongoDB connection string specifies the database to connect to?
    * **Reason**: The lesson defines 'Hostname', 'Port', and 'Authentication Options' as components of a connection string, but it never mentions or explains how to specify the 'database' within the URI. The question asks for information not provided in the text.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-hard-002-cfdff66e`
    * **Text**: Which option correctly sets the maximum number of connections in a PyMongo connection pool using a connection URI?
    * **Reason**: The question asks about 'maxPoolSize' (or similar connection pool parameters), which are not mentioned, defined, or demonstrated anywhere in the provided lesson. The lesson only covers basic URI components like hostname, port, connectTimeoutMS, and tls.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-007-80981e97`
    * **Text**: Which component in a MongoDB connection string specifies the maximum number of concurrent connections that the pool can maintain?
    * **Reason**: The question asks about 'maxPoolSize', 'minPoolSize', and 'maxConnecting' parameters. These specific connection pool management options are not mentioned or defined anywhere in the provided lesson text.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-008-7a8364ac`
    * **Text**: Consider the following PyMongo connection string used to establish a connection to a MongoDB server. Which option correctly specifies the `maxPoolSize` parameter in the connection URI?
    * **Reason**: The question asks about the 'maxPoolSize' parameter. While the lesson discusses connection URIs and case sensitivity, it never mentions or defines the 'maxPoolSize' parameter specifically. A student cannot know the correct syntax for this specific parameter based solely on the provided text.

  - **Q ID**: `certcoach-t11-connection-strings-and-uri-compo-medium-009-07658532`
    * **Text**: Consider the following PyMongo connection string used to establish a connection to a MongoDB server. Which option correctly specifies the `maxConnecting` parameter in the connection URI?
    * **Reason**: The question introduces a specific connection parameter ('maxConnecting') that is not mentioned anywhere in the lesson. While the lesson discusses 'connection options' generally and provides examples like 'connectTimeoutMS' and 'tls', it does not provide enough information to determine the correct syntax or validity of 'maxConnecting'.

  - **Q ID**: `certcoach-t11-mongoclient-medium-003-36c96bac`
    * **Text**: You are developing a Python application that needs to connect to a MongoDB deployment running on a remote server. The MongoDB instance is secured with authentication enabled. You need to create a MongoClient object using PyMongo to establish a connection. Which of the following options correctly creates a MongoClient object with the necessary authentication credentials?
    * **Reason**: The question requires knowledge of specific URI syntax for authentication (e.g., the 'username:password@host' format vs. query parameters). The provided lesson only mentions that a URI contains 'authentication details' and shows an example with connection options like 'connectTimeoutMS' and 'tls', but it never explains or provides examples of how to embed credentials within the URI string.


### Concept: MongoClient
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A correctly reflects the syntax provided in the 'DO: Best Practice' section (calling .insert_one() on a collection object). Options B, C, and D are incorrect based on the provided text: B uses 'insertOne' (not mentioned), C is technically valid but tests navigation logic not explicitly prioritized over the standard local variable approach shown in the example, and D incorrectly attempts to call insert_one on the client rather than the collection.)
* **Total Questions**: 1 (Aligned: 0, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `4e191929-6c44-4e42-975c-29f12db693ab`
    * **Text**: 28. What are two valid method names for MongoClient class? (Choose 2)
    * **Reason**: The question asks for valid method names of the MongoClient class. While 'close()' is mentioned in the Advanced Developers section (referring to closing the client), the lesson does not list or define any other methods for the MongoClient class, such as 'get_database()', 'open()', or 'destroy()'. Therefore, a student cannot determine which two are valid based solely on the provided text.


### Concept: Connection pooling
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the specific 'Do's & Don'ts' section regarding the correct casing of the `maxPoolSize` parameter and ignores outside concepts like timeouts or BSON types.)
* **Total Questions**: 9 (Aligned: 2, General: 7)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t11-connection-pooling-medium-001-96e668f8`
    * **Text**: Which PyMongo method is used to enable connection pooling when establishing a MongoDB client?
    * **Reason**: The question asks for a specific method (e.g., .connect(), .create_pool()) and parameter name (pool_size) that are not mentioned in the lesson. The lesson teaches that connection pooling is handled automatically by the driver and focuses specifically on the `maxPoolSize` parameter within the `MongoClient` constructor, rather than a separate method call.

  - **Q ID**: `certcoach-t11-connection-pooling-medium-003-d5dde32d`
    * **Text**: Which PyMongo method is used to enable connection pooling when creating a MongoClient?
    * **Reason**: The question asks for a specific method to 'enable' connection pooling, but the lesson does not mention an 'enable' method or any of the options provided (connect_pooling, pool_connections, set_connection_pool_size, enable_pooling). The lesson only discusses the `maxPoolSize` parameter within the `MongoClient` constructor.

  - **Q ID**: `certcoach-t11-connection-pooling-medium-004-bdbb94b6`
    * **Text**: Which method in PyMongo is used to enable connection pooling, allowing multiple database operations to share a pool of connections?
    * **Reason**: The question asks for a specific 'method' used to enable connection pooling (e.g., connect(), pool_connections()), but the lesson does not mention any such methods. The lesson explains that connection pooling is an inherent feature of the driver and focuses on the configuration parameter `maxPoolSize` within the `MongoClient` constructor, rather than a specific method call to 'enable' it.

  - **Q ID**: `certcoach-t11-connection-pooling-medium-005-43537ca6`
    * **Text**: Which PyMongo method is used to configure connection pooling when establishing a connection to MongoDB?
    * **Reason**: The question asks for a 'PyMongo method' used to configure connection pooling. The lesson does not mention any specific methods (like .connect() or .initiate()) for this purpose; instead, it teaches that configuration is done via the `maxPoolSize` parameter within the `MongoClient` constructor.

  - **Q ID**: `certcoach-t11-connection-pooling-easy-001-9acf7842`
    * **Text**: Which PyMongo method is used to enable connection pooling when establishing a connection to MongoDB?
    * **Reason**: The question asks which 'method' is used to enable connection pooling. The lesson does not state that there is a specific method for this; rather, it explains that connection pooling is an inherent feature of the driver and is configured via parameters (like `maxPoolSize`) within the `MongoClient` constructor.

  - **Q ID**: `certcoach-t11-connection-pooling-hard-001-24f72e1d`
    * **Text**: Which PyMongo method is used to configure connection pooling in a MongoDB client?
    * **Reason**: The question asks for a 'PyMongo method' used to configure connection pooling. The lesson does not mention any methods like .connect_pool(), .configure_pool(), or .set_connection_options(). Instead, the lesson teaches that configuration is done via parameters (specifically `maxPoolSize`) passed directly into the `MongoClient` constructor.

  - **Q ID**: `certcoach-t11-connection-pooling-medium-006-9d495eba`
    * **Text**: Which PyMongo method should you use to configure connection pooling when creating a MongoClient instance?
    * **Reason**: The question asks which 'method' should be used to configure connection pooling. The lesson does not mention any methods like .configure_connection_pool(), .set_connection_options(), etc. Instead, the lesson teaches that configuration is done via a parameter (maxPoolSize) directly within the MongoClient constructor.


### Concept: CRUD with PyMongo
* **Micro-Challenge Status**: Not Aligned (The question is not strictly aligned because options B, C, and D contain information (e.g., 'returns a cursor object' or 'returns the updated document') that are not mentioned in the lesson text. While A is also incorrect based on the text (it returns an acknowledgment result), the inclusion of technical details like 'cursor objects' constitutes a leak of external knowledge not provided in the context.)
* **Total Questions**: 2 (Aligned: 0, General: 2)
* **Unaligned Gaps Detail**:
  - **Q ID**: `735b0f69-a756-4c10-a7bd-196445617d5c`
    * **Text**: What is the issue with this Python script that attempts to interact with an SQLite database using the `sqlite3` module instead of MongoDB?
    * **Reason**: The question is completely unrelated to the lesson content. The lesson focuses on MongoDB and PyMongo CRUD operations, while the question asks about an SQLite database using the sqlite3 module. Furthermore, the provided options (A-D) are nonsensical in the context of both the question asked and the lesson provided.

  - **Q ID**: `certcoach-t11-mongoclient-medium-002-d5fbd603`
    * **Text**: You are developing a Python application that needs to connect to a MongoDB deployment running on a remote server. The MongoDB instance is secured with authentication enabled. You need to create a MongoClient object using PyMongo to establish this connection. Which of the following code snippets correctly creates the MongoClient object with the necessary authentication credentials?
    * **Reason**: The question asks about connection strings and authentication parameters for MongoClient (e.g., 'authSource', 'username', 'password'). The provided lesson context only covers basic CRUD operations (insert_one, find_one, update_one, delete_one), the difference between shell and PyMongo syntax, and indexing/COLLSCANs. It does not mention connection strings, authentication protocols, or specific URI parameters.


### Concept: Aggregation with PyMongo
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. The text explicitly mentions '$match' as a stage used for filtering in both the 'Intermediate Learners' section and the code examples. The other options ($project, $group) are also mentioned in the text but are associated with different functions (projection and grouping respectively), ensuring only one correct answer exists within the provided context.)
* **Total Questions**: 12 (Aligned: 2, General: 10)
* **Unaligned Gaps Detail**:
  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-medium-001-a3dd3535`
    * **Text**: Which PyMongo method is used to perform an aggregation pipeline with a `$search` stage?
    * **Reason**: The question asks about a specific '$search' stage and related PyMongo methods (like 'aggregate_search'), which are not mentioned in the lesson. The lesson only covers standard aggregation stages like $match, $group, $sort, and $project using the .aggregate() method.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-medium-003-60670143`
    * **Text**: Which PyMongo method is used to perform an aggregation operation that includes a `$search` stage?
    * **Reason**: The question refers to a '$search' stage and specific PyMongo methods like 'aggregate_search', which are not mentioned in the lesson. The lesson only covers the standard .aggregate() method and basic stages like $match, $group, $sort, and $project.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-medium-004-d731fc13`
    * **Text**: Which PyMongo method is used to perform an aggregation with a `$search` stage on a MongoDB Atlas cluster?
    * **Reason**: The question introduces a specific stage ('$search') and a specific environment (MongoDB Atlas cluster) that are not mentioned in the lesson. The lesson only covers standard aggregation stages like $match, $group, $sort, and $project.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-medium-005-e653fe9e`
    * **Text**: Which PyMongo method is used to perform an aggregation pipeline that includes a `$search` stage on MongoDB Atlas?
    * **Reason**: The question introduces a specific stage ('$search') and a specific platform (MongoDB Atlas) that are not mentioned in the lesson. While the method 'aggregate()' is mentioned, the student cannot determine if it is the correct answer based solely on the provided text because the text does not discuss '$search' or Atlas-specific features.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-hard-001-90f4a19e`
    * **Text**: Which PyMongo method is used to perform an aggregation pipeline that includes a `$search` stage?
    * **Reason**: The question introduces a specific stage, `$search`, which is not mentioned anywhere in the lesson. The lesson only covers `$match`, `$sort`, `$group`, and `$project`.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-hard-002-0550a173`
    * **Text**: Which PyMongo method is used to perform an aggregation pipeline that includes a `$search` stage on a MongoDB Atlas collection?
    * **Reason**: The question refers to a `$search` stage and MongoDB Atlas-specific functionality, neither of which are mentioned in the lesson. The lesson only covers standard aggregation stages like `$match`, `$group`, `$sort`, and `$project`.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-hard-003-eb87bb5a`
    * **Text**: Which PyMongo method is used to perform an aggregation pipeline that includes a `$search` stage to query data in a MongoDB Atlas collection?
    * **Reason**: The question introduces a '$search' stage and mentions 'MongoDB Atlas', neither of which are mentioned in the lesson. The lesson only covers standard aggregation stages like $match, $group, $sort, and $project.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-hard-004-2ebbd071`
    * **Text**: Which PyMongo method is used to perform an aggregation with a `$search` stage on a MongoDB Atlas collection?
    * **Reason**: The question refers to a '$search' stage and 'MongoDB Atlas', neither of which are mentioned in the lesson. The lesson only covers standard aggregation stages like $match, $group, $sort, and $project.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-easy-001-81e59013`
    * **Text**: Which PyMongo method is used to perform an aggregation operation with a `$search` stage?
    * **Reason**: The question asks about a specific method for performing a '$search' stage. The lesson only mentions the standard `.aggregate()` method and does not mention or define any specialized search methods like 'aggregate_search' or 'search_pipeline'.

  - **Q ID**: `certcoach-t11-aggregation-with-pymongo-easy-003-a5b4369e`
    * **Text**: Which PyMongo method is used to perform an aggregation with a `$search` stage in MongoDB?
    * **Reason**: The question refers to a '$search' stage and specific methods for search-based aggregation which are not mentioned in the lesson. The lesson only covers standard aggregation stages like $match, $group, $sort, and $project.


## Topic 12: Tools, Tooling & Atlas Search

### Concept: Load Atlas Sample Dataset
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. It tests the specific `db.runCommand` syntax provided in the 'Do's & Don'ts' section. While the dataset name changed from 'AirBnB' to 'Mflix', the structure of the command remains identical to the example provided, and the incorrect options (B, C, D) are not supported by the text, ensuring only the correct syntax pattern is valid.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: Data Explorer document lookup
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A reflects the 'Do' example provided in the text (using an ObjectId for a lookup), while Option B represents the specific 'Exam Trap' mentioned (using query operators like $eq). Option C tests the requirement of using the correct format/field as described in the 'Advanced' and 'Syntax' sections.)
* **Total Questions**: 0 (Aligned: 0, General: 0)

### Concept: Atlas Search indexes
* **Micro-Challenge Status**: Aligned (The question is strictly aligned with the lesson. Option A is addressed in the 'Exam Radar' section (distinguishing search indexes from traditional ones). Option B is directly supported by the 'DON'T / EXAM TRAP' and 'Exam Radar' sections regarding dynamic mappings vs. explicit definitions. Options C and D are clearly incorrect based on the text: C contradicts the role of analyzers for text processing, and D introduces 'searchAfter' and '$sort', which are not mentioned in the lesson.)
* **Total Questions**: 1 (Aligned: 0, General: 1)
* **Unaligned Gaps Detail**:
  - **Q ID**: `14544111-7406-4943-8abf-1c95c6c00076`
    * **Text**: What query satisfies these requirements? (Choose 1)
    * **Reason**: The question requires knowledge of specific query operators (like 'query', 'path', and 'synonym') and the structure of a `$search` aggregation stage. The lesson only mentions that 'Query Operators' are used in search queries but does not provide any examples of them or define their syntax.


### Concept: Atlas Search queries
* **Micro-Challenge Status**: Not Aligned (The question is not strictly aligned because options B and D both contain the $search stage as the first stage. According to the lesson text, the only rule provided is that '$search' must be the first stage in a pipeline. Since both B and D satisfy this specific requirement based on the provided text, there is no single 'correct' answer among the choices provided; both are technically valid under the rules described.)
* **Total Questions**: 0 (Aligned: 0, General: 0)
