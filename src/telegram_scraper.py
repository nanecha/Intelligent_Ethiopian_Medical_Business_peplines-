# import
import json
from datetime import datetime
from pathlib import Path
import logging
from telethon.sync import TelegramClient
from telethon.tl.types import MessageMediaPhoto

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('telegram_scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


async def scrape_telegram_channels(api_id, api_hash, channels, data_lake_path=
                                   'F:/Intelligent_Ethiopian_Medical_Business_peplines-/data/raw/telegram_messages'):
    """
    Scrape messages and images from specified Telegram, 
    channels and store in a data lake.

    Args:
        api_id (str): Telegram API ID
        api_hash (str): Telegram API Hash
        channels (list): List of Telegram channel URLs or usernames (e.g., ['@Chemed123', 't.me/lobelia4cosmetics'])
        data_lake_path (str): Base path for data lake storage

    Returns:
        list: List of paths to saved JSON files
    """
    try:
        # Initialize Telegram client
        client = TelegramClient('session_name', api_id, api_hash)
        await client.start()
        logger.info("Telegram client initialized")

        # Set up data lake directory
        DATA_LAKE_PATH = Path(data_lake_path)
        DATA_LAKE_PATH.mkdir(parents=True, exist_ok=True)

        saved_files = []

        # Process each channel
        for channel_url in channels:
            try:
                # Normalize channel URL or username
                channel_name = channel_url.split('/')[-1] if 't.me' in channel_url else channel_url.lstrip('@')
                logger.info(f"Processing channel: {channel_name}")

                # Resolve channel entity
                channel = await client.get_entity(channel_url)

                # Get current date for partitioning
                current_date = datetime.now().strftime('%Y-%m-%d')
                output_dir = DATA_LAKE_PATH / current_date / channel_name
                output_dir.mkdir(parents=True, exist_ok=True)

                # Scrape messages
                messages_data = []
                async for message in client.iter_messages(channel, limit=100):  # Adjust limit as needed
                    try:
                        msg_data = {
                            'message_id': message.id,
                            'date': message.date.isoformat(),
                            'text': message.text or '',
                            'sender_id': message.sender_id,
                            'views': message.views or 0,
                            'forwards': message.forwards or 0,
                            'media': None
                        }

                        # Handle media (photos)
                        if isinstance(message.media, MessageMediaPhoto):
                            try:
                                photo_path = output_dir / f"photo_{message.id}.jpg"
                                await message.download_media(file=str(photo_path))
                                msg_data['media'] = str(photo_path)
                                logger.info(f"Downloaded photo for message {message.id} to {photo_path}")
                            except Exception as e:
                                logger.error(f"Error downloading media for message {message.id}: {str(e)}")

                        messages_data.append(msg_data)
                    except Exception as e:
                        logger.error(f"Error processing message {message.id} in {channel_name}: {str(e)}")
                        continue

                # Save messages to JSON
                if messages_data:
                    output_file = output_dir / 'messages.json'
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(messages_data, f, ensure_ascii=False, indent=2)
                    logger.info(f"Saved {len(messages_data)} messages to {output_file}")
                    saved_files.append(str(output_file))
                else:
                    logger.warning(f"No messages scraped for {channel_name}")

            except Exception as e:
                logger.error(f"Error processing channel {channel_name}: {str(e)}")
                continue

        await client.disconnect()
        logger.info("Telegram client disconnected")
        return saved_files

    except Exception as e:
        logger.error(f"Fatal error in scrape_telegram_channels: {str(e)}")
        raise
   

if __name__ == "__main__":
    pass 


# for displaying some of the message
def print_messages_from_data_lake(data_lake_path=
                                  'F:/Intelligent_Ethiopian_Medical_Business_peplines-/data/raw/telegram_messages'):
    """
    Reads and prints a sample of messages from the data lake.

    Args:
        data_lake_path (str): Base path for data lake storage
    """
    DATA_LAKE_PATH = Path(data_lake_path)

    if not DATA_LAKE_PATH.exists():
        print(f"Data lake path not found: {data_lake_path}")
        return

    print(f"Looking for message files in: {data_lake_path}")
    # Find all messages.json files within the data lake structure
    message_files = list(DATA_LAKE_PATH.rglob('messages.json'))

    if not message_files:
        print("No 'messages.json' files found in the data lake.")
        return

    print(f"Found {len(message_files)} message files.")

    for msg_file in message_files:
        try:
            with open(msg_file, 'r', encoding='utf-8') as f:
                messages = json.load(f)
                print(f"\n--- Messages from {msg_file} ---")
                # Print a sample of messages
                for i, msg in enumerate(messages[:5]): # Print first 5 messages
                    print(f"  Message ID: {msg['message_id']}")
                    print(f"  Date: {msg['date']}")
                    print(f"  Text: {msg['text'][:100]}...")
                    print("-" * 20)
                if len(messages) > 5:
                    print(f"  ... and {len(messages) - 5} more messages.")

        except Exception as e:
            print(f"Error reading file {msg_file}: {str(e)}")
