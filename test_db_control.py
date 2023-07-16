import unittest
from unittest.mock import patch, MagicMock
from datetime import date, datetime
import uuid
import sheet_handler

class TestFetchFutureEventsFromSheet(unittest.TestCase):
    @patch.object(sheet_handler, 'add_to_sheet')
    def test_handle_new_event(self, mock_add_to_sheet):
        # Arrange
        event = MagicMock()
        expected_event_id = str(uuid.uuid4())
        expected_event_details = "Badminton Event"
        expected_date = "2022-01-01"
        expected_timestamp = datetime.now().isoformat()
        expected_user_name = "Antonio"
        expected_group_id = 1

        # Act
        sheet_handler.add_to_sheet("Events", [expected_event_id, expected_event_details, expected_date, expected_timestamp, expected_user_name, expected_group_id])

        # Assert
        mock_add_to_sheet.assert_called_once_with(
            "Events",
            [expected_event_id, expected_event_details, expected_date, expected_timestamp, expected_user_name, expected_group_id]
        )

    @patch.object(sheet_handler, 'add_to_sheet')
    def test_handle_new_signup(self, mock_add_to_sheet):
        # Arrange
        event = MagicMock()
        expected_signup_id = str(uuid.uuid4())
        expected_event_id = 1
        expected_timestamp = datetime.now().isoformat()
        expected_user_name = "Antonio"

        # Act
        sheet_handler.add_to_sheet("Signups", [expected_signup_id, expected_event_id, expected_timestamp, expected_user_name])

        # Assert
        mock_add_to_sheet.assert_called_once_with(
            "Signups",
            [expected_signup_id, expected_event_id, expected_timestamp, expected_user_name]
        )
    @patch('pygsheets.Worksheet.get_all_values')
    def test_fetch_future_events_from_sheet(self, mock_get_all_values):
        # Arrange
        mock_get_all_values.return_value = [
            ['event_id', '2023-07-20', '18:00', '1', 'User A', 'channel1', '2023-07-15'],
            ['event_id', '2023-07-21', '18:00', '2', 'User B', 'channel1', '2023-07-16'],
            ['event_id', '2023-07-22', '18:00', '3', 'User C', 'channel2', '2023-07-17'],
        ]
        expected_result = [
            ['event_id', '2023-07-21', '18:00', '2', 'User B', 'channel1', '2023-07-16'],
        ]

        # Act
        # for row in mock_get_all_values.return_value:
        #     sheet_handler.add_to_sheet("Events", row)
        result = sheet_handler.fetch_future_events_from_sheet("Events", 'channel1', date(2023, 7, 21))

        # Assert
        self.assertEqual(result, expected_result)

if __name__ == '__main__':
    unittest.main()