from pyrogram import Client, filters
from pyrogram.types import Message
from helper.database import db
from pyromod.exceptions import ListenerTimeout
from config import Txt
from plugins.features import features_button


@Client.on_message(filters.private & filters.command('metadata'))
async def handle_metadata(bot: Client, message: Message):

    ms = await message.reply_text("**Please Wait...**")
    user_metadata = await db.get_metadata_code(message.from_user.id)
    markup = await features_button(message.from_user.id)

    await ms.edit(f'**ʜᴇʀᴇ ᴛʜᴇ ᴀᴠᴀɪʟᴀʙʟᴇ ғᴇᴀᴛᴜʀᴇ** 🍀**\n\nYour Current Metadata:-\n\n➜ `{user_metadata}` ', reply_markup=markup)


@Client.on_message(filters.private & filters.command('set_metadata'))
async def handle_set_metadata(bot: Client, message: Message):
    try:
        metadata = await bot.ask(text=Txt.SEND_METADATA, chat_id=message.from_user.id, filters=filters.text, timeout=30, disable_web_page_preview=True)
    except ListenerTimeout:
        await message.reply_text("⚠️ Error!!\n\n**Request timed out.**\nRestart by using /metadata", reply_to_message_id=message.id)
        return
    print(metadata.text)
    ms = await message.reply_text("**Please Wait...**", reply_to_message_id=metadata.id)
    await db.set_metadata_code(message.from_user.id, metadata_code=metadata.text)
    await ms.edit("**Your Metadta Code Set Successfully ✅**")


from pyrogram import Client, filters
from pyrogram.types import (
    ChatJoinRequest, InlineKeyboardMarkup,
    InlineKeyboardButton, CallbackQuery, Message
)
import asyncio


# /approve command (creates approve button)
@Client.on_message(filters.command("approve"))
async def approve_button_command(client: Client, message: Message):
    buttons = InlineKeyboardMarkup(
        [[InlineKeyboardButton("✅ Approve All Pending", callback_data="approve_all")]]
    )
    await message.reply("Click below to approve all pending join requests:", reply_markup=buttons)

# Handle button press
@Client.on_callback_query(filters.regex("^approve_all$"))
async def handle_approve_all(client: Client, callback_query: CallbackQuery):
    chat_id = callback_query.message.chat.id
    approved = 0
    user_ids = []

    try:
        async for req in client.get_chat_join_requests(chat_id):
            await client.approve_chat_join_request(chat_id, req.from_user.id)
            user_ids.append(req.from_user.id)
            approved += 1
            await asyncio.sleep(0.3)  # Prevent floodwait

        # Try sending DMs
        for uid in user_ids:
            await send_dm(client, uid)
            await asyncio.sleep(0.3)

        await callback_query.answer()
        await callback_query.edit_message_text(f"✅ Approved {approved} pending request(s).")

    except Exception as e:
        await callback_query.answer("❌ Error occurred!", show_alert=True)
        await callback_query.edit_message_text(f"❌ Error: {e}")

# Helper to send DM
async def send_dm(client: Client, user_id: int):
    markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✦ Uᴩᴅᴀᴛᴇꜱ", url="https://t.me/bot_Cracker"),
            InlineKeyboardButton("Cʜᴀɴɴᴇʟ ✦", url="https://t.me/Mod_Moviez_X")
        ],
        [
            InlineKeyboardButton("◈ Mᴏʀᴇ ◈", url="https://t.me/Instant_Approval_Bot?start=")
        ]
    ])
    try:
        await client.send_message(
            user_id,
            "Yᴏᴜʀ RᴇQᴜᴇꜱᴛ Tᴏ Jᴏɪɴ Tʜᴇ Cʜᴀᴛ Hᴀꜱ Bᴇᴇɴ Aᴄᴄᴇᴩᴛᴇᴅ Iɴꜱᴛᴀɴᴛʟʏ! 🎍\nTᴀᴩ Bᴇʟᴏᴡ Bᴜᴛᴛᴏɴ Tᴏ Kɴᴏᴡ Mᴏʀᴇ..! 🕯️",
            reply_markup=markup
        )
    except Exception as e:
        print(f"❌ Failed to DM {user_id}: {e}")
