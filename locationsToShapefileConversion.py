from http.client import HTTPConnection
import urllib.parse
import json
import shapefile

__author__ = 'timothy'

class Location:
    sename = None
    address = None

    lat = None
    long = None

    attributes = None

    def __init__(self):
        self.attributes = {}

    def isValidLatLong(self):
        return self.lat is not None and \
               self.long is not None and \
               112.85 <= self.long <= 153.69 and \
               -43.7 <= self.lat <= -9.86


def mapquestKey():
    return open('mapquestkey.txt').read().strip()


MAP_QUEST_BASE_URL = 'www.mapquestapi.com'
MAP_QUEST_BATCH_RESOURCE = '/geocoding/v1/batch?key=' + mapquestKey() + '&thumbMaps=false&maxResults=1'


def addLatLongs(locations):

    numLocationInfosHandled = 0

    while numLocationInfosHandled < len(locations):
        currentLocationInfoBatch = locations[numLocationInfosHandled: (numLocationInfosHandled + 90)]

        addLatLongsWithoutBatchLimit(currentLocationInfoBatch)

        numLocationInfosHandled += len(currentLocationInfoBatch)

        print('Added latitudes and longtitudes for ' + str(numLocationInfosHandled) + ' of ' +
              str(len(locations)) + ' locations')


def addLatLongsWithoutBatchLimit(locations):

    queryString = MAP_QUEST_BATCH_RESOURCE

    addressStringToLocationMap = {}

    for location in locations:
        addressString = location.address
        addressStringToLocationMap[addressString] = location
        queryString = queryString + '&location=' + urllib.parse.quote(addressString)

    connection = HTTPConnection(MAP_QUEST_BASE_URL, 80)

    connection.request('GET', queryString)
    response = connection.getresponse().read().decode('utf-8')

    jsonResponse = json.loads(response)

    addLatLongFromMapQuestResponse(addressStringToLocationMap, jsonResponse)


def addLatLongFromMapQuestResponse(addressStringToLocationMap, jsonResponse):
    for result in jsonResponse['results']:
        addressString = result['providedLocation']['location']
        lat = result['locations'][0]['latLng']['lat']
        long = result['locations'][0]['latLng']['lng']

        location = addressStringToLocationMap[addressString]
        location.lat = lat
        location.long = long


def writeToShapeFile(locations, fileName, attributes):
    writer = shapefile.Writer(shapefile.POINT)

    writer.field('Name', 'C', '200')
    writer.field('Address', 'C', '200')

    for attribute in attributes:
        writer.field(attribute, 'C', '200')

    for location in locations:
        if location.isValidLatLong():
            writer.point(location.long, location.lat)

            attributeValues = []

            for attribute in attributes:
                attributeValues.append(location.attributes[attribute])

            writer.record(location.name, location.address, *attributeValues)
        else:
            print('Ignoring location \'' + location.name + '\' at \'' + location.address +
                  '\' with spurious lat/long ' + str(location.lat) + ',' + str(location.long))

    writer.save('shapeFiles/' + fileName)