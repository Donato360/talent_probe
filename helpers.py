from datetime import datetime
from dateparser.search import search_dates
import locationtagger
import logging

# Create a logger object for error logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

# Create a file handler and set the log file name
log_file = 'error.log'
file_handler = logging.FileHandler(log_file)

# Create a formatter and add it to the file handler
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
file_handler.setFormatter(formatter)

# Add the file handler to the logger
logger.addHandler(file_handler)

# Create second logger object to output API requests and responses
logger2 = logging.getLogger('api')
logger2.setLevel(logging.INFO)

# Create a file handler and set the log file name
log_file2 = 'api.log'
file_handler2 = logging.FileHandler(log_file2)

# Create a formatter and add it to the file handler
formatter2 = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(message)s')
file_handler2.setFormatter(formatter2)

# Add the file handler to the logger
logger2.addHandler(file_handler2)

def sanitize_file_name(file_name):
    # Remove any characters that are not allowed in a file name
    invalid_chars = '/\\?%*:|"<>!$'
    sanitized_name = ''.join('_' if char in invalid_chars else char for char in file_name)
    return sanitized_name

def average(list):
    return sum(list) / len(list)

def getUniqueItems(iterable):
    seen = set()
    result = []
    for item in iterable:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result

class Helper:
    def processDate(self, aStringWithDate):
        dates = None

        sep = '·'
        aStringWithDate = aStringWithDate.split(sep, 1)[0]

        dates = search_dates(aStringWithDate, languages=['en'], settings={'TIMEZONE': 'UTC', 'RELATIVE_BASE': datetime(2020, 1, 1), 'REQUIRE_PARTS': ['year']})
        # print('dates: {}'.format(dates))

        if not dates:
            start_date = None
            end_date = None
        else:
            if len(dates) == 1:
                aStringWithDate = aStringWithDate.lower()

                if 'present' in aStringWithDate:
                    start_date = dates[0][1].strftime('%Y-%m-%d')
                    end_date = 'present'
                else:
                    start_date = None
                    end_date = dates[0][1].strftime('%Y-%m-%d')
            elif len(dates) > 1:
                start_date = dates[0][1].strftime('%Y-%m-%d')
                end_date = dates[1][1].strftime('%Y-%m-%d')

        if start_date == None and end_date == None:
            parsedDatesJson = None
        else:
            parsedDatesJson = {'start_date': start_date, 'end_date': end_date }

        return parsedDatesJson
    
    def processLocation(self, aStringWithLocation):
        parsedLocationsJson = None
        entities = None
        entities = locationtagger.find_locations(text = aStringWithLocation)

        if entities.cities or entities.regions or entities.countries:
            parsedLocationsJson = {'cities': entities.cities, 'regions': entities.regions, 'countries': entities.countries}

        return parsedLocationsJson
