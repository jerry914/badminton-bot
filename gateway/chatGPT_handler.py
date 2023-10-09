import os
import json
from dotenv import load_dotenv
load_dotenv()
import openai
import sheet_handler
from datetime import date, datetime
import uuid

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_future_events(channel_id):
    today = date.today()
    events = sheet_handler.fetch_future_events_from_sheet("Events", channel_id, today)
    return events

def add_event(date, time, location, organizer_id, organizer_name, channel_id):
    event_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    row = [event_id, date, time, location, organizer_id, organizer_name, channel_id, timestamp]
    sheet_handler.add_to_sheet("Events", row)
    return event_id
def cancel_event(event_id):
    result = sheet_handler.remove_event_from_sheet("Events", event_id)
    if result:
        return 'Event cancelled'
    else:
        raise Exception("Event not found")
def get_participants(event_id):
    participants = sheet_handler.fetch_participants_by_id('Signups', event_id)
    return participants
def add_signup(event_id, user_id, user_name):
    signup_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    row = [signup_id, event_id, user_id, user_name, timestamp]
    sheet_handler.add_to_sheet("Signups", row)
    return signup_id
def cancel_signup(signup_id):
    result = sheet_handler.remove_signup_from_sheet("Signups", signup_id)
    if result:
        return 'Signup cancelled'
    else:
        raise Exception("Signup not found")
def send_random_video(video_type):
    video = sheet_handler.send_random_video_from_sheet("VideoList", video_type)
    if video:
        return video
    else:
        raise Exception("Video not found")


def run_conversation(user_message):
    # Step 1: send the conversation and available functions to GPT
    messages = [{"role": "user", "content": user_message}]
    functions = [
        {
            "name": "get_future_events",
            "description": "Fetch all future events that match the given channel_id",
            "parameters": {
                "type": "object",
                "properties": {
                    "channel_id": {
                        "type": "string",
                        "description": "The ID of the channel to fetch events for",
                    },
                },
                "required": ["channel_id"],
            },
        },
        {
            "name": "add_event",
            "description": "Add a new event to the Google Sheet",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {"type": "string", "description": "The date of the event in the format MM/DD/YYYY"},
                    "time": {"type": "string", "description": "The time of the event in the format HH:MM AM/PM"},
                    "location": {"type": "string"},
                    "organizer_id": {"type": "string"},
                    "organizer_name": {"type": "string"},
                    "channel_id": {"type": "string"},
                },
                "required": ["date", "time", "location", "organizer_id", "organizer_name", "channel_id"],
            },
        },
        {
            "name": "cancel_event",
            "description": "Cancel a specific event by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The unique ID of the event to be cancelled",
                    },
                },
                "required": ["event_id"],
            },
        },
        {
            "name": "get_participants",
            "description": "Fetch participants of a specific event by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {
                        "type": "string",
                        "description": "The unique ID of the event to fetch participants for",
                    },
                },
                "required": ["event_id"],
            },
        },
        {
            "name": "add_signup",
            "description": "Add a new signup for an event",
            "parameters": {
                "type": "object",
                "properties": {
                    "event_id": {"type": "string"},
                    "user_id": {"type": "string"},
                    "user_name": {"type": "string"},
                },
                "required": ["event_id", "user_id", "user_name"],
            },
        },
        {
            "name": "cancel_signup",
            "description": "Cancel a specific signup by its ID",
            "parameters": {
                "type": "object",
                "properties": {
                    "signup_id": {
                        "type": "string",
                        "description": "The unique ID of the signup to be cancelled",
                    },
                },
                "required": ["signup_id"],
            },
        },
        {
            "name": "send_random_video",
            "description": "Send a random video based on the given video type",
            "parameters": {
                "type": "object",
                "properties": {
                    "video_type": {
                        "type": "string",
                        "description": "The type/category of the video to be fetched",
                    },
                },
                "required": ["video_type"],
            },
        }
    ]
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions=functions,
        function_call="auto",
    )
    response_message = response["choices"][0]["message"]

    # Step 2: check if GPT wanted to call a function
    if response_message.get("function_call"):
        # Step 3: call the function
        # Note: the JSON response may not always be valid; be sure to handle errors
        available_functions = {
            "get_future_events": get_future_events,
            "add_event": add_event,
            "cancel_event": cancel_event,
            "get_participants": get_participants,
            "add_signup": add_signup,
            "cancel_signup": cancel_signup,
            "send_random_video": send_random_video,
        }
        function_name = response_message["function_call"]["name"]
        function_to_call = available_functions[function_name]
        function_args = json.loads(response_message["function_call"]["arguments"])
        function_response = function_to_call(**function_args)

        # Step 4: send the info on the function call and function response to GPT
        messages.append(response_message)  # extend conversation with assistant's reply
        messages.append(
            {
                "role": "function",
                "name": function_name,
                "content": function_response,
            }
        )  # extend conversation with function response
        second_response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-0613",
            messages=messages,
        )  # get a new response from GPT where it can see the function response
        return second_response["choices"][0]["message"]["content"]
    else:
        return response_message["content"]

# print(run_conversation("Cancle the signup of cbef28a4-b676-4e62-9cb3-97f5bfc03483"))