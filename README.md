# Primary Keys Benchmark for Django Projects

## Problem

Default primary keys reveal the number of available objects in the database. Also they allow to easily guess the previous and next created objects when the ID is used in the URL.

Sometimes that might be not the wanted behaviour.

Instead of the default numeric incremental ID, it is possible to use [UUIDField](https://docs.djangoproject.com/en/1.11/ref/models/fields/#uuidfield) or [CharField](https://docs.djangoproject.com/en/1.11/ref/models/fields/#charfield) for the primary key. But which one should we use in our projects?

## What is this project about?

This experimental will measure how fast various database operations take, when we use different types of primary keys.

Let's say, that there is a list of parks each of them having some amount of benches to take a rest on a sunny day. We will implement that with `Park` model and `Bench` model with a foreign key to the `Park` model. For our benchmark tests, we'll create three types of `Park` and `Bench` models: 

- `ParkA` and `BenchA` models will use the usual __numeric incremental IDs__,
- `ParkB` and `BenchB` models will use __UUID-based IDs__,
- `ParkC` and `BenchC` models will use __random character string IDs__.

We expect the IDs of __UUID-base IDs__ to be unique because of UUID format. It is long enough not to clash: 32 hexadecimal characters plus 4 hyphens. To generate it, different bits of the current timestamp and 12 random hex digits are used. When used in URLs and APIs, the UUID will be base58-encoded and its length will be 22 characters. The base58 encoding is like base64, but the following similar-looking characters are omitted: 0 (zero), O (capital o), I (capital i) and l (lower case L) as well as the non-alphanumeric characters + (plus) and / (slash).

To ensure that a __random-string ID__ is unique, we will recreate it until it doesn't clash with existing IDs in the database. That is for each creation we will do at least one check in the database to make sure that the ID doesn't exist yet. The ID length used in our tests will be 10-12 characters.

We'll be measuring the speed of creation, selection by ID, and filtering by a joined table for each type. Also we will check the differences of the size of each database table.

## Usage

We will use PostgreSQL database. The database name and user name will be "primary\_keys\_benchmark" and the password will be empty:

    $ createuser -d primary_keys_benchmark
    $ createdb -U primary_keys_benchmark primary_keys_benchmark

After creating the database, run:

    $ python manage.py makemigrations
    $ python manage.py migrate

To measure database operations, run:

    $ python manage.py benchmark

## Results

I ran the benchmark tests on my machine using Django 1.11, Python 3.6.0, PostgreSQL 9.5.1, and Mac OS X 10.12.3.

When the length of random string ID was 12 characters, 
the benchmark results were similar to these:

    Creation took 2.1891210739995586 seconds for Parks (numeric id)
    Creation took 4.680127620995336 seconds for Parks (uuid)
    Creation took 6.887378665996948 seconds for Parks (random varchar id)
    Selecting by ID took 2.0820247679948807 seconds for Parks (numeric id)
    Selecting by ID took 2.1918821449944517 seconds for Parks (uuid)
    Selecting by ID with base58 encoding/decoding to string took 2.4209505320031894 seconds for Parks (uuid)
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
    Selecting by ID with base58 encoding/decoding to string took 2.4234983259957517 seconds for Parks (uuid)
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
    Selecting by ID with base58 encoding/decoding to string took 2.5266951320008957 seconds for Parks (uuid)
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

So __UUID__ wins against random character string IDs in __write-heavy situations__ where you also need to __save disk space__.

__Random character string IDs__ win against UUID when __speedy performance__ is necessary and its __representation in URL and APIs should be much shorter__.