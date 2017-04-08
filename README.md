# Primary Keys Benchmark for Django Projects

This test project is measuring operations on the database for objects with different types of primary keys:

- The usual numeric incremental IDs,
- UUID based IDs (will be base58-encoded when used in URLs and APIs, the encoded length is 22 characters),
- Random string IDs (the length used here is 12 characters).

The project is expected to use PostgreSQL with database name and user name "primary_keys_benchmark" and empty password.

After creating the database, run:

    $ python manage.py migrate

To measure database operations, run:

    $ python manage.py benchmark

You will get results similar to these:

    Creation took 2.210341456004244 seconds for Parks (numeric id)
    Creation took 4.7278332540008705 seconds for Parks (uuid)
    Creation took 6.953359108003497 seconds for Parks (random varchar id)
    Selecting by ID took 2.0833924129983643 seconds for Parks (numeric id)
    Selecting by ID took 2.190063251000538 seconds for Parks (uuid)
    Selecting by ID with encoding/decoding to string took 2.4132918830000563 seconds for Parks (uuid)
    Selecting by ID took 2.151222598993627 seconds for Parks (random varchar id)
    Filtering by joined table field took 0.3518987499992363 seconds for Parks (numeric id)
    Filtering by joined table field took 0.3622393940022448 seconds for Parks (uuid)
    Filtering by joined table field took 0.4803413140034536 seconds for Parks (random varchar id)
    Database table sizes:
                              Table Size External Size
    Bench (random varchar id)    2648 kB       2424 kB
    Bench (uuid)                 1144 kB        864 kB
    Bench (numeric id)            992 kB        640 kB
    Park (random varchar id)      200 kB        184 kB
    Park (numeric id)             120 kB         96 kB
    Park (uuid)                    96 kB         80 kB
    Successfully finished