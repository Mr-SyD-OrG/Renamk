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
from aiolimiter import AsyncLimiter
import time
import logging
import re
import os
import time
from helper.utils import add_prefix_suffix, client, start_clone_bot, is_req_subscribed
from config import Config
from info import AUTH_CHANNEL


edit_limiter = AsyncLimiter(max_rate=1, time_period=1)
file_counter = 0  # Tracks processed files
total_files_processed = 0  # Tracks total processed files to ensure final edits
batch_size = 88
last_edit_time = 0

# Define a function to handle the 'rename' callback
logger = logging.getLogger(__name__)
SYD_CHATS = [-1002252619500]
MSYD = -1002332730533
MRSSSYD = -1002464733363
MRSSYD = -1002429058090
MRSSSSYD = -1002433450358
MRSSSSSYD = -1002280144341
processing = False
mrsydt_g = []
sydtg = -1002305372915
Syd_T_G = -1002160523059


def message_count(text, pattern, default_value):
    match = re.search(pattern, text)
    if match:
        current_count = int(match.group(1))
        new_count = current_count + 1
        syd = match.group(0).split(':')[0].strip()
        new_text = re.sub(pattern, f"{syd} : {new_count}", text)
    else:
        # Add the missing count if the pattern is not found
        new_text = f"{text}\n{default_value} : 1"  # Removed '<>' for consistency
    return new_text
    
def thesyd_message(text):
    text = message_count(text, r"ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : (\d+)", "ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ :")
    text = message_count(text, r"#1 ʀᴇᴍᴀɪɴɪɴɢ : (\d+)", "#1 ʀᴇᴍᴀɪɴɪɴɢ :")
    return text

def thesydd_message(text):
    text = message_count(text, r"ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : (\d+)", "ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ :")
    text = message_count(text, r"#2 ʀᴇᴍᴀɪɴɪɴɢ : (\d+)", "#2 ʀᴇᴍᴀɪɴɪɴɢ :")
    return text

def thesyddd_message(text):
    text = message_count(text, r"ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : (\d+)", "ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ :")
    text = message_count(text, r"#3 ʀᴇᴍᴀɪɴɪɴɢ : (\d+)", "#3 ʀᴇᴍᴀɪɴɪɴɢ :")
    return text
        
def syd_message(text):
    match = re.search(r"ʀᴇᴍᴀɪɴɪɴɢ : (\d+)", text)
    if match:
        current_count = int(match.group(1))
        new_count = current_count + 1
        new_text = re.sub(r"ʀᴇᴍᴀɪɴɪɴɢ : \d+", f"ʀᴇᴍᴀɪɴɪɴɢ : {new_count}", text)
        return new_text
    else:
        return "ʀᴇᴍᴀɪɴɪɴɢ : 1 [ᴇʀʀᴏʀ]"

def sydd_message(text):
    match = re.search(r"#2 ʀᴇᴍᴀɪɴɪɴɢ :  (\d+)", text)
    if match:
        current_count = int(match.group(1))
        new_count = current_count - 1
        new_text = re.sub(r"#2 ʀᴇᴍᴀɪɴɪɴɢ : \d+", f"#2 ʀᴇᴍᴀɪɴɪɴɢ : {new_count}", text)
        return new_text
    else:
        return "#2 ʀᴇᴍᴀɪɴɪɴɢ : 1 [ᴇʀʀᴏʀ]"
        
def syddd_message(text):
    match = re.search(r"#3 ʀᴇᴍᴀɪɴɪɴɢ :  (\d+)", text)
    if match:
        current_count = int(match.group(1))
        new_count = current_count - 1
        new_text = re.sub(r"#4 ʀᴇᴍᴀɪɴɪɴɢ : \d+", f"#3 ʀᴇᴍᴀɪɴɪɴɢ : {new_count}", text)
        return new_text
    else:
        return "#3 ʀᴇᴍᴀɪɴɪɴɢ : 1 [ᴇʀʀᴏʀ]"

async def limited_edit(client, syd_id, mrsyd_id, new_text):
    async with edit_limiter:
        await client.edit_message_text(chat_id=syd_id, message_id=mrsyd_id, text=new_text)


async def batch_edit(client, syd_id, mrsyd_id, syd_text, update_func, final=False):
    global file_counter
    global total_files_processed

    file_counter += 1
    total_files_processed += 1
    if file_counter % batch_size == 0 or final:
        new_text = update_func(syd_text)
        await limited_edit(client, syd_id, mrsyd_id, new_text)
        file_counter = 0 if final else file_counter

# Define the main message handler for private messages with replies
@Client.on_message(filters.document | filters.audio | filters.video)
async def refunc(client, message):
    global processing
    syd_id = {MRSSSYD, MRSSYD, MRSSSSYD, MRSSSSSYD}
    if message.chat.id in syd_id :
        try:
          #  chat_id = MSYD
            file = getattr(message, message.media.value)
            if not file:
                return
            if file.file_size > 2000 * 1024 * 1024:  # > 2 GB
                from_syd = message.chat.id
                syd_id = message.id
                await client.copy_message(sydtg, from_syd, syd_id)
                await message.delete()
                return
            if file.file_size < 1024 * 1024:  # < 1 MB
                from_syd = message.chat.id
                syd_id = message.id
                await client.copy_message(Syd_T_G, from_syd, syd_id)
                await message.delete()
                return
                
            syd = file.file_name
            
            sydfile = {
                'file_name': syd,
                'file_size': file.file_size,
                'message_id': message.id,
                'media': file,
                'message': message 
            }
            mrsydt_g.append(sydfile)
            if not processing:
                processing = True  # Set processing flag
                await process_queue(client)
                                    
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await message.reply_text("An error occurred while processing your request.")
         
async def process_queue(client):
    global processing
    try:
        # Process files one by one from the queue
        while mrsydt_g:
            file_details = mrsydt_g.pop(0)  # Get the first file in the queue
            await autosyd(client, file_details)  # Process it
    finally:
        processing = False
        
async def autosyd(client, file_details):
    try:
        syd = file_details['file_name']
        media = file_details['media']
        message = file_details['message']
        mrsyds = ['YTS.MX', 'SH3LBY', 'Telly', 'Moviez', 'NazzY', 'VisTa', 'PiRO', 'PAHE', 'ink', 'mkvcinemas', 'CZ', 'WADU', 'PrimeFix', 'HDA', 'PSA', 'GalaxyRG', '-Bigil', 'TR', 'www.', '@',
            '-TR', '-SH3LBY', '-Telly', '-NazzY', '-PAHE', '-WADU', 'MoviezVerse', 't3nzin', '[Tips', 'Eac3'
        ]
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
            if not any(x.startswith(mrsyd) for mrsyd in mrsyds) and x != '@GetTGLinks'
        ])


        filesize = humanize.naturalsize(media.file_size)
        sydd = ['psa', 'sh3lby', 'Archie', 'Jo', 'Spidey', 'mkvcinemas', 'Telly', 'SH3LBY.mkv', 'bigil', 'YTS.MX', 'WADU', 'budgetbits', 'HDA', 'TR', 'primefix', 'GalaxyRG265', 'bone', 'Incursi0', 'StreliziA', 'ikaRos', 'lssjbroly', 'soan', 'pahe', 'poke', 'galaxytv', 'galaxyrg', 'NazzY', 'VARYG', 'MICHAEL', 'FLUX', 'RAV1NE', '[YTS']
            
        mrsyd = filename.rsplit('-', 1)  # Split filename from the right at the last hyphen
        new_name = mrsyd[0].strip() if len(mrsyd) > 1 and any(term in mrsyd[1].strip().lower() for term in sydd) else filename
            
        if not (new_name.lower().endswith(".mkv") or new_name.lower().endswith(".mp4")):
            new_name += ".mkv"


        remove_list = ["-Telly", "-GalaxyRG", "-TR", "-PSA", "-GalaxyRG265", "-GalaxyTV", "PIRO", "Eac3", "-BUAM",
                       "-VARYG", "-PrimeFix", "-Pahe", "-Saon", "-Archie", "-Spidey", "-KuTTaN", "RARBG", "[KC]",
                       "-Jo", "[YTS.MX]", "-POKE", "-LSSJBroly", "-BiGiL", "-XEBEC", "-L0C1P3R", "-JR",
                       "-CPTN5DW", "DEVENU", "-ViSTA", "-SH3LBY", "+ -", "- +", "- -", "[", "]"]

        for item in remove_list:
            new_name = new_name.replace(item, "")

        syd_name = new_name
        pattern = r'(?P<filename>.*?)(\.\w+)?$'
        match = re.search(pattern, syd_name)
        filename = match.group('filename')
        extension = match.group(2) or ''
        kinsyd = "-SyD @GetTGLinks"
        new_filename = f"{filename} {kinsyd}{extension}" 
        file_path = f"downloads/{new_filename}"
        ms = await client.send_message(
            chat_id=MSYD,
            text=f"__**{syd}**__"
        )
  
        path = await client.download_media(
            message=media,
            file_name=file_path
           # progress=progress_for_pyrogram, 
           # progress_args=(f"\n⚠️ __**{syd}**__\n", ms, time.time())
        )
     
 
        duration = media.duration if hasattr(media, 'duration') else 0
        ph_path = None
        caption = f"**{new_filename}**" 
           
        PIS = 'https://envs.sh/Arr.jpg'
        PISS = 'https://envs.sh/Cdf.jpg'
        SYDD_PATH = 'downloads/syd.jpg'
        SYD_PATH = 'downloads/thumbnail.jpg'
        user_bot = await db.get_user_bot(Config.ADMIN[0])
        if media.file_size > 2000 * 1024 * 1024:
            try:
                syd_irl, syd_des = random.choice([(PIS, SYD_PATH), (PISS, SYDD_PATH)])
                await download_image(syd_irl, syd_des)
                app = await start_clone_bot(client(user_bot['session']))
                filw = await app.send_document(
                    Config.LOG_CHANNEL,
                    document=file_path,
                    thumb=syd_des,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("__{syd}__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
                )

                from_chat = filw.chat.id
                mg_id = filw.id
                time.sleep(1)
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
                syd_irl, syd_des = random.choice([(PIS, SYD_PATH), (PISS, SYDD_PATH)])
                await download_image(syd_irl, syd_des)
                mrsy = syd
                sy = -1002498086501
                await client.send_document(
                    sy,
                    document=file_path,
                    thumb=syd_des,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(f"__{mrsy}__\n\n🌨️ **Uᴩʟᴏᴀᴅɪɴ' Sᴛᴀʀᴛᴇᴅ....**", ms, time.time())
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
        
      #  if message.chat.id == MRSSSYD:
        syd_id = -1002332730533
        mrsyd_id = 13
        chat_message = await client.get_messages(syd_id, mrsyd_id)
        syd_text = chat_message.text
        new_text = syd_message(syd_text)
        await client.edit_message_text(chat_id=syd_id, message_id=mrsyd_id, text=new_text)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await message.reply_text(f"An error")

