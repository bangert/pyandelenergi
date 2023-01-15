
from urllib.request import urlopen
import csv
from datetime import datetime

def getDefaultData():
    startDate = getEarliestStartDate()
    endDate = getMaxFutureDate()
    defaultRegion = "east"
    url = buildUrl(defaultRegion, startDate, endDate)
    return fetchData(url)

def getEarliestStartDate():
    return "2023-01-08"

def getMaxFutureDate():
    return "2023-01-16"

def buildUrl(region, startDate, endDate):
    return f"https://andelenergi.dk/?obexport_format=csv&obexport_start={startDate}&obexport_end={endDate}&obexport_region={region}&obexport_tax=13%2C22"

def fetchData(url):
    # download csv
    with urlopen(url) as response:
        result = dict()
        body = response.read()
        decoded_content = body.decode('utf-8')
        # parse csv
        reader = csv.DictReader(decoded_content.splitlines(), skipinitialspace=True)
        for r in reader:
            date = r["Date"]
            for key in r:
                if key == "Date":
                    continue
                value = r[key]
                if value == "":
                    continue
                resultkey = date + "T" + key + ":00"
                result[resultkey] = r[key]
        return result
