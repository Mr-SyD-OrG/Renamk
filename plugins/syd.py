from pyrogram import Client, filters
from pyrogram.errors import FloodWait
from pyrogram.types import InputMediaDocument, Message 
from PIL import Image
from datetime import datetime
#from .mrsyd import process_queue
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.utils import progress_for_pyrogram, humanbytes, convert, download_image
from helper.database import db as madflixbotz
from config import Config
import os
import time, asyncio
import logging
import re
#import shutil
fulsyd = "fair"
db = madflixbotz
mrs = []
mrsydt_g = mrs
processing = False
MRSYD = -1002289521919
sydtg = -1002305372915
Syd_T_G = -1002160523059
renaming_operations = {}
logger = logging.getLogger(__name__)
last_season_number = 0
syd_top = 0
syd_qua = "None"
syd_mov = "None"

# Semaphore to ensure only one command is processed at a time
semaphore = asyncio.Semaphore(1)

@Client.on_message(filters.command("begin") & filters.user(1733124290))  # Replace with your user ID
async def start_processing(client, message):
    async with semaphore:
        try:
            # Validate and extract chat_id from the command
            if len(message.command) < 2:
                await message.reply_text("Usage: /begin <chat_id>")
                return

            chat_d = message.command[1]
            skip = message.command[3] if len(message.command) > 3 else None
            top = message.command[2] if len(message.command) > 2 else None

            if top and top.startswith("https://t.me/"):
                match = re.search(r"/(\d+)$", top)
                if match:
                    topic_id = match.group(1)
                else:
                    return await message.reply("<b>⚠ Invalid link provided. Make sure it ends with a numeric topic ID.</b>")

            if skip and skip.startswith("https://t.me/"):
                match = re.search(r"/(\d+)$", skip)
                if match:
                    skip_id = int(match.group(1))
                else:
                    return await message.reply("<b>⚠ Invalid link provided. Make sure it ends with a numeric topic ID.</b>")
            else:
                skip_id = int(skip) if skip else None

            if chat_d.startswith(('http')):
                username, message_d = chat_d.split('/')[-2], chat_d.split('/')[-1]
                chat_id = "@" + username
                last_message_id = int(message_d)
            else:
                await message.reply_text("Invalid chat link.")
                chat_id, message_d = chat_d.split('/')[-2], chat_d.split('/')[-1]

            try:
                chat = await client.get_chat(chat_id)
                if not chat:
                    await message.reply_text("Unable to access the specified chat. Please check the chat ID.")
                    return
            except Exception as e:
                await message.reply_text(f"Error accessing chat: {e}")
                return

            topic = topic_id if 'topic_id' in locals() else await db.get_topic(1733124290)
            prsyd = await message.reply_text(f"Processing started for messages in chat ID: {chat_id}")

            if skip_id:
                for message_id in range(skip_id, last_message_id + 1):
                    await process_existing_messages(client, chat_id, message_id, topic)
            else:
                for message_id in range(1, last_message_id + 1):
                    await process_existing_messages(client, chat_id, message_id, topic)
            await prsyd.edit_text(f"Now /process 🎉 {chat_id}")
        except Exception as e:
            logger.error(f"An error occurred in start_processing: {e}")
            await message.reply_text("An error occurred while processing your command.")


async def process_existing_messages(client, chat_id, message_id, sydtopic):
    global processing
    try:
        message = await client.get_messages(chat_id=chat_id, message_ids=message_id)
        #await syd.reply_text("1")
        if message.media:
            file = getattr(message, message.media.value, None)
            if file and file.file_size > 10 * 1024 * 1024:  # > 10 MB
                sydmen = await db.get_sydson(1733124290)
              #  syd = file.file_name
                await asyncio.sleep(0.8)
                mrsyd = sydtopic
                mrsydt = await db.get_rep(1733124290)
                synam = await db.get_format_template(1733124290)
                syd1 = mrsydt['sydd']
                syd2 = mrsydt['syddd']

                sydfile = {
                    'file_name': synam,
                    'file_size': file.file_size,
                    'message_id': message.id,
                    'media': file,
                    'topic': int(mrsyd),
                    'season': sydmen,
                    'repm': syd1,
                    'repw': syd2,
                    'message': message
                }
                mrsydt_g.append(sydfile)
               # await client.send_message(1733124290, text=". ")    # Add to the queue in order
               # if not processing:
                  #  processing = True  # Set processing flag
                   # await process_queue(client, syd)
    except Exception as e:
        logger.error(f"An error occurred while processing message {message_id}: {e}")

@Client.on_message(filters.command("process") & filters.user(1733124290))
async def process_quee(client, message):
    global processing
    try:
        # Process files one by one from the queue
        await client.send_message(1733124290, text="Pʀᴏᴄᴄᴇꜱꜱɪɴɢ!")
        while mrs:
            file_details = mrs.pop(0)# Get the first file in the queue
            await autosyd(client, file_details)  # Process i
        await client.send_message(1733124290, text="Done!")
    finally:
        processing = False  # Reset the processing flag



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
patternX = re.compile(r'\b(?!19[8-9]\d|20[0-4]\d)\d{1,4}(?!p)\b', re.IGNORECASE)
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
  #  match = re.search(pattern3_2, filename)
   # if match:
     #   print("Matched Pattern 3_2")
      #  return match.group(1)  # Extracted episode number
        
    # Try Pattern 4
    match = re.search(pattern4, filename)
    if match:
        print("Matched Pattern 4")
        return match.group(2)  # Extracted episode number

    # Try Pattern X
    match = re.search(patternX, filename)
    if match:
        print("Matched Pattern X")
        return match.group(0)  # Extracted episode number
        
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
    return '1'

# Example Usage:
filename = "Naruto Shippuden S01 - EP07 - 1080p [Dual Audio].mkv"
episode_number = extract_episode_number(filename)
print(f"Extracted Episode Number: {episode_number}")

# Inside the handler for file uploads


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
        return await client.send_message(1733124290, "Unsupported File Type")
        
  #  pat1 = re.sub(pattern1, "", sydd)
  #  pat2 = re.sub(pattern2, "", pat1)
   # pat3 = re.sub(pattern3, "", pat2)
   # pat4 = re.sub(pattern3_2, "", pat3)
   # pat5 = re.sub(pattern4, "", pat4)
  #  pat6 = re.sub(patternX, "", pat5)
   # pat7 = re.sub(season_pattern1, "", pat6)
  #  sydX = re.sub(season_pattern2, "", pat7)
    if file_id in renaming_operations:
        elapsed_time = (datetime.now() - renaming_operations[file_id]).seconds
        if elapsed_time < 10:
            print("File is being ignored as it is currently being renamed or was renamed recently.")
            return  # Exit the handler if the file is being ignored
    renaming_operations[file_id] = datetime.now()
    episode_number = extract_episode_number(file_name) or extract_episode_number(message.caption)
    qualit = extract_quality(file_name) or extract_quality(message.caption) or '4k'
    if qualit == "2160p":
        return
    season_no = extract_season_number(file_name) or '01'
    print(f"Extracted Episode Number: {season_no}")
    print(f"Extracted Episode Number: {episode_number}")
    
    if episode_number and season_no:
        syd_tg = int(episode_number)
        syd_xyz = int(season_no)
        tg_Syd_Xyz = file_details['season']
        if tg_Syd_Xyz == "True":
            formatted_episode = f"S{syd_xyz:02d}E{syd_tg:02d} "
        else:
            formatted_episode = f"E{syd_tg:02d} "
        Syd = formatted_episode + sydd
        mrsyds = ['YTS.MX', 'SH3LBY', 'Telly', 'Moviez', 'NazzY', 'VisTa', 'PiRO', 'PAHE', 'ink', 'mkvcinemas', 'CZ', 'WADU', 'PrimeFix', 'HDA', 'PSA', 'GalaxyRG', '-Bigil', 'TR', 'www.', '@',
            '-TR', '-SH3LBY', '-Telly', '-NazzY', '-PAHE', '-WADU', 'MoviezVerse', 't3nzin', '[Tips', 'Eac3', '(@'
                 ]
        sydmen = await db.get_rep(1733124290)
        syd1 = sydmen['sydd']
        syd2 = sydmen['syddd']
        sydd1 = file_details['repw']
        sydd2 = file_details['repm']
        if syd1 in Syd:
            Syd = Syd.replace(syd1, syd2)
        remove_list = ['-', '⌯', '[AL]', '[AH]', 'Esub', '(x265)', '[JoyBoy]', '[KDL]', '@Anime_Fair', '@Klands', 'Syd', 'KDL', 'foooir', '[', ']']
        for item in remove_list:
            Syd = Syd.replace(item, "")
        if '[Dual]' in Syd:
            Syd = Syd.replace('[Dual]', 'Dual')
        if '{quality}' in Syd:
            Syd = Syd.replace('{quality}', qualit)
        if '[Multi]' in Syd:
            Syd = Syd.replace('[Multi]', 'Multi')
        if '[Sub]' in Syd:
            Syd = Syd.replace('[Sub]', 'Sub')
        if fulsyd in Syd:
            Syd = Syd.replace(fulsyd, "")
        filenme = ' '.join([
            x for x in Syd.split()
            if not any(x.startswith(mrsyd) for mrsyd in mrsyds) and x != '@GetTGLinks'
        ])
        if sydd1 in filenme:
            filenme = filenme.replace(sydd1, sydd2)
        if '_' in filenme:
            filenme = filenme.replace('_', ' ')
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

        download_msg = await client.send_message(1733124290, text=f"<code>{sydd}</code> Trying To Download.....")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=(f"<code>{sydd}</code> Download Started....", download_msg, time.time()))
        except Exception as e:
            # Mark the file as ignored
            del renaming_operations[file_id]
            return await download_msg.edit(e)     

        _bool_metadata = await db.get_metadata(1733124290)

        if (_bool_metadata):
            metadata_path = f"Metadata/{new_file_name}"
            metadata = await db.get_metadata_code(1733124290)
            if metadata:

                await download_msg.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
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
                        return await download_msg.edit(str(er) + "\n\n**Error**")
                except BaseException:
                    pass

        duration = 0
        try:
            parser = createParser(file_path)
            metadata = extractMetadata(parser)
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            parser.close()

        except:
            pass

       # shutil.copy(file_path, syd_path)
        upload_msg = await download_msg.edit("Trying To Uploading.....")
        ph_path = None
        c_caption = await madflixbotz.get_caption(1733124290)
        c_thumb = await madflixbotz.get_thumbnail(1733124290)

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
                last_season_number = 0
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
        if syd_xyz != last_season_number:
            try:
                if syd_xyz != 1:
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
            mrsyd = await db.get_dump(1733124290)
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                sydfil = await client.send_document(
                    mrsyd,
                    document=metadata_path if _bool_metadata else file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> Upload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                sydfil = await client.send_video(
                    mrsyd,
                    video=metadata_path if _bool_metadata else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=("Upload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                sydfil = await client.send_audio(
                    mrsyd,
                    audio=metadata_path if _bool_metadata else file_path,
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
        #if mrsyyd != mrssyd:
           # await sydfil.delete()
            #os.remove(file_path)
           # if ph_path:
             #   os.remove(ph_path)
          #  del renaming_operations[file_id]
           # return await message.reply_text("Size Error")
        #if mrsyyd != mrsssyd:
            #await sydfile.delete()
            #os.remove(syd_path)
            #if ph_path:
                #os.remove(ph_path)
            #del renaming_operations[file_id]
            #return await message.reply_text("Size Error")
        if season_no == 0:
            await client.send_message(1733124290, f'Season No. 0 Error <code>{new_file_name}</code>')
        if episode_number == 0:
            await client.send_message(1733124290, f'Episode No. 0 Error <code>{new_file_name}</code>')
        #os.remove(file_path)
        #os.remove(syd_path)
        #await message.delete()
        try:  # Replace with the actual thread ID of the topic
            await client.copy_message(
                chat_id=-1002322136660,  # Replace with the target group ID
                from_chat_id=mrsyd,
                message_id=sydfil.id,
                reply_to_message_id=topic_syd_id
            )
        except Exception as e:
            return await client.send_message(1733124290, f"Failed to forward to topic: {e}")

# Remove the entry from renaming_operations after successful renaming
       # del renaming_operations[file_id]
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
        remove_list = ['-', '[AL]', '[AH]', '[KDL]', '@Anime_Fair', '@Klands', 'www', 'KDL', 'fair', '[', ']']
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
        topic_syd_id = file_details['topic']
        download_msg = await client.send_message(1733124290, text=f"<code>{sydd}</code> Trying To Download.....")
        try:
            path = await client.download_media(message=file, file_name=file_path, progress=progress_for_pyrogram, progress_args=("Download Started....", download_msg, time.time()))
        except Exception as e:
            # Mark the file as ignored
            del renaming_operations[file_id]
            return await download_msg.edit(e)
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
        _bool_metadata = await db.get_metadata(1733124290)

        if (_bool_metadata):
            metadata_path = f"Metadata/{new_file_name}"
            metadata = await db.get_metadata_code(1733124290)
            if metadata:

                await download_msg.edit("I Fᴏᴜɴᴅ Yᴏᴜʀ Mᴇᴛᴀᴅᴀᴛᴀ\n\n__**Pʟᴇᴀsᴇ Wᴀɪᴛ...**__\n**Aᴅᴅɪɴɢ Mᴇᴛᴀᴅᴀᴛᴀ Tᴏ Fɪʟᴇ....**")
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
                        return await download_msg.edit(str(er) + "\n\n**Error**")
                except BaseException:
                    pass

        duration = 0
        try:
            parser = createParser(file_path)
            metadata = extractMetadata(parser)
            if metadata.has("duration"):
                duration = metadata.get('duration').seconds
            parser.close()

        except:
            pass
       # shutil.copy(file_path, syd_path)
        upload_msg = await download_msg.edit(f"<code>{sydd}</code> Trying To Uploading.....")
        ph_path = None
        c_caption = await madflixbotz.get_caption(1733124290)
        c_thumb = await madflixbotz.get_thumbnail(1733124290)
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
            mrsyd = await db.get_dump(1733124290)
            type = media_type  # Use 'media_type' variable instead
            if type == "document":
                sydfil = await client.send_document(
                    mrsyd,
                    document=metadata_path if _bool_metama else file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> Upload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                sydfil = await client.send_video(
                    mrsyd,
                    video=metadata_path if _bool_metadata else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> Upload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                sydfil = await client.send_audio(
                    mrsyd,
                    audio=metadata_path if _bool_metadata else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> Upload Started.....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")
        await download_msg.edit(f'No ᴇᴩɪꜱᴏᴅᴇ ɴᴜᴍʙᴇʀ ᴀɴᴅ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ <code>{new_file_name}</code>')
        mrsyyd = sydfil.document.file_size if type == "document" else sydfil.video.file_size if type == "video" else sydfil.audio.file_size
        mrssyd = message.document.file_size if type == "document" else message.video.file_size if type == "video" else message.audio.file_size
        try:  # Replace with the actual thread ID of the topic
            await client.copy_message(
                chat_id=-1002322136660,  # Replace with the target group ID
                from_chat_id=mrsyd,
                message_id=sydfil.id,
                reply_to_message_id=topic_syd_id
            )
        except Exception as e:
            return await client.send_message(1733124290, f"Failed to forward to topic: {e}")
    if mrsyyd != mrssyd:
        await sydfil.delete()
        try:  # Use 'media_type' variable instead
            if type == "document":
                newsydfil = await client.send_document(
                    mrsyd,
                    document=metadata_path if _bool_metadata else file_path,
                    thumb=ph_path,
                    caption=caption,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> ReUpload Started.....", upload_msg, time.time())
                )
            elif type == "video":
                newsydfil = await client.send_video(
                    mrsyd,
                    video=metadata_path if _bool_metadata else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> ReUpload Started.....", upload_msg, time.time())
                )
            elif type == "audio":
                newsydfil = await client.send_audio(
                    mrsyd,
                    audio=metadata_path if _bool_metadata else file_path,
                    caption=caption,
                    thumb=ph_path,
                    duration=duration,
                    progress=progress_for_pyrogram,
                    progress_args=(f"<code>{sydd}</code> ReUpload Started.....", upload_msg, time.time())
                )
        except Exception as e:
            os.remove(file_path)
            if ph_path:
                os.remove(ph_path)
            # Mark the file as ignored
            return await upload_msg.edit(f"Error: {e}")
        mrsydnew = newsydfil.document.file_size if type == "document" else newsydfil.video.file_size if type == "video" else newsydfil.audio.file_size
        os.remove(file_path)
        if ph_path:
            os.remove(ph_path)
        del renaming_operations[file_id]
        return await client.send_message(1733124290, f"<code>{sydd}</code> ʀᴇᴜᴩʟᴏᴀᴅᴇᴅ")

        if mrsyyd != mrsydnew:
            if ph_path:
                os.remove(ph_path)
            if metadata_path:
                os.remove(metadata_path)
            return await client.send_message(1733124290, f"<code>{sydd}</code> ꜱɪᴢᴇ ᴍɪꜱᴍᴀᴛᴄʜ ᴀꜰᴛᴇʀ ꜱᴇᴄᴏɴᴅ ᴛʀʏ")
    if ph_path:
        os.remove(ph_path)
    if _bool_metadata:
        os.remove(metadata_path)

    os.remove(file_path)
    del renaming_operations[file_id]
    syd_id = -1002289521919
    mrsyd_id = 9521
    try:
        chat_message = await client.get_messages(syd_id, mrsyd_id)
        syd_text = chat_message.text + f'\n <code>{sydd}</code>'
        await client.edit_message_text(chat_id=syd_id, message_id=mrsyd_id, text=syd_text)
    except Exception as e:
        print(f"An error occurred: {e}")
    

