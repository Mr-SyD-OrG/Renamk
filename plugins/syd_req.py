from pyrogram import Client, filters, enums
from pyrogram.types import ChatJoinRequest
from helper.database import db
from config import Config
from info import AUTH_CHANNEL

ADMINS = Config.ADMIN

@Client.on_chat_join_request(filters.chat(AUTH_CHANNEL))
async def join_reqs(client, message: ChatJoinRequest):
  if not await db.find_join_req(message.from_user.id):
    await db.add_join_req(message.from_user.id)

@Client.on_message(filters.command("delreq") & filters.private & filters.user(ADMINS))
async def del_requests(client, message):
    await db.del_join_req()    
    await message.reply("<b>⚙ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ᴄʜᴀɴɴᴇʟ ʟᴇғᴛ ᴜꜱᴇʀꜱ ᴅᴇʟᴇᴛᴇᴅ</b>")

from pyrogram import Client, filters
from pyrogram.types import Message
import re

CHANNEL_ID = -1002691749157  # replace with your target channel ID

@Client.on_message(filters.command("addbot") & filters.private)
async def add_new_bot(client, message: Message):
    async def ask(prompt):
        await message.reply(prompt + "\n\n(Use /cancel to stop)", quote=True)
        response = await client.ask(message.chat.id, timeout=120)
        if response.text.lower() == "/cancel":
            await response.reply("❌ Cancelled.")
            raise Exception("Cancelled")
        return response.text.strip()

    try:
        # Ask for referral link
        referral_text = await ask("🔗 Sᴇɴᴅ ʀᴇꜰᴇʀᴀʟ ʟɪɴᴋ (like `https://t.me/username?start=173290`)")
        match = re.search(r"https://t\.me/([\w\d_]+)\?start=\d+", referral_text)
        if not match:
            await message.reply("❌ Invalid referral link format.")
            return
        username = match.group(1).replace("_", "")
        name = f"[{username}](https://t.me/{match.group(1)}?start=173290)"
        ref_link = f"https://t.me/{match.group(1)}?start=173290"

        # Ask for category
        cat = await ask("🗂 Sᴇɴᴅ ᴄᴀᴛᴇɢᴏʀʏ (like `stars`, `premium`, or `stars and premium`)")

        # Ask for criteria
        cri = await ask("🎯 Sᴇɴᴅ ᴄʀɪᴛᴇʀɪᴀ (`game` | `refer`)")

        # Ask for verified
        ver = await ask("✔️ Iꜱ ʙᴏᴛ ᴠᴇʀɪꜰɪᴇᴅ? (`true` | `false`)")

        # Ask for validity
        val = await ask("🕐 Sᴇɴᴅ ᴠᴀʟɪᴅɪᴛʏ (`unknown` | `few days` | `today` | `expired`)")

        # Ask for per refer
        ref = await ask("🎁 Sᴇɴᴅ ᴘᴇʀ ʀᴇꜰᴇʀ ʀᴇᴡᴀʀᴅ (`1 star` | `2 star` | `3 star`)")

        # Ask for minimum withdrawal
        min = await ask("💸 Sᴇɴᴅ ᴍɪɴ ᴡɪᴛʜᴅʀᴀᴡ")

        # Ask for optional more info
        await message.reply("ℹ️ Sᴇɴᴅ ᴍᴏʀᴇ ɪɴꜰᴏ (or /skip to skip)", quote=True)
        more_response = await client.ask(message.chat.id, timeout=120)
        if more_response.text.lower() == "/cancel":
            await more_response.reply("❌ Cancelled.")
            return
        more = more_response.text if more_response.text.lower() != "/skip" else "N/A"

        # Final message
        final_text = f"""\
ɴᴇᴡ ʙᴏᴛ       : {name}
ᴄᴀᴛᴇɢᴏʀʏ      : {cat}
ᴄʀɪᴛᴇʀɪᴀ       : {cri}
ᴠᴇʀɪꜰɪᴇᴅ       : {ver}
ᴠᴀʟɪᴅɪᴛʏ       : {val}
ᴩᴇʀ ʀᴇꜰᴇʀ     : {ref}
ᴍɪɴ ᴡɪᴛʜᴅʀᴀᴡ  : {min}
ᴍᴏʀᴇ ɪɴꜰᴏ     : {more}

({cat.lower()})
🔗 {ref_link}"""

        await client.send_message(CHANNEL_ID, final_text, disable_web_page_preview=True)
        await message.reply("✅ ʙᴏᴛ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ!")

    except Exception as e:
        print("AddBot Cancelled or Failed:", e)

