# Primary Keys Benchmark for Django Projects

This test project is measuring operations on the database for objects with different types of primary keys:

- The usual numeric incremental IDs,
- UUID based IDs,
- Random string IDs.

The project is expected to use PostgreSQL with database name and user name "primary_keys_benchmark" and empty password.

After creating the database, run:

    $ python manage.py migrate

To measure database operations, run:

    $ python manage.py benchmark

You will get results similar to these:

    Creation took 2.198154069003067 seconds for Parks (numeric id)
    Creation took 4.66604501799884 seconds for Parks (uuid)
    Creation took 7.108440816999064 seconds for Parks (random varchar id)
    Selecting took 2.0815744189967518 seconds for Parks (numeric id)
    Selecting took 2.225840673003404 seconds for Parks (uuid)
    Selecting took 2.207754114999261 seconds for Parks (random varchar id)
    Filtering took 0.36789353100175504 seconds for Parks (numeric id)
    Filtering took 0.39389091300108703 seconds for Parks (uuid)
    Filtering took 0.4649452739977278 seconds for Parks (random varchar id)
