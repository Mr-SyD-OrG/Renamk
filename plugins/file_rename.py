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
sydtg = asyncio.Semaphore(3)   #improve Accuracy @Syd_Xyz


@Client.on_callback_query(filters.regex('rename'))
async def rename(bot, update):
    await update.message.delete()
    await update.message.reply_text("__Pʟᴇᴀꜱᴇ Eɴᴛᴇʀ Nᴇᴡ Fɪʟᴇɴᴀᴍᴇ...__💦",
                                    reply_to_message_id=update.message.reply_to_message.id,
                                    reply_markup=ForceReply(True))

# Define the main message handler for private messages with replies


@Client.on_message(filters.private & (filters.document | filters.audio | filters.video))
async def refunc(client, message):
    chat_id = message.chat.id
    file = getattr(message, message.media.value)
    syd = file.file_name
    filename = ' '.join(filter(lambda x: not x.startswith('-PrimeFix') and not x.startswith('-HDA') and not x.startswith('-PSA') and not x.startswith('-PAHE') and not x.startswith('-GalaxyRG') and not x.startswith('-Bigil') and not x.startswith('-TR') and not x.startswith('[') and not x.startswith('www.') and (not x.startswith('@') or x == '@GetTGLinks'), file.file_name.split()))
    filesize = humanize.naturalsize(file.file_size)
    mrsyd = filename.rsplit('-', 1)
    if len(mrsyd) > 1:
        new_name = mrsyd[0].strip()
    else:
        new_name = filename
    
    media = file
    if ".mkv" in new_name.lower():  # If "mkv" is already part of the name
        new_name = new_name  # Keep the name unchanged
    else:
        extn = "mkv"
        new_name = f"{new_name}.{extn}"
    #if not "." in new_name:
       # if "." in media.file_name:
           # extn = media.file_name.rsplit('.', 1)[-1]
           # if extn.lower() != "mkv":  # If the extension is not "mkv"
           # extn = "mkv"  # Keep the name unchanged if it's already "mkv
       # else:
    # Add the extension to the new_name
        
    # Extracting necessary information
    prefix = await db.get_prefix(chat_id)
    suffix = await db.get_suffix(chat_id)
    new_filename_ = new_name
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
    async with sydtg:
        ms = await client.send_message(
             chat_id=message.chat.id,
             text=f"__**{syd}**__\n\n**Downloading...⏳**"
        )
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("\n⚠️ __**{syd}**__\n\n❄️ **Dᴏᴡɴʟᴏᴀᴅ Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
        except Exception as e:
            return await ms.edit(e)

        _bool_metadata = await db.get_metadata(chat_id)


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

              
                 if er:
                     try:
                         os.remove(path)
                         os.remove(metadata_path)
                     except:
                         pass
                     return await ms.edit(str(er) + "\n\n**Error**")

             await ms.edit("**Metadata added to the file successfully ✅**\n\n⚠️ __**Please wait...**__\n\n**Tʀyɪɴɢ Tᴏ Uᴩʟᴏᴀᴅɪɴɢ....**")
        else:
             await ms.edit("__**Pʟᴇᴀꜱᴇ ᴡᴀɪᴛ...**😇__\n\n**Uᴩʟᴏᴀᴅɪɴɢ....🗯️**")
    duration = 0
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

    if c_caption:
        try:
            caption = c_caption.format(filename=new_filename, filesize=humanbytes(
                media.file_size), duration=convert(duration))
        except Exception as e:
            return await ms.edit(text=f"Yᴏᴜʀ Cᴀᴩᴛɪᴏɴ Eʀʀᴏʀ Exᴄᴇᴩᴛ Kᴇyᴡᴏʀᴅ Aʀɢᴜᴍᴇɴᴛ ●> ({e})")
    else:
        caption = f"**{new_filename}**"

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
     
    user_bot = await db.get_user_bot(Config.ADMIN[0])
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
           syd_id = await db.get_dump(chat_id)
           await client.send_document(
                syd_id,
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
