import sqlite3
import json
import pyttsx3
import time

# Path to the SQLite database
db_path = r"C:\Users\philip\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"

# Connect to the database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Query to list all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")

# Fetch and print all table names
print("Tables in the database:")
for table in cursor.fetchall():
    print(table[0])

# Initialize the TTS engine
engine = pyttsx3.init()

# Function to speak text
speak = lambda text: engine.say(text) or engine.runAndWait()

# Set to store keys of processed messages
processed_keys = set()

# Initialize start_timestamp to None
start_timestamp = None

# Flag to check if it's the first loop
first_loop = True

while True:

    # cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
    cursor.execute("SELECT key, value FROM cursorDiskKV")
    print('processing start')

    # Fetch and read all messages
    for key, value in cursor.fetchall():
        if key not in processed_keys:
            print(key)
            try:
                data = json.loads(value)
                messages = data.get('conversation', [])
                for message in messages:
                    message_timestamp = message.get('timestamp', 0)
                    # On the first loop, set start_timestamp to the most recent message's timestamp
                    if first_loop:
                        start_timestamp = max(start_timestamp or 0, message_timestamp)
                    print(message_timestamp)
                    print(start_timestamp)
                    if message_timestamp > start_timestamp:
                        text = message.get('text', '')
                        print(f"[{['SYSTEM', 'USER', 'ASSISTANT'][message.get('type', 0)]}]: {text}")
                        speak(text)
                processed_keys.add(key)
            except json.JSONDecodeError:
                print(f"Error decoding JSON for key: {key}")

    # End of first loop
    first_loop = False

    # Wait for 5 seconds before checking again
    print('processing end')
    time.sleep(1)

# Close the connection
conn.close() 