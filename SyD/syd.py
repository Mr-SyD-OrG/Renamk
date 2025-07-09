import random
import logging
from pyrogram import Client, filters, enums
from pyrogram.enums import ParseMode
from pyrogram.errors import FloodWait, ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto, CallbackQuery
from helper.database import db
from config import Config, Txt

import humanize
from time import sleep
users = db.users
logger = logging.getLogger(__name__)

@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
   # await db.add_user(client, message)
    button = InlineKeyboardMarkup([[
        InlineKeyboardButton(
            'ᴜᴘᴅᴀᴛᴇꜱ', url='https://t.me/Bot_Cracker'),
        InlineKeyboardButton(
            'ꜱᴜᴘᴘᴏʀᴛ', url='https://t.me/+O1mwQijo79s2MjJl')],
        [InlineKeyboardButton('ᴏᴡɴᴇʀ', user_id=1733124290)
    ], [
        InlineKeyboardButton('ʙᴏᴛꜱ', url='https://t.me/Bot_Cracker/17'),
        InlineKeyboardButton('ᴜᴩᴅᴀᴛᴇꜱ', url='https://t.me/Mod_Moviez_X')]])
    if Config.PICS:
        await message.reply_photo(random.choice(Config.PICS), caption=Txt.START_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.START_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


@Client.on_message(filters.private & filters.command("disclaimer"))
async def disclaimer(client, message):
    await message.reply_text(
        text="""ᴅɪꜱᴄʟᴀɪᴍᴇʀ:
                ɴᴇᴠᴇʀ ꜱᴇɴᴅ ᴩᴇʀꜱᴏɴᴀʟ ꜰɪʟᴇꜱ, ꜱɪɴᴄᴇ ᴛʜᴇʏ ᴀʀᴇ ꜱᴛᴏʀᴇᴅ ᴛᴏ ꜰɪɴᴅ ᴀɴʏ ꜱᴜꜱᴩɪᴄɪᴏᴜꜱ ᴀᴄᴛɪᴠɪᴛʏ ᴅᴏɴᴇ ʙʏ ᴛʜᴇ ᴜꜱᴇʀꜱ
                ᴀʟᴡᴀʏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ ᴩʀᴏᴩᴇʀʟʏ ᴀɴᴅ ᴛᴀᴋᴇ ʀᴇꜱᴩᴏɴꜱɪʙɪʟᴛʏ ᴏꜰ ᴛʜᴇ ꜰɪʟᴇ, ᴛʜᴇʏ ᴀʀᴇ ʏᴏᴜʀ ᴩʀᴏᴩᴇʀᴛɪᴇꜱ ꜱᴏ ᴛʜᴇ ꜰɪʟᴇꜱ ᴀᴛ ʏᴏᴜʀ ᴏᴡɴ ʀɪꜱᴋ.
                ꜱʜᴀʀɪɴɢ ᴀᴅᴜʟᴛ ꜰɪʟᴇꜱ ᴡɪʟʟ ʟᴇᴀᴅ ᴛᴏ ʏᴏᴜʀ ʙᴀɴ, ᴀɴᴅ ꜰᴜʀᴛʜᴇʀ ʏᴏᴜ ᴍᴀʏ ɴᴏᴛ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴜꜱᴇ ᴛʜᴇ ʙᴏᴛ.""", 
        disable_web_page_preview=True
    )


from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

@Client.on_message(filters.private & filters.video)
async def ask_convert_button(client, message):
    if message.video.duration > 30:
        await message.reply("❌ Video too long! Max 30 seconds allowed.")
        return

    await message.reply(
        "Do you want to convert this video into a sticker?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎨 Convert", callback_data=f"convert_{message.id}")]]
        )
    )
import os
import ffmpeg
import asyncio

@Client.on_callback_query(filters.regex("^convert_"))
async def convert_video_to_sticker(client, callback_query):
    user_id = callback_query.from_user.id
    username = callback_query.from_user.username or f"user{user_id}"
    message_id = int(callback_query.data.split("_")[1])

    bot_info = await client.get_me()
    sticker_set_name = f"{username}_by_{bot_info.username}"

    # Check MongoDB if user already has sticker set name
    user_data = users.find_one({"user_id": user_id})
    if user_data:
        sticker_set_name = user_data["sticker_set"]
    else:
        users.insert_one({"user_id": user_id, "sticker_set": sticker_set_name})

    await callback_query.answer("⏳ Converting, please wait...", show_alert=True)

    # Get original video message
    message = await client.get_messages(callback_query.message.chat.id, message_id)

    # File paths
    temp_video = f"{user_id}_{message.id}.mp4"
    temp_webm = f"{user_id}_{message.id}.webm"

    # Download
    await message.download(temp_video)

    # Convert in background thread to avoid blocking
    loop = asyncio.get_event_loop()
    try:
        await loop.run_in_executor(None, convert_to_webm_ffmpeg, temp_video, temp_webm)
    except Exception as e:
        await callback_query.message.reply(f"❌ Conversion failed: {e}")
        os.remove(temp_video)
        return

    # Create or add to sticker set
    try:
        await client.get_sticker_set(sticker_set_name)
    except:
        # Create new sticker set
        try:
            await client.create_new_sticker_set(
                user_id=user_id,
                name=sticker_set_name,
                title=f"{username}'s Stickers",
                webm_stickers=[temp_webm],
                emojis=["😎"]
            )
        except Exception as e:
            await callback_query.message.reply(f"❌ Failed to create sticker set: {e}")
            cleanup(temp_video, temp_webm)
            return
    else:
        # Add to existing sticker set
        try:
            await client.add_sticker_to_set(
                user_id=user_id,
                name=sticker_set_name,
                webm_sticker=temp_webm,
                emojis="😎"
            )
        except Exception as e:
            await callback_query.message.reply(f"❌ Failed to add sticker: {e}")
            cleanup(temp_video, temp_webm)
            return

    await callback_query.message.reply(
        f"✅ Added to [sticker set](https://t.me/addstickers/{sticker_set_name})!",
        disable_web_page_preview=True
    )

    cleanup(temp_video, temp_webm)


def convert_to_webm_ffmpeg(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .filter('scale', 512, 512, force_original_aspect_ratio='decrease')
        .filter('pad', 512, 512, -1, -1, color='0x00000000')
        .output(output_path,
                vcodec='libvpx-vp9',
                **{'b:v': '500K'},
                an=None,
                r=30
        )
        .run(overwrite_output=True)
    )


def cleanup(*files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)


    
@Client.on_message(filters.command("start") & filters.chat(-1002687879857))
async def sydstart(client, message):
    await message.reply_text(".")
