import urllib.request
import urllib.response
from urllib.error import HTTPError
import json

api_key = 'x'
api_address = 'https://microsoft-apiappb01b17607f554d4292d7d17df5186565.azurewebsites.net:443/api/'

StartDate = '2015-12-09'
StartHour = '00'
StartMinute = '00'
StartSecond = '00'
StartDateTime = StartDate + '%20' + StartHour + '%3A' + StartMinute + '%3A' + StartSecond

EndDate = '2015-12-12'
EndHour = '00'
EndMinute = '00'
EndSecond = '00'
EndDateTime = EndDate + '%20' + EndHour + '%3A' + EndMinute + '%3A' + EndSecond

ShipReportBetweenDates = api_address + 'ShipReportBetweenDates?' + 'StartDate=' + StartDateTime \
                        + '&EndDate=' + EndDateTime + '&api_key=' + api_key
ShipReportECABetweenDates = api_address + 'ShipReportECABetweenDates?' + 'StartDate=' + StartDateTime \
                        + '&EndDate=' + EndDateTime + '&api_key=' + api_key
ShipReportECA = api_address + 'ShipReportECA?' + '&api_key=' + api_key
ShipReport = api_address + 'ShipReport?' + '&api_key=' + api_key

# req = urllib.request.Request(ShipReportECABetweenDates)
# req = urllib.request.Request(ShipReportBetweenDates)
req = urllib.request.Request(ShipReportECA)
# req = urllib.request.Request(ShipReport)

try:
    response = urllib.request.urlopen(req).read().decode("utf-8")
    json_data = json.loads(response)
    # print(json_data)
    for item in json_data:
        print("----------------------------------")
        print("Ship name: " + item["ShipName"])
        print("IMO number: " + item["ShipIMO"])
        for item2 in item["Position"]:
            print("Record time: " + item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
            print("Latitude: " + str(item2["Latitude"]))
            print("Longitude: " + str(item2["Longitude"]))
            print("Speed: " + str(item2["Speed"]))
            print("Heading: " + str(item2["Heading"]))
            for item3 in item2["DataFields"]:
                print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                print(item3["FieldName"] + ": " + str(item3["Value"]) + " " + item3["Unit"])
                # if item3["FieldName"] == "CO2":
                #   print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                #   print(str(item3["Value"]))
                # if item3["FieldName"] == "SOx":
                   # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                   # print(str(item3["Value"]))
                # if item3["FieldName"] == "FuelFlow":
                    # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                    # print(str(item3["Value"]))
                    # print(item3["FieldName"] + ": " + str(item3["Value"]) + " " + item3["Unit"])
            # print("******************")

except HTTPError as e:
    error = e.read().decode("utf-8")
