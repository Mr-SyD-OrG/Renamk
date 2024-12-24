from pyrogram import Client, filters, enums
from helper.database import db
import re

@Client.on_message(filters.private & filters.command('set_prefix'))
async def add_caption(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @Roofiverse`**")
    prefix = message.text.split(" ", 1)[1]
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_prefix(message.from_user.id, prefix)
    await SnowDev.edit("__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('del_prefix'))
async def delete_prefix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await db.get_prefix(message.from_user.id)
    if not prefix:
        return await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await db.set_prefix(message.from_user.id, None)
    await SnowDev.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")


@Client.on_message(filters.private & filters.command('see_prefix'))
async def see_caption(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    prefix = await db.get_prefix(message.from_user.id)
    if prefix:
        await SnowDev.edit(f"**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{prefix}`")
    else:
        await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")


# SUFFIX
@Client.on_message(filters.private & filters.command('set_suffix'))
async def add_csuffix(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Suffix__\n\nExᴀᴍᴩʟᴇ:- `/set_suffix @Roofiverse`**")
    suffix = message.text.split(" ", 1)[1]
    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_suffix(message.from_user.id, suffix)
    await SnowDev.edit("__**✅ ꜱᴜꜰꜰɪx ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('del_suffix'))
async def delete_suffix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await db.get_suffix(message.from_user.id)
    if not suffix:
        return await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
    await db.set_suffix(message.from_user.id, None)
    await SnowDev.edit("__**❌️ ꜱᴜꜰꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")


@Client.on_message(filters.private & filters.command('see_suffix'))
async def see_csuffix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await db.get_suffix(message.from_user.id)
    if suffix:
        await SnowDev.edit(f"**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`")
    else:
        await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
        
@Client.on_message(filters.private & filters.command('set_dump'))
async def add_dump(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @Roofiverse`**")
    dump = message.text.split(" ", 1)[1]
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_dump(message.from_user.id, dump)
    await SyD.edit("__**✅ ᴘʀᴇꜰɪx ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('del_dump'))
async def delete_dump(client, message):

    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_dump(message.from_user.id)
    if not dump:
        return await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await db.set_dump(message.from_user.id, message.from_user.id)
    await SyD.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")


@Client.on_message(filters.private & filters.command('see_from'))
async def see_csuffix(client, message):

    SnowDev = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    suffix = await db.get_syd(message.from_user.id)
    if suffix:
        await SnowDev.edit(f"**ʏᴏᴜʀ ꜱᴜꜰꜰɪx:-**\n\n`{suffix}`")
    else:
        await SnowDev.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ꜱᴜꜰꜰɪx**__")
        
@Client.on_message(filters.private & filters.command('set_from'))
async def add_dump(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @Roofiverse`**")
    frm = message.text.split(" ", 1)[1]
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_syd(message.from_user.id, frm)
    await SyD.edit("__**✅ ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('del_from'))
async def delete_dump(client, message):

    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_dump(message.from_user.id)
    if not dump:
        return await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await db.set_syd(message.from_user.id, message.from_user.id)
    await SyD.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('see_dump'))
async def see_dump(client, message):

    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_dump(message.from_user.id)
    if dump:
        await SyD.edit(f"**ʏᴏᴜʀ ᴘʀᴇꜰɪx:-**\n\n`{dump}`")
    else:
        await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")

@Client.on_message(filters.private & filters.command('set_dump'))
async def add_dump(client, message):

    if len(message.command) == 1:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @Roofiverse`**")
    dump = message.text.split(" ", 1)[1]
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_dump(message.from_user.id, dump)
    await SyD.edit("__**✅ ꜱᴀᴠᴇᴅ**__")


@Client.on_message(filters.private & filters.command('set_rep'))
async def add_rep(client, message):
    if len(message.command) < 3:
        return await message.reply_text("**__Give The Prefix__\n\nExᴀᴍᴩʟᴇ:- `/set_prefix @Roofiverse`**")
    txt = message.text.split(" ", 2)
    Sydd = txt[1]
    Syddd = txt[2] if txt[2] else ''
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_rep(message.from_user.id, Sydd, Syddd)
    await SyD.edit("__**ꜱᴀᴠᴇᴅ !**__")


@Client.on_message(filters.private & filters.command('del_rep'))
async def delete_rep(client, message):
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    dump = await db.get_rep(message.from_user.id)
    if not dump:
        return await SyD.edit("__**😔 ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴀɴʏ ᴘʀᴇꜰɪx**__")
    await db.set_rep(message.from_user.id, None, None)
    await SyD.edit("__**❌️ ᴘʀᴇꜰɪx ᴅᴇʟᴇᴛᴇᴅ**__")

@Client.on_message(filters.private & filters.command('set_topic'))
async def add_topic(client, message):
    if len(message.command) == 1:
        return await message.reply_text("**__Give The ᴅᴜᴍᴩ ᴄʜᴀɴɴᴇʟ ɪᴅ__\n\nExᴀᴍᴩʟᴇ:- `/set_dump -1002042969565`**")
    mrsyd = message.text.split(" ", 1)[1]
   # mrsyd = await client.ask(message.from_user.id, "<b>ꜱᴇɴᴅ ᴍᴇ ᴛʜᴇ ᴛᴏᴩɪᴄ ɪᴅ ᴏʀ ʟɪɴᴋ.\n\n/cancel - ᴄᴀɴᴄᴇʟ ᴛʜɪs ᴘʀᴏᴄᴇss.</b>")
    if mrsyd.startswith("https://t.me/"):
        match = re.search(r"/(\d+)$", mrsyd)
        if match:
            topic_id = match.group(1)
            txt = topic_id
        else:
            return await message.reply("<b>⚠ Invalid link provided. Make sure it ends with a numeric topic ID.</b>")
    else:
        txt = mrsyd.split(" ", 1)[0]
    SyD = await message.reply_text("Please Wait ...", reply_to_message_id=message.id)
    await db.set_topic(message.from_user.id, txt)
    await SyD.edit("__**✅ ᴛᴏᴩɪᴄ ꜱᴀᴠᴇᴅ**__")
