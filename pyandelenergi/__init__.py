
from urllib.request import urlopen
from datetime import date, datetime, timedelta
from decimal import Decimal
import csv

def get_default_data():
    start_date = get_earliest_start_date()
    end_date = get_max_future_date()
    default_region = "east"
    url = build_url(default_region, start_date, end_date)
    return fetch_data(url)

def get_earliest_start_date():
    # today
    start_date = date.today()
    return start_date.strftime("%Y-%m-%d")

def get_max_future_date():
    future_date = date.today() + timedelta(days=2)
    return future_date.strftime("%Y-%m-%d")

def build_url(region, start_date, end_date):
    return f"https://andelenergi.dk/?obexport_format=csv&obexport_start={start_date}&obexport_end={end_date}&obexport_region={region}&obexport_tax=0&obexport_product_id=1%231%23TIMEENERGI"

def get_decimal(as_string):
    return Decimal(as_string.replace(",","."))

def fetch_data(url):
    # download csv
    with urlopen(url) as response:
        result = dict()
        body = response.read()
        decoded_content = body.decode('utf-8')
        # parse csv
        reader = csv.DictReader(decoded_content.splitlines(), skipinitialspace=True)
        for r in reader:
            date = r["Start"]
            for key in r:
                if key == "Start":
                    continue
                value = r[key]
                if value == "":
                    continue
                price = dict()
                price["price"] = get_decimal(r["Elpris"])
                price["transport_and_tax"] = get_decimal(r["Transport og afgifter"])
                price["total"] = get_decimal(r["Total"])
                #'02.01.2025 - 00:00'
                current_date = datetime.strptime(date, "%d.%m.%Y - %H:%M")

                result[current_date.isoformat()] = price
        return result
