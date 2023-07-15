# Sport Event Management API

This API is designed to manage events, signups, and random videos, all backed by a Google Sheet. The application provides endpoints to create, retrieve, and delete events and signups, and fetch random videos based on a type.

## Getting Started

These instructions will help you get the project up and running on your local machine.

### Prerequisites

You will need to have Python 3.6+ and pip installed on your system.

### Installing

1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Install the required dependencies using the following command:

```bash
pip install Flask
```

Make sure to set up the Google Sheets API and include the appropriate credentials file and `client_secret.json` in your directory.

### Running the Application

You can run the application using the following command:

```bash
python3 app.py
```

#### (In DEV mode)Test the APIs with `ngork`
```
ngrok http 5001
```

## Endpoints

### `/events` (GET)

Retrieves all future events for a specific channel ID.

- Query parameter: `channel_id`

### `/events` (POST)

Adds an event to the system.

- Parameters: `date`, `time`, `organizer_id`, `organizer_name`, `channel_id`

### `/events/<event_id>` (DELETE)

Cancels an event by its unique ID.

### `/signups/<event_id>` (GET)

Fetches participants for a given event ID.

### `/signups` (POST)

Adds a signup to an event.

- Parameters: `event_id`, `user_id`, `user_name`

### `/signups/<signup_id>` (DELETE)

Cancels a signup by its unique ID.

### `/videos/<video_type>` (GET)

Sends a random video from the Google Sheet based on the specified video type.

## Contributing

Feel free to fork the repository and submit pull requests.
