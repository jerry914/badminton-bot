import pygsheets
import os
import sys
from datetime import date, datetime
from dateutil.parser import parse
# take environment variables from .env.
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
sheet_url = os.getenv('SHEET_URL')
# Initialize Google Sheets API
gc = pygsheets.authorize(service_account_json=os.getenv('CLIENT_SECRET_JSON'))
sheet = gc.open_by_url(sheet_url)

def parse_event_data(event_data):
    # List to store parsed events
    parsed_events = []
    idx = 1
    # Loop through the events
    for event in event_data:
        print(event)
        # Extract the other fields
        date = event[1]
        time = event[2]
        location = event[3]
        host = event[5]
        event_id = event[0]

        # Create a formatted string for the event
        parsed_event = f'{idx}. Date: {date}, Time: {time}, Location: {location}'
        
        # Add the parsed event to the list
        parsed_events.append(parsed_event)
        idx+=1
    # Combine the parsed events into a single string
    parsed_events_str = "\n\n".join(parsed_events)

    return parsed_events_str
def add_to_sheet(sheet_name, row):
    # This function will add a row to a Google Sheet
    ws = sheet.worksheet_by_title(sheet_name)
    values = [row] # matrix
    ws.append_table(values=values) 
def fetch_future_events_from_sheet(sheet_name, channel_id, date):
    ws = sheet.worksheet_by_title(sheet_name)
    # Fetch all rows from the worksheet
    rows = ws.get_all_values()
    # Filter the rows based on the channel_id and date
    future_events = []
    for row in rows:
        # Skip the row if it's completely empty
        if all(cell == '' for cell in row):
            continue
        try:
            row_date =  datetime.strptime(row[1], "%Y/%m/%d").date()
            if row_date >= date:
                future_events.append(row)
        except:
            print(f"Could not parse date: {row[1]}")
    return parse_event_data(future_events)
def fetch_participants_by_id(sheet_name, event_id):
    # Select the worksheet by its title
    ws = sheet.worksheet_by_title(sheet_name)

    # Fetch all rows from the worksheet
    rows = ws.get_all_values()

    # Filter the rows based on the event_id
    participants = []
    for row in rows[1:]:  # Start at index 1 to skip the header row
        # Skip the row if it's completely empty
        if all(cell == '' for cell in row):
            continue
        # Check if the event_id matches the one we're looking for
        if row[1] == event_id:  # Event_id is in the second column
            participants.append(row)

    return participants

def remove_event_from_sheet(sheet_name, event_id):
    # Select the worksheet by its title
    ws = sheet.worksheet_by_title(sheet_name)

    # Fetch all rows from the worksheet
    rows = ws.get_all_values()

    # Find the row with the specified event_id
    for i, row in enumerate(rows):
        if row[0] == event_id:  # Event_id is in the first column
            ws.delete_rows(i+1)  # delete_rows() uses 1-based indexing
            return f"Deleted event with id {event_id}"

    return "Event not found"

def remove_signup_from_sheet(sheet_name, signup_id):
    # Select the worksheet by its title
    ws = sheet.worksheet_by_title(sheet_name)

    # Fetch all rows from the worksheet
    rows = ws.get_all_values()

    # Find the row with the specified signup_id
    for i, row in enumerate(rows):
        if row[0] == signup_id:  # Signup_id is in the first column
            ws.delete_rows(i+1)  # delete_rows() uses 1-based indexing
            return f"Deleted signup with id {signup_id}"

    return "Signup not found"
def send_random_video_from_sheet(sheet_name, video_type): # video_type: 可以選擇「教學」、「精華」、「shorts」
    # Select the worksheet by its title
    ws = sheet.worksheet_by_title("VideoList").get_values(start='A2', end='C', include_empty=False)
    ws_df = pd.DataFrame(ws).loc[1:, 0:2]

    # Slice the dataframe by video_type
    try:
        df = ws_df[ws_df[2] == video_type]
        # Randomly select a row from the dataframe
        random_row = df.sample()[1]
        return random_row.values[0]
    except:
        return "https://youtu.be/YzyEPCEIkcE"