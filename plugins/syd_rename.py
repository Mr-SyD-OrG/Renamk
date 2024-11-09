import random
import humanize
from helper.ffmpeg import fix_thumb, take_screen_shot
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import db, download_image
from PIL import Image
import asyncio
import logging
import re
import os
import time
from helper.utils import add_prefix_suffix, client, start_clone_bot, is_req_subscribed
from config import Config
from info import AUTH_CHANNEL

# Define a function to handle the 'rename' callback
logger = logging.getLogger(__name__)
SYD_CHATS = [-1002252619500]
MSYD = -1002464733363
processing = False
mrsydt_g = []

# Define the main message handler for private messages with replies
@Client.on_message(filters.document | filters.audio | filters.video)
async def refunc(client, message):
    if message.chat.id == MSYD:
        try:
            chat_id = MSYD
            file = getattr(message, message.media.value)
            syd = file.file_name
            
            sydfile = {
                'file_name': syd,
                'file_size': file.file_size,
                'message_id': message.id,
                'media': file,
                'message': message 
            }
            mrsydt_g.append(sydfile)
            asyncio.create_task(process_queue(client))
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await message.reply_text("An error occurred while processing your request.")
            
async def process_queue(client):
    # Process files
    
    while mrsydt_g:
        file_details = mrsydt_g.pop(0)
        await autosyd(client, file_details)
        
async def autosyd(client, file_details):
    try:
        syd = file_details['file_name']
        media = file_details['media']
        message = file_details['message']
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

        filesize = humanize.naturalsize(media.file_size)
        sydd = ['psa', 'sh3lby', 'Telly', '[', 'SH3LBY.mkv', 'bigil', 'YTS.MX', 'budgetbits', 'HDA', 'TR', 'primefix', 'GalaxyRG265', 'bone', 'Incursi0', 'StreliziA', 'ikaRos', 'lssjbroly', 'soan', 'pahe', 'poke', 'galaxytv', 'galaxyrg', 'NazzY', 'VARYG', 'MICHAEL', 'FLUX', 'RAV1NE']
            
        mrsyd = filename.rsplit('-', 1)  # Split filename from the right at the last hyphen
        new_name = mrsyd[0].strip() if len(mrsyd) > 1 and any(term in mrsyd[1].strip().lower() for term in sydd) else filename
            
        if not new_name.lower().endswith(".mkv"):
            new_name += ".mkv"
                
        pattern = r'(?P<filename>.*?)(\.\w+)?$'
        match = re.search(pattern, new_name)
        filename = match.group('filename')
        extension = match.group(2) or ''
        kinsyd = "@GetTGLinks"
        new_filename = f"{filename} {kinsyd}{extension}" 
        file_path = f"downloads/{new_filename}"
        ms = await client.send_message(
            chat_id=MSYD,
            text=f"__**{syd}**__"
        )
  
        path = await client.download_media(
            message=media,
            file_name=file_path, 
            progress=progress_for_pyrogram, 
            progress_args=(f"\n⚠️ __**{syd}**__\n", ms, time.time())
        )
     
 
        duration = media.duration if hasattr(media, 'duration') else 0
        ph_path = None
        caption = f"**{new_filename}**" 
           
        PIS = 'https://envs.sh/Arr.jpg'
        SYD_PATH = 'downloads/thumbnail.jpg'
        user_bot = await db.get_user_bot(Config.ADMIN[0])
        if media.file_size > 2000 * 1024 * 1024:
            try:
                await download_image(PIS, SYD_PATH)
                app = await start_clone_bot(client(user_bot['session']))
                filw = await app.send_document(
                    Config.LOG_CHANNEL,
                    document=file_path,
                    thumb=SYD_PATH,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("__{syd}__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                )

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
                return await ms.edit(f" Eʀʀᴏʀ {e}")
        else:
            try:
                await download_image(PIS, SYD_PATH)
                mrsy = syd
                sy = -1002498086501
                await client.send_document(
                    sy,
                    document=file_path,
                    thumb=SYD_PATH,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("__{mrsy}__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                )
            except Exception as e:
                os.remove(file_path)
                if ph_path:
                    os.remove(ph_path)
                return await ms.edit(f" Eʀʀᴏʀ {e}")

        await ms.delete()
        await message.delete()
        if ph_path:
            os.remove(ph_path)
        if file_path:
            os.remove(file_path)

    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await message.reply_text(f"An error")

