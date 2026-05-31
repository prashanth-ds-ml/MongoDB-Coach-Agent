> Source: https://www.mongodb.com/docs/manual/reference/operator/aggregation/
> Fetch method: html_fallback

# Expressions - Database Manual - MongoDB Docs Expressions

Expressions - Database Manual - MongoDB Docs

[Make the MongoDB docs better! We value your opinion. Share your feedback for a chance to win $100.](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

[Click here >](https://research.rallyuxr.com/recruit/clf9wl0m50006e31jbdt7hn51/study/cmobv8cnk2hpei2l3h8qw9zax?channel=share)

Docs Menu

Ask MongoDB AI

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Query Language](/docs/manual/reference/mql)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Query Language](/docs/manual/reference/mql)

[Docs Home](https://www.mongodb.com/docs/)/
[Development](/docs/development)/
[Query Language](/docs/manual/reference/mql)

# Expressions

Copy page

Expressions are MQL components that resolve to a value. Expressions are stateless, meaning they return a value without mutating any of the values used to build the expression. You can use expressions in the following MQL contexts:

-
Some aggregation pipeline stages, such as `[$project](/docs/manual/reference/operator/aggregation/project/#mongodb-pipeline-pipe.-project)`, `[$addFields](/docs/manual/reference/operator/aggregation/addFields/#mongodb-pipeline-pipe.-addFields)`, and `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`

-
[Query predicates](/docs/manual/reference/glossary/#std-term-query-predicate)that use `[$expr](/docs/manual/reference/operator/query/expr/#mongodb-query-op.-expr)`

-
Find command [projections](/docs/manual/tutorial/project-fields-from-query-results/#std-label-read-operations-projection)

In the MongoDB Query Language, you can build expressions from the following components:

Component

Example

Constants

`3 `

Operators

`[$add](/docs/manual/reference/operator/aggregation/add/#mongodb-expression-exp.-add)`

Field path expressions

`"$<path.to.field>" `

For example, `{ $add: [ 3, "$inventory.total" ] } `is an expression that consists of the `$add `operator and two operands:

-
The constant `3 `

-
The [field path expression](/docs/manual/core/aggregation-pipeline/#std-label-agg-quick-ref-field-paths)`"$inventory.total" `

The expression returns the result of adding 3 to the value at path `inventory.total `of the input document.

Expression operators are similar to functions that take arguments. In general, these operators take an array of arguments and have the following form:

```

{ <operator>: [ <argument1>,<argument2> ... ] }
```

If an operator accepts a single argument, you can omit the outer array designating the argument list:

```

{ <operator>: <argument> }
```

This page lists operators that you can use to construct [expressions](/docs/manual/reference/glossary/#std-term-expression)[.](/docs/manual/reference/glossary/#std-term-expression)

## Arithmetic Operators

Arithmetic expressions perform mathematic operations on numbers. Some arithmetic expressions can also support date arithmetic.

Name

Description

`[$abs](/docs/manual/reference/operator/aggregation/abs/#mongodb-expression-exp.-abs)`

Returns the absolute value of a number.

`[$add](/docs/manual/reference/operator/aggregation/add/#mongodb-expression-exp.-add)`

Adds numbers to return the sum, or adds numbers and a date to return a new date. If adding numbers and a date, treats the numbers as milliseconds. Accepts any number of argument expressions, but at most, one expression can resolve to a date.

`[$ceil](/docs/manual/reference/operator/aggregation/ceil/#mongodb-expression-exp.-ceil)`

Returns the smallest integer greater than or equal to the specified number.

`[$divide](/docs/manual/reference/operator/aggregation/divide/#mongodb-expression-exp.-divide)`

Returns the result of dividing the first number by the second. Accepts two argument expressions.

`[$exp](/docs/manual/reference/operator/aggregation/exp/#mongodb-expression-exp.-exp)`

Raises e to the specified exponent.

`[$floor](/docs/manual/reference/operator/aggregation/floor/#mongodb-expression-exp.-floor)`

Returns the largest integer less than or equal to the specified number.

`[$ln](/docs/manual/reference/operator/aggregation/ln/#mongodb-expression-exp.-ln)`

Calculates the natural log of a number.

`[$log](/docs/manual/reference/operator/aggregation/log/#mongodb-expression-exp.-log)`

Calculates the log of a number in the specified base.

`[$log10](/docs/manual/reference/operator/aggregation/log10/#mongodb-expression-exp.-log10)`

Calculates the log base 10 of a number.

`[$mod](/docs/manual/reference/operator/aggregation/mod/#mongodb-expression-exp.-mod)`

Returns the remainder of the first number divided by the second. Accepts two argument expressions.

`[$multiply](/docs/manual/reference/operator/aggregation/multiply/#mongodb-expression-exp.-multiply)`

Multiplies numbers to return the product. Accepts any number of argument expressions.

`[$pow](/docs/manual/reference/operator/aggregation/pow/#mongodb-expression-exp.-pow)`

Raises a number to the specified exponent.

`[$round](/docs/manual/reference/operator/aggregation/round/#mongodb-expression-exp.-round)`

Rounds a number to to a whole integer or to a specified decimal place.

`[$sigmoid](/docs/manual/reference/operator/aggregation/sigmoid/#mongodb-expression-exp.-sigmoid)`

Returns the result of the sigmoid function (the integration of the normal distribution with standard deviation 1).

`[$sqrt](/docs/manual/reference/operator/aggregation/sqrt/#mongodb-expression-exp.-sqrt)`

Calculates the square root.

`[$subtract](/docs/manual/reference/operator/aggregation/subtract/#mongodb-expression-exp.-subtract)`

Returns the result of subtracting the second value from the first. If the two values are numbers, return the difference. If the two values are dates, return the difference in milliseconds. If the two values are a date and a number in milliseconds, return the resulting date. Accepts two argument expressions. If the two values are a date and a number, specify the date argument first as it is not meaningful to subtract a date from a number.

`[$trunc](/docs/manual/reference/operator/aggregation/trunc/#mongodb-expression-exp.-trunc)`

Truncates a number to a whole integer or to a specified decimal place.

## Array Operators

Name

Description

`[$arrayElemAt](/docs/manual/reference/operator/aggregation/arrayElemAt/#mongodb-expression-exp.-arrayElemAt)`

Returns the element at the specified array index.

`[$arrayToObject](/docs/manual/reference/operator/aggregation/arrayToObject/#mongodb-expression-exp.-arrayToObject)`

Converts an array of key value pairs to a document.

`[$concatArrays](/docs/manual/reference/operator/aggregation/concatArrays/#mongodb-expression-exp.-concatArrays)`

Concatenates arrays to return the concatenated array.

`[$filter](/docs/manual/reference/operator/aggregation/filter/#mongodb-expression-exp.-filter)`

Selects a subset of the array to return an array with only the elements that match the filter condition.

`[$firstN](/docs/manual/reference/operator/aggregation/firstN/#mongodb-expression-exp.-firstN)`

Returns a specified number of elements from the beginning of an array. Distinct from the `[$firstN](/docs/manual/reference/operator/aggregation/firstN/#mongodb-group-grp.-firstN)`accumulator.

`[$in](/docs/manual/reference/operator/aggregation/in/#mongodb-expression-exp.-in)`

Returns a boolean indicating whether a specified value is in an array.

`[$indexOfArray](/docs/manual/reference/operator/aggregation/indexOfArray/#mongodb-expression-exp.-indexOfArray)`

Searches an array for an occurrence of a specified value and returns the array index of the first occurrence. Array indexes start at zero.

`[$isArray](/docs/manual/reference/operator/aggregation/isArray/#mongodb-expression-exp.-isArray)`

Determines if the operand is an array. Returns a boolean.

`[$lastN](/docs/manual/reference/operator/aggregation/lastN/#mongodb-expression-exp.-lastN)`

Returns a specified number of elements from the end of an array. Distinct from the `[$lastN](/docs/manual/reference/operator/aggregation/lastN/#mongodb-group-grp.-lastN)`accumulator.

`[$map](/docs/manual/reference/operator/aggregation/map/#mongodb-expression-exp.-map)`

Applies a subexpression to each element of an array and returns the array of resulting values in order. Accepts named parameters.

`[$maxN](/docs/manual/reference/operator/aggregation/maxN-array-element/#mongodb-expression-exp.-maxN)`

Returns the `n `largest values in an array. Distinct from the `[$maxN](/docs/manual/reference/operator/aggregation/maxN/#mongodb-group-grp.-maxN)`accumulator.

`[$minN](/docs/manual/reference/operator/aggregation/minN-array-element/#mongodb-expression-exp.-minN)`

Returns the `n `smallest values in an array. Distinct from the `[$minN](/docs/manual/reference/operator/aggregation/minN/#mongodb-group-grp.-minN)`accumulator.

`[$objectToArray](/docs/manual/reference/operator/aggregation/objectToArray/#mongodb-expression-exp.-objectToArray)`

Converts a document to an array of documents representing key-value pairs.

`[$range](/docs/manual/reference/operator/aggregation/range/#mongodb-expression-exp.-range)`

Outputs an array containing a sequence of integers according to user-defined inputs.

`[$reduce](/docs/manual/reference/operator/aggregation/reduce/#mongodb-expression-exp.-reduce)`

Applies an expression to each element in an array and combines them into a single value.

`[$reverseArray](/docs/manual/reference/operator/aggregation/reverseArray/#mongodb-expression-exp.-reverseArray)`

Returns an array with the elements in reverse order.

`[$size](/docs/manual/reference/operator/aggregation/size/#mongodb-expression-exp.-size)`

Returns the number of elements in the array. Accepts a single expression as argument.

`[$slice](/docs/manual/reference/operator/aggregation/slice/#mongodb-expression-exp.-slice)`

Returns a subset of an array.

`[$sortArray](/docs/manual/reference/operator/aggregation/sortArray/#mongodb-expression-exp.-sortArray)`

Sorts the elements of an array.

`[$zip](/docs/manual/reference/operator/aggregation/zip/#mongodb-expression-exp.-zip)`

Merge two arrays together.

## Bitwise Operators

Name

Description

`[$bitAnd](/docs/manual/reference/operator/aggregation/bitAnd/#mongodb-expression-exp.-bitAnd)`

Returns the result of a bitwise `and `operation on an array of `int `or `long `values.

New in version 6.3 .

`[$bitNot](/docs/manual/reference/operator/aggregation/bitNot/#mongodb-expression-exp.-bitNot)`

Returns the result of a bitwise `not `operation on a single argument or an array that contains a single `int `or `long `value.

New in version 6.3 .

`[$bitOr](/docs/manual/reference/operator/aggregation/bitOr/#mongodb-expression-exp.-bitOr)`

Returns the result of a bitwise `or `operation on an array of `int `or `long `values.

New in version 6.3 .

`[$bitXor](/docs/manual/reference/operator/aggregation/bitXor/#mongodb-expression-exp.-bitXor)`

Returns the result of a bitwise `xor `(exclusive or) operation on an array of `int `and `long `values.

New in version 6.3 .

## Boolean Operators

Boolean expressions evaluate their argument expressions as booleans and return a boolean as the result.

In addition to the `false `boolean value, Boolean expression evaluates as `false `the following: `null `, `0 `, and `undefined `values. The Boolean expression evaluates all other values as `true `, including non-zero numeric values and arrays.

Name

Description

`[$and](/docs/manual/reference/operator/aggregation/and/#mongodb-expression-exp.-and)`

Returns `true `only when all its expressions evaluate to `true `. Accepts any number of argument expressions.

`[$not](/docs/manual/reference/operator/aggregation/not/#mongodb-expression-exp.-not)`

Returns the boolean value that is the opposite of its argument expression. Accepts a single argument expression.

`[$or](/docs/manual/reference/operator/aggregation/or/#mongodb-expression-exp.-or)`

Returns `true `when any of its expressions evaluates to `true `. Accepts any number of argument expressions.

## Comparison Operators

Comparison expressions return a boolean except for `[$cmp](/docs/manual/reference/operator/aggregation/cmp/#mongodb-expression-exp.-cmp)`which returns a number.

The comparison expressions take two argument expressions and compare both value and type, using the [specified BSON comparison order](/docs/manual/reference/bson-type-comparison-order/#std-label-bson-types-comparison-order)for values of different types.

Name

Description

`[$cmp](/docs/manual/reference/operator/aggregation/cmp/#mongodb-expression-exp.-cmp)`

Returns `0 `if the two values are equivalent, `1 `if the first value is greater than the second, and `-1 `if the first value is less than the second.

`[$eq](/docs/manual/reference/operator/aggregation/eq/#mongodb-expression-exp.-eq)`

Returns `true `if the values are equivalent.

`[$gt](/docs/manual/reference/operator/aggregation/gt/#mongodb-expression-exp.-gt)`

Returns `true `if the first value is greater than the second.

`[$gte](/docs/manual/reference/operator/aggregation/gte/#mongodb-expression-exp.-gte)`

Returns `true `if the first value is greater than or equal to the second.

`[$lt](/docs/manual/reference/operator/aggregation/lt/#mongodb-expression-exp.-lt)`

Returns `true `if the first value is less than the second.

`[$lte](/docs/manual/reference/operator/aggregation/lte/#mongodb-expression-exp.-lte)`

Returns `true `if the first value is less than or equal to the second.

`[$ne](/docs/manual/reference/operator/aggregation/ne/#mongodb-expression-exp.-ne)`

Returns `true `if the values are not equivalent.

## Conditional Operators

Name

Description

`[$cond](/docs/manual/reference/operator/aggregation/cond/#mongodb-expression-exp.-cond)`

A ternary operator that evaluates one expression, and depending on the result, returns the value of one of the other two expressions. Accepts either three expressions in an ordered list or three named parameters.

`[$ifNull](/docs/manual/reference/operator/aggregation/ifNull/#mongodb-expression-exp.-ifNull)`

Returns either the non-null result of the first expression or the result of the second expression if the first expression results in a null result. Null result encompasses instances of undefined values or missing fields. Accepts two expressions as arguments. The result of the second expression can be null.

`[$switch](/docs/manual/reference/operator/aggregation/switch/#mongodb-expression-exp.-switch)`

Evaluates a series of case expressions. When it finds an expression which evaluates to `true `, `$switch `executes a specified expression and breaks out of the control flow.

## Custom Aggregation Operators

Name

Description

`[$accumulator](/docs/manual/reference/operator/aggregation/accumulator/#mongodb-group-grp.-accumulator)`

Defines a custom accumulator function.

`[$function](/docs/manual/reference/operator/aggregation/function/#mongodb-expression-exp.-function)`

Defines a custom function.

## Data Size Operators

The following operators return the size of a data element:

Name

Description

`[$binarySize](/docs/manual/reference/operator/aggregation/binarySize/#mongodb-expression-exp.-binarySize)`

Returns the size of a given string or binary data value's content in bytes.

`[$bsonSize](/docs/manual/reference/operator/aggregation/bsonSize/#mongodb-expression-exp.-bsonSize)`

Returns the size in bytes of a given document (i.e. bsontype `Object `) when encoded as [BSON](/docs/manual/reference/glossary/#std-term-BSON)[.](/docs/manual/reference/glossary/#std-term-BSON)

## Date Operators

The following operators returns date objects or components of a date object:

Name

Description

`[$dateAdd](/docs/manual/reference/operator/aggregation/dateAdd/#mongodb-expression-exp.-dateAdd)`

Adds a number of time units to a date object.

`[$dateDiff](/docs/manual/reference/operator/aggregation/dateDiff/#mongodb-expression-exp.-dateDiff)`

Returns the difference between two dates.

`[$dateFromParts](/docs/manual/reference/operator/aggregation/dateFromParts/#mongodb-expression-exp.-dateFromParts)`

Constructs a BSON Date object given the date's constituent parts.

`[$dateFromString](/docs/manual/reference/operator/aggregation/dateFromString/#mongodb-expression-exp.-dateFromString)`

Converts a date/time string to a date object.

`[$dateSubtract](/docs/manual/reference/operator/aggregation/dateSubtract/#mongodb-expression-exp.-dateSubtract)`

Subtracts a number of time units from a date object.

`[$dateToParts](/docs/manual/reference/operator/aggregation/dateToParts/#mongodb-expression-exp.-dateToParts)`

Returns a document containing the constituent parts of a date.

`[$dateToString](/docs/manual/reference/operator/aggregation/dateToString/#mongodb-expression-exp.-dateToString)`

Returns the date as a formatted string.

`[$dateTrunc](/docs/manual/reference/operator/aggregation/dateTrunc/#mongodb-expression-exp.-dateTrunc)`

Truncates a date.

`[$dayOfMonth](/docs/manual/reference/operator/aggregation/dayOfMonth/#mongodb-expression-exp.-dayOfMonth)`

Returns the day of the month for a date as a number between 1 and 31.

`[$dayOfWeek](/docs/manual/reference/operator/aggregation/dayOfWeek/#mongodb-expression-exp.-dayOfWeek)`

Returns the day of the week for a date as a number between 1 (Sunday) and 7 (Saturday).

`[$dayOfYear](/docs/manual/reference/operator/aggregation/dayOfYear/#mongodb-expression-exp.-dayOfYear)`

Returns the day of the year for a date as a number between 1 and 366 (leap year).

`[$hour](/docs/manual/reference/operator/aggregation/hour/#mongodb-expression-exp.-hour)`

Returns the hour for a date as a number between 0 and 23.

`[$isoDayOfWeek](/docs/manual/reference/operator/aggregation/isoDayOfWeek/#mongodb-expression-exp.-isoDayOfWeek)`

Returns the weekday number in ISO 8601 format, ranging from `1 `(for Monday) to `7 `(for Sunday).

`[$isoWeek](/docs/manual/reference/operator/aggregation/isoWeek/#mongodb-expression-exp.-isoWeek)`

Returns the week number in ISO 8601 format, ranging from `1 `to `53 `. Week numbers start at `1 `with the week (Monday through Sunday) that contains the year's first Thursday.

`[$isoWeekYear](/docs/manual/reference/operator/aggregation/isoWeekYear/#mongodb-expression-exp.-isoWeekYear)`

Returns the year number in ISO 8601 format. The year starts with the Monday of week 1 (ISO 8601) and ends with the Sunday of the last week (ISO 8601).

`[$millisecond](/docs/manual/reference/operator/aggregation/millisecond/#mongodb-expression-exp.-millisecond)`

Returns the milliseconds of a date as a number between 0 and 999.

`[$minute](/docs/manual/reference/operator/aggregation/minute/#mongodb-expression-exp.-minute)`

Returns the minute for a date as a number between 0 and 59.

`[$month](/docs/manual/reference/operator/aggregation/month/#mongodb-expression-exp.-month)`

Returns the month for a date as a number between 1 (January) and 12 (December).

`[$second](/docs/manual/reference/operator/aggregation/second/#mongodb-expression-exp.-second)`

Returns the seconds for a date as a number between 0 and 60 (leap seconds).

`[$toDate](/docs/manual/reference/operator/aggregation/toDate/#mongodb-expression-exp.-toDate)`

Converts value to a Date.

`[$week](/docs/manual/reference/operator/aggregation/week/#mongodb-expression-exp.-week)`

Returns the week number for a date as a number between 0 (the partial week that precedes the first Sunday of the year) and 53 (leap year).

`[$year](/docs/manual/reference/operator/aggregation/year/#mongodb-expression-exp.-year)`

Returns the year for a date as a number (e.g. 2014).

The following arithmetic operators can take date operands:

Name

Description

`[$add](/docs/manual/reference/operator/aggregation/add/#mongodb-expression-exp.-add)`

Adds numbers and a date to return a new date. If adding numbers and a date, treats the numbers as milliseconds. Accepts any number of argument expressions, but at most, one expression can resolve to a date.

`[$subtract](/docs/manual/reference/operator/aggregation/subtract/#mongodb-expression-exp.-subtract)`

Returns the result of subtracting the second value from the first. If the two values are dates, return the difference in milliseconds. If the two values are a date and a number in milliseconds, return the resulting date. Accepts two argument expressions. If the two values are a date and a number, specify the date argument first as it is not meaningful to subtract a date from a number.

## Expressions Associated with Accumulators

Some accumulators for the `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`stage are also available for use as expressions. When used as expressions, they calculate an aggregate value over the given input arguments or input array.

The following operators are accumulators, but they are also available as expressions which accept an array of values as input.

Name

Description

`[$avg](/docs/manual/reference/operator/aggregation/avg/#mongodb-group-grp.-avg)`

Returns an average of the specified expression or list of expressions for each document. Ignores non-numeric values.

`[$concatArrays](/docs/manual/reference/operator/aggregation/concatArrays/#mongodb-group-grp.-concatArrays)`

Returns a single array that combines the elements of two or more arrays.

New in version 8.1 .

`[$first](/docs/manual/reference/operator/aggregation/first/#mongodb-group-grp.-first)`

Returns the result of an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)for the first document in a group.

`[$last](/docs/manual/reference/operator/aggregation/last/#mongodb-group-grp.-last)`

Returns the result of an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)for the last document in a group.

`[$max](/docs/manual/reference/operator/aggregation/max/#mongodb-group-grp.-max)`

Returns the maximum of the specified expression or list of expressions for each document

`[$median](/docs/manual/reference/operator/aggregation/median/#mongodb-group-grp.-median)`

Returns an approximation of the [median](/docs/manual/reference/glossary/#std-term-median), the 50th [percentile](/docs/manual/reference/glossary/#std-term-percentile), as a scalar value.

New in version 7.0 .

`[$min](/docs/manual/reference/operator/aggregation/min/#mongodb-group-grp.-min)`

Returns the minimum of the specified expression or list of expressions for each document

`[$percentile](/docs/manual/reference/operator/aggregation/percentile/#mongodb-group-grp.-percentile)`

Returns an array of scalar values that correspond to specified [percentile](/docs/manual/reference/glossary/#std-term-percentile)values.

New in version 7.0 .

`[$setUnion](/docs/manual/reference/operator/aggregation/setUnion/#mongodb-group-grp.-setUnion)`

Takes two or more arrays and returns an array containing the elements that appear in any input array.

New in version 8.1 .

`[$stdDevPop](/docs/manual/reference/operator/aggregation/stdDevPop/#mongodb-group-grp.-stdDevPop)`

Returns the population standard deviation of the input values.

`[$stdDevSamp](/docs/manual/reference/operator/aggregation/stdDevSamp/#mongodb-group-grp.-stdDevSamp)`

Returns the sample standard deviation of the input values.

`[$sum](/docs/manual/reference/operator/aggregation/sum/#mongodb-group-grp.-sum)`

Returns a sum of numerical values. Ignores non-numeric values.

## Literal Expression Operators

Name

Description

`[$literal](/docs/manual/reference/operator/aggregation/literal/#mongodb-expression-exp.-literal)`

Return a value without parsing. Use for values that the aggregation pipeline may interpret as an expression. For example, use a `[$literal](/docs/manual/reference/operator/aggregation/literal/#mongodb-expression-exp.-literal)`expression to a string that starts with a dollar sign ( `$ `) to avoid parsing as a field path.

## Miscellaneous Operators

Name

Description

`[$createObjectId](/docs/manual/reference/operator/aggregation/createObjectId/#mongodb-expression-exp.-createObjectId)`

Generate a new random ObjectId value.

`[$getField](/docs/manual/reference/operator/aggregation/getField/#mongodb-expression-exp.-getField)`

Returns the value of a specified field from a document. You can use `[$getField](/docs/manual/reference/operator/aggregation/getField/#mongodb-expression-exp.-getField)`to retrieve the value of fields with names that contain periods ( `. `) or start with dollar signs ( `$ `).

`[$hash](/docs/manual/reference/operator/aggregation/hash/#mongodb-expression-exp.-hash)`

Generates a binary hash value from a UTF-8 string or binary data.

`[$hexHash](/docs/manual/reference/operator/aggregation/hexHash/#mongodb-expression-exp.-hexHash)`

Generates an uppercase hexadecimal hash string from a UTF-8 string or binary data.

`[$rand](/docs/manual/reference/operator/aggregation/rand/#mongodb-expression-exp.-rand)`

Returns a random float between 0 and 1

`[$sampleRate](/docs/manual/reference/operator/aggregation/sampleRate/#mongodb-expression-exp.-sampleRate)`

Randomly select documents at a given rate. Although the exact number of documents selected varies on each run, the quantity chosen approximates the sample rate expressed as a percentage of the total number of documents.

`[$toHashedIndexKey](/docs/manual/reference/operator/aggregation/toHashedIndexKey/#mongodb-expression-exp.-toHashedIndexKey)`

Computes and returns the hash of the input expression using the same hash function that MongoDB uses to create a hashed index.

## Object Operators

Name

Description

`[$mergeObjects](/docs/manual/reference/operator/aggregation/mergeObjects/#mongodb-expression-exp.-mergeObjects)`

Combines multiple documents into a single document.

`[$objectToArray](/docs/manual/reference/operator/aggregation/objectToArray/#mongodb-expression-exp.-objectToArray)`

Converts a document to an array of documents representing key-value pairs.

`[$setField](/docs/manual/reference/operator/aggregation/setField/#mongodb-expression-exp.-setField)`

Adds, updates, or removes a specified field in a document. You can use `[$setField](/docs/manual/reference/operator/aggregation/setField/#mongodb-expression-exp.-setField)`to add, update, or remove fields with names that contain periods ( `. `) or start with dollar signs ( `$ `).

New in version 5.0 .

## Set Operators

Set expressions performs set operation on arrays, treating arrays as sets. Set expressions ignores the duplicate entries in each input array and the order of the elements.

If the set operation returns a set, the operation filters out duplicates in the result to output an array that contains only unique entries. The order of the elements in the output array is unspecified.

If a set contains a nested array element, the set expression does not descend into the nested array but evaluates the array at top-level.

Name

Description

`[$allElementsTrue](/docs/manual/reference/operator/aggregation/allElementsTrue/#mongodb-expression-exp.-allElementsTrue)`

Returns `true `if no element of a set evaluates to `false `, otherwise, returns `false `. Accepts a single argument expression.

`[$anyElementTrue](/docs/manual/reference/operator/aggregation/anyElementTrue/#mongodb-expression-exp.-anyElementTrue)`

Returns `true `if any elements of a set evaluate to `true `; otherwise, returns `false `. Accepts a single argument expression.

`[$setDifference](/docs/manual/reference/operator/aggregation/setDifference/#mongodb-expression-exp.-setDifference)`

Returns a set with elements that appear in the first set but not in the second set; i.e. performs a [relative complement](http://en.wikipedia.org/wiki/Complement_(set_theory))of the second set relative to the first. Accepts exactly two argument expressions.

`[$setEquals](/docs/manual/reference/operator/aggregation/setEquals/#mongodb-expression-exp.-setEquals)`

Returns `true `if the input sets have the same distinct elements. Accepts two or more argument expressions.

`[$setIntersection](/docs/manual/reference/operator/aggregation/setIntersection/#mongodb-expression-exp.-setIntersection)`

Returns a set with elements that appear in all of the input sets. Accepts any number of argument expressions.

`[$setIsSubset](/docs/manual/reference/operator/aggregation/setIsSubset/#mongodb-expression-exp.-setIsSubset)`

Returns `true `if all elements of the first set appear in the second set, including when the first set equals the second set; i.e. not a [strict subset](http://en.wikipedia.org/wiki/Subset). Accepts exactly two argument expressions.

`[$setUnion](/docs/manual/reference/operator/aggregation/setUnion/#mongodb-expression-exp.-setUnion)`

Returns a set with elements that appear in any of the input sets.

## String Operators

String expressions, with the exception of `[$concat](/docs/manual/reference/operator/aggregation/concat/#mongodb-expression-exp.-concat)`, only have a well-defined behavior for strings of ASCII characters.

`[$concat](/docs/manual/reference/operator/aggregation/concat/#mongodb-expression-exp.-concat)`behavior is well-defined regardless of the characters used.

Name

Description

`[$concat](/docs/manual/reference/operator/aggregation/concat/#mongodb-expression-exp.-concat)`

Concatenates any number of strings.

`[$dateFromString](/docs/manual/reference/operator/aggregation/dateFromString/#mongodb-expression-exp.-dateFromString)`

Converts a date/time string to a date object.

`[$dateToString](/docs/manual/reference/operator/aggregation/dateToString/#mongodb-expression-exp.-dateToString)`

Returns the date as a formatted string.

`[$indexOfBytes](/docs/manual/reference/operator/aggregation/indexOfBytes/#mongodb-expression-exp.-indexOfBytes)`

Searches a string for an occurrence of a substring and returns the UTF-8 byte index of the first occurrence. If the substring is not found, returns `-1 `.

`[$indexOfCP](/docs/manual/reference/operator/aggregation/indexOfCP/#mongodb-expression-exp.-indexOfCP)`

Searches a string for an occurrence of a substring and returns the UTF-8 code point index of the first occurrence. If the substring is not found, returns `-1 `

`[$ltrim](/docs/manual/reference/operator/aggregation/ltrim/#mongodb-expression-exp.-ltrim)`

Removes whitespace or the specified characters from the beginning of a string.

`[$regexFind](/docs/manual/reference/operator/aggregation/regexFind/#mongodb-expression-exp.-regexFind)`

Applies a regular expression (regex) to a string and returns information on the first matched substring.

`[$regexFindAll](/docs/manual/reference/operator/aggregation/regexFindAll/#mongodb-expression-exp.-regexFindAll)`

Applies a regular expression (regex) to a string and returns information on the all matched substrings.

`[$regexMatch](/docs/manual/reference/operator/aggregation/regexMatch/#mongodb-expression-exp.-regexMatch)`

Applies a regular expression (regex) to a string and returns a boolean that indicates if a match is found or not.

`[$replaceOne](/docs/manual/reference/operator/aggregation/replaceOne/#mongodb-expression-exp.-replaceOne)`

Replaces the first instance of a matched string in a given input.

`[$replaceAll](/docs/manual/reference/operator/aggregation/replaceAll/#mongodb-expression-exp.-replaceAll)`

Replaces all instances of a matched string in a given input.

`[$rtrim](/docs/manual/reference/operator/aggregation/rtrim/#mongodb-expression-exp.-rtrim)`

Removes whitespace or the specified characters from the end of a string.

`[$split](/docs/manual/reference/operator/aggregation/split/#mongodb-expression-exp.-split)`

Splits a string into substrings based on a delimiter. Returns an array of substrings. If the delimiter is not found within the string, returns an array containing the original string.

`[$strLenBytes](/docs/manual/reference/operator/aggregation/strLenBytes/#mongodb-expression-exp.-strLenBytes)`

Returns the number of UTF-8 encoded bytes in a string.

`[$strLenCP](/docs/manual/reference/operator/aggregation/strLenCP/#mongodb-expression-exp.-strLenCP)`

Returns the number of UTF-8 [code points](http://www.unicode.org/glossary/#code_point)in a string.

`[$strcasecmp](/docs/manual/reference/operator/aggregation/strcasecmp/#mongodb-expression-exp.-strcasecmp)`

Performs case-insensitive string comparison and returns: `0 `if two strings are equivalent, `1 `if the first string is greater than the second, and `-1 `if the first string is less than the second.

`[$substr](/docs/manual/reference/operator/aggregation/substr/#mongodb-expression-exp.-substr)`

Deprecated. Use `[$substrBytes](/docs/manual/reference/operator/aggregation/substrBytes/#mongodb-expression-exp.-substrBytes)`or `[$substrCP](/docs/manual/reference/operator/aggregation/substrCP/#mongodb-expression-exp.-substrCP)`[.](/docs/manual/reference/operator/aggregation/substrCP/#mongodb-expression-exp.-substrCP)

`[$substrBytes](/docs/manual/reference/operator/aggregation/substrBytes/#mongodb-expression-exp.-substrBytes)`

Returns the substring of a string. Starts with the character at the specified UTF-8 byte index (zero-based) in the string and continues for the specified number of bytes.

`[$substrCP](/docs/manual/reference/operator/aggregation/substrCP/#mongodb-expression-exp.-substrCP)`

Returns the substring of a string. Starts with the character at the specified UTF-8 [code point (CP)](http://www.unicode.org/glossary/#code_point)index (zero-based) in the string and continues for the number of code points specified.

`[$toLower](/docs/manual/reference/operator/aggregation/toLower/#mongodb-expression-exp.-toLower)`

Converts a string to lowercase. Accepts a single argument expression.

`[$toString](/docs/manual/reference/operator/aggregation/toString/#mongodb-expression-exp.-toString)`

Converts value to a string.

`[$trim](/docs/manual/reference/operator/aggregation/trim/#mongodb-expression-exp.-trim)`

Removes whitespace or the specified characters from the beginning and end of a string.

`[$toUpper](/docs/manual/reference/operator/aggregation/toUpper/#mongodb-expression-exp.-toUpper)`

Converts a string to uppercase. Accepts a single argument expression.

### Encrypted String Operators

Encrypted string expressions evaluate an argument against an encrypted field in a collection with [Queryable Encryption](/docs/manual/core/queryable-encryption/#std-label-qe-manual-feature-qe)enabled, and return a boolean.

Name

Description

`[$encStrContains](/docs/manual/reference/operator/aggregation/encStrContains/#mongodb-expression-exp.-encStrContains)`

Returns `true `if a subset of characters in the encrypted string match the specified string.

`[$encStrEndsWith](/docs/manual/reference/operator/aggregation/encStrEndsWith/#mongodb-expression-exp.-encStrEndsWith)`

Returns `true `if the last characters of the encrypted string match the specified string.

`[$encStrNormalizedEq](/docs/manual/reference/operator/aggregation/encStrNormalizedEq/#mongodb-expression-exp.-encStrNormalizedEq)`

Returns `true `if the [normalized string](/docs/manual/reference/glossary/#std-term-normalized-string)form of the encrypted string matches normalized string form of the specified string.

`[$encStrStartsWith](/docs/manual/reference/operator/aggregation/encStrStartsWith/#mongodb-expression-exp.-encStrStartsWith)`

Returns `true `if the first characters of the encrypted string match the specified string.

## Text Operators

Name

Description

`[$meta](/docs/manual/reference/operator/aggregation/meta/#mongodb-expression-exp.-meta)`

Access available per-document metadata related to the aggregation operation.

## Timestamp Operators

Timestamp expression operators return values from a [timestamp](/docs/manual/reference/bson-types/#std-label-document-bson-type-timestamp)[.](/docs/manual/reference/bson-types/#std-label-document-bson-type-timestamp)

Name

Description

`[$tsIncrement](/docs/manual/reference/operator/aggregation/tsIncrement/#mongodb-expression-exp.-tsIncrement)`

Returns the incrementing ordinal from a [timestamp](/docs/manual/reference/bson-types/#std-label-document-bson-type-timestamp)as a `[long](/docs/manual/reference/mongodb-extended-json-v1/#mongodb-bsontype-data_numberlong)`[.](/docs/manual/reference/mongodb-extended-json-v1/#mongodb-bsontype-data_numberlong)

New in version 5.1 .

`[$tsSecond](/docs/manual/reference/operator/aggregation/tsSecond/#mongodb-expression-exp.-tsSecond)`

Returns the seconds from a [timestamp](/docs/manual/reference/bson-types/#std-label-document-bson-type-timestamp)as a `[long](/docs/manual/reference/mongodb-extended-json-v1/#mongodb-bsontype-data_numberlong)`[.](/docs/manual/reference/mongodb-extended-json-v1/#mongodb-bsontype-data_numberlong)

New in version 5.1 .

## Trigonometry Operators

Trigonometry expressions perform trigonometric operations on numbers. Values that represent angles are always input or output in radians. Use `[$degreesToRadians](/docs/manual/reference/operator/aggregation/degreesToRadians/#mongodb-expression-exp.-degreesToRadians)`and `[$radiansToDegrees](/docs/manual/reference/operator/aggregation/radiansToDegrees/#mongodb-expression-exp.-radiansToDegrees)`to convert between degree and radian measurements.

Name

Description

`[$sin](/docs/manual/reference/operator/aggregation/sin/#mongodb-expression-exp.-sin)`

Returns the sine of a value that is measured in radians.

`[$cos](/docs/manual/reference/operator/aggregation/cos/#mongodb-expression-exp.-cos)`

Returns the cosine of a value that is measured in radians.

`[$tan](/docs/manual/reference/operator/aggregation/tan/#mongodb-expression-exp.-tan)`

Returns the tangent of a value that is measured in radians.

`[$asin](/docs/manual/reference/operator/aggregation/asin/#mongodb-expression-exp.-asin)`

Returns the inverse sin (arc sine) of a value in radians.

`[$acos](/docs/manual/reference/operator/aggregation/acos/#mongodb-expression-exp.-acos)`

Returns the inverse cosine (arc cosine) of a value in radians.

`[$atan](/docs/manual/reference/operator/aggregation/atan/#mongodb-expression-exp.-atan)`

Returns the inverse tangent (arc tangent) of a value in radians.

`[$atan2](/docs/manual/reference/operator/aggregation/atan2/#mongodb-expression-exp.-atan2)`

Returns the inverse tangent (arc tangent) of `y / x `in radians, where `y `and `x `are the first and second values passed to the expression respectively.

`[$asinh](/docs/manual/reference/operator/aggregation/asinh/#mongodb-expression-exp.-asinh)`

Returns the inverse hyperbolic sine (hyperbolic arc sine) of a value in radians.

`[$acosh](/docs/manual/reference/operator/aggregation/acosh/#mongodb-expression-exp.-acosh)`

Returns the inverse hyperbolic cosine (hyperbolic arc cosine) of a value in radians.

`[$atanh](/docs/manual/reference/operator/aggregation/atanh/#mongodb-expression-exp.-atanh)`

Returns the inverse hyperbolic tangent (hyperbolic arc tangent) of a value in radians.

`[$sinh](/docs/manual/reference/operator/aggregation/sinh/#mongodb-expression-exp.-sinh)`

Returns the hyperbolic sine of a value that is measured in radians.

`[$cosh](/docs/manual/reference/operator/aggregation/cosh/#mongodb-expression-exp.-cosh)`

Returns the hyperbolic cosine of a value that is measured in radians.

`[$tanh](/docs/manual/reference/operator/aggregation/tanh/#mongodb-expression-exp.-tanh)`

Returns the hyperbolic tangent of a value that is measured in radians.

`[$degreesToRadians](/docs/manual/reference/operator/aggregation/degreesToRadians/#mongodb-expression-exp.-degreesToRadians)`

Converts a value from degrees to radians.

`[$radiansToDegrees](/docs/manual/reference/operator/aggregation/radiansToDegrees/#mongodb-expression-exp.-radiansToDegrees)`

Converts a value from radians to degrees.

## Type Operators

Name

Description

`[$convert](/docs/manual/reference/operator/aggregation/convert/#mongodb-expression-exp.-convert)`

Converts a value to a specified type.

`[$isNumber](/docs/manual/reference/operator/aggregation/isNumber/#mongodb-expression-exp.-isNumber)`

Returns boolean `true `if the specified expression resolves to an `[integer](/docs/manual/reference/mongodb-extended-json/#mongodb-bsontype-Int32)`, `[decimal](/docs/manual/reference/mongodb-extended-json/#mongodb-bsontype-Decimal128)`, `[double](/docs/manual/reference/mongodb-extended-json/#mongodb-bsontype-Double)`, or `[long](/docs/manual/reference/mongodb-extended-json/#mongodb-bsontype-Int64)`[.](/docs/manual/reference/mongodb-extended-json/#mongodb-bsontype-Int64)

Returns boolean `false `if the expression resolves to any other [BSON type](/docs/manual/reference/bson-types/#std-label-bson-types), `null `, or a missing field.

`[$toArray](/docs/manual/reference/operator/aggregation/toArray/#mongodb-expression-exp.-toArray)`

Converts a value to an array.

`[$toBool](/docs/manual/reference/operator/aggregation/toBool/#mongodb-expression-exp.-toBool)`

Converts value to a boolean.

`[$toDate](/docs/manual/reference/operator/aggregation/toDate/#mongodb-expression-exp.-toDate)`

Converts value to a Date.

`[$toDecimal](/docs/manual/reference/operator/aggregation/toDecimal/#mongodb-expression-exp.-toDecimal)`

Converts value to a Decimal128.

`[$toDouble](/docs/manual/reference/operator/aggregation/toDouble/#mongodb-expression-exp.-toDouble)`

Converts value to a double.

`[$toInt](/docs/manual/reference/operator/aggregation/toInt/#mongodb-expression-exp.-toInt)`

Converts value to an integer.

`[$toLong](/docs/manual/reference/operator/aggregation/toLong/#mongodb-expression-exp.-toLong)`

Converts value to a long.

`[$toObject](/docs/manual/reference/operator/aggregation/toObject/#mongodb-expression-exp.-toObject)`

Converts a string to an object.

`[$toObjectId](/docs/manual/reference/operator/aggregation/toObjectId/#mongodb-expression-exp.-toObjectId)`

Converts value to an ObjectId.

`[$toString](/docs/manual/reference/operator/aggregation/toString/#mongodb-expression-exp.-toString)`

Converts value to a string.

`[$type](/docs/manual/reference/operator/aggregation/type/#mongodb-expression-exp.-type)`

Return the BSON data type of the field.

`[$toUUID](/docs/manual/reference/operator/aggregation/toUUID/#mongodb-expression-exp.-toUUID)`

Converts a string to a UUID .

## Variable Operators

Name

Description

`[$let](/docs/manual/reference/operator/aggregation/let/#mongodb-expression-exp.-let)`

Defines variables for use within the scope of a subexpression and returns the result of the subexpression. Accepts named parameters.

Accepts any number of argument expressions.

## Vector Similarity Operators

Name

Description

`[$similarityCosine](/docs/manual/reference/operator/aggregation/similarityCosine/#mongodb-expression-exp.-similarityCosine)`

Returns the cosine similarity between two numeric vectors. Accepts an optional `score `parameter to return a normalized score in the range `[0, 1] `.

`[$similarityDotProduct](/docs/manual/reference/operator/aggregation/similarityDotProduct/#mongodb-expression-exp.-similarityDotProduct)`

Returns the dot product of two numeric vectors. Accepts an optional `score `parameter to return a normalized score.

`[$similarityEuclidean](/docs/manual/reference/operator/aggregation/similarityEuclidean/#mongodb-expression-exp.-similarityEuclidean)`

Returns the Euclidean distance between two numeric vectors. Accepts an optional `score `parameter to return a normalized score in the range `(0, 1] `.

## Window Operators

Window operators return values from a defined span of documents from a collection, known as a window . A [window](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)is defined in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage, available starting in MongoDB 5.0.

The following window operators are available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

Name

Description

`[$addToSet](/docs/manual/reference/operator/aggregation/addToSet/#mongodb-group-grp.-addToSet)`

Returns an array of all unique values that results from applying an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$avg](/docs/manual/reference/operator/aggregation/avg/#mongodb-group-grp.-avg)`

Returns the average for the specified [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions). Ignores non-numeric values.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$bottom](/docs/manual/reference/operator/aggregation/bottom/#mongodb-group-grp.-bottom)`

Returns the bottom element within a group according to the specified sort order.

New in version 5.2 .

Available in the `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`and `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stages.

`[$bottomN](/docs/manual/reference/operator/aggregation/bottomN/#mongodb-group-grp.-bottomN)`

Returns an aggregation of the bottom `n `fields within a group, according to the specified sort order.

New in version 5.2 .

Available in the `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`and `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stages.

`[$count](/docs/manual/reference/operator/aggregation/count-accumulator/#mongodb-group-grp.-count)`

Returns the number of documents in the group or window.

Distinct from the `[$count](/docs/manual/reference/operator/aggregation/count/#mongodb-pipeline-pipe.-count)`pipeline stage.

New in version 5.0 .

`[$covariancePop](/docs/manual/reference/operator/aggregation/covariancePop/#mongodb-group-grp.-covariancePop)`

Returns the population covariance of two numeric [expressions](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)[.](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)

New in version 5.0 .

`[$covarianceSamp](/docs/manual/reference/operator/aggregation/covarianceSamp/#mongodb-group-grp.-covarianceSamp)`

Returns the sample covariance of two numeric [expressions](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)[.](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)

New in version 5.0 .

`[$denseRank](/docs/manual/reference/operator/aggregation/denseRank/#mongodb-group-grp.-denseRank)`

Returns the document position (known as the rank) relative to other documents in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage [partition](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-partitionBy). There are no gaps in the ranks. Ties receive the same rank.

New in version 5.0 .

`[$derivative](/docs/manual/reference/operator/aggregation/derivative/#mongodb-group-grp.-derivative)`

Returns the average rate of change within the specified [window](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)[.](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)

New in version 5.0 .

`[$documentNumber](/docs/manual/reference/operator/aggregation/documentNumber/#mongodb-group-grp.-documentNumber)`

Returns the position of a document (known as the document number) in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage [partition](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-partitionBy). Ties result in different adjacent document numbers.

New in version 5.0 .

`[$expMovingAvg](/docs/manual/reference/operator/aggregation/expMovingAvg/#mongodb-group-grp.-expMovingAvg)`

Returns the exponential moving average for the numeric [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)[.](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)

New in version 5.0 .

`[$first](/docs/manual/reference/operator/aggregation/first/#mongodb-group-grp.-first)`

Returns the result of an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)for the first document in a group or [window](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)[.](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$integral](/docs/manual/reference/operator/aggregation/integral/#mongodb-group-grp.-integral)`

Returns the approximation of the area under a curve.

New in version 5.0 .

`[$last](/docs/manual/reference/operator/aggregation/last/#mongodb-group-grp.-last)`

Returns the result of an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)for the last document in a group or [window](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)[.](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$linearFill](/docs/manual/reference/operator/aggregation/linearFill/#mongodb-group-grp.-linearFill)`

Fills `null `and missing fields in a [window](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)using [linear interpolation](https://en.wikipedia.org/wiki/Linear_interpolation)based on surrounding field values.

Available in `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`[.](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)

New in version 5.3 .

`[$locf](/docs/manual/reference/operator/aggregation/locf/#mongodb-group-grp.-locf)`

Last observation carried forward. Sets values for `null `and missing fields in a [window](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-window)to the last non-null value for the field.

Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

New in version 5.2 .

`[$max](/docs/manual/reference/operator/aggregation/max/#mongodb-group-grp.-max)`

Returns the maximum value that results from applying an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$min](/docs/manual/reference/operator/aggregation/min/#mongodb-group-grp.-min)`

Returns the minimum value that results from applying an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$minMaxScaler](/docs/manual/reference/operator/aggregation/minMaxScaler/#mongodb-group-grp.-minMaxScaler)`

Scales the value that results from applying an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

New in version 8.2 .

`[$minN](/docs/manual/reference/operator/aggregation/minN/#mongodb-group-grp.-minN)`

Returns an aggregation of the `n `minimum valued elements in a group. Distinct from the `[$minN](/docs/manual/reference/operator/aggregation/minN-array-element/#mongodb-expression-exp.-minN)`array operator.

New in version 5.2 .

Available in `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`, `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`and as an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)[.](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)

`[$push](/docs/manual/reference/operator/aggregation/push/#mongodb-group-grp.-push)`

Returns an array of values that result from applying an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$rank](/docs/manual/reference/operator/aggregation/rank/#mongodb-group-grp.-rank)`

Returns the document position (known as the rank) relative to other documents in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage [partition](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-partitionBy)[.](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-partitionBy)

New in version 5.0 .

`[$shift](/docs/manual/reference/operator/aggregation/shift/#mongodb-group-grp.-shift)`

Returns the value from an [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)applied to a document in a specified position relative to the current document in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage [partition](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-partitionBy)[.](/docs/manual/reference/operator/aggregation/setWindowFields/#std-label-setWindowFields-partitionBy)

New in version 5.0 .

`[$stdDevPop](/docs/manual/reference/operator/aggregation/stdDevPop/#mongodb-group-grp.-stdDevPop)`

Returns the population standard deviation that results from applying a numeric [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$stdDevSamp](/docs/manual/reference/operator/aggregation/stdDevSamp/#mongodb-group-grp.-stdDevSamp)`

Returns the sample standard deviation that results from applying a numeric [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$sum](/docs/manual/reference/operator/aggregation/sum/#mongodb-group-grp.-sum)`

Returns the sum that results from applying a numeric [expression](/docs/manual/reference/mql/expressions/#std-label-aggregation-expressions)to each document.

Changed in version 5.0 : Available in the `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stage.

`[$top](/docs/manual/reference/operator/aggregation/top/#mongodb-group-grp.-top)`

Returns the top element within a group according to the specified sort order.

New in version 5.2 .

Available in the `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`and `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stages.

`[$topN](/docs/manual/reference/operator/aggregation/topN/#mongodb-group-grp.-topN)`

Returns an aggregation of the top `n `fields within a group, according to the specified sort order.

New in version 5.2 .

Available in the `[$group](/docs/manual/reference/operator/aggregation/group/#mongodb-pipeline-pipe.-group)`and `[$setWindowFields](/docs/manual/reference/operator/aggregation/setWindowFields/#mongodb-pipeline-pipe.-setWindowFields)`stages.

[Back](/docs/manual/reference/operator/query/where/)

[$where](/docs/manual/reference/operator/query/where/)

[Next](/docs/manual/reference/operator/aggregation/abs/)

[$abs](/docs/manual/reference/operator/aggregation/abs/)

Rate this page

On this page

- [Arithmetic Operators](#arithmetic-operators)

- [Array Operators](#array-operators)

- [Bitwise Operators](#bitwise-operators)

- [Boolean Operators](#boolean-operators)

- [Comparison Operators](#comparison-operators)

- [Conditional Operators](#conditional-operators)

- [Custom Aggregation Operators](#custom-aggregation-operators)

- [Data Size Operators](#data-size-operators)

- [Date Operators](#date-operators)

- [Expressions Associated with Accumulators](#expressions-associated-with-accumulators)

- [Literal Expression Operators](#literal-expression-operators)

- [Miscellaneous Operators](#miscellaneous-operators)

- [Object Operators](#object-operators)

- [Set Operators](#set-operators)

- [String Operators](#string-operators)

- [Text Operators](#text-operators)

- [Timestamp Operators](#timestamp-operators)

- [Trigonometry Operators](#trigonometry-operators)

- [Type Operators](#type-operators)

- [Variable Operators](#variable-operators)

- [Vector Similarity Operators](#vector-similarity-operators)

- [Window Operators](#window-operators)

On this page

- [Arithmetic Operators](#arithmetic-operators)

- [Array Operators](#array-operators)

- [Bitwise Operators](#bitwise-operators)

- [Boolean Operators](#boolean-operators)

- [Comparison Operators](#comparison-operators)

- [Conditional Operators](#conditional-operators)

- [Custom Aggregation Operators](#custom-aggregation-operators)

- [Data Size Operators](#data-size-operators)

- [Date Operators](#date-operators)

- [Expressions Associated with Accumulators](#expressions-associated-with-accumulators)

- [Literal Expression Operators](#literal-expression-operators)

- [Miscellaneous Operators](#miscellaneous-operators)

- [Object Operators](#object-operators)

- [Set Operators](#set-operators)

- [String Operators](#string-operators)

- [Text Operators](#text-operators)

- [Timestamp Operators](#timestamp-operators)

- [Trigonometry Operators](#trigonometry-operators)

- [Type Operators](#type-operators)

- [Variable Operators](#variable-operators)

- [Vector Similarity Operators](#vector-similarity-operators)

- [Window Operators](#window-operators)
