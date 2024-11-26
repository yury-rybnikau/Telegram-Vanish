from telethon import TelegramClient, types
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.errors import FloodWaitError
import csv
import logging
import asyncio
import time

api_id = YOUR_API_ID  # Your API ID
api_hash = 'YOUR_API_HASH'  # Your API HASH
client = TelegramClient('session_name', api_id, api_hash)

# Logging setup
logging.basicConfig(filename='script.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Function to get chats (including those you have left)
async def export_chats():
    await client.start()
    me = await client.get_me()

    chats = []
    async for dialog in client.iter_dialogs():
        chat = dialog.entity
        messages = await client.get_messages(chat, from_user='me', limit=1)
        if messages.total > 0:
            chat_info = {
                'chat_id': chat.id,
                'title': getattr(chat, 'title', None) or getattr(chat, 'first_name', 'No Name'),
                'username': getattr(chat, 'username', ''),
                'type': type(chat).__name__
            }
            chats.append(chat_info)

    # Save chats to a CSV file
    with open('chats_list.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['chat_id', 'title', 'username', 'type']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for chat in chats:
            writer.writerow(chat)

    print("Chat list has been saved to 'chats_list.csv'.")
    logging.info("Chat list exported and saved to file.")

# Function to get chat ID by username (e.g., @minks_new)
async def get_chat_id_by_username(username: str):
    await client.start()
    try:
        entity = await client.get_entity(username)  # Get chat entity by username
        print(f"Chat ID for {username}: {entity.id}")
        logging.info(f"Chat ID for {username}: {entity.id}")
        return entity.id
    except Exception as e:
        print(f"Failed to find chat with username {username}: {e}")
        logging.error(f"Failed to find chat with username {username}: {e}")
        return None

# Function to delete messages and leave chats from a list of IDs in a CSV file
async def delete_messages_from_csv():
    filename = input("Enter the CSV file name (default is 'chats_list.csv'): ") or 'chats_list.csv'
    chat_ids = []

    # Load chat IDs from CSV file
    try:
        with open(filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                chat_ids.append(row['chat_id'])
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return

    await delete_messages_and_leave_chats(chat_ids)

# Function to delete messages and leave a specific chat by its ID
async def delete_messages_from_chat():
    chat_id = input("Enter chat ID: ")
    await delete_messages_and_leave_chats([chat_id])

# General function to delete messages and leave chats
async def delete_messages_and_leave_chats(chat_ids):
    await client.start()
    me = await client.get_me()

    for chat_id in chat_ids:
        try:
            entity = await client.get_entity(int(chat_id))

            # Delete messages in batches of 100 to respect API limits
            offset_id = 0
            limit = 100
            total_deleted = 0

            while True:
                try:
                    messages = await client.get_messages(entity, from_user='me', limit=limit, offset_id=offset_id)
                    if not messages:
                        break

                    message_ids = [msg.id for msg in messages]
                    await client.delete_messages(entity, message_ids)
                    total_deleted += len(message_ids)
                    logging.info(f"Deleted {len(message_ids)} messages in chat ID: {chat_id}")
                    print(f"Deleted {len(message_ids)} messages in chat ID: {chat_id}")

                    offset_id = messages[-1].id
                    await asyncio.sleep(1)  # Pause to respect API rate limits
                except FloodWaitError as e:
                    wait_time = e.seconds + 5
                    logging.warning(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                    print(f"Rate limit exceeded. Waiting for {wait_time} seconds.")
                    time.sleep(wait_time)
                except Exception as e:
                    logging.error(f"Error while deleting messages in chat ID {chat_id}: {e}")
                    print(f"Error while deleting messages in chat ID {chat_id}: {e}")
                    break

            logging.info(f"Total deleted {total_deleted} messages in chat ID: {chat_id}")
            print(f"Total deleted {total_deleted} messages in chat ID: {chat_id}")

            # Leave the chat (if it is not a personal chat)
            if not isinstance(entity, (types.User, types.InputPeerUser)):
                await client(LeaveChannelRequest(entity))
                logging.info(f"Left chat ID: {chat_id}")
                print(f"Left chat ID: {chat_id}")
            else:
                logging.info(f"Cannot leave personal chat with user ID: {chat_id}")
                print(f"Cannot leave personal chat with user ID: {chat_id}")
        except Exception as e:
            logging.error(f"Error processing chat ID {chat_id}: {e}")
            print(f"Error processing chat ID {chat_id}: {e}")

# Interactive menu
def print_menu():
    print("\nSelect an action:")
    print("1. Export chats and bots where you have sent messages to a CSV file")
    print("2. Delete all your messages and leave chats listed in a CSV file")
    print("3. Delete all your messages and leave a specific chat by ID")
    print("4. Get chat ID by username (e.g., @minks_new)")
    print("0. Exit")

async def main_menu():
    while True:
        print_menu()
        choice = input("Enter action number: ")

        if choice == '1':
            await export_chats()
        elif choice == '2':
            await delete_messages_from_csv()
        elif choice == '3':
            await delete_messages_from_chat()
        elif choice == '4':
            username = input("Enter chat or bot username (e.g., @minks_new): ")
            await get_chat_id_by_username(username)
        elif choice == '0':
            print("Exiting the program.")
            break
        else:
            print("Invalid input. Please select a valid number.")

with client:
    client.loop.run_until_complete(main_menu())

