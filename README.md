# Cursor Chat Monitor

## Cursor Chat Monitor Script Explanation

The `cursor_chat_monitor.py` script is designed to monitor Cursor's state database and extract chat data in real-time. Here's how it works:

1. **Database Connection**: The script connects to Cursor's SQLite database located at `C:\Users\philip\AppData\Roaming\Cursor\User\globalStorage\state.vscdb`.

2. **Continuous Monitoring**: It runs in an infinite loop, checking for new chat entries every 5 seconds.

3. **Chat Tracking**: The script keeps track of the last processed chat ID and updates to existing chats to avoid showing the same messages multiple times.

4. **Formatted Output**: When new chats or updates are detected, they are formatted nicely and printed to the terminal, showing:
   - Chat ID
   - Timestamp
   - Chat title
   - Messages with their roles (USER/ASSISTANT)

5. **Error Handling**: The script includes robust error handling for database connection issues, file not found errors, and JSON parsing problems.

6. **Text-to-Speech**: The script uses Google Text-to-Speech (gTTS) and Pygame to read out new chat messages.

### How to run the script:

1. **Open a terminal or command prompt**
2. **Navigate to the directory containing the script**
   ```bash
   cd C:\Users\philip\Documents\cursor-narrator
   ```

3. **Run the script with options**:
   - To monitor for new chats and save output to a file:
     ```bash
     python cursor_chat_monitor.py --output cursor_chats.txt
     ```
   
4. **Enable Debug Mode**:
   ```bash
   python cursor_chat_monitor.py --debug
   ```

5. **Print All Existing Chats**:
   ```bash
   python cursor_chat_monitor.py --print-all
   ```

6. **Stop Monitoring**:
   - Press `Ctrl+C` to stop the script when you're done.

The script requires the `gTTS` and `pygame` packages for text-to-speech functionality. You can install them using:

```bash
pip install gTTS pygame
```