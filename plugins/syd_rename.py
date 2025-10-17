import random
import humanize
from helper.ffmpeg import fix_thumb, take_screen_shot
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
from pyrogram.enums import MessageMediaType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply
from helper.utils import progress_for_pyrogram, convert, humanbytes
from helper.database import download_image
from PIL import Image
import asyncio
from aiolimiter import AsyncLimiter
import time
import logging
import re
import os
import time
from helper.utils import add_prefix_suffix, client, start_clone_bot #, is_req_subscribed
from config import Config
#from .mrsyds import mrsydtg
#from info import AUTH_CHANNEL
from motor.motor_asyncio import AsyncIOMotorClient

class Database:
    def __init__(self, mongo_uri: str, db_name: str = "syd_queue"):
        self.client = AsyncIOMotorClient(mongo_uri)
        self.db = self.client[db_name]
        self.queue = self.db["queue"]

    async def add_to_queue(self, item: dict):
        """Add one file entry to queue"""
        await self.queue.insert_one(item)

    async def pop_from_queue(self):
        """Pop the oldest file from queue"""
        doc = await self.queue.find_one(sort=[("_id", 1)])
        if doc:
            await self.queue.delete_one({"_id": doc["_id"]})
        return doc

    async def get_all_queue(self):
        """Return all pending queue items"""
        return await self.queue.find().to_list(length=None)

    async def clear_queue(self):
        """Clear all queue items"""
        await self.queue.delete_many({})

    async def count(self):
        """Return total queue count"""
        return await self.queue.count_documents({})





db = Database(Config.DB_URL, Config.DB_NAME)
processing = False

@Client.on_message(filters.document | filters.audio | filters.video)
async def refnc(client, message):
    global processing

    syd_ids = {MRSSSYD, MRSSYD, MRSSSSYD, MRSSSSSYD}
    if message.chat.id in syd_ids:
        try:
            file = getattr(message, message.media.value)
            if not file:
                return

            # Over 2GB → forward and delete
            if file.file_size > 2000 * 1024 * 1024:
                await client.copy_message(sydtg, message.chat.id, message.id)
                await message.delete()
                return

            # Below 1MB → forward and delete
            if file.file_size < 1024 * 1024:
                await client.copy_message(Syd_T_G, message.chat.id, message.id)
                await message.delete()
                return

            # Normal file → add to queue
            file_data = {
                "file_id": file.file_id,
                "file_name": file.file_name,
                "caption": message.caption,
                "file_size": file.file_size,
                "message_id": message.id,
                "chat_id": message.chat.id,
                "media": file,
                "message": message,
                "media_type": message.media.value,
            }

            await db.add_to_queue(file_data)

            if not processing:
                processing = True
                await process_queue(client)

        except Exception as e:
            await message.reply_text(f"❌ Error: {e}")

async def process_queue(client):
    global processing
    try:
        while True:
            file_details = await db.pop_from_queue()
            if not file_details:
                break
            await autosydd(client, file_details)
    finally:
        processing = False

# Define a function to handle the 'rename' callback


# Language mappings to handle duplicates
syyydtg_map = {
    'Eng': 'English', 'English': 'English',
    'Hin': 'Hindi', 'Hindi': 'Hindi',
    'Tam': 'Tamil', 'Tamil': 'Tamil',
    'Tel': 'Telugu', 'Telugu': 'Telugu',
    'Kan': 'Kannada', 'Kannada': 'Kannada',
    'Mal': 'Malayalam', 'Malayalam': 'Malayalam',
    'Mar': 'Marathi', 'Marathi': 'Marathi',
    'Ben': 'Bengali', 'Bengali': 'Bengali',
    'Ind': 'Indonesian', 'Indonesian': 'Indonesian',
    'Pun': 'Punjabi', 'Punjabi': 'Punjabi',
    'Urd': 'Urdu', 'Urdu': 'Urdu',
    'Guj': 'Gujarati', 'Gujarati': 'Gujarati',
    'Bhoj': 'Bhojpuri', 'Bhojpuri': 'Bhojpuri',
    'Ori': 'Odia', 'Odia': 'Odia',
    'Ass': 'Assamese', 'Assamese': 'Assamese',
    'San': 'Sanskrit', 'Sanskrit': 'Sanskrit',
    'Sin': 'Sinhala', 'Sinhala': 'Sinhala',
    'Ara': 'Arabic', 'Arabic': 'Arabic',
    'Fre': 'French', 'French': 'French',
    'Spa': 'Spanish', 'Spanish': 'Spanish',
    'Por': 'Portuguese', 'Portuguese': 'Portuguese',
    'Ger': 'German', 'German': 'German',
    'Rus': 'Russian', 'Russian': 'Russian',
    'Jap': 'Japanese', 'Japanese': 'Japanese',
    'Kor': 'Korean', 'Korean': 'Korean',
    'Ita': 'Italian', 'Italian': 'Italian',
    'Chi': 'Chinese', 'Chinese': 'Chinese',
    'Man': 'Mandarin', 'Mandarin': 'Mandarin',
    'Tha': 'Thai', 'Thai': 'Thai',
    'Vie': 'Vietnamese', 'Vietnamese': 'Vietnamese',
    'Fil': 'Filipino', 'Filipino': 'Filipino',
    'Tur': 'Turkish', 'Turkish': 'Turkish',
    'Swe': 'Swedish', 'Swedish': 'Swedish',
    'Nor': 'Norwegian', 'Norwegian': 'Norwegian',
    'Dan': 'Danish', 'Danish': 'Danish',
    'Pol': 'Polish', 'Polish': 'Polish',
    'Gre': 'Greek', 'Greek': 'Greek',
    'Heb': 'Hebrew', 'Hebrew': 'Hebrew',
    'Cze': 'Czech', 'Czech': 'Czech',
    'Hun': 'Hungarian', 'Hungarian': 'Hungarian',
    'Fin': 'Finnish', 'Finnish': 'Finnish',
    'Ned': 'Dutch', 'Dutch': 'Dutch',
    'Rom': 'Romanian', 'Romanian': 'Romanian',
    'Bul': 'Bulgarian', 'Bulgarian': 'Bulgarian',
    'Ukr': 'Ukrainian', 'Ukrainian': 'Ukrainian',
    'Cro': 'Croatian', 'Croatian': 'Croatian',
    'Slv': 'Slovenian', 'Slovenian': 'Slovenian',
    'Ser': 'Serbian', 'Serbian': 'Serbian',
    'Afr': 'Afrikaans', 'Afrikaans': 'Afrikaans',
    'Lat': 'Latin', 'Latin': 'Latin'
}

@Client.on_message(filters.command("doit"))
async def doit(client, message):
    global processing
    try:
        args = message.text.strip().split()   # ✅ split on spaces only
        if len(args) < 3:
            return await message.reply_text("Usage: /doit {username} {last_message_id} {skip (optional)}")

        username = args[1]
        last_msg_id = int(args[2])
        skip = int(args[3]) if len(args) > 3 else 0

        await message.reply_text(
            f"🔎 Parsed command:\n"
            f"• Username: `{username}`\n"
            f"• Last Msg ID: `{last_msg_id}`\n"
            f"• Skip: `{skip}`"
        )
        # Validate user
        try:
            target = await client.get_chat(username)
        except (PeerIdInvalid, UsernameNotOccupied):
            return await message.reply_text(f"❌ Username `{username}` not found or invalid")


        processed = 0
        skipped = 0

        
        # Send initial status message
        status_msg = await message.reply_text("⏳ Starting...")

        for msg_id in range(1, last_msg_id + 1):
            try:
                msg = await client.get_messages(target.id, msg_id)
            except Exception:
                continue  # message might not exist

            if not msg or not (msg.document or msg.audio or msg.video):
                continue

            # skip handling
            if skip > 0:
                skip -= 1
                skipped += 1
                continue

            file = getattr(msg, msg.media.value)
            if not file:
                continue

            # > 2 GB
            if file.file_size > 2000 * 1024 * 1024:
                await client.copy_message(sydtg, msg.chat.id, msg.id)
                await msg.delete()
                processed += 1
                continue

            # < 1 MB
            if file.file_size < 1024 * 1024:
                await client.copy_message(Syd_T_G, msg.chat.id, msg.id)
                await msg.delete()
                processed += 1
                continue

            # Queue system
            sydfile = {
                'file_name': file.file_name,
                'caption': msg.caption,
                'file_size': file.file_size,
                'message_id': msg.id,
                'media': file,
                'message': msg
            }
            mrsydtg.append(sydfile)
            processed += 1

            if not processing:
                processing = True
                await proces_queue(client)

            # Update status every 10 processed
            if processed % 10 == 0:
                try:
                    await status_msg.edit_text(
                        f"⚡ Processing...\nProcessed: {processed}\nSkipped: {skipped}"
                    )
                except Exception:
                    pass  # ignore if message can't be edited

        # Final update
        try:
            await status_msg.edit_text(
                f"✅ Done.\nProcessed: {processed}\nSkipped: {skipped}"
            )
        except Exception:
            await message.reply_text(
                f"✅ Done.\nProcessed: {processed}\nSkipped: {skipped}"
            )

    except Exception as e:
      #  logger.error(f"/doit failed: {e}")
        await message.reply_text(f"⚠️ Error in /doit: {e}")


def rearrange_string(syd, nesyd):
    year_match = re.search(r'\b(19|20)\d{2}\b', syd)
    year = year_match.group() if year_match else ""

    words = syd.split()
    nesyd_languages = {syyydtg_map[word] for word in nesyd.split() if word in syyydtg_map}  # Unique valid languages

    new_words = []
    lang_set = set()

    for word in words:
        if word in syyydtg_map:
            full_lang = syyydtg_map[word]  # Convert abbreviation to full name
            if full_lang not in lang_set:
                new_words.append(full_lang)  # Add only if not already included
                lang_set.add(full_lang)
        else:
            new_words.append(word)  # Preserve non-language words

    # Add missing languages from nesyd at the end
    missing_languages = nesyd_languages - lang_set
    new_words.extend(sorted(missing_languages))  # Sorted to maintain consistency

    return " ".join(new_words).strip()

    
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
    text = message_count(text, r"ᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ : tᴛᴏᴛᴀʟ ꜰɪʟᴇꜱ :")
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
        
def sydddmessage(text):
    match = re.search(r"#3 ʀᴇᴍᴀɪɴɪɴɢ :  (\d+)", text)
    if match:
        current_count = int(match.group(1))
        new_count = current_count - 1
        new_text = re.sub(r"#4 ʀᴇᴍᴀɪɴɪɴɢ : \d+", f"#3 ʀᴇᴍᴀɪɴɪɴɢ : {new_count}", text)
        return new_text
    else:
        return "#3 ʀᴇᴍᴀɪɴɪɴɢ : 1 [ᴇʀʀᴏʀ]"


# Define the main message handler for private messages with replies
#@Client.on_message(filters.document | filters.audio | filters.video)
async def refnc(client, message):
    global processing
    syd_id = {MRSSSYD, MRSSYD, MRSSSSYD, MRSSSSSYD}
    if message.chat.id in syd_id :
        try:
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
                
            sydd = message.caption
            syd = file.file_name
            sydfile = {
                'file_name': syd,
                'caption': sydd,
                'file_size': file.file_size,
                'message_id': message.id,
                'media': file,
                'message': message 
            }
            mrsydtg.append(sydfile)
            if not processing:
                processing = True  # Set processing flag
                await proces_queue(client)
                                    
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await message.reply_text(f"An error occurred while processing your request {e}.")
         
async def proces_qeue(client):
    global processing
    try:
        # Process files one by one from the queue
        while mrsydtg:
            file_details = mrsydtg.pop(0)  # Get the first file in the queue
            await autosydd(client, file_details)  # Process it
    finally:
        processing = False
        
async def autosydd(client, file_details):
    try:
      #  remov_list = [ "", "", "", ""]
        sydy = file_details['file_name']
        sydyy = file_details['caption']
        mrsyds = ['YTS.MX', 'SH3LBY', 'Telly', 'Moviez', 'NazzY', 'VisTa', 'PiRO', 'PAHE', 'ink', 'mkvcinemas', 'CZ', 'WADU', 'PrimeFix', 'HDA', 'PSA', 'GalaxyRG', '-Bigil', 'TR', 'www.', '@',
            '-TR', '-SH3LBY', '-Telly', '-NazzY', '-PAHE', '-WADU', 'MoviezVerse', 't3nzin', '[Tips', 'Eac3', 'mkv', 'mp4', '@Smile'
        ]
        remove_list = ["-Telly", "-GalaxyRG", "-TR", "-PSA", "-GalaxyRG265", "-GalaxyTV", "PIRO", "Eac3", "-BUAM", "St4LiLiN", "-HDHub4u.Tv", "HiQVE", "CG", "KMH", "Movie Bazar", "A2Movies",
                       "-VARYG", "-PrimeFix", "-Pahe", "-Saon", "-Archie", "-Spidey", "-KuTTaN", "RARBG", "[KC]", "-VXT", "-HDHub4u", "(SABUJ)", "MSM", "CC", "CF", "RWD", "Mux-Soft", "Mux-Hard",
                       "-Jo", "[YTS.MX]", "-POKE", "-LSSJBroly", "-BiGiL", "-XEBEC", "-L0C1P3R", "-JR", "PrivateMovieZ", "MM", "PMZ", "COSMOS", "YamRaaj", "NonDRM",
                       "-CPTN5DW", "DEVENU", "-ViSTA", "-SH3LBY", "[]", "-.", "+ -", "- +", "- -", "[", "]", "--", "_"]
        sydd = ['psa', 'sh3lby', 'Archie', 'Jo', 'Spidey', 'mkvcinemas', 'Telly', 'SH3LBY.mkv', 'bigil', 'YTS.MX', 'WADU', 'budgetbits', 'HDA', 'TR', 'primefix', 'GalaxyRG265', 'bone', 'Incursi0', 'StreliziA', 'ikaRos', 'lssjbroly', 'soan', 'pahe', 'poke', 'galaxytv', 'galaxyrg', 'NazzY', 'VARYG', 'MICHAEL', 'FLUX', 'RAV1NE', '[YTS']
        for w in mrsyds + remove_list + sydd:
            sydyy = sydyy.replace(w, " ")
            
        sydyy = sydyy.replace("_", " ")
        sydyy = sydyy.replace(".", " ")
        sydy = sydy.replace("_", " ")
        sydy = sydy.replace(".", " ")
        sydy = sydy.replace(" - ", " ")
        sydy = sydy.replace("- ", " ")
            
        #syd = rearrange_string(sydy, sydyy)
        syd = sydy
        media = file_details['media']
        message = file_details['message']
        
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
            if not any(x.startswith(mrsyd) for mrsyd in mrsyds) and not x.startswith('@')
        ])
        sy = -1002498086501
        await client.get_chat(MSYD)
        await client.get_chat(sy)
        filesize = humanize.naturalsize(media.file_size)
        
        mrsyd = filename.rsplit('-', 1)  # Split filename from the right at the last hyphen
        new_name = mrsyd[0].strip() if len(mrsyd) > 1 and any(term in mrsyd[1].strip().lower() for term in sydd) else filename
        for item in remove_list:
            new_name = new_name.replace(item, "")

        if not (new_name.lower().endswith(".mkv") or new_name.lower().endswith(".mp4")):
            new_name += ".mkv"
        syd_name = re.sub(r"\s+", " ", new_name).strip()
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
           
        #PIS = 'https://envs.sh/i2P.jpg'
       # PISS = 'https://envs.sh/i2w.jpg'
        SYD_PATH = ['SydMage/IMG_1.jpg', 'SydMage/IMG_2.jpg']
      #  SYD_PATH = 'downloads/thumbnail.jpg'
        #user_bot = await db.get_user_bot(Config.ADMIN[0])
        if media.file_size > 2000 * 1024 * 1024:
            try:
                syd_des = random.choice(SYD_PATH)
                #syd_irl, syd_des = random.choice([(PIS, SYD_PATH), (PISS, SYDD_PATH)])
               # await download_image(syd_irl, syd_des)
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
                syd_des = random.choice(SYD_PATH)
                #syd_irl, syd_des = random.choice([(PIS, SYD_PATH), (PISS, SYDD_PATH)])
                #await download_image(syd_irl, syd_des)
                mrsy = syd
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
        #if syd_des:
            #os.remove(syd_des)
        syd_id = -1002332730533
        mrsyd_id = 13
        chat_message = await client.get_messages(syd_id, mrsyd_id)
        syd_text = chat_message.text
        new_text = syd_message(syd_text)
        await client.edit_message_text(chat_id=syd_id, message_id=mrsyd_id, text=new_text)
        
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        await message.reply_text(f"An error")

