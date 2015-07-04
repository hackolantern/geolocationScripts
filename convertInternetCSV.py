import csv
from locationsToShapefileConversion import Location
import locationsToShapefileConversion

__author__ = 'timothy'


dhsFileLocation = 'csvData/public-Internet-locations.csv'

def locationsFromCSVFile():
    print('Reading file ' + dhsFileLocation)

    handle = open(dhsFileLocation, newline='', encoding='utf-8')
    reader = csv.DictReader(handle, ['Title','Address1','Address2','Suburb','Postcode','State','Contact1_Phone',
                                     'Contact2_Phone','Contact3_Phone','Fax','Cost','Bookings','Opening_Hours_Mon_Open',
                                     'Opening_Hours_Mon_Close','Opening_Hours_Tue_Open','Opening_Hours_Tue_Close',
                                     'Opening_Hours_Wen_Open','Opening_Hours_Wen_Close','Opening_Hours_Thu_Open',
                                     'Opening_Hours_Thu_Close','Opening_Hours_Fri_Open','Opening_Hours_Fri_Close',
                                     'Opening_Hours_Sat_Open','Opening_Hours_Sat_Close','Opening_Hours_Sun_Open',
                                     'Opening_Hours_Sun_Close','Num_Terminals','Disability_Friendly_Terminals',
                                     'Printing_Available','Touch_Screen','Trackball','Large_Keyboard','Large_Monitor',
                                     'Accessibility_Options','Speech_Synthesizer','Disability_Software','Documentation',
                                     'Assistance','Multilingual_Staff','Multilingual_Access','Training',
                                     'Wheelchair_Access','Funded','Environment','Adjustable Arm/Base','Adjustable Desk',
                                     'Content Filtering','Food Kiosk','Other Facilities'])

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

    returned.address = row['Address1'] + ' ' + row['Address2'] + ' ' + row['Suburb'] + ' ' + row['State'] + ', Australia'
    returned.name = row['Title']

    returned.attributes['phone'] = row['Contact1_Phone']
    returned.attributes['category'] = 'Public internet location'

    returned.attributes['Num_Terminals'] = row['Num_Terminals']

    returned.attributes['Multilingual_Staff'] = row['Multilingual_Staff']
    returned.attributes['Multilingual_Access'] = row['Multilingual_Access']
    returned.attributes['Training'] = row['Training']

    return returned


if __name__ == "__main__":

    print('Loading information from CSV')
    locations = locationsFromCSVFile()

    print('Adding latitudes and longitudes to location information')
    locationsToShapefileConversion.addLatLongs(locations)

    print('Writing to shapefile')
    locationsToShapefileConversion.writeToShapeFile(locations, 'Internet', ['phone', 'category', 'Num_Terminals',
                                                                            'Multilingual_Staff', 'Multilingual_Access',
                                                                            'Training'])