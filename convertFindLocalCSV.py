import csv
from locationsToShapefileConversion import Location
import locationsToShapefileConversion

__author__ = 'timothy'


findLocationFileLocation = 'csvData/findLocalLocations.csv'

def locationsFromCSVFile():
    print('Reading file ' + findLocationFileLocation)

    handle = open(findLocationFileLocation, newline='', encoding='utf-8')
    reader = csv.DictReader(handle, ['Name','Address1','Address2','phone'])

    locations = []

    isFirstRow = True

    for row in reader:
        if isFirstRow:
            isFirstRow = False
            continue

        locations.append(locationFromRow(row))

    print('Retrieved information for ' + str(len(locations)) + ' locations from file ' + findLocationFileLocation)

    return locations


def locationFromRow(row):
    returned = Location()

    returned.address = row['Address1'] + ', ' + row['Address2'] + ', VIC, Australia'
    returned.name = row['Name']

    returned.attributes['phone'] = row['phone']

    return returned


if __name__ == "__main__":

    print('Loading information from CSV')
    locations = locationsFromCSVFile()

    print('Adding latitudes and longitudes to location information')
    locationsToShapefileConversion.addLatLongs(locations)

    print('Writing to shapefile')
    locationsToShapefileConversion.writeToShapeFile(locations, 'FindLocal', ['phone'])