# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from collections import namedtuple
from django.core.management.base import BaseCommand, CommandError
from park_benches.models import ParkA, ParkB, ParkC, BenchA, BenchB, BenchC

ParkData = namedtuple("ParkData", ["name", "benches"])
BenchData = namedtuple("BenchData", ["latitude", "longitude"])


def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple("Result", [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


class Command(BaseCommand):
    help = "Creates some parks and benches in those parks and does some database queries on them. Measures the performance and size of the data."

    def handle(self, *args, **options):
        from timeit import default_timer as timer

        self._cleanup_database()

        parks = self._load_data()

        start = timer()
        self._create_new_parks(parks=parks, park_model=ParkA, bench_model=BenchA)
        end = timer()
        delta_a = end - start
        self.stdout.write("Creation took {} seconds for {}".format(delta_a, ParkA._meta.verbose_name_plural))

        start = timer()
        self._create_new_parks(parks=parks, park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write("Creation took {} seconds for {}".format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._create_new_parks(parks=parks, park_model=ParkC, bench_model=BenchC)
        end = timer()
        delta_c = end - start
        self.stdout.write("Creation took {} seconds for {}".format(delta_c, ParkC._meta.verbose_name_plural))

        start = timer()
        self._select_parks(park_model=ParkA, bench_model=BenchA)
        end = timer()
        delta_a = end - start
        self.stdout.write("Selecting by ID took {} seconds for {}".format(delta_a, ParkA._meta.verbose_name_plural))

        start = timer()
        self._select_parks(park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write("Selecting by ID took {} seconds for {}".format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._select_parks_with_encoding(park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write("Selecting by ID with base58 encoding/decoding to string took {} seconds for {}".format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._select_parks(park_model=ParkC, bench_model=BenchC)
        end = timer()
        delta_c = end - start
        self.stdout.write("Selecting by ID took {} seconds for {}".format(delta_c, ParkC._meta.verbose_name_plural))

        start = timer()
        self._filter_benches(park_model=ParkA, bench_model=BenchA)
        end = timer()
        delta_a = end - start
        self.stdout.write("Filtering by joined table field took {} seconds for {}".format(delta_a, ParkA._meta.verbose_name_plural))

        start = timer()
        self._filter_benches(park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write("Filtering by joined table field took {} seconds for {}".format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._filter_benches(park_model=ParkC, bench_model=BenchC)
        end = timer()
        delta_c = end - start
        self.stdout.write("Filtering by joined table field took {} seconds for {}".format(delta_c, ParkC._meta.verbose_name_plural))

        self._check_table_sizes()

        self.stdout.write(self.style.SUCCESS("Successfully finished"))

    def _create_new_parks(self, parks, park_model, bench_model):
        for park_data in parks:
            park = park_model()
            park.name = park_data.name
            park.save()
            for bench_data in park_data.benches:
                bench = bench_model()
                bench.park = park
                bench.latitude = bench_data.latitude
                bench.longitude = bench_data.longitude
                bench.save()

    def _select_parks(self, park_model, bench_model):
        # testing selects by ids
        for park in bench_model.objects.all():
            park_reloaded = bench_model.objects.get(pk=park.pk)

    def _select_parks_with_encoding(self, park_model, bench_model):
        # testing selects by ids also encoding and decoding to base58
        import uuid
        from park_benches.base58 import b58encode, b58decode
        # base58 is like base64, but the following similar-looking letters are omitted:
        # 0 (zero), O (capital o), I (capital i) and l (lower case L) as well as the non-alphanumeric characters + (plus) and / (slash).
        for park in bench_model.objects.all():
            # The encoded_id like "EnEZfZ79Dk7UPbyntGeU8U" will be used in URLs and APIs
            encoded_id = b58encode(park.pk.bytes)
            decoded_bytes = b58decode(encoded_id)
            # prefix decoded bytes with zeroth byte character if it is shorter than 16 (otherwise the UUID creation fails)
            decoded_bytes = b'\x00' * (16 - len(decoded_bytes)) + decoded_bytes
            id = uuid.UUID(bytes=decoded_bytes)
            park_reloaded = bench_model.objects.get(pk=id)

    def _filter_benches(self, park_model, bench_model):
        # testing joins
        # we are interested in comparison instead of the lenght of single operations,
        # so let"s execute the selection multiple times
        for index in range(300):
            for bench in bench_model.objects.filter(park__name__contains="park"):
                pass

    def _cleanup_database(self):
        # Delete the parks - the benches will be deleted automatically as they will be cascaded.
        ParkA.objects.all().delete()
        ParkB.objects.all().delete()
        ParkC.objects.all().delete()

    def _load_data(self):
        import csv
        parks = []
        with open("data/parks.csv", "r") as f:
            reader = csv.reader(f)
            for row in reader:
                benches = []
                for index in range(int(row[1])):
                    benches.append(self._generate_bench_geoposition())
                park_data = ParkData(row[0], benches)
                parks.append(park_data)
        return parks

    def _generate_bench_geoposition(self):
        import random
        import math

        radius = 10000  # Choose your own radius
        radiusInDegrees = radius / 111300
        r = radiusInDegrees

        # New York"s geoposition
        x0 = 40.84
        y0 = -73.87

        u = float(random.uniform(0.0, 1.0))
        v = float(random.uniform(0.0, 1.0))

        w = r * math.sqrt(u)
        t = 2 * math.pi * v
        x = w * math.cos(t)
        y = w * math.sin(t)

        latitude = x + x0
        longitude = y + y0

        return BenchData(latitude, longitude)

    def _check_table_sizes(self):
        """
        checks the database table sizes
        """
        import pandas as pd  # we'll use pandas for nice table representation
        from django.db import connection
        from ...models import ParkA, ParkB, ParkC, BenchA, BenchB, BenchC
        TABLE_NAME_TO_MODEL_VERBOSE_NAME = dict((
            (model._meta.db_table, model._meta.verbose_name)
            for model in (ParkA, ParkB, ParkC, BenchA, BenchB, BenchC)
        ))

        with connection.cursor() as cursor:
            cursor.execute("""SELECT
                relname AS "table",
                pg_size_pretty(pg_total_relation_size(relid)) AS "size",
                pg_size_pretty(pg_total_relation_size(relid) - pg_relation_size(relid)) AS "external_size"
                FROM pg_catalog.pg_statio_user_tables ORDER BY pg_total_relation_size(relid) DESC""")
            results = namedtuplefetchall(cursor)

            self.stdout.write("Database table sizes:")

            index = []
            data = []
            for result in results:
                if result.table in TABLE_NAME_TO_MODEL_VERBOSE_NAME:
                    index.append(TABLE_NAME_TO_MODEL_VERBOSE_NAME[result.table])
                    data.append([
                        result.size,  # The total size that this table takes
                        result.external_size,  # The size that related objects of this table like indices take
                    ])
            data_frame = pd.DataFrame(data, columns=["Table Size", "External Size"], index=index)
            self.stdout.write(str(data_frame))
