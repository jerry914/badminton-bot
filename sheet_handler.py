import pygsheets
import os
from datetime import date, datetime
from dateutil.parser import parse
# take environment variables from .env.
from dotenv import load_dotenv
load_dotenv()
sheet_url = os.getenv('SHEET_URL')
# Initialize Google Sheets API
gc = pygsheets.authorize(service_file='client_secret.json')
sheet = gc.open_by_url(sheet_url)


def parse_event_data(event_data):
    # List to store parsed events
    parsed_events = []
    idx = 1
    # Loop through each event in the data
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
        row_date = '2022-01-01'
        try:
            # Attempt to parse the date
            row_date = parse(row[1], fuzzy=True).date()
            # row_date = parsed_date.strftime('%Y-%m-%d')
        except:
            print(f"Could not parse date: {row[1]}")
        if row[6] == channel_id and row_date >= date:
            future_events.append(row)

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
        if row[1] == event_id:  # Assuming event_id is in the second column
            participants.append(row)

    return participants

def remove_event_from_sheet(sheet_name, event_id):
    # Select the worksheet by its title
    ws = sheet.worksheet_by_title(sheet_name)

    # Fetch all rows from the worksheet
    rows = ws.get_all_values()

    # Find the row with the specified event_id
    for i, row in enumerate(rows):
        if row[0] == event_id:  # Assuming event_id is in the first column
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
        if row[0] == signup_id:  # Assuming signup_id is in the first column
            ws.delete_rows(i+1)  # delete_rows() uses 1-based indexing
            return f"Deleted signup with id {signup_id}"

    return "Signup not found"
