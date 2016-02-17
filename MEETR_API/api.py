import urllib.request
import urllib.response
from urllib.error import HTTPError
import json

api_key = 'Polestar:978VJRPHC385WRE8'

api_address = 'https://microsoft-apiappb01b17607f554d4292d7d17df5186565.azurewebsites.net:443/api/'

StartDate = '2015-12-10'
StartHour = '00'
StartMinute = '00'
StartSecond = '00'
StartDateTime = StartDate + '%20' + StartHour + '%3A' + StartMinute + '%3A' + StartSecond

EndDate = '2015-12-10'
EndHour = '01'
EndMinute = '00'
EndSecond = '00'
EndDateTime = EndDate + '%20' + EndHour + '%3A' + EndMinute + '%3A' + EndSecond

ShipReportBetweenDates = api_address + 'ShipReportBetweenDates?' \
                        + 'StartDate=' + StartDateTime \
                        + '&EndDate=' + EndDateTime \
                        + '&api_key=' + api_key

ShipReportECABetweenDates = api_address + 'ShipReportECABetweenDates?' \
                        + 'StartDate=' + StartDateTime \
                        + '&EndDate=' + EndDateTime \
                        + '&api_key=' + api_key

ShipReportECA = api_address + 'ShipReportECA?' + '&api_key=' + api_key

ShipReport = api_address + 'ShipReport?' + '&api_key=' + api_key

#req = urllib.request.Request(ShipReportECABetweenDates)
req = urllib.request.Request(ShipReportBetweenDates)
#req = urllib.request.Request(ShipReportECA)
#req = urllib.request.Request(ShipReport)

try:
    response = urllib.request.urlopen(req).read().decode("utf-8")
except HTTPError as e:
    venue = e.read().decode("utf-8")

json_data = json.loads(response)

for item in json_data:
    print("----------------------------------")
    print(item["ShipName"])
    for item2 in item["Position"]:
        print(item2["RecordTime"])
        print(item2["Latitude"])
        print(item2["Longitude"])
        print("******************")
