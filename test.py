import pyandelenergi
import json

url = pyandelenergi.buildUrl("east", "2023-01-08", "2023-01-16")
#print(url)

print(json.dumps(pyandelenergi.fetchData(url)))

