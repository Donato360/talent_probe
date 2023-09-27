import subprocess
from typing import Optional
from fastapi import FastAPI, HTTPException, status
import linkedin_scraper as scraper
from datetime import datetime
import time
import json
from helpers import logger2

app = FastAPI()

@app.get("/enrich/profiles/{profile_id}", status_code=status.HTTP_200_OK)
async def read_item(profile_id):
    # Process the profile
    source = ['profile', profile_id]

    if profile_id is not None:
        # Build the command to execute the scraper script inside the container
        command = [
            "docker", "exec",
            "talent_probe",
            "python", "-c",
            f"from linkedin_scraper import main; main({source!r})"
        ]

        # Execute the command using subprocess
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)

            # Log success message
            logger2.info(f"Processing of profile {profile_id} started by the talent_probe container.")
        except subprocess.CalledProcessError as e:
            logger2.error(f"Error running the subprocess for the profile {profile_id}:") + str(e)
    else:
        logger2.error(f"Error: No profile_id provided")