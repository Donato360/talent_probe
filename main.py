from fastapi import FastAPI
import linkedin_scraper as scraper
from os import system
from datetime import datetime
import json

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/enrich/profiles/{profile_id}")
async def read_item(profile_id):
    source = ['profile', profile_id]
    json_objects_array = scraper.main(source)

    # save data to file
    now = datetime.now()
    timestamp = datetime.timestamp(now)# current date and time

    json_object = json_objects_array[0] | {
        'metadata': { 
            "last_update": timestamp
        }
    }

    file_name = profile_id + '.json'

    with open(file_name, 'w') as f:
        json.dump(json_object, f)
    
    return json_object