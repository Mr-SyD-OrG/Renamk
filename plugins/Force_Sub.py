from pyrogram import Client, filters, enums 
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import Config
from helper.database import db

async def not_subscribed(_, client, message):
    await db.add_user(client, message)
    if not Config.FORCE_SUB:
        return False
    try:             
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id) 
        if user.status == enums.ChatMemberStatus.BANNED:
            return True 
        else:
            return False                
    except UserNotParticipant:
        pass
    return True


@Client.on_message(filters.private & filters.create(not_subscribed))
async def forces_sub(client, message):
    buttons = [[InlineKeyboardButton(text="📢 Join Update Channel 📢", url=f"https://t.me/{Config.FORCE_SUB}") ]]
    text = "**Sᴏʀʀy Bʀᴏ 🥲, \nYᴏᴜ'ʀᴇ Nᴏᴛ Jᴏɪɴᴇᴅ My Cʜᴀɴɴᴇʟ 😐. Sᴏ Pʟᴇᴀꜱᴇ Jᴏɪɴ Oᴜʀ Uᴩᴅᴀᴛᴇ Cʜᴀɴɴᴇʟ Tᴏ Cᴄᴏɴᴛɪɴᴜᴇ Pʟᴇᴀꜱᴇ⚡⚡\n ⚡⚡⚡⚡**"
    try:
        user = await client.get_chat_member(Config.FORCE_SUB, message.from_user.id)    
        if user.status == enums.ChatMemberStatus.BANNED:                                   
            return await client.send_message(message.from_user.id, text="Sᴏʀʀy Yᴏᴜ'ʀᴇ Bᴀɴɴᴇᴅ Tᴏ Uꜱᴇ Mᴇ")  
    except UserNotParticipant:                       
        return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
    return await message.reply_text(text=text, reply_markup=InlineKeyboardMarkup(buttons))
          




from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
import re

CHANNEL_ID = -1001234567890  # 🔁 Replace this with your target channel ID

@Client.on_message(filters.command("addbot") & filters.private)
async def add_bot_handler(client, message: Message):
    async def ask_user(prompt: str):
        sent = await message.reply(f"🔸 {prompt}\n\nType /cancel to cancel.")
        try:
            response = await client.listen(chat_id=message.chat.id, timeout=60000)
            if response.text.lower() == "/cancel":
                await response.reply("❌ Cancelled.")
                return None
            return response
        except asyncio.TimeoutError:
            await sent.reply("⏰ Timed out.")
            return None

    await message.reply("🔍 Let's gather the details for the new bot.")

    # Step 1: Referral Link
    q1 = await ask_user("Send the referral link:\n`https://t.me/username?start=173290`")
    if not q1: return
    match = re.search(r"https://t\.me/(\w+)\?start=\w+", q1.text)
    if not match:
        return await message.reply("❌ Invalid referral link format.")
    username = match.group(1)
    name = username.replace("_", "")
    ref_link = q1.text
    name_link = f"[{name}]({ref_link})"

    # Step 2: Category
    q2 = await ask_user("Category? (`ꜱᴛᴀʀꜱ` | `ᴩʀᴇᴍɪᴜᴍ` | `ꜱᴛᴀʀꜱ ᴀɴᴅ ᴩʀᴇᴍɪᴜᴍ`)")
    if not q2: return
    cat = q2.text

    # Step 3: Criteria
    q3 = await ask_user("Criteria? (`ɢᴀᴍᴇ` | `ʀᴇꜰᴇʀ` | `ᴏᴛʜᴇʀꜱ`)")
    if not q3: return
    cri = q3.text

    # Step 4: Verified
    q4 = await ask_user("Verified? (`ᴛʀᴜᴇ` | `ꜰᴀʟꜱᴇ`)")
    if not q4: return
    ver = q4.text

    # Step 5: Validity
    q5 = await ask_user("Validity? (`ᴜɴᴋɴᴏᴡɴ` | `ꜰᴇᴡ ᴅᴀʏꜱ` | `ꜱᴛᴏᴩᴩᴇᴅ` | `ᴇxᴩɪʀᴇᴅ` | `ʟɪꜰᴇᴛɪᴍᴇ`)")
    if not q5: return
    val = q5.text

    # Step 6: Per Refer
    q6 = await ask_user("Per refer? (`1 ꜱᴛᴀʀ` | `2 ꜱᴛᴀʀ` | `3 ꜱᴛᴀʀ` | `ᴩᴏɪɴᴛꜱ`)")
    if not q6: return
    ref = q6.text

    # Step 7: Min Withdrawal
    q7 = await ask_user("Minimum refer?")
    if not q7: return
    min_amt = q7.text

    # Step 8: More info (optional)
    q8 = await ask_user("More info? (or /skip)")
    more = "**ᴍᴏʀᴇ ɪɴꜰᴏ :** " + q8.text + "\n" if q8 and q8.text.lower() != "/skip" else ""

    # 🔷 Final formatted message
    bot_info = f"""\
**ɴᴇᴡ ʙᴏᴛ** : {name_link}
**ᴄᴀᴛᴇɢᴏʀʏ** : {cat}
**ᴄʀɪᴛᴇʀɪᴀ** : {cri}
**ᴠᴇʀɪꜰɪᴇᴅ** : {ver}
**ᴡᴏʀᴋɪɴɢ** : {val}
**ᴩᴇʀ ʀᴇꜰᴇʀ** : {ref}
**ᴍɪɴ ʀᴇꜰᴇʀ** : {min_amt}
{more}
__**ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ'ꜱ ɪɴꜰᴏʀᴍᴀᴛɪᴏɴ ᴍᴀʏ ɴᴏᴛ ʙᴇ ᴜᴩ ᴛᴏ ᴅᴀᴛᴇ ᴏʀ ᴍᴀʏ ʙᴇ ꜰᴀʟꜱᴇ, ᴩʟᴇᴀꜱᴇ ᴄʜᴇᴄᴋ ʏᴏᴜʀꜱᴇʟꜰ.__
__[*ᴛᴇʀᴍꜱ ᴀɴᴅ ᴄᴏɴᴅɪᴛɪᴏɴꜱ](https://t.me/Free_Stars_Premium_Bots/3) ᴀᴩᴩʟɪᴇᴅ**__
"""

    # 🔻 Send first message to channel
    sent_msg = await client.send_message(
        chat_id=-1002559631421,
        text=bot_info,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("ᴏᴩᴇɴ ʙᴏᴛ", url=ref_link)]]
        ),
        disable_web_page_preview=True
    )

    # 🔺 Send a query message as a reply to that
    

    await message.reply("✅ Bot info posted to channel.")

    # 🧾 Also return query example
    print(f"To respond in channel:\nReply to message ID {sent_msg.id} with your verdict.")


