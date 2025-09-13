import random
import logging
import sys
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, CallbackQuery
from config import Config, Txt
import humanize
from time import sleep

logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            '⛅ Uᴘᴅᴀᴛᴇꜱ', url='https://t.me/Bot_Cracker'),
        InlineKeyboardButton(
            ' Sᴜᴘᴘᴏʀᴛ 🌨️', url='https://t.me/+O1mwQijo79s2MjJl')
    ], [
        InlineKeyboardButton('❄️ Δʙᴏᴜᴛ', callback_data='about'),
        InlineKeyboardButton('βᴏᴛꜱ ⚧️', url='https://t.me/Bot_Cracker/17'),
        InlineKeyboardButton(' Hᴇʟᴩ ❗', callback_data='help')
    ], [InlineKeyboardButton('⚙️ sᴛΔᴛs ⚙️', callback_data='stats')]])
    if Config.PICS:
        await message.reply_photo(random.choice(Config.PICS), caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)

@Client.on_message(filters.command("start") & filters.chat(-1002687879857))
async def sydstart(client, message):
    await message.reply_text(".")


import re
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



@Client.on_message(filters.command("addbutton") & filters.private)
async def addbutton(client, message):
    try:
        await message.reply("📌 Forward the message OR send its ID/link (public/private channel).")

        user_input = await client.listen(message.chat.id)

        channel_id = None
        msg_id = None

        # Case 1: Forwarded message
        if user_input.forward_from_chat:
            channel_id = user_input.forward_from_chat.id
            msg_id = user_input.forward_from_message_id

        # Case 2: Just a number (message ID in the same chat/channel)
        elif user_input.text and user_input.text.isdigit():
            msg_id = int(user_input.text)
            channel_id = message.chat.id  # ⚠️ set your channel_id manually here if needed

        # Case 3: Link (public or private)
        elif user_input.text:
            text = user_input.text.strip()

            # Public channel: https://t.me/username/123
            pub_match = re.match(r"https?://t\.me/([a-zA-Z0-9_]+)/(\d+)", text)
            # Private channel: https://t.me/c/123456789/123
            priv_match = re.match(r"https?://t\.me/c/(\d+)/(\d+)", text)

            if pub_match:
                username, msg_id = pub_match.groups()
                msg_id = int(msg_id)
                chat = await client.get_chat(username)
                channel_id = chat.id

            elif priv_match:
                chat_id, msg_id = priv_match.groups()
                # private "c/" links have chat_id without -100 prefix → must add it
                channel_id = int(f"-100{chat_id}")
                msg_id = int(msg_id)

        if not channel_id or not msg_id:
            await message.reply("❌ Couldn’t detect channel/message. Please forward the message or send a valid link/ID.")
            return

        # Step 2: Collect buttons
        buttons = []
        await message.reply("➕ Send buttons in format:\n`text|url|row`\nSend /end when finished.")

        while True:
            btn_msg = await client.listen(message.chat.id)

            if btn_msg.text and btn_msg.text.lower() == "/end":
                break

            try:
                text, url, row = map(str.strip, btn_msg.text.split("|"))
                row = int(row) - 1  # convert to zero-based index

                while len(buttons) <= row:
                    buttons.append([])

                buttons[row].append(InlineKeyboardButton(text=text, url=url))
            except Exception as e:
                await message.reply(f"⚠️ Invalid format. Use: `text|url|row`\nError: {e}")
                continue

        # Step 3: Edit the message
        await client.edit_message_reply_markup(
            chat_id=channel_id,
            message_id=msg_id,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        await message.reply("✅ Buttons added successfully!")

    except Exception as e:
        await message.reply(f"🚨 Unexpected error: `{e}`")
