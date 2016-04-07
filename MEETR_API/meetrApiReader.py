import urllib.request
import urllib.response
from urllib.error import HTTPError
import json

api_key = 'Polestar:978VJRPHC385WRE8'
api_address = 'https://microsoft-apiappb01b17607f554d4292d7d17df5186565.azurewebsites.net:443/api/'

StartDate = '2016-03-24'
StartHour = '00'
StartMinute = '00'
StartSecond = '00'
StartDateTime = StartDate + '%20' + StartHour + '%3A' + StartMinute + '%3A' + StartSecond

EndDate = '2016-03-31'
EndHour = '14'
EndMinute = '30'
EndSecond = '00'
EndDateTime = EndDate + '%20' + EndHour + '%3A' + EndMinute + '%3A' + EndSecond

# Ship ID: 11
# Ship name: Hartland Point
# ImoNumber = '9248538'

# Ship ID: 12
# Ship name: AM ANNABA
# ImoNumber = '9669330'

# Ship ID: 14
# Ship name: Hong Kong Spirit
# ImoNumber = '9602289'

# Ship ID: 15
# Ship name: AM Zenica
# ImoNumber = '9669342'

StartEndDateTime = 'StartDate=' + StartDateTime + '&EndDate=' + EndDateTime

# reportSpecific = 'ShipReport?'
# reportSpecific = 'ShipReportBetweenDates?' + StartEndDateTime
# reportSpecific = 'ShipReportECA?'
reportSpecific = 'ShipReportECABetweenDates?' + StartEndDateTime
# reportSpecific = 'ShipReportECABetweenDatesByShipIMO?' + StartEndDateTime + '&IMONumber=' + ImoNumber

ShipReportUrl = api_address + reportSpecific + '&api_key=' + api_key
req = urllib.request.Request(ShipReportUrl)

try:
    response = urllib.request.urlopen(req).read().decode("utf-8")
    json_data = json.loads(response)
    # print(json_data)

    for item in json_data:
        dataString = ""
        fieldNameString = ""
        print("---------------------------------------------------------------------------------------------")
        print("Ship ID: " + str(item["ShipID"]))
        print("Ship name: " + item["ShipName"])
        print("IMO number: " + item["ShipIMO"])
        fieldNameDone = False
        for item2 in item["Position"]:
            fieldNameString = "Record time,Latitude,Longitude,Speed(knots),Heading(degrees)"
            dataString = item2["RecordTime"][:10] + " " + item2["RecordTime"][11:] + ","
            dataString += str(item2["Latitude"]) + ","
            dataString += str(item2["Longitude"]) + ","
            dataString += str(item2["Speed"]) + ","
            dataString += str(item2["Heading"])

            # print("Record time: " + item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
            # print("Latitude: " + str(item2["Latitude"]))
            # print("Longitude: " + str(item2["Longitude"]))
            # print("Speed: " + str(item2["Speed"]))
            # print("Heading: " + str(item2["Heading"]))
            for item3 in item2["DataFields"]:
                # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                # print(item3["FieldName"] + ": " + str(item3["Value"]) + " " + item3["Unit"])
                # print(item3["FieldName"] + ", " + item3["Unit"])
                fieldNameString += "," + item3["FieldName"] + "(" + item3["Unit"] + ")"
                dataString += "," + str(item3["Value"])
                # if item3["FieldName"] == "CO2":
                    # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                    # print(str(item3["Value"]))
                # if item3["FieldName"] == "SOx":
                   # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                   # print(str(item3["Value"]))
                # if item3["FieldName"] == "FuelFlow":
                    # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                    # print(str(item3["Value"]))
                    # print(item3["FieldName"] + ": " + str(item3["Value"]) + " " + item3["Unit"])
                # if item3["FieldName"] == "Sulfur in Fuel":
                    # print(item2["RecordTime"][:10] + " " + item2["RecordTime"][11:])
                    # print(str(item3["Value"]))
                    # print(item3["FieldName"] + ": " + str(item3["Value"]) + " " + item3["Unit"])
            # print("******************")
            if not fieldNameDone:
                print(fieldNameString)
                fieldNameDone = True
            print(dataString)

except HTTPError as e:
    error = e.read().decode("utf-8")
