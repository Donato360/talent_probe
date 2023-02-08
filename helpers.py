from datetime import datetime
from dateparser import parse
from dateparser_data.settings import default_parsers
from dateparser.search import search_dates

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

        dates = search_dates(aStringWithDate, languages=['en'])

        if not dates:
            start_date = None
            end_date = None
        else:
            if len(dates) == 1:
                start_date = None
                end_date = dates[0][1].strftime('%Y-%m-%d')
            elif len(dates) > 1:
                start_date = dates[0][1].strftime('%Y-%m-%d')
                end_date = dates[1][1].strftime('%Y-%m-%d')

        parsedDatesJson = {'start_date': start_date, 'end_date': end_date }

        return parsedDatesJson
