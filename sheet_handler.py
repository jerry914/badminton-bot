import pygsheets
import os
from datetime import date, datetime
# take environment variables from .env.
from dotenv import load_dotenv
load_dotenv()
sheet_url = os.getenv('SHEET_URL')
# Initialize Google Sheets API
gc = pygsheets.authorize(service_file='client_secret.json')
sheet = gc.open_by_url(sheet_url)

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
            row_date = datetime.strptime(row[1], '%Y-%m-%d').date()
        except ValueError:
            print(f"Skipping row with invalid date: {row}")
            if row[5] == channel_id:
                future_events.append(row)
            continue

        if row[5] == channel_id and row_date >= date:
            future_events.append(row)

    return future_events
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
