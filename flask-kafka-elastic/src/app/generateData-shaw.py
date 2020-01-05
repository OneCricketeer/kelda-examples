#!/usr/bin/env python

from __future__ import print_function
import json
import math
import random
import sys
import time
from datetime import datetime, timedelta


class Warehouse:
    def __init__(self, _id, loc):
        self.id = _id
        self.loc = loc


class Product:
    def __init__(self, sellstyle, unitcost, quantity=1, popularity=None):
        """
        popularity: A list of tuples ( start_hour, end_hour, multiplier, {storeIds..} )
                Default: All day, no multiplier, all stores
        """
        if popularity is None:
            popularity = [(0, 23, 1, None)]
        self.sellstyle = sellstyle
        self.cost = unitcost * quantity
        self.popularity = popularity


products = [
    Product('THUNDRSTRUKRR12', 5.22, 1),
    Product('MAGICATLST 3(12', 19.80, 18),
    Product('VICTORIOUS DELI', 4.19, 2),
    Product('IN THE LOOP', 16.20, 30, popularity=[(17, 20, 20, {'Plant 71', 'Plant 98'}), (0, 23, 1, None)]),
    Product('T-MOLDING LVT', 13.77, 5),
    Product('RUBY 7/16 20', 1.88, 20, popularity=[(0, 23, 1, {'Plant 1', 'Plant 3'})]),
    Product('PACIFIC RIDGE', 17.55, 45),
    Product('PREMIUM TWST AC', 16.74, 35),
    Product('PREMIUMTXTACCNT', 16.74, 16, popularity=[(0, 23, 5, None)]),
    Product('LUCKY ROLL', 17.91, 17, popularity=[(2, 8, 1, {'Plant 2'}), (14, 18, 2, None)])
]

warehouses = [
    Warehouse('Plant 1', [-84.960318, 34.763608]),
    Warehouse('Plant 2', [-84.966608, 34.723846]),
    Warehouse('Plant 3', [-84.962569, 34.762944]),
    Warehouse('Plant 27', [-84.946799, 34.760733]),
    Warehouse('Plant 61', [-84.959132, 34.760661]),
    Warehouse('Plant 68', [-84.965390, 34.768552]),
    Warehouse('Plant 71', [-84.958678, 34.758070]),
    Warehouse('Plant 98', [-84.954429, 34.759460])
]


def randomTime(day_offset, time):
    hour = int(math.floor(time))
    minute = int(round((time - hour) * 60))
    return day_offset, hour, minute

def chooseProduct(hour, product_id):
    global products
    tmp_products = []
    for p in products:
        for (start_hour, end_hour, popularity_multiplier, _id) in p.popularity:
            if start_hour <= hour <= end_hour and (_id is None or product_id in _id):
                for _ in range(popularity_multiplier):
                    tmp_products.append(p)

    return random.choice(tmp_products)


date_fmt = '%Y-%m-%dT%H:%M:%SZ'


def formatHrMin(day, hour, minute):
    dt = datetime.now()
    dt = dt + timedelta(days=day)
    dt = dt.replace(hour=hour % 24, minute=minute % 60, second=0)
    return dt.strftime(date_fmt)


def makeEntry(timestamp, data_format="json"):
    global warehouses
    warehouse = random.choice(warehouses)
    city = "Dalton, GA" # all Shaw warehouses are in Georgia
    date = datetime.strptime(timestamp, date_fmt)
    utc_date = date - timedelta(hours=-5)
    chosen_product = chooseProduct(date.hour, warehouse.id)

    # https://www.elastic.co/guide/en/elasticsearch/reference/current/geo-point.html
    geopoint = ",".join(map(str, warehouse.loc[::-1]))

    if data_format == "json":
        data = {
            'event_time': 1000*int(utc_date.timestamp()), # utc_date.strftime(date_fmt),
            'warehouseId': warehouse.id,
            'city': city,
            'location': geopoint,
            'product': chosen_product.sellstyle,
            'cost': float(round(chosen_product.cost, 2))
        }

        return json.dumps(data)
    elif data_format == "csv":
        return "|".join(
            map(str, [utc_date.strftime(date_fmt), warehouse.id, city, warehouse.loc[0], warehouse.loc[1],
                      chosen_product.sellstyle, chosen_product.cost]))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Wrong number of arguments")
        print("Usage: ", __file__, "n [json|csv]")
        sys.exit(1)
    num = int(sys.argv[1])
    data_format = "json"  # default to JSON
    if len(sys.argv) == 3:
        data_format = sys.argv[2]
        if data_format == "csv":
            print("|".join(
                ["timestamp", "warehouse_id", "warehouse_city", "warehouse_loc_lat", "warehouse_loc_long",
                 "product_name", "product_cost"]))
    # (peak_hour,multiplier,stddev)
    peaks = [(2, 0.25, 1), (7, 1, 1), (12, 4, 2), (18, 3, 2)]
    # last 3 days from now
    for day in range(-2, 1):
        for (peak, factor, stddev) in peaks:
            for x in range(int(num * factor * stddev)):
                entry_time = formatHrMin(*randomTime(day, random.gauss(peak, stddev)))
                print(makeEntry(entry_time, data_format))
