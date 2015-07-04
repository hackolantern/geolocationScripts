import locationsToShapefileConversion

__author__ = 'timothy'

import csv
import os


def getGFYLDataFiles():
    gfylDataFiles = []

    for dataFileName in os.listdir('csvData'):
        if (dataFileName.startswith('GFYL')):
            gfylDataFiles.append(dataFileName)

    return gfylDataFiles


def locationsFromGFYLDataFile(dataFile):
    print('Reading file ' + dataFile)

    handle = open('csvData/' + dataFile, newline='', encoding='utf-8')
    reader = csv.DictReader(handle, ['Name','Address','Suburb','Postcode','State','Business Category','LGA','Region'])

    locations = []

    isFirstRow = True

    for row in reader:
        if isFirstRow:
            isFirstRow = False
            continue

        locations.append(locationFromGFYLRow(row))

    print('Retrieved information for ' + str(len(locations)) + ' locations from file ' + dataFile)

    return locations


def locationFromGFYLRow(row):
    returned = locationsToShapefileConversion.Location()

    returned.name = row['Name']
    returned.address = row['Address'] + ' ' + row['Suburb'] + ' ' + row['State']

    returned.attributes['category'] = row['Business Category']

    return returned


if __name__ == "__main__":
    print('Listing GFYLDataFiles')
    datafiles = getGFYLDataFiles()

    locationInfos = []

    print('Loading information from GFYLFiles')
    for dataFile in datafiles:
        locationInfos.extend(locationsFromGFYLDataFile(dataFile))

    print('Adding latitudes and longitudes to location information')
    locationsToShapefileConversion.addLatLongs(locationInfos)

    print('Writing to shapefile')
    locationsToShapefileConversion.writeToShapeFile(locationInfos, 'GFYL', ['category'])