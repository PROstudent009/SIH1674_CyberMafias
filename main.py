from telethon import TelegramClient, events
from flask import Flask, render_template, request
import asyncio
import emoji
from threading import Thread
import sqlite3

# Telegram API credentials
api_id = '#your_api_id'
api_hash = '#your_api_hash'
phone = '#your_number'

# Initialize the Telegram client
client = TelegramClient('session_name', api_id, api_hash)

# Keywords and emojis to flag
suspicious_keywords = [
    'heroin', 'brown sugar', 'smack', 'horse', 'h', 'junk', 'stuff', 'chitta', 'powder', 'dragon',
    'opium', 'afeem', 'doda', 'poppy', 'o', 'gum', 'amulet', 'kali', 'bhukki', 'khus khus',
    'cannabis', 'marijuana', 'hashish', 'ganja', 'charas', 'weed', 'pot', 'bhang', 'grass', 'mary jane', 'joint', 'dope',
    'cocaine', 'coke', 'snow', 'blow', 'white', 'crack', 'dust', 'girl', 'white lady', 'flake',
    'methamphetamine', 'ice', 'crystal', 'glass', 'chalk', 'speed', 'tina', 'meth', 'crystal meth',
    'mdma', 'ecstasy', 'molly', 'x', 'e', 'adam', 'love drug', 'xtc', 'candy', 'happy pill',
    'lsd', 'lysergic acid diethylamide', 'acid', 'blotter', 'lucy', 'lemon drops', 'window pane', 'dots', 'tab', 'trips',
    'ketamine', 'k', 'special k', 'kit-kat', 'vitamin k', 'cat valium',
    'prescription drugs', 'benzodiazepines', 'opioids', 'benzos', 'downers', 'reds', 'blues', 'xanax', 'ativan', 'percs', 'oxy', 'roxy',
    'codeine', 'lean', 'purple drank', 'sizzurp', 'cough syrup', 'syrup', 'cotton candy',
    'methadone', 'fizzies', 'chocolate chip cookies', 'jungle juice', 'juice',
    'barbiturates', 'barbs', 'pink ladies', 'yellow jackets', 'blue birds',
    'synthetic cannabinoids', 'spice', 'k2', 'fake weed', 'legal high', 'black mamba', 'valium', 'snowflake', 'Viagra', 'Kamagra', 'Welgra', 'Milam', 'Nitrazepam', 'Codeine base', 'promethazine', 'Codeine', 'benzo Ephedrine',
    'Sildenafil Citrate'
]

suspicious_emojis = [emoji.emojize(':pill:'), emoji.emojize(':herb:')]

# Flask app initialization
app = Flask(_name_)

# Specify the channel ID to monitor
channel_id = '-1001753063808'

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('flagged_messages.db')
    c = conn.cursor()
    # Create a table for flagged messages if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS flagged_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER,
            message TEXT,
            channel_id INTEGER,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            bio TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Store flagged messages in the SQLite database
def store_flagged_message(sender_id, message, channel_id, user_info):
    try:
        with sqlite3.connect('flagged_messages.db') as conn:
            c = conn.cursor()
            c.execute('''
                INSERT INTO flagged_messages (sender_id, message, channel_id, username, first_name, last_name, bio)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (sender_id, message, channel_id, user_info['username'], user_info['first_name'], user_info['last_name'], user_info['bio']))
            conn.commit()
    except sqlite3.Error as e:
        print(f"SQLite error: {e}")

# Asynchronous function to get user information
# Asynchronous function to get user information
async def get_user_info(sender_id):
    try:
        user = await client.get_entity(sender_id)

        # Access user details
        return {
            "username": user.username if hasattr(user, 'username') else "No username",
            "first_name": user.first_name if hasattr(user, 'first_name') else "No first name",
            "last_name": user.last_name if hasattr(user, 'last_name') else "No last name",
            "bio": user.about if hasattr(user, 'about') else "No bio",
        }
    except Exception as e:
        print(f"Error retrieving user info: {e}")
        return {
            "username": "Unknown",
            "first_name": "Unknown",
            "last_name": "Unknown",
            "bio": "Unknown"
        }

# Asynchronous event handler for Telegram messages
@client.on(events.NewMessage(chats=int(channel_id)))
async def message_handler(event):
    message_text = event.raw_text.lower()
    sender_id = event.sender_id
    print(f"Received message: {message_text}")  # Debugging print

    # Check if the message contains suspicious keywords or emojis
    if any(keyword in message_text for keyword in suspicious_keywords) or any(e in message_text for e in suspicious_emojis):
        user_info = await get_user_info(sender_id)
        store_flagged_message(sender_id, event.raw_text, event.chat_id, user_info)
        print(f"Flagged message stored: {event.raw_text}")
        print(f"User info: {user_info}")
    else:
        print(f"Message not flagged: {message_text}")

# Flask route to display flagged messages
@app.route('/')
def index():
    conn = sqlite3.connect('flagged_messages.db')
    c = conn.cursor()
    c.execute('SELECT * FROM flagged_messages')
    messages = c.fetchall()
    conn.close()
    return render_template('index2.html', messages=messages)

# Flask route to clear messages
@app.route('/clear', methods=['POST'])
def clear_messages():
    conn = sqlite3.connect('flagged_messages.db')
    c = conn.cursor()
    c.execute('DELETE FROM flagged_messages')
    conn.commit()
    conn.close()
    return 'Flagged messages cleared.'

# Coroutine to run the Telegram client
async def run_telegram_client():
    await client.start(phone=phone)
    await client.run_until_disconnected()

# Function to run Flask and Telethon concurrently
def run_flask_and_telegram():
    # Run Flask in a separate thread
    flask_thread = Thread(target=lambda: app.run(port=5000, debug=True, use_reloader=False))
    flask_thread.start()

    # Run the Telegram client in the main thread with its asyncio event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_telegram_client())

# Main execution
if _name_ == '_main_':
    # Initialize the database
    init_db()
    
    # Start Flask and Telegram monitoring
    run_flask_and_telegram()
