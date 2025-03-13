import sqlite3
import json
import os
from datetime import datetime
import glob
import time
import argparse
import sys

def find_cursor_db():
    """Search for the Cursor database file in common locations."""
    # Hardcoded path based on user confirmation
    hardcoded_path = r"C:\Users\philip\AppData\Roaming\Cursor\User\globalStorage\state.vscdb"
    if os.path.exists(hardcoded_path):
        print(f"Found database at confirmed location: {hardcoded_path}")
        return hardcoded_path
    
    possible_paths = [
        r"C:\Users\philip\AppData\Roaming\Cursor\User\globalStorage\state.vscdb",
        r"C:\Users\philip\AppData\Roaming\Cursor\state.vscdb",
        r"C:\Users\philip\AppData\Roaming\Cursor\User\state.vscdb",
        r"C:\Users\philip\AppData\Local\Cursor\User\globalStorage\state.vscdb",
        r"C:\Users\philip\AppData\Local\Cursor\state.vscdb"
    ]
    
    # Try the predefined paths
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Found database at: {path}")
            return path
    
    # Search in AppData directories
    search_patterns = [
        r"C:\Users\philip\AppData\**\Cursor\**\*.vscdb",
        r"C:\Users\philip\AppData\**\Cursor\**\*.db",
        r"C:\Users\philip\AppData\**\Cursor\**\state*"
    ]
    
    found_files = []
    for pattern in search_patterns:
        try:
            found_files.extend(glob.glob(pattern, recursive=True))
        except Exception as e:
            print(f"Error searching pattern {pattern}: {str(e)}")
    
    if found_files:
        print("Found potential database files:")
        for i, file in enumerate(found_files):
            print(f"{i+1}. {file} ({os.path.getsize(file)} bytes)")
        
        # Return the first found file
        return found_files[0]
    
    print("No database files found.")
    return None

def format_composer_data(composer_data, debug=False):
    """Format composer data for display."""
    try:
        data = json.loads(composer_data)
        
        if debug:
            print(f"DEBUG: Keys in composer data: {list(data.keys())}")
        
        composer_id = data.get('composerId', 'Unknown')
        created_at = data.get('createdAt', 0)
        formatted_time = datetime.fromtimestamp(created_at / 1000).strftime('%Y-%m-%d %H:%M:%S') if created_at else 'Unknown'
        
        conversation = data.get('conversation', [])
        
        if debug and conversation:
            print(f"DEBUG: First message keys: {list(conversation[0].keys())}")
        
        output = f"\n{'='*80}\n"
        output += f"COMPOSER ID: {composer_id}\n"
        output += f"CREATED: {formatted_time}\n"
        output += f"{'-'*80}\n\n"
        
        for msg in conversation:
            msg_type = msg.get('type', 0)
            role = "USER" if msg_type == 1 else "ASSISTANT" if msg_type == 2 else "SYSTEM"
            text = msg.get('text', '')
            
            if text:
                output += f"[{role}]:\n{text}\n\n"
        
        return output
    except json.JSONDecodeError:
        return f"Error parsing composer data: {composer_data[:100]}..."
    except Exception as e:
        return f"Error formatting composer data: {str(e)}"

def print_database_info(db_path):
    """Print information about the database structure."""
    if not db_path or not os.path.exists(db_path):
        print("Database file not found.")
        return
        
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Get list of tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"\nDatabase file: {db_path}")
        print(f"File size: {os.path.getsize(db_path)} bytes")
        print(f"Tables in database: {[table[0] for table in tables]}")
        
        # For each table, show structure and sample data
        for table in tables:
            table_name = table[0]
            print(f"\nTable: {table_name}")
            
            # Get column info
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()
            print(f"Columns: {[col[1] for col in columns]}")
            
            # Get row count
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            row_count = cursor.fetchone()[0]
            print(f"Row count: {row_count}")
            
            # Get sample data (first 5 rows)
            if row_count > 0:
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 5")
                sample_data = cursor.fetchall()
                print("Sample data (first 5 rows):")
                for row in sample_data:
                    print(f"  {row}")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")
    except Exception as e:
        print(f"Error: {e}")

def print_all_chats(db_path, output_file=None, debug=False):
    """Print all chats from the database."""
    if not db_path or not os.path.exists(db_path):
        print("Database file not found.")
        return
    
    # Open output file if specified
    file_handle = None
    if output_file:
        try:
            file_handle = open(output_file, 'w', encoding='utf-8')
            file_handle.write(f"Cursor Chat Data Export - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        except Exception as e:
            print(f"Error opening output file: {str(e)}")
            output_file = None
    
    def write_output(text):
        print(text)
        if file_handle:
            file_handle.write(text + "\n")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Try different queries to find chat data
        queries = [
            "SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'",
            "SELECT key, value FROM ItemTable WHERE key LIKE 'chat:%'",
            "SELECT key, value FROM ItemTable WHERE key LIKE '%chat%'"
        ]
        
        for query in queries:
            write_output(f"\nExecuting query: {query}")
            cursor.execute(query)
            results = cursor.fetchall()
            
            if not results:
                write_output("No results found for this query.")
                continue
                
            write_output(f"Found {len(results)} results.")
            
            # Process results
            if 'composerData' in query:
                for key, value in results:
                    try:
                        # Try to parse as JSON to see if it's valid composer data
                        json_data = json.loads(value)
                        if debug:
                            write_output(f"DEBUG: Keys in {key}: {list(json_data.keys())}")
                        
                        if 'conversation' in json_data and json_data['conversation']:
                            formatted_data = format_composer_data(value, debug)
                            write_output(formatted_data)
                        else:
                            write_output(f"Key: {key}, Empty conversation")
                    except Exception as e:
                        write_output(f"Error processing {key}: {str(e)}")
            elif 'chat' in query:
                for key, value in results:
                    try:
                        # Try to parse as JSON to see if it's valid chat data
                        json_data = json.loads(value)
                        if 'messages' in json_data:
                            formatted_data = format_chat_message(value)
                            write_output(formatted_data)
                        else:
                            write_output(f"Key: {key}, Value: {value[:100]}...")
                    except Exception as e:
                        write_output(f"Error processing {key}: {str(e)}")
            
        conn.close()
        
    except sqlite3.Error as e:
        write_output(f"SQLite error: {e}")
    except Exception as e:
        write_output(f"Error: {e}")
    
    # Close output file if opened
    if file_handle:
        file_handle.close()
        print(f"Chat data saved to {output_file}")

def format_chat_message(chat_data):
    """Format chat data for display."""
    try:
        data = json.loads(chat_data)
        
        # Format timestamp
        timestamp = datetime.fromtimestamp(data.get('timestamp', 0) / 1000)
        formatted_time = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        
        # Extract messages
        messages = data.get('messages', [])
        
        output = f"\n{'='*80}\n"
        output += f"CHAT ID: {data.get('id', 'Unknown')}\n"
        output += f"TIME: {formatted_time}\n"
        output += f"TITLE: {data.get('title', 'Untitled Chat')}\n"
        output += f"{'-'*80}\n\n"
        
        for msg in messages:
            role = msg.get('role', 'unknown').upper()
            content = msg.get('content', '')
            output += f"[{role}]:\n{content}\n\n"
        
        return output
    except json.JSONDecodeError:
        return f"Error parsing chat data: {chat_data[:100]}..."
    except Exception as e:
        return f"Error formatting chat: {str(e)}"

def monitor_chats(db_path, output_file=None, debug=False):
    """Monitor the database for new chats and print them to the terminal."""
    if not db_path or not os.path.exists(db_path):
        print("Database file not found.")
        return
    
    # Open output file if specified
    file_handle = None
    if output_file:
        try:
            file_handle = open(output_file, 'a', encoding='utf-8')
            file_handle.write(f"\n\n=== MONITORING STARTED AT {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ===\n\n")
        except Exception as e:
            print(f"Error opening output file: {str(e)}")
            output_file = None
    
    def write_output(text):
        print(text)
        if file_handle:
            file_handle.write(text + "\n")
    
    write_output(f"Monitoring Cursor chat database at: {db_path}")
    write_output("Waiting for new chats...\n")
    write_output("Press Ctrl+C to stop monitoring.")
    
    # Keep track of seen composer IDs
    seen_composers = set()
    
    # Get initial list of composers
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("SELECT key FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
        results = cursor.fetchall()
        for row in results:
            seen_composers.add(row[0])
        conn.close()
        
        if debug:
            write_output(f"DEBUG: Initialized with {len(seen_composers)} existing composers")
    except Exception as e:
        write_output(f"Error initializing: {str(e)}")
    
    try:
        while True:
            try:
                # Connect to the database
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                
                # Query for composer data
                cursor.execute("SELECT key, value FROM cursorDiskKV WHERE key LIKE 'composerData:%'")
                results = cursor.fetchall()
                
                if debug and len(results) > len(seen_composers):
                    write_output(f"DEBUG: Found {len(results)} composers, {len(seen_composers)} already seen")
                
                # Check for new composers
                for key, value in results:
                    if key not in seen_composers:
                        seen_composers.add(key)
                        try:
                            json_data = json.loads(value)
                            if 'conversation' in json_data and json_data['conversation']:
                                formatted_data = format_composer_data(value, debug)
                                write_output(f"\nNEW CHAT DETECTED: {key}")
                                write_output(formatted_data)
                            else:
                                if debug:
                                    write_output(f"DEBUG: New composer {key} has empty conversation")
                        except Exception as e:
                            write_output(f"Error processing new composer {key}: {str(e)}")
                
                conn.close()
                
            except sqlite3.Error as e:
                write_output(f"SQLite error: {e}")
            except Exception as e:
                write_output(f"Error: {e}")
                
            # Wait before checking again
            time.sleep(2)
    except KeyboardInterrupt:
        write_output("\nMonitoring stopped by user.")
    finally:
        if file_handle:
            file_handle.close()
            print(f"Monitoring data saved to {output_file}")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Extract and monitor Cursor chat data')
    parser.add_argument('--info', action='store_true', help='Print database information')
    parser.add_argument('--output', '-o', type=str, help='Save output to file')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug output')
    parser.add_argument('--no-monitor', action='store_true', help='Do not monitor for new chats')
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    print("Searching for Cursor database...")
    db_path = find_cursor_db()
    
    if db_path:
        if args.info:
            print("\n=== DATABASE INFORMATION ===")
            print_database_info(db_path)
        
        print("\n=== CHAT DATA ===")
        print_all_chats(db_path, args.output, args.debug)
        
        if not args.no_monitor:
            print("\n=== MONITORING FOR NEW CHATS ===")
            monitor_chats(db_path, args.output, args.debug)
    else:
        print("Could not find Cursor database file. Please check if Cursor is installed.") 