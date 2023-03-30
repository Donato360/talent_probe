from datetime import datetime
from dateparser.search import search_dates
import locationtagger

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
