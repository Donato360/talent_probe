## linkedIn Data Scraper - author Donato Cappiello

### 1) use the script

Users can use a query, pass a single profile, a CSV or python file to scrape user profiles.
Here are some coding examples that demonstrate how to utilise the script. 

command to get help
```
python3 linkedin-scraper.py -h
```

commands for single profiles
```
python3 linkedin-scraper.py --source query 'site:linkedin.com/in AND "python developer" AND "London”'

python3 linkedin-scraper.py --source query 'site:linkedin.com/in AND "machine learning engineer" AND "bristol”'
```

profiles that can be used to enrich a search
```
 ['https://www.linkedin.com/in/ykpgrr/', 'https://www.linkedin.com/in/lee-braybrooke-73666927/', 'https://www.linkedin.com/in/saman-nejad/', 'https://www.linkedin.com/in/eluert-mukja/', 'https://www.linkedin.com/in/sir-hossein-yassaie-freng-fiet-55685012/']
```