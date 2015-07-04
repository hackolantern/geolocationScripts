import csv
from locationsToShapefileConversion import Location
import locationsToShapefileConversion

__author__ = 'timothy'

fileLocation = 'csvData/kindergartens.csv'

def locationsFromCSVFile():
    print('Reading file ' + fileLocation)

    handle = open(fileLocation, newline='', encoding='utf-8')
    reader = csv.DictReader(handle, ['Service Name','Street','Suburb','Postcode','State','LGA'])

    locations = []

    isFirstRow = True

    for row in reader:
        if isFirstRow:
            isFirstRow = False
            continue

        locations.append(locationFromRow(row))

    print('Retrieved information for ' + str(len(locations)) + ' locations from file ' + fileLocation)

    return locations


def locationFromRow(row):
    returned = Location()

    returned.address = row['Street'] + ', ' + row['Suburb'] + ', ' + row['State'] + ', Australia'
    returned.name = row['Service Name']

    returned.attributes['LGA'] = row['LGA']

    return returned


if __name__ == "__main__":

    print('Loading information from CSV')
    csvColumns = locationsFromCSVFile()

    print('Adding latitudes and longitudes to location information')
    locationsToShapefileConversion.addLatLongs(csvColumns)

    print('Writing to shapefile')
    locationsToShapefileConversion.writeToShapeFile(csvColumns, 'Kindergartens',
                                                    ['LGA'])