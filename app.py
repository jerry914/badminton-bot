from flask import Flask, request, jsonify
from datetime import datetime, date
import uuid
import os
import sheet_handler

app = Flask(__name__)

@app.route('/')
def root():
    return jsonify({'message': 'Connection successful!'}), 200

@app.route('/events', methods=['GET'])
def get_future_events():
    # Get the channel_id query parameter
    data = request.form
    channel_id = data['channel_id']

    if not channel_id:
        return jsonify({'error': 'Missing channel_id query parameter'}), 400

    # Get today's date
    today = date.today()

    # Fetch all future events from the Google Sheet that match the channel_id
    events = sheet_handler.fetch_future_events_from_sheet("Events", channel_id, today)

    return jsonify(events), 200
@app.route('/events', methods=['POST'])
def add_event():
    data = request.form
    # Validate the data
    if 'organizer_id' not in data or 'organizer_name' not in data:
        return jsonify({'error': 'Missing organizer_id or organizer_name'}), 400

    # Generate a unique ID for the event
    event_id = str(uuid.uuid4())

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Add the event to the Google Sheet
    row = [event_id, data['date'], data['time'], data['location'], data['organizer_id'], data['organizer_name'], data['channel_id'], timestamp]
    sheet_handler.add_to_sheet("Events", row)

    return jsonify({'event_id': event_id}), 201

@app.route('/events/<event_id>', methods=['DELETE'])
def cancel_event(event_id):
    # Cancel the event (remove it from the Google Sheet)
    result = sheet_handler.remove_event_from_sheet("Events", event_id)

    if result:
        return jsonify({'result': 'Event cancelled'}), 200
    else:
        abort(404)

@app.route('/signups/<event_id>')
def get_participants(event_id):
    participants = sheet_handler.fetch_participants_by_id('Signups', event_id)
    return jsonify(participants)

@app.route('/signups', methods=['POST'])
def add_signup():
    data = request.form

    # Validate the data
    if 'event_id' not in data or 'user_id' not in data:
        return jsonify({'error': 'Missing event_id or user_id'}), 400

    # Generate a unique ID for the signup
    signup_id = str(uuid.uuid4())

    # Get the current timestamp
    timestamp = datetime.now().isoformat()

    # Add the signup to the Google Sheet
    row = [signup_id, data['event_id'], data['user_id'], data['user_name'], timestamp]
    sheet_handler.add_to_sheet("Signups", row)

    return jsonify({'signup_id': signup_id}), 201

@app.route('/signups/<signup_id>', methods=['DELETE'])
def cancel_signup(signup_id):
    # Cancel the signup (remove it from the Google Sheet)
    result = sheet_handler.remove_signup_from_sheet("Signups", signup_id)

    if result:
        return jsonify({'result': 'Signup cancelled'}), 200
    else:
        abort(404)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)
