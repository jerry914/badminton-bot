import pygsheets
import os
from datetime import datetime
import uuid
import re

# take environment variables from .env.
from dotenv import load_dotenv
load_dotenv()
sheet_url = os.getenv('SHEET_URL')
# Initialize Google Sheets API
gc = pygsheets.authorize(service_file='client_secret.json')
sheet = gc.open_by_url(sheet_url)

def handle_message(event):
    # This function will be called when a message event is received
    if event.source.type == "group":
        # Assume that the event message has the format "Event: <event details>"
        match_event = re.search(r'Event: (.*)', event.message.text)
        if match_event:
            handle_new_event(event)
        # Assume that a "+1" message indicates a sign-up
        if event.message.text == "+1":
            handle_new_signup(event)
        

def handle_new_event(event):
    print(event)
    # Generate a unique ID for the event
    event_id = str(uuid.uuid4())

    # Get the event details from the message
    event_details = "Badminton Event"

    # Get the event date from the message
    date = "2022-01-01"

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Get the organizer's name
    user_name = "Antonio"  # Placeholder

    # Get the group ID
    group_id = 1  # Placeholder

    # Add the event to the Google Sheet
    add_to_sheet("Events", [event_id, event_details, date, timestamp, user_name, group_id])

def handle_new_signup(event):
    print(event)
    # Generate a unique ID for the signup (you'll need to implement this)
    signup_id = str(uuid.uuid4())

    # Get the Event ID (you would actually get this from the event data)
    event_id = 1  # Placeholder

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Get the user's name (you would actually get this from the event data)
    user_name = "Antonio"  # Placeholder

    # Add the signup to the Google Sheet
    add_to_sheet("Signups", [signup_id, event_id, timestamp, user_name])
def add_to_sheet(sheet_name, row):
    # This function will add a row to a Google Sheet
    ws = sheet.worksheet_by_title(sheet_name)
    values = [row] # matrix
    ws.append_table(values=values) 

handle_new_event('Events')