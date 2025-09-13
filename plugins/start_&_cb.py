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


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command("addbutton") & filters.private)
async def addbutton(client, message):
    try:
        # Step 1: Ask for a forwarded message
        await message.reply("📌 Please forward me the message from the channel that you want to edit.")

        forwarded = await client.listen(message.chat.id)

        if not forwarded.forward_from_chat:
            await message.reply("❌ You must forward a message from a channel.")
            return

        channel_id = forwarded.forward_from_chat.id
        msg_id = forwarded.forward_from_message_id

        # Step 2: Loop for button creation
        buttons = []
        await message.reply("➕ Send button info in format:\n`text|url|row`\nSend /end when finished.")

        while True:
            btn_msg = await client.listen(message.chat.id)

            if btn_msg.text and btn_msg.text.lower() == "/end":
                break

            try:
                text, url, row = map(str.strip, btn_msg.text.split("|"))
                row = int(row) - 1  # convert to zero-based index

                # Ensure rows exist
                while len(buttons) <= row:
                    buttons.append([])

                buttons[row].append(InlineKeyboardButton(text=text, url=url))
            except Exception as e:
                await message.reply(f"⚠️ Invalid format. Use: `text|url|row`\nError: {e}")
                continue

        # Step 3: Edit the forwarded message in the channel
        await client.edit_message_reply_markup(
            chat_id=channel_id,
            message_id=msg_id,
            reply_markup=InlineKeyboardMarkup(buttons)
        )

        await message.reply("✅ Buttons added successfully!")

    except Exception as e:
        await message.reply(f"🚨 Unexpected error: `{e}`")
