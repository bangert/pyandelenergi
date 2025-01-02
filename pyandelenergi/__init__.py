
from urllib.request import urlopen
import csv
from datetime import date, datetime, timedelta

def getDefaultData():
    startDate = getEarliestStartDate()
    endDate = getMaxFutureDate()
    defaultRegion = "east"
    url = buildUrl(defaultRegion, startDate, endDate)
    return fetchData(url)

def getEarliestStartDate():
    # today
    startDate = date.today()
    return startDate.strftime("%Y-%m-%d")

def getMaxFutureDate():
    futureDate = date.today() + timedelta(days=2)
    return futureDate.strftime("%Y-%m-%d")

def buildUrl(region, startDate, endDate):
    return f"https://andelenergi.dk/?obexport_format=csv&obexport_start={startDate}&obexport_end={endDate}&obexport_region={region}&obexport_tax=0&obexport_product_id=1%231%23TIMEENERGI"

def fetchData(url):
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
                price["price"] = r["Elpris"]
                price["transport_and_tax"] = r["Transport og afgifter"]
                price["total"] = r["Total"]
                #'02.01.2025 - 00:00'
                current_date = datetime.strptime(date, "%d.%m.%Y - %H:%M")

                result[current_date.isoformat()] = price
        return result
