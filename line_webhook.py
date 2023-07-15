from linebot import LineBotApi, WebhookHandler
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import os
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

def handle_message(event):
    # This function will be called when a message event is received
    # You'll need to parse the event to determine if it's a new event or a signup
    # And then call the appropriate function to handle it

def handle_new_event(event):
    # This function will be called when a new event is detected
    # You'll need to add the event to the Google Sheet

def handle_new_signup(event):
    # This function will be called when a new signup is detected
    # You'll need to add the signup to the Google Sheet

def add_to_sheet(sheet_name, row):
    # This function will add a row to a Google Sheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('client_secret.json', scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    sheet.append_row(row)
