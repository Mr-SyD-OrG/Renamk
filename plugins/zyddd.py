import asyncio
from telethon import TelegramClient, events
from asyncio import Semaphore
from info import *
# Telegram API credentials
api_id = SYD_CODEE  # Replace with your API ID
api_hash = SYD_CODEEE  # Replace with your API Hash
phone_number = SYD_CODEEEE  # Your phone number
app_password = SYD_CODE  # Use App Password if 2FA is enabled

# Chat IDs
SOURCE_CHAT_ID = -1001234567890  # Replace with chat X (source)
DESTINATION_CHAT_ID = -1009876543210  # Replace with chat Y (destination)

# Create Telegram client session
client = TelegramClient("userbot_session", api_id, api_hash)

# Semaphore to limit concurrent forwards (1 at a time)
semaphore = Semaphore(2)

async def forward_message(event):
    async with semaphore:  # Ensures only 1 message is forwarded at a time
        try:
            print(f"Forwarding message from {SOURCE_CHAT_ID} to {DESTINATION_CHAT_ID}...")
            await client.send_message(DESTINATION_CHAT_ID, event.message)
            print("Message forwarded successfully!")
            
            # Wait for 90 seconds before processing the next message
            #print("Waiting 90 seconds before next message...")
            await asyncio.sleep(124)

        except Exception as e:
            print(f"Error forwarding message: {e}")

@client.on(events.NewMessage(chats=SOURCE_CHAT_ID))
async def handler(event):
    await forward_message(event)

async def main():
    await client.start(phone_number, password=app_password)  # Auto-login
    print("Userbot is running...")
    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
