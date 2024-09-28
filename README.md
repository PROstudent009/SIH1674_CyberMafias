    Libraries Used:
        Telethon: Used for interacting with Telegram API.
        Flask: For creating a simple web application.
        sqlite3: For storing flagged messages locally in an SQLite database.
        emoji: To work with emojis.
        asyncio & threading: To manage asynchronous tasks and run Flask and Telegram client concurrently.

    Main Components:
        Telegram Client: Monitors a specified Telegram channel for messages.
        Flagging Logic: Messages containing specific keywords or emojis are flagged.
        SQLite Storage: Flagged messages along with the sender’s information are stored in a local SQLite database.
        Flask App: Displays flagged messages in a web interface and allows clearing messages.

System Flow:

    Initialization:
        The Telegram client is initialized using API credentials.
        A connection to SQLite is created to store flagged messages.

    Telegram Monitoring:
        A background process listens for new messages in a specified Telegram channel.
        If a message contains suspicious keywords or emojis, the sender’s information is retrieved asynchronously, and the message is stored in the SQLite database.

    Flask Web Interface:
        A web interface (/) displays all flagged messages retrieved from the SQLite database.
        There is an option to clear the flagged messages using the /clear route.

    Concurrency:
        Flask and the Telegram client run concurrently, where Flask runs in a separate thread, and the Telegram client operates using the asyncio event loop.

1. Open Visual Studio Code with latest version.
2. Create an app.py file and paste the above code.
3. Install and import all the necessary files listed in the requirements.txt file.
4. The user will be able to access the chats of a particular group in Telegram.
5. Go to the given web address to access the flagged messages.
6. Refresh the page in case of new chats to be discovered.
