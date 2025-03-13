# Cursor Chat Monitor

A Python script that monitors and extracts chat data from Cursor's state database in real-time.

## Description

This script connects to Cursor's SQLite database (`state.vscdb`) and continuously monitors it for new chat entries. When new chats are detected, they are formatted and printed to the terminal.

## Requirements

- Python 3.6+
- SQLite3 (included in Python standard library)

## Usage

1. Make sure Cursor is installed on your system
2. Run the script:

```bash
python cursor_chat_monitor.py
```

3. The script will continuously monitor for new chats and print them to the terminal
4. Press `Ctrl+C` to stop the monitoring

## Features

- Real-time monitoring of new chat entries
- Formatted display of chat messages with timestamps
- Tracks the last processed chat ID to avoid duplicates
- Handles database connection errors gracefully

## Notes

- The script is configured to look for the database at: `C:\Users\philip\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`
- If your Cursor database is located elsewhere, modify the `DB_PATH` variable in the script
- The script creates a `last_processed_id.txt` file to keep track of which chats have already been processed 