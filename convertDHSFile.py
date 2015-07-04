import csv
from locationsToShapefileConversion import Location
import locationsToShapefileConversion

__author__ = 'timothy'


dhsFileLocation = 'VETdata/govhack dhs locations geo.csv'

def locationsFromDHSFile():
    print('Reading file ' + dhsFileLocation)

    handle = open(dhsFileLocation, newline='', encoding='utf-8')
    reader = csv.DictReader(handle, ['DHS Office Location','Telephone','Type of office','LGA1','LGA2','LGA3','LGA4',
                                     'LGA5','LGA6','LGA7','LGA8','LGA9','LGA10'])

    locations = []

    isFirstRow = True

    for row in reader:
        if isFirstRow:
            isFirstRow = False
            continue

        locations.append(locationFromRow(row))

    print('Retrieved information for ' + str(len(locations)) + ' locations from file ' + dhsFileLocation)

    return locations


def locationFromRow(row):
    returned = Location()

    returned.address = row['DHS Office Location'] + ', Australia'
    returned.name = 'DHS' + row['Type of office']

    returned.attributes['phone'] = row['Telephone']
    returned.attributes['Type of office'] = row['Type of office']

    returned.attributes['LGA01'] = row['LGA1']
    returned.attributes['LGA02'] = row['LGA2']
    returned.attributes['LGA03'] = row['LGA3']
    returned.attributes['LGA04'] = row['LGA4']
    returned.attributes['LGA05'] = row['LGA5']
    returned.attributes['LGA06'] = row['LGA6']
    returned.attributes['LGA07'] = row['LGA7']
    returned.attributes['LGA08'] = row['LGA8']
    returned.attributes['LGA09'] = row['LGA9']
    returned.attributes['LGA10'] = row['LGA10']

    return returned


if __name__ == "__main__":

    print('Loading information from CSV')
    locations = locationsFromDHSFile()

    print('Adding latitudes and longitudes to location information')
    locationsToShapefileConversion.addLatLongs(locations)

    print('Writing to shapefile')
    locationsToShapefileConversion.writeToShapeFile(locations, 'DHS', ['phone', 'Type of office', 'LGA01',
                                                                       'LGA02','LGA03','LGA04','LGA05','LGA06','LGA07',
                                                                       'LGA08','LGA09','LGA10'])