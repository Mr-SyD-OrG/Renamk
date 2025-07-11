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

logger = logging.getLogger(__name__)
user_locks = {}
MRSYD = ["📈", "😔", "🙂", "😅", "😁", "🥹", "⚠️", "✅", "😐", "😇", "🤩", "🥰", "😍", "🤗", "😋", "😜", "🤖", "✋🏻", "👋🏻", "❤️", "🙏🏻", "👀", "⬇️", "↙️", "⬆️", "↗️", "▶️", "♂️", "♀️", "❌", "❓", "❗", "❔", "❕", "➕", "➖", "🤪", "😪", "😶", "🤯", "😎"]
@Client.on_message(filters.private & filters.command("start"))
async def start(client, message):

    if message.from_user.id in Config.BANNED_USERS:
        await message.reply_text("Sorry, You are banned.")
        return

    user = message.from_user
    await db.add_user(client, message)
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
        await message.reply_photo(random.choice(Config.PICS), caption=Txt.STRT_TXT.format(user.mention), reply_markup=button)
    else:
        await message.reply_text(text=Txt.STRT_TXT.format(user.mention), reply_markup=button, disable_web_page_preview=True)


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

@Client.on_message(filters.private & (filters.video | filters.animation | filters.photo))
async def ask_convert_button(client, message):
    if message.video and message.video.duration > 30:
        await message.reply("Vɪᴅᴇᴏ ᴛᴏᴏ ʟᴏɴɢ! Mᴀx 30 ꜱᴇᴄᴏɴᴅꜱ ᴀʟʟᴏᴡᴇᴅ.")
        return

    await message.reply(
        "Dᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴍᴇ ᴛᴏ ᴄᴏɴᴠᴇʀᴛ ᴛʜɪꜱ ᴍᴇᴅɪᴀ ɪɴᴛᴏ ᴀ ꜱᴛɪᴄᴋᴇʀ ?",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("🎨 Cᴏɴᴠᴇʀᴛ", callback_data=f"convert_{message.id}")]]
        )
    )

import os
import ffmpeg
import asyncio
import aiohttp
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton


@Client.on_callback_query(filters.regex("^convert_"))
async def convert_media_to_sticker(client, cb):
    user_id = cb.from_user.id
    if user_locks.get(user_id):
        await cb.answer("ᴏɴᴇ ᴩʀᴏᴄᴇꜱꜱ ɪꜱ ᴀʟʀᴇᴀᴅʏ ɪɴ ᴩʀᴏɢʀᴇꜱꜱ, ᴩʟᴇᴀꜱᴇ ᴡᴀɪᴛ ᴜɴᴛɪʟ ɪᴛ'ꜱ ᴏᴠᴇʀ. 🙂", show_alert=True)
        return
    user_locks[user_id] = True
    username = cb.from_user.username or f"user{user_id}"
    message_id = int(cb.data.split("_")[1])
    bot_info = await client.get_me()

    # Get original message
    message = await client.get_messages(cb.message.chat.id, message_id)
    
    # Detect type
    if message.photo:
        media_type = "static"
    elif message.video or message.animation:
        media_type = "video"
    else:
        await cb.message.reply("Unsupported media type. \n⚠️ Rᴇᴩᴏʀᴛ ɪꜰ ɪᴛ'ꜱ ᴇʀʀᴏʀ @SyD_XyZ ")
        user_locks.pop(user_id, None)
        return

    SyD = await cb.message.reply("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▢▢▢▢▢▢▢▢] 10%")
    await cb.message.delete()

    base_set_name = f"{username}_{media_type}_by_{bot_info.username}"

    # Get sticker set name from DB or init
    user_data = await db.users.find_one({"user_id": user_id}) or {}
    sticker_set_name = user_data.get(f"{media_type}_set") or base_set_name

    await cb.answer("⏳ Cᴏɴᴠᴇʀᴛɪɴɢ, ᴩʟᴇᴀꜱᴇ ᴡᴀɪᴛ...", show_alert=True)

    # Download to temp
    ext = ".png" if media_type == "static" else ".webm"
    temp_file = f"/tmp/{user_id}_{message.id}{ext}"
    await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▢▢▢▢▢▢▢] 20%")
    await message.download(temp_file)
    await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▢▢▢▢▢▢] 30%")
    loop = asyncio.get_event_loop()
    token = Config.SYD_TOKEN
    ok = False

    # Process file
  
    await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▢▢▢▢▢] 40%")
    ok = False  # <-- define before branching

    if media_type == "static":
        await loop.run_in_executor(None, resize_image_to_png, temp_file)
        res = await add_sticker_to_set(token, user_id, sticker_set_name, temp_file, random.choice(MRSYD), media_type)
        if res.get("ok"):
            ok = True
        else:
            await cb.message.reply(f"Fᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ꜱᴛɪᴄᴋᴇʀ: {res} \n⚠️ Rᴇᴩᴏʀᴛ ᴇʀʀᴏʀ ʙʏ ꜰᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ: @SyD_XyZ ")
    else:
        bitrates = ['300K', '200K', '100K', '50K', '10K']
        tried = 0
        while tried < len(bitrates):
            bitrate = bitrates[tried]
            tried += 1
            temp_out = f"{temp_file}_tmp.webm"
            await loop.run_in_executor(None, convert_to_webm_ffmpeg, temp_file, temp_out, bitrate)

            # Replace original file with re-encoded smaller one
            if os.path.exists(temp_out):
                os.replace(temp_out, temp_file)

            res = await add_sticker_to_set(token, user_id, sticker_set_name, temp_file, random.choice(MRSYD), media_type)
            if res.get("ok"):
                ok = True
                break
            elif "file is too big" in str(res).lower():
                continue
            else:
                await cb.message.reply(f"Fᴀɪʟᴇᴅ ᴛᴏ ᴀᴅᴅ ꜱᴛɪᴄᴋᴇʀ: {res}\n⚠️ Rᴇᴩᴏʀᴛ ɪꜰ ɪᴛ'ꜱ ᴇʀʀᴏʀ @SyD_XyZ  ")
                break

        await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▣▢▢▢▢] 50%")
        if not ok and tried == len(bitrates):
            await cb.message.reply("Fɪʟᴇ ɪꜱ ꜱᴛɪʟʟ ᴛᴏᴏ ʟᴀʀɢᴇ ᴀꜰᴛᴇʀ ꜱᴇᴠᴇʀᴀʟ ᴛʀɪᴇꜱ. Pʟᴇᴀꜱᴇ ꜱᴇɴᴅ ꜱʜᴏʀᴛᴇʀ ᴏʀ **ʟᴏᴡᴇʀ-qᴜᴀʟɪᴛʏ** ᴠɪᴅᴇᴏ.")
            user_locks.pop(user_id, None)
            cleanup(temp_file)
            await SyD.delete()
            return

    try:
        await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▣▢▢▢▢] 50%")  # debug to see if code reaches here
    except:
        pass
    
    # Try to create sticker set if not exists
    if not ok:
        exists = await sticker_set_exists(token, sticker_set_name)
        await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▣▣▢▢▢] 60%")
        if not exists:
            title = f"{username}'s Stickers By @Video_To_Stickers_Bot"
            res = await create_new_sticker_set(token, user_id, sticker_set_name, title, temp_file, random.choice(MRSYD), media_type)
            if res.get("ok"):
                await db.users.update_one({"user_id": user_id}, {"$set": {f"{media_type}_set": sticker_set_name}}, upsert=True)
                ok = True
            else:
                await cb.message.reply(f"Fᴀɪʟᴇᴅ ᴛᴏ ᴄʀᴇᴀᴛᴇ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ: {res}  \n⚠️ Rᴇᴩᴏʀᴛ ᴇʀʀᴏʀ ʙʏ ꜰᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ: @SyD_XyZ")
                cleanup(temp_file)
                user_locks.pop(user_id, None)
                await SyD.delete()
                return
        await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▣▣▣▢▢] 80%")
         
    # Success: send sticker + button
    if ok:
        await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▣▣▣▣▢] 90%")
        res = await get_sticker_set(Config.SYD_TOKEN, sticker_set_name)
        if res.get("ok") and res["result"]["stickers"]:
            last_sticker = res["result"]["stickers"][-1]
            await cb.message.reply_sticker(
                last_sticker["file_id"],
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Oᴩᴇɴ Sᴛɪᴄᴋᴇʀ Sᴇᴛ ➚", url=f"https://t.me/addstickers/{sticker_set_name}")]]
                )
            )
        else:
            await cb.message.reply(f"Cᴏᴜʟᴅ ɴᴏᴛ ɢᴇᴛ ꜱᴛɪᴄᴋᴇʀ ꜱᴇᴛ: {res}  \n⚠️ Rᴇᴩᴏʀᴛ ᴇʀʀᴏʀ ʙʏ ꜰᴏʀᴡᴀʀᴅɪɴɢ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ ᴛᴏ: @SyD_XyZ")
    else:
        await cb.message.reply("Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ ᴡʀᴏɴɢ, ꜰᴏʀ ʜᴇʟᴩ ᴍᴇꜱꜱᴀɢᴇ ᴏᴡɴᴇʀ.")
    await SyD.edit("Gᴇɴᴇʀᴀᴛɪɴɢ : [▣▣▣▣▣▣▣▣▣] 100%")
    await asyncio.sleep(1)
    await SyD.delete()
    user_locks.pop(user_id, None)

    cleanup(temp_file)









    
@Client.on_message(filters.command("start") & filters.chat(-1002687879857))
async def sydstart(client, message):
    await message.reply_text(".")


def cleanup(*files):
    for f in files:
        if os.path.exists(f):
            os.remove(f)
async def sticker_set_exists(token, name):
    async with aiohttp.ClientSession() as s:
        r = await s.get(f"https://api.telegram.org/bot{token}/getStickerSet", params={"name":name})
        j = await r.json()
        return j.get("ok", False)

async def create_new_sticker_set(token, user_id, name, title, file_path, emojis, media_type):
    url = f"https://api.telegram.org/bot{token}/createNewStickerSet"
    fmt = "video" if media_type=="video" else "static"
    field = "webm_sticker" if media_type=="video" else "png_sticker"
    async with aiohttp.ClientSession() as s:
        with open(file_path,'rb') as f:
            form = aiohttp.FormData()
            form.add_field("user_id", str(user_id))
            form.add_field("name", name)
            form.add_field("title", title)
            form.add_field("sticker_format", fmt)
            form.add_field("emojis", emojis)
            form.add_field(field, f, filename=os.path.basename(file_path))
            r = await s.post(url, data=form)
            return await r.json()

async def add_sticker_to_set(token, user_id, name, file_path, emojis, media_type):
    url = f"https://api.telegram.org/bot{token}/addStickerToSet"
    field = "webm_sticker" if media_type=="video" else "png_sticker"
    async with aiohttp.ClientSession() as s:
        with open(file_path,'rb') as f:
            form = aiohttp.FormData()
            form.add_field("user_id", str(user_id))
            form.add_field("name", name)
            form.add_field("emojis", emojis)
            form.add_field(field, f, filename=os.path.basename(file_path))
            r = await s.post(url, data=form)
            return await r.json()

async def get_sticker_set(token, name):
    url = f"https://api.telegram.org/bot{token}/getStickerSet"
    params = {"name": name}
    async with aiohttp.ClientSession() as s:
        async with s.get(url, params=params) as r:
            return await r.json()

def resize_image_to_png(path):
    from PIL import Image
    im = Image.open(path).convert("RGBA")
    im.thumbnail((512,512))
    im.save(path, "PNG")

def convert_to_webm_ffmpeg(input_path, output_path, bitrate="300K"):
    (
        ffmpeg
        .input(input_path)
        .filter('scale', 'if(gt(a,1),512,-1)', 'if(gt(a,1),-1,512)', force_original_aspect_ratio='decrease')
        .output(
            output_path,
            vcodec='libvpx-vp9',
            pix_fmt='yuv420p',
            **{'b:v': bitrate},
            an=None,
            r=30
        )
        .run(overwrite_output=True)
    )
