from config import Config
from pyrogram import Client, filters, enums


API_ID = Config.API_ID
API_HASH = Config.API_HASH
ADMINS = Config.ADMIN

@Client.on_message(filters.command("clone") & filters.user(ADMINS))
async def clone_menu(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ ɪᴅ__\n\nExᴀᴍᴩʟᴇ:- `/set_dump -1002042969565`**")
    mrsyd = message.text.split(" ", 1)[1]
    syd = Client(
        f"{mrsyd}", API_ID, API_HASH,
        bot_token=mrsyd,
        plugins={"root": "For"}
    )
    await syd.start()
    await message.reply_text("✅")
