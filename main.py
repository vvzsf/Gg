import asyncio
import sys
import logging
from os import environ
from dotenv import load_dotenv
from pyrogram import Client
from pyrogram.types import Chat, User
from pyrogram.errors import FloodWait

load_dotenv('config.env', override=True)

BOT_TOKEN = environ.get('BOT_TOKEN', '')
if len(BOT_TOKEN) == 0:
  logging.error("BOT_TOKEN variable is missing! Exiting now")
  exit(1)

TELEGRAM_API = environ.get('TELEGRAM_API', '')
if len(TELEGRAM_API) == 0:
  logging.error("TELEGRAM_API variable is missing! Exiting now")
  exit(1)
else:
  TELEGRAM_API = int(TELEGRAM_API)

TELEGRAM_HASH = environ.get('TELEGRAM_HASH', '')
if len(TELEGRAM_HASH) == 0:
  logging.error("TELEGRAM_HASH variable is missing! Exiting now")
  exit(1)

logging.basicConfig(stream=sys.stdout,
                    level=logging.INFO,
                    format='%(asctime)s | %(levelname)s | %(message)s')

app = Client('z_bot', TELEGRAM_API, TELEGRAM_HASH, bot_token=BOT_TOKEN)

logging.info('Bot Started Successfully!')


async def delete_message(client, message, delay):
  await asyncio.sleep(delay)
  try:
    if message.sender_chat and message.sender_chat.type == 'bot':
      await client.delete_messages(chat_id=message.chat.id,
                                   message_ids=message.id)
      logging.info(
        f'Deleted message from Bot: {message.sender_chat.username} | Msg: {message.text}'
      )
    elif isinstance(
        message.from_user,
        User) and not message.from_user.status in ["administrator", "creator"]:
      await client.delete_messages(chat_id=message.chat.id,
                                   message_ids=message.id)
      logging.info(
        f'Deleted message from User: {message.from_user.first_name} | Username: {message.from_user.username} | User ID: {message.from_user.id} | Msg: {message.text}'
      )
    elif isinstance(message.sender_chat, Chat):
      await client.delete_messages(chat_id=message.chat.id,
                                   message_ids=message.id)
      logging.info(
        f'Deleted message from Chat: {message.chat.title} | Chat ID: {message.chat.id} | Msg: {message.text}'
      )
  except FloodWait as e:
    await asyncio.sleep(e.x)
    logging.warning(f'Flood wait: {e}')


@app.on_message()
async def my_handler(client, message):
  asyncio.ensure_future(delete_message(client, message, 60))
  try:
    if message.sender_chat and message.sender_chat.type == 'bot':
      logging.info(
        f'Deleted message from Bot: {message.sender_chat.username} | Msg: {message.text}'
      )
    if isinstance(message.from_user, User):
      logging.info(
        f'Received message from User: {message.from_user.first_name} | Username: {message.from_user.username} | User ID: {message.from_user.id} | Msg: {message.text}'
      )
    elif isinstance(message.sender_chat, Chat):
      logging.info(
        f'Received message from Chat: {message.chat.title} | Chat ID: {message.chat.id} | Msg: {message.text}'
      )
  except AttributeError as e:
    logging.error(f'{e}')
    pass


app.run()