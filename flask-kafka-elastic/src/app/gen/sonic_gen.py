#!/usr/bin/env python

from __future__ import print_function
import json
import math
import random
import sys
from datetime import datetime, timedelta


class Store():
    def __init__(self, _id, city, utc, loc):
        self.id = _id
        self.city = city
        self.utc = utc
        self.loc = loc


class Food():
    def __init__(self, name, cost, popularity=[(0, 23, 1, None)]):
        '''
        popularity: A list of tuples ( start_hour, end_hour, multiplier, {storeIds..} )
                    Default: All day, no multiplier, all stores
        '''
        self.name = name
        self.cost = cost
        self.popularity = popularity


menu = [
    Food('Water', 0.00),
    Food('COCA-COLA', 1.69),
    Food('Blue Raspberry with Rainbox Candy', 2.59),
    Food('Super Crunch Chicken Strip Dinner', 6.09,
         popularity=[(17, 20, 20, None), (0, 23, 1, None)]),
    Food('SONIC Bacon Cheeseburger', 4.59),
    Food('Bacon Cheeseburger TOASTER', 5.79,
         popularity=[(0, 23, 1, {'atx1', 'atx2'})]),
    Food('Jr. Burger', 3.24),
    Food('Chili Cheese Lil Doggie', 5.09),
    Food('All-American Dog', 3.78, popularity=[(0, 23, 5, None)]),
    Food('SuperSONIC Breakfast Burrito', 2.78, popularity=[
         (2, 8, 1, {'ny'}), (14, 18, 2, None)])
]

stores = [
    Store('atx1', 'Austin, TX', -6, [-97.779086, 30.245228]),
    Store('atx2', 'Austin, TX', -6, [-97.651026, 30.387784]),
    Store('seatac', 'Tacoma, WA', -8, [-122.506592, 47.254914]),
    Store('ny', 'North Babylon, NY', -5, [-73.322771, 40.743618]),
    Store('jersey', 'North Bergen, NJ', -5, [-74.037901, 40.774098]),
    Store('chicago', 'Cicero, IL', -6, [-87.744277, 41.839248]),
    Store('dallas', 'Dallas, TX', -6, [-96.831787, 32.825900])
]


def randomTime(day_offset, x):
    hour = int(math.floor(x))
    minute = int(round((x - hour) * 60))
    return (day_offset, hour, minute)


def chooseFood(hour, store_id):
    tmp_menu = []
    for f in menu:
        for (s, e, p, sid) in f.popularity:
            if s <= hour <= e and (sid is None or store_id in sid):
                for i in range(p):
                    tmp_menu.append(f)

    return random.choice(tmp_menu)


def formatHrMin(day, hour, minute, date_fmt='%Y-%m-%dT%H:%M:%SZ'):
    dt = datetime.now()
    dt = dt + timedelta(days=day)
    dt = dt.replace(hour=hour % 24, minute=minute % 60, second=0)
    return dt.strftime(date_fmt)


def makeEntry(timestamp, data_format="json", date_fmt='%Y-%m-%dT%H:%M:%SZ'):
    store = random.choice(stores)
    date = datetime.strptime(timestamp, date_fmt)
    utc_date = date - timedelta(hours=store.utc)
    menu_item = chooseFood(date.hour, store.id)

    if data_format == "json":
        data = {
            'event_time': utc_date.strftime(date_fmt),
            'storeId': store.id,
            'city': store.city,
            'geoip': {'location': store.loc},
            'food': menu_item.name,
            'cost': menu_item.cost
        }

        return json.dumps(data)
    elif data_format == "csv":
        return "|".join(map(str, [
          utc_date.strftime(date_fmt), 
          store.id, 
          store.city, 
          store.loc[0], store.loc[1], 
          menu_item.name, 
          menu_item.cost]))


def generate(num, peaks, day_range=range(-2, 1), data_format='json'):
    '''
    num: Some multiplier to get more data
    peaks: List of tuples for (peak_hour,multiplier,stddev)
    day_range: (iterable) decides how many days to generate data against
    data_format: [json|csv] Format to create the records in
    '''
    if data_format == "csv":
        print("|".join(["timestamp", "store_id", "store_city",
                        "store_loc_lat", "store_loc_long", "item_name", "item_cost"]))

    for day in day_range:
        for (peak, factor, stddev) in peaks:
            for x in range(int(num * factor * stddev)):
                entry_time = formatHrMin(
                    *randomTime(day, random.gauss(peak, stddev)))
                entry = makeEntry(entry_time, data_format)
                yield entry


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Wrong number of arguments")
        print("Usage: ", __file__, "n [json|csv]")
        sys.exit(1)
    num = int(sys.argv[1])
    data_format = "json"  # default to JSON
    if len(sys.argv) == 3:
        data_format = sys.argv[2]
    # (peak_hour,multiplier,stddev)
    peaks = [(2, 0.25, 1), (7, 1, 1), (12, 4, 2), (18, 3, 2)]
    for entry in generate(num, peaks, data_format=data_format):
        print(entry)