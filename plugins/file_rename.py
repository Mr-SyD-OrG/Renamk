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
sydtg = asyncio.Semaphore(2)   #improve Accuracy @Syd_Xyz
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
    mrsyds = ['YTS.MX', 'SH3LBY', 'Telly', 'Moviez', 'NazzY', 'PAHE', 'PrimeFix', 'HDA', 'PSA', 'GalaxyRG', '-Bigil', 'TR', '[', 'www.', '@']
    sydt_g = [
        '[Tam', '[Tamil', '[Tel', '[Telugu', '[Kan', '[Kannada', '[Mal', '[Malayalam',
        '[Eng', '[English', '[Hin', '[Hindi', '[Mar', '[Marathi', '[Ben', '[Bengali',
        '[Ind', '[Indonesian', '[Pun', '[Punjabi', '[Urd', '[Urdu', '[Guj', '[Gujarati',
        '[Bhoj', '[Bhojpuri', '[Ori', '[Odia', '[Ass', '[Assamese', '[San', '[Sanskrit',
        '[Sin', '[Sinhala', '[Ara', '[Arabic', '[Fre', '[French', '[Spa', '[Spanish',
        '[Por', '[Portuguese', '[Ger', '[German', '[Rus', '[Russian', '[Jap', '[Japanese',
        '[Kor', '[Korean', '[Ita', '[Italian', '[Chi', '[Chinese', '[Man', '[Mandarin',
        '[Tha', '[Thai', '[Vie', '[Vietnamese', '[Fil', '[Filipino', '[Tur', '[Turkish',
        '[Swe', '[Swedish', '[Nor', '[Norwegian', '[Dan', '[Danish', '[Pol', '[Polish',
        '[Gre', '[Greek', '[Heb', '[Hebrew', '[Cze', '[Czech', '[Hun', '[Hungarian',
        '[Fin', '[Finnish', '[Ned', '[Dutch', '[Rom', '[Romanian', '[Bul', '[Bulgarian',
        '[Ukr', '[Ukrainian', '[Cro', '[Croatian', '[Slv', '[Slovenian', '[Ser', '[Serbian',
        '[Afr', '[Afrikaans', '[Lat', '[Latin'
    ]
    filename = ' '.join([
        x for x in syd.split()
        if x not in sydt_g and not any(x.startswith(mrsyd) for mrsyd in mrsyds) and x != '@GetTGLinks'
    ])
    filesize = humanize.naturalsize(file.file_size)
    sydd = ['psa', 'sh3lby', 'Telly', '[', 'SH3LBY.mkv', 'bigil', 'YTS.MX', 'budgetbits', 'HDA', 'TR', 'primefix', 'GalaxyRG265', 'bone', 'Incursi0', 'StreliziA', 'ikaRos', 'lssjbroly', 'soan', 'pahe', 'poke', 'galaxytv', 'galaxyrg', 'NazzY', 'VARYG', 'MICHAEL', 'FLUX', 'RAV1NE']
    mrsyd = filename.rsplit('-', 1)  # Split filename from the right at the last hyphen
    new_name = mrsyd[0].strip() if len(mrsyd) > 1 and any(term in mrsyd[1].strip().lower() for term in sydd) else filename
    if not new_name.lower().endswith(".mkv"):
        new_name += ".mkv"
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
    media = file
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
             text=f"__**{syd}**__"
        )
        max_retries = 2
        for attempt in range(max_retries):
            try:
                path = await client.download_media(message=media, file_name=file_path, 
                                                    progress=progress_for_pyrogram, 
                                                    progress_args=(f"\n⚠️ __**{syd}**__\n\n❄️", ms, time.time()))
                if os.path.exists(path) and os.path.getsize(path) == file.file_size:
                    break  # Exit the loop if the file is downloaded successfully
                else:
                    await ms.edit(f"⚠️ {syd} \nSize mismatch detected. Attempting to re-download... ({attempt + 1}/{max_retries})")
                    os.remove(path)
            except Exception as e:
                return await ms.edit(f"⚠️ Error downloading file: {e}")
        else:
            return await ms.edit("⚠️{syd} Failed to download the file after multiple attempts.")

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
    #SyD_Xyz
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
                progress_args=("__{syd}__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))

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
           sy = syd
           await client.send_document(
                syd_id,
                document=metadata_path if _bool_metadata else file_path,
                thumb=ph_path,
                caption=caption,
                progress=progress_for_pyrogram,
                progress_args=("__{sy}__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time()))
           
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
    await message.delete()
  #SyD_Xyz
    if ph_path:
        os.remove(ph_path)
    if file_path:
        os.remove(file_path)
    if metadata_path:
        os.remove(metadata_path)
