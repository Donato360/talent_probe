from fastapi import FastAPI, HTTPException, Response, status
import linkedin_scraper as scraper
from datetime import datetime
import time
import json
from helpers import logger2

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/enrich/profiles/{profile_id}", status_code=status.HTTP_200_OK)
async def read_item(profile_id):
    try:
        # Start measuring execution time
        start_time = time.time()

        # Process the profile
        source = ['profile', profile_id]
        json_objects_array = scraper.main(source)

        # Save data to file
        timestamp = datetime.now().timestamp()
        json_object = json_objects_array[0] | {
            'metadata': {
                "last_update": timestamp
            }
        }

        file_name = f"{profile_id}.json"

        with open(file_name, 'w') as f:
            json.dump(json_object, f)

        # Log success message with execution time
        execution_time = time.time() - start_time
        logger2.info(f"Profile {profile_id} processed successfully in {execution_time} seconds. Status Code: {Response.status_code}")

        return json_object
    
    except Exception as e:
        # Log error message
        logger2.error(f"Error processing profile {profile_id}: {e}. Status Code: {Response.status_code}")

        # Handle the error gracefully or re-raise it
        raise HTTPException(status_code=500, detail="An error occurred while enriching the profile")
