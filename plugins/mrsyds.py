from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message 
from PIL import Image
from datetime import datetime
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, humanbytes, convert, download_image
from helper.database import db
from config import Config
from asyncio import Lock
import os
import time, asyncio
import logging
import re
#import shutil

fulsyd = "faibjkmmr"
processing_lock = Lock()
mrsydt_g = []
processing = False
MRSYD = -1002200259696
sydtg = -1002305372915
Syd_T_G = -1002160523059
renaming_operations = {}
logger = logging.getLogger(__name__)
last_season_number = 0
syd_top = 0
syd_qua = "None"
syd_mov = "None"

# Pattern 1: S01E02 or S01EP02
pattern1 = re.compile(r'S(\d+)(?:E|EP)(\d+)')
# Pattern 2: S01 E02 or S01 EP02 or S01 - E01 or S01 - EP02
pattern2 = re.compile(r'S(\d+)\s*(?:E|EP|-\s*EP)(\d+)')
# Pattern 3: Episode Number After "E" or "EP"
pattern3 = re.compile(r'(?:[([<{]?\s*(?:E|EP)\s*(\d+)\s*[)\]>}]?)')
# Pattern 3_2: episode number after - [hyphen]
pattern3_2 = re.compile(r'(?:\s*-\s*(\d+)\s*)')
# Pattern 4: S2 09 ex.
pattern4 = re.compile(r'S(\d+)[^\d]*(\d+)', re.IGNORECASE)
# Pattern X: Standalone Episode Number
patternX = re.compile(r'\b(?!\d{3,4}p\b)\d{3,4}\b', re.IGNORECASE)
# Pattern 1: Explicit "S" or "Season" with optional separators
season_pattern1 = re.compile(r'(?:S|Season)\s*[-:]?\s*(\d+)', re.IGNORECASE)
# Pattern 2: Flexible detection with explicit prefixes only
season_pattern2 = re.compile(r'(?:^|[^\w])(?:S|Season)\s*[-:]?\s*(\d+)(?=[^\d]|$)', re.IGNORECASE)

#QUALITY PATTERNS 
# Pattern 5: 3-4 digits before 'p' as quality
pattern5 = re.compile(r'\b(?:.*?(\d{3,4}[^\dp]*p).*?|.*?(\d{3,4}p))\b', re.IGNORECASE)
# Pattern 6: Find 4k in brackets or parentheses
pattern6 = re.compile(r'[([<{]?\s*4k\s*[)\]>}]?', re.IGNORECASE)
# Pattern 7: Find 2k in brackets or parentheses
pattern7 = re.compile(r'[([<{]?\s*2k\s*[)\]>}]?', re.IGNORECASE)
# Pattern 8: Find HdRip without spaces
pattern8 = re.compile(r'[([<{]?\s*HdRip\s*[)\]>}]?|\bHdRip\b', re.IGNORECASE)
# Pattern 9: Find 4kX264 in brackets or parentheses
pattern9 = re.compile(r'[([<{]?\s*4kX264\s*[)\]>}]?', re.IGNORECASE)
# Pattern 10: Find 4kx265 in brackets or parentheses
pattern10 = re.compile(r'[([<{]?\s*4kx265\s*[)\]>}]?', re.IGNORECASE)

def extract_quality(filename):
    # Try Quality Patterns
    match5 = re.search(pattern5, filename)
    if match5:
        print("Matched Pattern 5")
        quality5 = match5.group(1) or match5.group(2)  # Extracted quality from both patterns
        print(f"Quality: {quality5}")
        return quality5

    match6 = re.search(pattern6, filename)
    if match6:
        print("Matched Pattern 6")
        quality6 = "4k"
        print(f"Quality: {quality6}")
        return quality6

    match7 = re.search(pattern7, filename)
    if match7:
        print("Matched Pattern 7")
        quality7 = "2k"
        print(f"Quality: {quality7}")
        return quality7

    # Return "Unknown" if no pattern matches
    unknown_quality = "Unknown"
    print(f"Quality: {unknown_quality}")
    return unknown_quality
    

def extract_episode_number(filename):    
    # Try Pattern 1
    match = re.search(pattern1, filename)
    if match:
        print("Matched Pattern 1")
        return match.group(2)  # Extracted episode number
    
    # Try Pattern 2
    match = re.search(pattern2, filename)
    if match:
        print("Matched Pattern 2")
        return match.group(2)  # Extracted episode number

    # Try Pattern 3
    match = re.search(pattern3, filename)
    if match:
        print("Matched Pattern 3")
        return match.group(1)  # Extracted episode number

    # Try Pattern 3_2
    match = re.search(pattern3_2, filename)
    if match:
        print("Matched Pattern 3_2")
        return match.group(1)  # Extracted episode number
        
    # Try Pattern 4
    match = re.search(pattern4, filename)
    if match:
        print("Matched Pattern 4")
        return match.group(2)  # Extracted episode number

    # Try Pattern X
    match = re.search(patternX, filename)
    if match:
        print("Matched Pattern X")
        return match.group(1)  # Extracted episode number
        
    # Return None if no pattern matches
    return None

def extract_season_number(filename):    
    # Try Pattern 1
    match = re.search(season_pattern1, filename)
    if match:
        print("Matched Pattern 1")
        return match.group(1)  # Extracted episode number
    
    # Try Pattern 2
    match = re.search(season_pattern2, filename)
    if match:
        print("Matched Pattern 2")
        return match.group(1)  # Extracted episode number
    return None

# Example Usage:
filename = "Naruto Shippuden S01 - EP07 - 1080p [Dual Audio].mkv"
episode_number = extract_episode_number(filename)
print(f"Extracted Episode Number: {episode_number}")

# Inside the handler for file uploads
@Client.on_message(filters.document | filters.video | filters.audio)
async def refuntion(client, message):
    global processing
    syd_id = {MRSYD, MRSYD}
    if message.chat.id in syd_id :
        try:
            file = getattr(message, message.media.value)
            if not file:
                return
            if file.file_size > 2000 * 1024 * 1024:  # > 2 GB
                from_syd = message.chat.id
                syd_id = message.id
                await client.copy_message(-1002213261472, from_syd, syd_id)
                await message.delete()
                return
            if file.file_size < 1024 * 1024:  # < 1 MB
                from_syd = message.chat.id
                syd_id = message.id
                await client.copy_message(Syd_T_G, from_syd, syd_id)
                await message.delete()
                return

            sydmen = await db.get_sydson(1733124290)
            syd = file.file_name
            await asyncio.sleep(1)
            mrsyd = await db.get_topic(1733124290)
            sydfile = {
                'file_name': syd,
                'file_size': file.file_size,
                'message_id': message.id,
                'media': file,
                'topic': mrsyd,
                'season': sydmen,
                'message': message,
                'timestamp': message.date.timestamp()
            }
            mrsydt_g.append(sydfile)
            mrsydt_g.sort(key=lambda x: x['timestamp'])  # Ensure chronological order

            if not processing:
                processing = True
                await process_queue(client)
                                    
        
        except Exception as e:
            logger.error(f"An error occurred: {e}")
            await message.reply_text("An error occurred while processing your request.")
         
async def process_queue(client):
    global processing
    try:
        while mrsydt_g:
            file_details = mrsydt_g.pop(0)  # Get the file with the earliest timestamp
            await autosyd(client, file_details)  # Process it
    finally:
        processing = False


async def autosyd(client, file_details):
    global last_season_number, syd_top, syd_mov, syd_qua
    sydd = file_details['file_name']
    media = file_details['media']
    message = file_details['message']
    #user_id = message.from_user.id
    #firstname = message.from_user.first_name
   # format_template = await madflixbotz.get_format_template(user_id)
    #media_preference = await madflixbotz.get_media_preference(user_id)
    # Extract information from the incoming file name
    if message.document:
        file_id = message.document.file_id
        file_name = message.document.file_name
        media_type = "document"  # Use preferred media type or default to document
    elif message.video:
        file_id = message.video.file_id
        file_name = f"{message.video.file_name}.mp4"
        media_type = "video"  # Use preferred media type or default to video
    elif message.audio:
        file_id = message.audio.file_id
        file_name = f"{message.audio.file_name}.mp3"
        media_type = "audio"  # Use preferred media type or default to audio
    else:
        return await message.reply_text("Unsupported File Type")

    pat1 = re.sub(pattern1, "", sydd)
    pat2 = re.sub(pattern2, "", pat1)
    pat3 = re.sub(pattern3, "", pat2)
    pat4 = re.sub(pattern3_2, "", pat3)
    pat5 = re.sub(pattern4, "", pat4)
    pat6 = re.sub(patternX, "", pat5)
    pat7 = re.sub(season_pattern1, "", pat6)
    sydX = re.sub(season_pattern2, "", pat7)
    if file_id in renaming_operations:
        elapsed_time = (datetime.now() - renaming_operations[file_id]).seconds
        if elapsed_time < 10:
            print("File is being ignored as it is currently being renamed or was renamed recently.")
            return  # Exit the handler if the file is being ignored
    renaming_operations[file_id] = datetime.now()
    qualit = extract_quality(file_name) if extract_quality(file_name) else '4k'
    episode_number = extract_episode_number(file_name)
    season_no = extract_season_number(file_name) if extract_season_number(file_name) else '01'
    print(f"Extracted Episode Number: {episode_number}")
    
    if episode_number and season_no:
        syd_tg = int(episode_number)
        syd_xyz = int(season_no)
        tg_Syd_Xyz = file_details['season']
        if tg_Syd_Xyz == "True":
            formatted_episode = f"S{syd_xyz:02d}E{syd_tg:02d} "
        elif tg_Syd_Xyz == "False":
            formatted_episode = f"E{syd_tg:02d} "
        Syd = formatted_episode + sydX
        mrsyds = ['YTS.MX', 'SH3LBY', 'Telly', 'Moviez', 'NazzY', 'VisTa', 'PiRO', 'PAHE', 'ink', 'mkvcinemas', 'CZ', 'WADU', 'PrimeFix', 'HDA', 'PSA', 'GalaxyRG', '-Bigil', 'TR', 'www.', '@',
            '-TR', '-SH3LBY', '-Telly', '-NazzY', '-PAHE', '-WADU', 'MoviezVerse', 't3nzin', '[Tips', 'Eac3', '(@'
                 ]
        sydmen = await db.get_rep(1733124290)
        syd1 = sydmen['sydd']
        syd2 = sydmen['syddd']
        if syd1 in Syd:
            Syd = Syd.replace(syd1, syd2)
        remove_list = ['-', '[AL]', '[KDL]', '@Anime_Fair', '@Klands', 'Syd', 'KDL', 'foooir', '[', ']']
        for item in remove_list:
            Syd = Syd.replace(item, "")
        if '[Dual]' in Syd:
            Syd = Syd.replace('[Dual]', 'Dual')
        if '[Multi]' in Syd:
            Syd = Syd.replace('[Multi]', 'Multi')
        if fulsyd in Syd:
            Syd = Syd.replace(fulsyd, "")
        filenme = ' '.join([
            x for x in Syd.split()
            if not any(x.startswith(mrsyd) for mrsyd in mrsyds) and x != '@GetTGLinks'
        ])
        if '_' in Syd:
            Syd = Syd.replace('_', ' ')
        if not (filenme.lower().endswith(".mkv") or filenme.lower().endswith(".mp4") or filenme.lower().endswith(".Mkv")):
            filenme += ".mkv"
        pattern = r'(?P<filename>.*?)(\.\w+)?$'
        match = re.search(pattern, filenme)
        filename = match.group('filename')
        extension = match.group(2) or ''
        #syd_name = f"{filename} SyD @GetTGLinks{extension}"
        new_file_name = f"[KDL] {filename} @Klands{extension}"
        file_path = f"downloads/{new_file_name}"
        #syd_path = f"download/{syd_name}"
        file = message

        download_msg = await message.reply_text(text="Trying To Download.....")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", download_msg, time.time()))
        except Exception as e:
            # Mark the file as ignored
            del renaming_operations[file_id]
            return await download_msg.edit(e)     

        duration = 0
       # shutil.copy(file_path, syd_path)
        upload_msg = await download_msg.edit("Trying To Uploading.....")
        ph_path = None
        c_caption = await db.get_caption(1733124290)
        c_thumb = await db.get_thumbnail(1733124290)

        topic_syd_id = file_details['topic']
        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}**"
        if syd_top == 0:
            syd_top = topic_syd_id
            
        if syd_top != topic_syd_id:
            try:
                await client.send_sticker(
                    chat_id=-1002322136660,
                    sticker="CAACAgUAAxkBAAEEOcxnZO0ftNzDaNCCvOdzqjnmTwiwWwACawgAAvJ9SFVrAAGBhWipiW4eBA",
                    reply_to_message_id=syd_top
                )
                syd_top = topic_syd_id
            except Exception as e:
                print(f"Failed to end send sticker to topic: {e}")
        
        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")
        

        #SYD_PATH = 'downloads/thumbnail.jpg'
        #PIS = 'https://envs.sh/Arr.jpg'
        if last_season_number == 0:
            last_season_number = syd_xyz
            
        if syd_xyz == last_season_number + 1:
            try:
                await client.send_sticker(
                    chat_id=-1002322136660,
                    sticker="CAACAgUAAxkBAAEEOXZnZBMPFXQQ8Kgv-cGa4s001eWt6gACuxAAAtRd8FbK2QFnTLfR9x4E",
                    reply_to_message_id=topic_syd_id
                )
                amsyd = f'Season {syd_xyz} 🌟'
                await client.send_message(chat_id=-1002322136660, text=amsyd, reply_to_message_id=topic_syd_id)
                
            except Exception as e:
                print(f"Failed to send sticker to topic: {e}")
        last_season_number = syd_xyz
        if syd_qua == "None":
            syd_qua = qualit
        if syd_qua != qualit:
            try:
                if qualit == "360p":
                    await client.send_sticker(
                        chat_id=-1002322136660,
                        sticker="CAACAgUAAxkBAAEEOvZnasxONLg3zHkwBi52PsbiYZDy4AACLxQAAuwdUFcKB6KPifdvMB4E",
                        reply_to_message_id=topic_syd_id
                    )
                elif qualit == "480p":
                    await client.send_sticker(
                        chat_id=-1002322136660,
                        sticker="CAACAgUAAxkBAAEEOvVnasxNvJquI8hykr3CUvnFwuhD0AACvhIAAkZ3WVeHD_oDDwlT-h4E",
                        reply_to_message_id=topic_syd_id
                )
                elif qualit == "720p":
                    await client.send_sticker(
                        chat_id=-1002322136660,
                        sticker="CAACAgUAAxkBAAEEOvdnasxPpmOR0wtba78SUUrcz7OCdgACjhEAArLMWVeqZU0pn2UNDx4E",
                        reply_to_message_id=topic_syd_id
                    )
                elif qualit == "1080p":
                    await client.send_sticker(
                        chat_id=-1002322136660,
                        sticker="CAACAgUAAxkBAAEEOvhnasxQl3SeR-S-iLJuLmW16ItMfQACWxUAAvcKWVdq4miltFHN9h4E",
                        reply_to_message_id=topic_syd_id
                    )
                elif qualit == "2160p":
                    await client.send_sticker(
                        chat_id=-1002322136660,
                        sticker="CAACAgUAAxkBAAEEOvlnasxRvumZMN2V17odpte8j6NxgwACnRUAAicgWFcwwUluHbCrbR4E",
                        reply_to_message_id=topic_syd_id
                    )
                elif qualit == "4K":
                    await client.send_sticker(
                        chat_id=-1002322136660,
                        sticker="CAACAgUAAxkBAAEEOvpnasxTpXTMsefsYw-pEBXpmFvzPwACawgAAvJ9SFVrAAGBhWipiW4eBA",
                        reply_to_message_id=topic_syd_id
                )
            except Exception as e:
                print(f"Failed to send sticker to topic for quality : {e}")
        syd_qua = qualit
        try:
            mrsyd = -1002267379845
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                sydfil = await client.send_document(
                    mrsyd,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                sydfil = await client.send_video(
                    mrsyd,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                sydfil = await client.send_audio(
                    mrsyd,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")

        #try:
            #await download_image(PIS, SYD_PATH)
            #type = media_type  # Use 'media_type' variable instead
            #if type == "document":
                #sydfile = await client.send_document(
                    #-1002163302783,
                    #document=syd_path,
                    #thumb=SYD_PATH,
                    #caption=caption
                #)
         #   elif type == "video":
              #  sydfile = await client.send_video(
            #        -1002163302783,
             #       video=syd_path,
             #       caption=caption,
              #      thumb=SYD_PATH,
               #     duration=duration
             #   )
          #  elif type == "audio":
               # sydfile = await client.send_audio(
                 #   -1002163302783,
                  #  audio=syd_path,
                #    caption=caption,
                  #  thumb=SYD_PATH,
                   # duration=duration
              #  )
        #except Exception as e:
            #os.remove(file_path)
            #if ph_path:
                #os.remove(ph_path)
            # Mark the file as ignored
            #return await upload_msg.edit(f"Error: {e}")

                
        await download_msg.delete() 
        mrsyyd = sydfil.document.file_size if type == "document" else sydfil.video.file_size if type == "video" else sydfil.audio.file_size
        mrssyd = message.document.file_size if type == "document" else message.video.file_size if type == "video" else message.audio.file_size
        #mrsssyd = sydfile.document.file_size if type == "document" else sydfile.video.file_size if type == "video" else sydfile.audio.file_size
        if mrsyyd != mrssyd:
            await sydfil.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await message.reply_text("Size Error")
        #if mrsyyd != mrsssyd:
            #await sydfile.delete()
            #os.remove(syd_path)
            #if ph_path:
                #os.remove(ph_path)
            #del renaming_operations[file_id]
            #return await message.reply_text("Size Error")
        if season_no == 0:
            os.remove(file_path)
            os.remove(syd_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await message.reply_text("Season No. 0 Error")
        if episode_number == 0:
            os.remove(file_path)
            os.remove(syd_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await message.reply_text("Episode No. 0 Error")
        os.remove(file_path)
        #os.remove(syd_path)
        await message.delete()
        try:  # Replace with the actual thread ID of the topic
            await client.copy_message(
                chat_id=-1002322136660,  # Replace with the target group ID
                from_chat_id=mrsyd,
                message_id=sydfil.id,
                reply_to_message_id=topic_syd_id
            )
        except Exception as e:
            return await message.reply_text(f"Failed to forward to topic: {e}")

        if ph_path:
            os.remove(ph_path)

# Remove the entry from renaming_operations after successful renaming
        del renaming_operations[file_id]
    else:
        Syd = sydX
        sydmen = await db.get_rep(1733124290)
        syd1 = sydmen['sydd']
        syd2 = sydmen['syddd']
        mrsyds = ['YTS.MX', 'SH3LBY', 'Telly', 'Moviez', 'NazzY', 'VisTa', 'PiRO', 'PAHE', 'ink', 'mkvcinemas', 'CZ', 'WADU', 'PrimeFix', 'HDA', 'PSA', 'GalaxyRG', '-Bigil', 'TR', 'www.', '@',
            '-TR', '-SH3LBY', '-Telly', '-NazzY', '-PAHE', '-WADU', 'MoviezVerse', 't3nzin', '[Tips', 'Eac3', '(@'
                 ]
        if syd1 in Syd:
            Syd = Syd.replace(syd1, syd2)
        if '[Dual]' in Syd:
            Syd = Syd.replace('[Dual]', 'Dual')
        if '[Multi]' in Syd:
            Syd = Syd.replace('[Multi]', 'Multi')
        remove_list = ['-', '[AL]', '[KDL]', '@Anime_Fair', '@Klands', 'www', 'KDL', 'fair', '[', ']']
        for item in remove_list:
            Syd = Syd.replace(item, "")
        if fulsyd in Syd:
            Syd = Syd.replace(fulsyd, "")
        filenme = ' '.join([
            x for x in Syd.split()
            if not any(x.startswith(mrsyd) for mrsyd in mrsyds) and x != '@GetTGLinks'
        ])
        if '_' in Syd:
            Syd = Syd.replace('_', ' ')
        if not (filenme.lower().endswith(".mkv") or filenme.lower().endswith(".mp4") or filenme.lower().endswith(".Mkv")):
            filenme += ".mkv"
        pattern = r'(?P<filename>.*?)(\.\w+)?$'
        match = re.search(pattern, filenme)
        filename = match.group('filename')
        extension = match.group(2) or ''
        #syd_name = f"{filename} SyD @GetTGLinks{extension}"
        new_file_name = f"[KDL] {filename} @Klands{extension}"
        file_path = f"downloads/{new_file_name}"
        #syd_path = f"download/{syd_name}"
        sydname = filename.replace("480p", "").replace("720p", "").replace("1080p", "").strip()
        file = message
        download_msg = await message.reply_text(text="Trying To Download.....")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", download_msg, time.time()))
        except Exception as e:
            # Mark the file as ignored
            del renaming_operations[file_id]
            return await download_msg.edit(e)
        if syd_mov == "None":
            syd_mov = sydname
        if syd_mov != sydname:
            try:
                await client.send_sticker(
                    chat_id=-1002322136660,
                    sticker="CAACAgUAAxkBAAEEOXZnZBMPFXQQ8Kgv-cGa4s001eWt6gACuxAAAtRd8FbK2QFnTLfR9x4E",
                    reply_to_message_id=topic_syd_id
                )
                amsyd = f'Movie {sydname} 🌟'
                await client.send_message(chat_id=-1002322136660, text=amsyd, reply_to_message_id=topic_syd_id)
                
            except Exception as e:
                print(f"Failed to send sticker to topic: {e}")
        syd_mov = sydname
        duration = 0
       # shutil.copy(file_path, syd_path)
        upload_msg = await download_msg.edit("Trying To Uploading.....")
        ph_path = None
        c_caption = await db.get_caption(1733124290)
        c_thumb = await db.get_thumbnail(1733124290)
        topic_syd_id = file_details['topic']
        caption = c_caption.format(filename=new_file_name, filesize=humanbytes(message.document.file_size), duration=convert(duration)) if c_caption else f"**{new_file_name}**"
        if syd_top == 0:
            syd_top = topic_syd_id
            
        if syd_top != topic_syd_id:
            try:
                await client.send_sticker(
                    chat_id=-1002322136660,
                    sticker="CAACAgUAAxkBAAEEOcxnZO0ftNzDaNCCvOdzqjnmTwiwWwACawgAAvJ9SFVrAAGBhWipiW4eBA",
                    reply_to_message_id=syd_top
                )
                syd_top = topic_syd_id
            except Exception as e:
                print(f"Failed to end send sticker to topic: {e}")
        if c_thumb:
            ph_path = await client.download_media(c_thumb)
            print(f"Thumbnail downloaded successfully. Path: {ph_path}")
        elif media_type == "video" and message.video.thumbs:
            ph_path = await client.download_media(message.video.thumbs[0].file_id)

        if ph_path:
            Image.open(ph_path).convert("RGB").save(ph_path)
            img = Image.open(ph_path)
            img.resize((320, 320))
            img.save(ph_path, "JPEG")
        try:
            mrsyd = -1002267379845
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                sydfil = await client.send_document(
                    mrsyd,
                    document=file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                sydfil = await client.send_video(
                    mrsyd,
                    video=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                sydfil = await client.send_audio(
                    mrsyd,
                    audio=file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")
        await download_msg.edit("No ᴇᴩɪꜱᴏᴅᴇ ɴᴜᴍʙᴇʀ ᴀɴᴅ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ")
        mrsyyd = sydfil.document.file_size if type == "document" else sydfil.video.file_size if type == "video" else sydfil.audio.file_size
        mrssyd = message.document.file_size if type == "document" else message.video.file_size if type == "video" else message.audio.file_size
        if mrsyyd != mrssyd:
            await sydfil.delete()
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            del renaming_operations[file_id]
            return await message.reply_text("Size Error")
        try:  # Replace with the actual thread ID of the topic
            await client.copy_message(
                chat_id=-1002322136660,  # Replace with the target group ID
                from_chat_id=mrsyd,
                message_id=sydfil.id,
                reply_to_message_id=topic_syd_id
            )
        except Exception as e:
            return await message.reply_text(f"Failed to forward to topic: {e}")
        if ph_path:
            os.remove(ph_path)
        del renaming_operations[file_id]
