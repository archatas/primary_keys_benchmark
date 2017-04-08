# Primary Keys Benchmark for Django Projects

## Problem

Default primary keys reveal the count of available objects in the database and allow to easily guess the previous and next created objects when the id is used in the URL.

Sometimes that might be not the wanted behavior.

It is possible instead of the default numeric incremental id to use UUIDField or CharField for the primary key.

## What is this project about?

This test project is measuring operations on the database for objects with different types of primary keys:

- The usual numeric incremental IDs,
- UUID based IDs (will be base58-encoded when used in URLs and APIs, the encoded length is 22 characters),
- Random string IDs (the length used here is 10-12 characters).

To test the performance speeds and database sizes, in this project we create a list of parks each of them having some amount of benches.

We will have three types of park and bench models:

- Type A will be using the numeric IDs.
- Type B will be using UUID (uniqueness is expected from the uuid algorithm).
- Type C will be using random-string IDs (the IDs are recreated until they are unique).

We'll be measuring the speed of creation, selection by ID, and filtering by a joined table for each type.
Also we will check the differences of the size of each database table.

## Usage

The project is expected to use PostgreSQL with database name and user name "primary\_keys\_benchmark" and empty password:

    $ createuser -d primary_keys_benchmark
    $ createdb -U primary_keys_benchmark primary_keys_benchmark

After creating the database, run:

    $ python manage.py makemigrations
    $ python manage.py migrate

To measure database operations, run:

    $ python manage.py benchmark

## Results

The benchmark tests were using Django 1.11 on Python 3.6, Mac OS X 10.12.3.

When the length of random string ID was 12 characters, 
the benchmark results were similar to these:

    Creation took 2.1891210739995586 seconds for Parks (numeric id)
    Creation took 4.680127620995336 seconds for Parks (uuid)
    Creation took 6.887378665996948 seconds for Parks (random varchar id)
    Selecting by ID took 2.0820247679948807 seconds for Parks (numeric id)
    Selecting by ID took 2.1918821449944517 seconds for Parks (uuid)
    Selecting by ID with encoding/decoding to string took 2.4209505320031894 seconds for Parks (uuid)
    Selecting by ID took 2.143886667996412 seconds for Parks (random varchar id)
    Filtering by joined table field took 0.3137620009947568 seconds for Parks (numeric id)
    Filtering by joined table field took 0.34382708899647696 seconds for Parks (uuid)
    Filtering by joined table field took 0.3347244890028378 seconds for Parks (random varchar id)
    Database table sizes:
                              Table Size External Size
    Bench (random varchar id)     824 kB        600 kB
    Bench (uuid)                  536 kB        312 kB
    Bench (numeric id)            376 kB        200 kB
    Park (random varchar id)       72 kB         56 kB
    Park (numeric id)              56 kB         40 kB
    Park (uuid)                    56 kB         40 kB
    
When the length of random string ID was 11 characters (the same as currently used for YouTube video ids), 
the benchmark results were similar to these:

    Creation took 2.1721825860004174 seconds for Parks (numeric id)
    Creation took 4.663145505997818 seconds for Parks (uuid)
    Creation took 6.913711889996193 seconds for Parks (random varchar id)
    Selecting by ID took 2.082028558004822 seconds for Parks (numeric id)
    Selecting by ID took 2.173269920000166 seconds for Parks (uuid)
    Selecting by ID with encoding/decoding to string took 2.4234983259957517 seconds for Parks (uuid)
    Selecting by ID took 2.1411008150025737 seconds for Parks (random varchar id)
    Filtering by joined table field took 0.3147929100014153 seconds for Parks (numeric id)
    Filtering by joined table field took 0.3383102570005576 seconds for Parks (uuid)
    Filtering by joined table field took 0.3282908809997025 seconds for Parks (random varchar id)
    Database table sizes:
                              Table Size External Size
    Bench (random varchar id)     856 kB        632 kB
    Bench (uuid)                  544 kB        320 kB
    Bench (numeric id)            376 kB        200 kB
    Park (random varchar id)       72 kB         56 kB
    Park (numeric id)              56 kB         40 kB
    Park (uuid)                    56 kB         40 kB
    
When the length of random string ID was 10 characters, 
the benchmark results were similar to these:

    Creation took 2.180306248999841 seconds for Parks (numeric id)
    Creation took 4.664441665998311 seconds for Parks (uuid)
    Creation took 6.943970259002526 seconds for Parks (random varchar id)
    Selecting by ID took 2.095865210001648 seconds for Parks (numeric id)
    Selecting by ID took 2.205640936997952 seconds for Parks (uuid)
    Selecting by ID with encoding/decoding to string took 2.5266951320008957 seconds for Parks (uuid)
    Selecting by ID took 2.19395816699398 seconds for Parks (random varchar id)
    Filtering by joined table field took 0.3190960339998128 seconds for Parks (numeric id)
    Filtering by joined table field took 0.3501416959989001 seconds for Parks (uuid)
    Filtering by joined table field took 0.3337787409982411 seconds for Parks (random varchar id)
    Database table sizes:
                              Table Size External Size
    Bench (random varchar id)     824 kB        600 kB
    Bench (uuid)                  544 kB        320 kB
    Bench (numeric id)            376 kB        200 kB
    Park (random varchar id)       72 kB         56 kB
    Park (numeric id)              56 kB         40 kB
    Park (uuid)                    56 kB         40 kB

## Conclusion

- Creating random strings and double-checking the uniqueness of random strings is expensive.
- Varchar fields take much more space in the database than UUID fields.
- Selecting element by id is faster with random strings rather than with UUID fields.
- Joins are faster with random string fields than UUID fields.

So UUID wins against random string ids in write-heavy situations where you also need to save disk space.

Random string ids win against UUID when performance speed is necessary and the representation in URL and APIs should be much shorter.