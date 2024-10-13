import random
import humanize
from helper.ffmpeg import fix_thumb, take_screen_shot
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db
from PIL import Image
import asyncio
import logging
import os
import time
from helper.utils import add_prefix_suffix, client, start_clone_bot, is_req_subscribed
from config import Config
from info import AUTH_CHANNEL

# Define a function to handle the 'rename' callback
logger = logging.getLogger(__name__)

@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    await update.message.delete()
    await update.message.reply_text("__Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...__💦",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

# Define the main message handler for private messages with replies


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def refunc(client, message):
    s=await message.reply_text(f"**😢 You Don'tplan**")
    await s.delete()
    chat_id = message.chat.id
    file = getattr(message, message.media.value)
    filename = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('www.') and (not x.startswith('@') or x == '@GetTGLinks'), file.file_name.split()))
    filesize = humanize.naturalsize(file.file_size)
    new_name = filename
    s=await message.reply_text(f"**1**")
    media = file
    s=await message.reply_text(f"**2**")
    if not "." in new_name:
        if "." in media.file_name:
            extn = media.file_name.rsplit('.', 1)[-1]
        else:
            extn = "mkv"
        new_name = new_name + "." + extn

    # Extracting necessary information
    s=await message.reply_text(f"**3**")
    prefix = await db.get_prefix(chat_id)
    s=await message.reply_text(f"**31**")
    suffix = await db.get_suffix(chat_id)
    s=await message.reply_text(f"**32**")
    new_filename_ = new_name
    s=await message.reply_text(f"**4**")
    try:
        # adding prefix and suffix
        new_filename = add_prefix_suffix(new_filename_, prefix, suffix)
    
    except Exception as e:
        return await client.send_message(
            chat_id=message.chat.id,
            text=f"⚠️ Something went wrong while setting <b>Prefix</b> or <b>Suffix</b> ☹️\n\n"
                 f"🎋 For support, forward this message to my creator <a href='https://t.me/Syd_Xyz'>ᴍʀ ѕчδ 🌍</a>\nError: {e}",
            parse_mode="html"
        )
    file_path = f"downloads/{new_filename}"
    file = media

    s=await message.reply_text(f"**52**")
    ms = await client.send_message(
        chat_id=message.chat.id,
        text="__**Please wait...**🥺__\n\n**Downloading...⏳**"
    )
    try:
        path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("\n⚠️ __**Please wait...**__\n\n❄️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
    except Exception as e:
        return await ms.edit(e)

    _bool_metadata = await db.get_metadata(chat_id)


    s=await message.reply_text(f"**100**")
    if (_bool_metadata):
        metadata_path = f"Metadata/{new_filename}"
        metadata = await db.get_metadata_code(update.message.chat.id)
        if metadata:

            await ms.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
            cmd = f"""ffmpeg -i "{path}" {metadata} "{metadata_path}" """

            process = await asyncio.create_subprocess_shell(
                cmd, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
            )

            stdout, stderr = await process.communicate()
            er = stderr.decode()

            try:
                if er:
                    try:
                        os.remove(path)
                        os.remove(metadata_path)
                    except:
                        pass
                    return await ms.edit(str(er) + "\n\n**Error**")
            except BaseException:
                pass
        await ms.edit("**Metadata added to the file successfully ✅**\n\n⚠️ __**Please wait...**__\n\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
    else:
        await ms.edit("__**Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...**😇__\n\n**Uᴩʟᴏᴀᴅɪɴɢ....🗯️**")

    duration = 0
    s=await message.reply_text(f"**101**")
    try:
        parser = createParser(file_path)
        metadata = extractMetadata(parser)
        if metadata.has("duration"):
            duration = metadata.get('duration').seconds
        parser.close()

    except:
        pass
    ph_path = None
    media = file
    c_caption = await db.get_caption(chat_id)
    c_thumb = await db.get_thumbnail(chat_id)
    s=await message.reply_text(f"**1002**")

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(
                media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

    s=await message.reply_text(f"**100r**")
    if (media.thumbs or c_thumb):
        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            width, height, ph_path = await fix_thumb(ph_path)
        else:
            try:
                ph_path_ = await take_screen_shot(file_path, os.path.dirname(os.path.abspath(file_path)), random.randint(0, duration - 1))
                width, height, ph_path = await fix_thumb(ph_path_)
            except Exception as e:
                ph_path = None
                print(e)
     
    s=await message.reply_text(f"**1005**")
    type = message.data.split("_")[1]
    s=await message.reply_text(f"**10055**")
    user_bot = await db.get_user_bot(Config.ADMIN[0])

    s=await message.reply_text(f"**1006**")
    if media.file_size > 2000 * 1024 * 1024:
        try:
            app = await start_clone_bot(client(user_bot['session']))

            

            filw = await app.send_document(
                Config.LOG_CHANNEL,
                document=metadata_path if _bool_metadata else file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("⚠️ __**Pʟᴇᴀꜱᴇ Wᴀɪᴛ...**__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))

            from_chat = filw.chat.id
            mg_id = filw.id
            time.sleep(2)
            await client.copy_message(message.from_user.id, from_chat, mg_id)
            await ms.delete()
            await client.delete_messages(from_chat, mg_id)
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
            if path:
                os.remove(path)
            return await ms.edit(f" Eʀʀᴏʀ {e}")

    else:

        try:
           await client.send_document(
                chat_id,
                document=metadata_path if _bool_metadata else file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("⚠️ __**Pʟᴇᴀꜱᴇ Wᴀɪᴛ...**__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
            if path:
                os.remove(path)
            return await ms.edit(f" Eʀʀᴏʀ {e}")

    await ms.delete()

    if ph_path:
        os.remove(ph_path)
    if file_path:
        os.remove(file_path)
    if metadata_path:
        os.remove(metadata_path)
