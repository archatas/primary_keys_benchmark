# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from collections import namedtuple
from django.core.management.base import BaseCommand, CommandError
from park_benches.models import ParkA, ParkB, ParkC, BenchA, BenchB, BenchC

ParkData = namedtuple('ParkData', ['name', 'benches'])
BenchData = namedtuple('BenchData', ['latitude', 'longitude'])

class Command(BaseCommand):
    help = 'Creates some parks and benches in those parks and does some database queries on them. Measures the performance.'

    def handle(self, *args, **options):
        from timeit import default_timer as timer

        self._cleanup_database()

        parks = self._load_data()

        start = timer()
        self._create_new_parks(parks=parks, park_model=ParkA, bench_model=BenchA)
        end = timer()
        delta_a = end - start
        self.stdout.write('Creation took {} seconds for {}'.format(delta_a, ParkA._meta.verbose_name_plural))

        start = timer()
        self._create_new_parks(parks=parks, park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write('Creation took {} seconds for {}'.format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._create_new_parks(parks=parks, park_model=ParkC, bench_model=BenchC)
        end = timer()
        delta_c = end - start
        self.stdout.write('Creation took {} seconds for {}'.format(delta_c, ParkC._meta.verbose_name_plural))

        start = timer()
        self._select_parks(park_model=ParkA, bench_model=BenchA)
        end = timer()
        delta_a = end - start
        self.stdout.write('Selecting took {} seconds for {}'.format(delta_a, ParkA._meta.verbose_name_plural))

        start = timer()
        self._select_parks(park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write('Selecting took {} seconds for {}'.format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._select_parks(park_model=ParkC, bench_model=BenchC)
        end = timer()
        delta_c = end - start
        self.stdout.write('Selecting took {} seconds for {}'.format(delta_c, ParkC._meta.verbose_name_plural))

        start = timer()
        self._filter_benches(park_model=ParkA, bench_model=BenchA)
        end = timer()
        delta_a = end - start
        self.stdout.write('Filtering took {} seconds for {}'.format(delta_a, ParkA._meta.verbose_name_plural))

        start = timer()
        self._filter_benches(park_model=ParkB, bench_model=BenchB)
        end = timer()
        delta_b = end - start
        self.stdout.write('Filtering took {} seconds for {}'.format(delta_b, ParkB._meta.verbose_name_plural))

        start = timer()
        self._filter_benches(park_model=ParkC, bench_model=BenchC)
        end = timer()
        delta_c = end - start
        self.stdout.write('Filtering took {} seconds for {}'.format(delta_c, ParkC._meta.verbose_name_plural))

        self.stdout.write(self.style.SUCCESS('Successfully finished'))

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

    def _filter_benches(self, park_model, bench_model):
        # testing joins
        # we are interested in comparison instead of the lenght of single operations,
        # so let's execute the selection multiple times
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
        with open('data/parks.csv', 'r') as f:
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

        radius = 10000 # Choose your own radius
        radiusInDegrees=radius/111300
        r = radiusInDegrees

        # New York's geoposition
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