# Telegram Vanish

**Telegram Vanish** is a Python script that allows users to delete their messages in Telegram groups and channels. Additionally, it helps you leave unwanted chats after messages are deleted.

## Features

- **Export Chats**: Export the list of chats and groups where you have sent messages into a CSV file.
- **Delete Messages**: Remove all your messages from selected chats or groups using a CSV file.
- **Leave Chats**: Leave groups or channels after deleting all your messages.
- **User-Friendly Menu**: Interactive command-line menu for easy usage.

## Prerequisites

- Python 3.7 or higher
- `telethon` library
- `asyncio`
- `csv`
- `logging`
- Telegram API credentials (API ID and API Hash)

## Installation

1. Clone the repository:

   ```sh
   git clone https://github.com/yourusername/Telegram-Vanish.git
   cd Telegram-Vanish
   ```

2. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

3. Set your Telegram API credentials in the script:

   ```python
   api_id = YOUR_API_ID
   api_hash = 'YOUR_API_HASH'
   ```

## Usage

Run the script by executing:

```sh
python telegram_vanish.py
```

You will be prompted with the following options:

1. **Export Chats**: Export all the chats where you have posted messages into a CSV file named `chats_list.csv`.
2. **Delete Messages from CSV**: Delete all your messages in chats listed in a CSV file (`chats_list.csv`).
3. **Delete Messages from Specific Chat**: Enter the chat ID to delete your messages from that particular chat.

## Example

- To delete messages from all your chats listed in `chats_list.csv`, select option 2 from the menu.

## Logging

All actions are logged into `script.log` for tracking.

## Note

- The script respects Telegram API limits and handles rate-limiting automatically.
- Make sure to use the script responsibly, as excessive usage could lead to temporary bans by Telegram.

## License

This project is licensed under the MIT License. 


