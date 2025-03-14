# Query Messages Script

This script, `query_messages.py`, is designed to interact with an SQLite database to fetch and process messages, and then use a text-to-speech (TTS) engine to read them aloud.

## Features
- Connects to a specified SQLite database.
- Lists all tables in the database.
- Continuously checks for new messages in the `cursorDiskKV` table.
- Uses a TTS engine to read messages aloud.

## Requirements
- Python 3.x
- `sqlite3` library (usually included with Python)
- `pyttsx3` library for text-to-speech functionality

## Installation
1. Ensure Python 3.x is installed on your system.
2. Install the `pyttsx3` library using pip:
   ```bash
   pip install pyttsx3
   ```

## Usage
1. Update the `db_path` variable in the script to point to your SQLite database file.
2. Run the script:
   ```bash
   python query_messages.py
   ```
3. The script will list all tables in the database and continuously check for new messages in the `cursorDiskKV` table.
4. New messages will be read aloud using the TTS engine.

## Notes
- Ensure the database path is correct and accessible.
- The script runs indefinitely, checking for new messages every 5 seconds.

## Troubleshooting
- If you encounter a `JSONDecodeError`, ensure the data in the database is correctly formatted as JSON.
- Verify that the `pyttsx3` library is installed and functioning correctly.

## License
This project is licensed under the MIT License. 