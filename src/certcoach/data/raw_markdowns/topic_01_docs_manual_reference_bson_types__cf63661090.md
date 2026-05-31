> Source: https://www.mongodb.com/docs/manual/reference/bson-types/
> Fetch method: direct_markdown

# BSON Types

[BSON](https://www.mongodb.com/docs/reference/glossary/#std-term-BSON) is a binary serialization format used to store documents and make remote procedure calls in MongoDB. The BSON specification is located at [bsonspec.org](http://bsonspec.org/).

Each BSON type has both integer and string identifiers as listed in the following table:

<table>
<tr>
<th id="Type">
Type

</th>
<th id="Number">
Number

</th>
<th id="Alias">
Alias

</th>
<th id="Notes">
Notes

</th>
</tr>
<tr>
<td headers="Type">
Double

</td>
<td headers="Number">
1

</td>
<td headers="Alias">
"double"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
String

</td>
<td headers="Number">
2

</td>
<td headers="Alias">
"string"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Object

</td>
<td headers="Number">
3

</td>
<td headers="Alias">
"object"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Array

</td>
<td headers="Number">
4

</td>
<td headers="Alias">
"array"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Binary data

</td>
<td headers="Number">
5

</td>
<td headers="Alias">
"binData"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Undefined

</td>
<td headers="Number">
6

</td>
<td headers="Alias">
"undefined"

</td>
<td headers="Notes">
Deprecated.

</td>
</tr>
<tr>
<td headers="Type">
ObjectId

</td>
<td headers="Number">
7

</td>
<td headers="Alias">
"objectId"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Boolean

</td>
<td headers="Number">
8

</td>
<td headers="Alias">
"bool"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Date

</td>
<td headers="Number">
9

</td>
<td headers="Alias">
"date"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Null

</td>
<td headers="Number">
10

</td>
<td headers="Alias">
"null"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Regular Expression

</td>
<td headers="Number">
11

</td>
<td headers="Alias">
"regex"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
DBPointer

</td>
<td headers="Number">
12

</td>
<td headers="Alias">
"dbPointer"

</td>
<td headers="Notes">
Deprecated.

</td>
</tr>
<tr>
<td headers="Type">
JavaScript

</td>
<td headers="Number">
13

</td>
<td headers="Alias">
"javascript"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Symbol

</td>
<td headers="Number">
14

</td>
<td headers="Alias">
"symbol"

</td>
<td headers="Notes">
Deprecated.

</td>
</tr>
<tr>
<td headers="Type">
JavaScript with scope

</td>
<td headers="Number">
15

</td>
<td headers="Alias">
"javascriptWithScope"

</td>
<td headers="Notes">
Deprecated.

</td>
</tr>
<tr>
<td headers="Type">
32-bit integer

</td>
<td headers="Number">
16

</td>
<td headers="Alias">
"int"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Timestamp

</td>
<td headers="Number">
17

</td>
<td headers="Alias">
"timestamp"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
64-bit integer

</td>
<td headers="Number">
18

</td>
<td headers="Alias">
"long"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Decimal128

</td>
<td headers="Number">
19

</td>
<td headers="Alias">
"decimal"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Min key

</td>
<td headers="Number">
-1

</td>
<td headers="Alias">
"minKey"

</td>
<td headers="Notes">

</td>
</tr>
<tr>
<td headers="Type">
Max key

</td>
<td headers="Number">
127

</td>
<td headers="Alias">
"maxKey"

</td>
<td headers="Notes">

</td>
</tr>
</table>- The [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) operator supports using these values to query fields by their BSON type. [`$type`](https://www.mongodb.com/docs/reference/operator/query/type/#mongodb-query-op.-type) also supports the `number` alias, which matches the integer, decimal, double, and long BSON types.

- The [`$type`](https://www.mongodb.com/docs/reference/operator/aggregation/type/#mongodb-expression-exp.-type) aggregation operator returns the BSON type of its argument.

- The [`$isNumber`](https://www.mongodb.com/docs/reference/operator/aggregation/isNumber/#mongodb-expression-exp.-isNumber) aggregation operator returns `true` if its argument is a BSON integer, decimal, double, or long.

To determine a field's type, see [Type Checking](https://www.mongodb.com/docs/mongodb-shell/reference/data-types/#std-label-check-types-in-shell).

If you convert BSON to JSON, see the [Extended JSON](https://www.mongodb.com/docs/reference/mongodb-extended-json/#std-label-mongodb-extended-json-v2) reference.

The following sections describe special considerations for particular BSON types.

## Binary Data

A BSON binary `binData` value is a byte array. A `binData` value has a subtype that indicates how to interpret the binary data. The following table shows the subtypes:

<table>
<tr>
<th id="Number">
Number

</th>
<th id="Description">
Description

</th>
</tr>
<tr>
<td headers="Number">
0

</td>
<td headers="Description">
Generic binary subtype

</td>
</tr>
<tr>
<td headers="Number">
1

</td>
<td headers="Description">
Function data

</td>
</tr>
<tr>
<td headers="Number">
2

</td>
<td headers="Description">
Binary (old)

</td>
</tr>
<tr>
<td headers="Number">
3

</td>
<td headers="Description">
UUID (old)

</td>
</tr>
<tr>
<td headers="Number">
4

</td>
<td headers="Description">
UUID

</td>
</tr>
<tr>
<td headers="Number">
5

</td>
<td headers="Description">
MD5

</td>
</tr>
<tr>
<td headers="Number">
6

</td>
<td headers="Description">
Encrypted BSON value

</td>
</tr>
<tr>
<td headers="Number">
7

</td>
<td headers="Description">
Compressed time series data

</td>
</tr>
<tr>
<td headers="Number">
8

</td>
<td headers="Description">
Sensitive data, such as a key or secret. MongoDB does not log literal values for binary data with subtype 8. Instead, MongoDB logs a placeholder value of `###`.

</td>
</tr>
<tr>
<td headers="Number">
9

</td>
<td headers="Description">
Vector data, which is densely packed arrays of numbers of the same type.

</td>
</tr>
<tr>
<td headers="Number">
128

</td>
<td headers="Description">
Custom data

</td>
</tr>
</table>

## ObjectId

ObjectIds are small, likely unique, fast to generate, and ordered. ObjectId values are 12 bytes in length, consisting of:

- A 4-byte timestamp, representing the ObjectId's creation, measured in seconds since the Unix epoch.

- A 5-byte random value generated once per client-side process. This random value is unique to the machine and process. If the process restarts or the primary node of the process changes, this value is re-generated.

- A 3-byte incrementing counter per client-side process, initialized to a random value. The counter resets when a process restarts.

For timestamp and counter values, the most significant bytes appear first in the byte sequence (big-endian). This is unlike other BSON values, where the least significant bytes appear first (little-endian).

If an integer value is used to create an ObjectId, the integer replaces the timestamp.

In MongoDB, each document stored in a standard collection requires a unique [_id](https://www.mongodb.com/docs/reference/glossary/#std-term-_id) field that acts as a [primary key](https://www.mongodb.com/docs/reference/glossary/#std-term-primary-key). If an inserted document omits the `_id` field, the MongoDB driver automatically generates an [ObjectId](https://www.mongodb.com/docs/reference/bson-types/#std-label-objectid) for the `_id` field.

This also applies to documents inserted through update operations with [upsert: true](https://www.mongodb.com/docs/reference/method/db.collection.update/#std-label-upsert-parameter).

MongoDB clients should add an `_id` field with a unique ObjectId. Using ObjectIds for the `_id` field provides the following additional benefits:

- You can access `ObjectId` creation time in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) using the [`ObjectId.getTimestamp()`](https://www.mongodb.com/docs/reference/method/ObjectId.getTimestamp/#mongodb-method-ObjectId.getTimestamp) method.

- ObjectIds are approximately ordered by creation time, but are not perfectly ordered. Sorting a collection on an `_id` field containing `ObjectId` values is roughly equivalent to sorting by creation time.

  While [ObjectId](https://www.mongodb.com/docs/reference/bson-types/#std-label-objectid) values should increase over time, they are not necessarily monotonic. This is because they:

  - Only contain one second of temporal resolution, so [ObjectId](https://www.mongodb.com/docs/reference/bson-types/#std-label-objectid) values created within the same second do not have a guaranteed ordering, and

  - Are generated by clients, which may have differing system clocks.

Use the [`ObjectId()`](https://www.mongodb.com/docs/reference/method/ObjectId/#mongodb-method-ObjectId) methods to set and retrieve ObjectId values.

Starting in MongoDB 5.0, [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh) replaces the legacy `mongo` shell. The `ObjectId()` methods work differently in `mongosh` than in the legacy `mongo` shell. For more information on the legacy methods, see [Legacy mongo Shell](https://www.mongodb.com/docs/reference/mongo/#std-label-mongo).

## String

BSON strings are UTF-8. In general, drivers for each programming language convert from the language's string format to UTF-8 when serializing and deserializing BSON. This makes it possible to store most international characters in BSON strings with ease.  In addition, MongoDB [`$regex`](https://www.mongodb.com/docs/reference/operator/query/regex/#mongodb-query-op.-regex) queries support UTF-8 in the regex string.

Given strings using UTF-8 character sets, using [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) on strings will be reasonably correct. However, because internally [`sort()`](https://www.mongodb.com/docs/reference/method/cursor.sort/#mongodb-method-cursor.sort) uses the C++ `strcmp` api, the sort order may handle some characters incorrectly.

## Timestamps

BSON has a special timestamp type for *internal* MongoDB use and is **not** associated with the regular [Date](https://www.mongodb.com/docs/reference/bson-types/#std-label-document-bson-type-date) type. This internal timestamp type is a 64 bit value where:

- the most significant 32 bits are a `time_t` value (seconds since the Unix epoch)

- the least significant 32 bits are an incrementing `ordinal` for operations within a given second.

While the BSON format is little-endian, and therefore stores the least significant bits first, the [`mongod`](https://www.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) instance always compares the `time_t` value before the `ordinal` value on all platforms, regardless of endianness.

In replication, the [oplog](https://www.mongodb.com/docs/reference/glossary/#std-term-oplog) has a `ts` field. The values in this field reflect the operation time, which uses a BSON timestamp value.

Within a single [`mongod`](https://www.mongodb.com/docs/reference/program/mongod/#mongodb-binary-bin.mongod) instance, timestamp values in the [oplog](https://www.mongodb.com/docs/reference/glossary/#std-term-oplog) are always unique.

The BSON timestamp type is for *internal* MongoDB use. For most cases, in application development, you will want to use the BSON date type. See [Date](https://www.mongodb.com/docs/reference/bson-types/#std-label-document-bson-type-date) for more information.

## Date

BSON Date is a 64-bit integer that represents the number of milliseconds since the Unix epoch (Jan 1, 1970). This results in a representable date range of about 290 million years into the past and future.

The [official BSON specification](http://bsonspec.org/#/specification) refers to the BSON Date type as the *UTC datetime*.

BSON Date type is signed.  Negative values represent dates before 1970.

To construct a `Date` in [`mongosh`](https://www.mongodb.com/docs/mongodb-shell/#mongodb-binary-bin.mongosh), you can use the `new Date()` or `ISODate()` constructor.

### Construct a Date With the New Date() Constructor

To construct a `Date` with the `new Date()` constructor, run the following command:

```javascript
var mydate1 = new Date()
```

The `mydate1` variable outputs a date and time wrapped as an ISODate:

```javascript
mydate1
```

```javascript
ISODate("2020-05-11T20:14:14.796Z")
```

### Construct a Date With the ISODate() Constructor

To construct a `Date` using the `ISODate()` constructor, run the following command:

```javascript
var mydate2 = ISODate()
```

The `mydate2` variable stores a date and time wrapped as an ISODate:

```javascript
mydate2
```

```javascript
ISODate("2020-05-11T20:14:14.796Z")
```

### Convert a Date to a String

To print the `Date` in a `string` format, use the `toString()` method:

```javascript
mydate1.toString()
```

```javascript
Mon May 11 2020 13:14:14 GMT-0700 (Pacific Daylight Time)
```

### Return the Month Portion of a Date

You can also return the month portion of the `Date` value. Months are zero-indexed, so that January is month `0`.

```javascript
mydate1.getMonth()
```

```javascript
4
```

Prior to version 2.0, `Date` values were incorrectly interpreted as *unsigned* integers, which affected sorts, range queries, and indexes on `Date` fields. Because indexes are not recreated when upgrading, please re-index if you created an index on `Date` values with an earlier version, and dates before 1970 are relevant to your application.

## `decimal128` BSON Data Type

`decimal128` is a 128-bit decimal representation for storing very large or very precise numbers, whenever rounding decimals is important. It was created in August 2009 as part of the [IEEE 754-2008](https://en.wikipedia.org/wiki/IEEE_754-2008_revision) revision of floating points. When you need high precision when working with BSON data types, you should use `decimal128`.

`decimal128` supports 34 decimal digits of precision, or [significand](https://en.wikipedia.org/wiki/Significand) along with an exponent range of -6143 to +6144. The significand is not normalized in the `decimal128` standard, allowing for multiple possible representations: `10 x 10^-1 = 1 x 10^0 = .1 x 10^1 = .01 x 10^2`, etc. Having the ability to store maximum and minimum values in the order of `10^6144` and `10^-6143`, respectively, allows for a lot of precision.

### Use `decimal128` With the `Decimal128()` Constructor

In MongoDB, you can store data in `decimal128` format using the `Decimal128()` constructor. If you pass in the decimal value as a string, MongoDB stores the value in the database as follows:

```javascript
Decimal128("9823.1297")
```

You can also pass in the decimal value as a `double`:

```javascript
Decimal128.fromStringWithRounding("1234.99999999999")
```

You should also consider the usage and support your programming language has for `decimal128`. The following languages don’t natively support this feature and require a plugin or additional package to get the functionality:

- **Python:** The [decimal.Decimal](https://docs.python.org/3/library/decimal.html) module can be used for floating-point arithmetic.

- **Java:** The [Java BigDecimal](https://docs.oracle.com/javase/1.5.0/docs/api/java/math/BigDecimal.html) class provides support for `decimal128` numbers.

- **Node.js:**  There are several packages that provide support, such as [js-big-decimal](https://www.npmjs.com/package/js-big-decimal) or [node.js bigdecimal](https://www.npmjs.com/package/bigdecimal) available on [npm](https://www.npmjs.com/).

### Use Cases

When you perfom mathematical calculations programmatically, you can sometimes receive unexpected results. The following example in Node.js yields incorrect results:

```javascript
> 0.1
0.1
> 0.2
0.2
> 0.1 * 0.2
0.020000000000000004
> 0.1 + 0.1
0.010000000000000002
```

Similarly, the following example in Java produces incorrect output:

```java
class Main {
   public static void main(String[] args) {
      System.out.println("0.1 * 0.2:");
      System.out.println(0.1 * 0.2);
   }
}
```

```javascript
0.1 * 0.2:
0.020000000000000004
```

The same computations in Python, Ruby, Rust, and other languages produce the same results. This happens because binary floating-point numbers do not represent base 10 values well.

For example, the `0.1` used in the above examples is represented in binary as `0.0001100110011001101`. Most of the time, this does not cause any significant issues. However, in applications such as finance or banking where precision is important, use `decimal128` as your data type.

## BSON with MongoDB Drivers

To see how specific drivers handle BSON, refer to the documentation for your driver:

- [C: BSON](https://www.mongodb.com/docs/languages/c/c-driver/data-formats/bson/)

- [C++: Working with BSON](https://www.mongodb.com/docs/languages/cpp/cpp-driver/current/data-formats/working-with-bson/)

- [C#: BSON Operations](https://www.mongodb.com/docs/drivers/csharp/current/document-formats/bson/#std-label-csharp-bson)

- [Go: Work with BSON](https://www.mongodb.com/docs/drivers/go/current/data-formats/bson/#std-label-golang-bson)

- [Java Sync: Document Data Format: BSON](https://www.mongodb.com/docs/drivers/java/sync/data-formats/document-data-format-bson/)

- [Kotlin: Document Data Format: BSON](https://www.mongodb.com/docs/drivers/kotlin/coroutine/data-formats/document-data-format-bson/)

- [PHP: Custom Data Types](https://www.mongodb.com/docs/php-library/upcoming/data-formats/custom-types/#std-label-php-custom-types)

- [Node.js: Work with BSON Data](https://www.mongodb.com/docs/drivers/node/current/data-formats/bson/#std-label-node-bson)

- [PyMongo: BSON](https://www.mongodb.com/docs/languages/python/pymongo-driver/data-formats/bson/#std-label-pymongo-bson)

- [Ruby: BSON Data Format](http://www.mongodb.com/docs/ruby-driver/data-formats/bson/)

- [Rust: How Do I Convert Between BSON and Rust Types](https://www.mongodb.com/docs/drivers/rust/faq/#how-do-i-convert-between-bson-and-rust-types-)
