from http.client import HTTPConnection
import json

__author__ = 'timothy'

import shapefile
import csv
import os
import urllib.parse

class LocationInfo:
    name = ''
    streetAddress = ''
    suburb = ''
    postcode = ''
    state = ''
    category = ''
    lat = None
    long = None


    @classmethod
    def fromGFYLRow(cls, row):
        returned = LocationInfo()

        returned.name = row['Name']
        returned.streetAddress = row['Address']
        returned.suburb = row['Suburb']
        returned.postcode = row['Postcode']
        returned.state = row['State']
        returned.category = row['Business Category']

        return returned


    def addressString(self):
        return self.streetAddress + ' ' + self.suburb + ' ' + self.state


    def isValidLatLong(self):
        return self.lat is not None and \
               self.long is not None and \
               112.85 <= self.long <= 153.69 and \
               -43.7 <= self.lat <= -9.86


def getGFYLDataFiles():
    gfylDataFiles = []

    for dataFileName in os.listdir('csvData'):
        if (dataFileName.startswith('GFYL')):
            gfylDataFiles.append(dataFileName)

    return gfylDataFiles


def locationInfosFromGFYLDataFile(dataFile):
    print('Reading file ' + dataFile)

    handle = open('csvData/' + dataFile, newline='', encoding='utf-8')
    reader = csv.DictReader(handle, ['Name','Address','Suburb','Postcode','State','Business Category','LGA','Region'])

    locationInfos = []

    isFirstRow = True

    for row in reader:
        if isFirstRow:
            isFirstRow = False
            continue

        locationInfos.append(LocationInfo.fromGFYLRow(row))

    print('Retrieved information for ' + str(len(locationInfos)) + ' locations from file ' + dataFile)

    return locationInfos

def mapquestKey():
    return open('mapquestkey.txt').read().strip()

MAP_QUEST_KEY = mapquestKey()
MAP_QUEST_BASE_URL = 'www.mapquestapi.com'
MAP_QUEST_BATCH_RESOURCE = '/geocoding/v1/batch?key=' + MAP_QUEST_KEY + '&thumbMaps=false&maxResults=1'

def addLatLongs(locationInfos):

    numLocationInfosHandled = 0

    while numLocationInfosHandled < len(locationInfos):
        currentLocationInfoBatch = locationInfos[numLocationInfosHandled: (numLocationInfosHandled + 90)]

        addLatLongsWithoutBatchLimit(currentLocationInfoBatch)

        numLocationInfosHandled += len(currentLocationInfoBatch)

        print('Added latitudes and longtitudes for ' + str(numLocationInfosHandled) + ' of ' +
              str(len(locationInfos)) + ' locations')


def addLatLongsWithoutBatchLimit(locationInfos):

    queryString = MAP_QUEST_BATCH_RESOURCE

    addressStringToLocationInfoMap = {}

    for locationInfo in locationInfos:
        addressString = locationInfo.addressString()
        addressStringToLocationInfoMap[addressString] = locationInfo
        queryString = queryString + '&location=' + urllib.parse.quote(addressString)

    connection = HTTPConnection(MAP_QUEST_BASE_URL, 80)

    connection.request('GET', queryString)
    response = connection.getresponse().read().decode('utf-8')

    jsonResponse = json.loads(response)

    addLatLongFromMapQuestResponse(addressStringToLocationInfoMap, jsonResponse)


def addLatLongFromMapQuestResponse(addressStringToLocationInfoMap, jsonResponse):
    for result in jsonResponse['results']:
        addressString = result['providedLocation']['location']
        lat = result['locations'][0]['latLng']['lat']
        long = result['locations'][0]['latLng']['lng']

        locationInfo = addressStringToLocationInfoMap[addressString]
        locationInfo.lat = lat
        locationInfo.long = long


def writeToShapeFile(locationInfos, fileName):
    writer = shapefile.Writer(shapefile.POINT)

    writer.field('Name', 'C', '100')
    writer.field('Address', 'C', '200')
    writer.field('Category', 'C', '100')

    for locationInfo in locationInfos:
        if (locationInfo.isValidLatLong()):
            writer.point(locationInfo.long, locationInfo.lat)
            writer.record(locationInfo.name, locationInfo.addressString(), locationInfo.category)
        else:
            print('Ignoring location \'' + locationInfo.name + '\' at \'' + locationInfo.addressString() +
                  '\' with spurious lat/long ' + str(locationInfo.lat) + ',' + str(locationInfo.long))

    writer.save('shapeFiles/' + fileName)


if __name__ == "__main__":
    print('Listing GFYLDataFiles')
    datafiles = getGFYLDataFiles()

    locationInfos = []

    print('Loading information from GFYLFiles')
    for dataFile in datafiles:
        locationInfos.extend(locationInfosFromGFYLDataFile(dataFile))

    print('Adding latitudes and longitudes to location information')
    addLatLongs(locationInfos)

    print('Writing to shapefile')
    writeToShapeFile(locationInfos, 'GFYL')