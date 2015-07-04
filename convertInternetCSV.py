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

    returned.attributes['Cost'] = row['Cost']
    returned.attributes['Bookings'] = row['Bookings']
    returned.attributes['Opening_Hours_Mon_Open'] = row['Opening_Hours_Mon_Open']
    returned.attributes['Opening_Hours_Mon_Close'] = row['Opening_Hours_Mon_Close']
    returned.attributes['Opening_Hours_Tue_Open'] = row['Opening_Hours_Tue_Open']
    returned.attributes['Opening_Hours_Tue_Close'] = row['Opening_Hours_Tue_Close']
    returned.attributes['Opening_Hours_Wen_Open'] = row['Opening_Hours_Wen_Open']
    returned.attributes['Opening_Hours_Wen_Close'] = row['Opening_Hours_Wen_Close']
    returned.attributes['Opening_Hours_Thu_Open'] = row['Opening_Hours_Thu_Open']
    returned.attributes['Opening_Hours_Thu_Close'] = row['Opening_Hours_Thu_Close']
    returned.attributes['Opening_Hours_Fri_Open'] = row['Opening_Hours_Fri_Open']
    returned.attributes['Opening_Hours_Fri_Close'] = row['Opening_Hours_Fri_Close']
    returned.attributes['Opening_Hours_Sat_Open'] = row['Opening_Hours_Sat_Open']
    returned.attributes['Opening_Hours_Sat_Close'] = row['Opening_Hours_Sat_Close']
    returned.attributes['Opening_Hours_Sun_Open'] = row['Opening_Hours_Sun_Open']
    returned.attributes['Opening_Hours_Sun_Close'] = row['Opening_Hours_Sun_Close']
    returned.attributes['Num_Terminals'] = row['Num_Terminals']
    returned.attributes['Disability_Friendly_Terminals'] = row['Disability_Friendly_Terminals']
    returned.attributes['Printing_Available'] = row['Printing_Available']
    returned.attributes['Touch_Screen'] = row['Touch_Screen']
    returned.attributes['Trackball'] = row['Trackball']
    returned.attributes['Large_Keyboard'] = row['Large_Keyboard']
    returned.attributes['Large_Monitor'] = row['Large_Monitor']
    returned.attributes['Accessibility_Options'] = row['Accessibility_Options']
    returned.attributes['Speech_Synthesizer'] = row['Speech_Synthesizer']
    returned.attributes['Disability_Software'] = row['Disability_Software']
    returned.attributes['Documentation'] = row['Documentation']
    returned.attributes['Assistance'] = row['Assistance']
    returned.attributes['Multilingual_Staff'] = row['Multilingual_Staff']
    returned.attributes['Multilingual_Access'] = row['Multilingual_Access']
    returned.attributes['Training'] = row['Training']
    returned.attributes['Wheelchair_Access'] = row['Wheelchair_Access']
    returned.attributes['Funded'] = row['Funded']
    returned.attributes['Environment'] = row['Environment']
    returned.attributes['Adjustable Arm/Base'] = row['Adjustable Arm/Base']
    returned.attributes['Adjustable Desk'] = row['Adjustable Desk']
    returned.attributes['Content Filtering'] = row['Content Filtering']
    returned.attributes['Food Kiosk'] = row['Food Kiosk']

    return returned


if __name__ == "__main__":

    print('Loading information from CSV')
    locations = locationsFromCSVFile()

    print('Adding latitudes and longitudes to location information')
    locationsToShapefileConversion.addLatLongs(locations)

    print('Writing to shapefile')
    locationsToShapefileConversion.writeToShapeFile(locations, 'Internet',
        ['phone', 'category','Cost','Bookings','Opening_Hours_Mon_Open','Opening_Hours_Mon_Close',
         'Opening_Hours_Tue_Open','Opening_Hours_Tue_Close','Opening_Hours_Wen_Open','Opening_Hours_Wen_Close',
         'Opening_Hours_Thu_Open','Opening_Hours_Thu_Close','Opening_Hours_Fri_Open','Opening_Hours_Fri_Close',
         'Opening_Hours_Sat_Open','Opening_Hours_Sat_Close','Opening_Hours_Sun_Open','Opening_Hours_Sun_Close',
         'Num_Terminals','Disability_Friendly_Terminals','Printing_Available','Touch_Screen','Trackball',
         'Large_Keyboard','Large_Monitor','Accessibility_Options','Speech_Synthesizer','Disability_Software',
         'Documentation','Assistance','Multilingual_Staff','Multilingual_Access','Training','Wheelchair_Access',
         'Funded','Environment','Adjustable Arm/Base','Adjustable Desk','Content Filtering','Food Kiosk'])