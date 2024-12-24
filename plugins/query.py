import shutil
import time
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from config import Config, Txt
from helper.database import db
import random
import psutil
from info import AUTH_CHANNEL
from syd import is_req_subscribed
from helper.utils import humanbytes


@Client.on_callback_query()
async def cb_handler(client, query: CallbackQuery):
    data = query.data
    if data == "start":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.START_TXT.format(query.from_user.mention),

            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton(
                    '⛅ Uᴩᴅᴀᴛᴇꜱ', url='https://t.me/Bot_Cracker'),
                InlineKeyboardButton(
                    'Sᴜᴩᴩᴏʀᴛ ⛈️', url='https://t.me/+O1mwQijo79s2MjJl')
            ], [
                InlineKeyboardButton('❄️ Δʙᴏᴜᴛ', callback_data='about'),
                InlineKeyboardButton('ʙΔᴄᴋ-ᴜᴩ 🗯️', url='https://t.me/+1C8Usv5MSzA3MGM1'),
                InlineKeyboardButton('Hᴇʟᴩ ❗', callback_data='help')
            ], [InlineKeyboardButton('⊛ Jᴏɪɴ ᴍᴏᴠɪєꜱ CʜᴀɴɴᴇL ⊛', url='https://t.me/Mod_Moviez_X')
            ]])
        )
    elif data == "help":

        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.HELP_TXT

            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
                
            ]])
        )

    elif data == "sydcheck":
        if AUTH_CHANNEL and not await is_req_subscribed:
          await query.answer("ʀᴇQᴇᴜꜱᴛ ᴛᴏ Jᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴍᴀʜɴ! 😒 Dᴏɴᴛ ᴛʀʏ ᴛᴏ ꜱʜᴏᴡ ʏᴏᴜʀ ᴏᴠᴇʀꜱᴍᴀʀᴛɴᴇꜱꜱ ᴩʟᴢ🥲🥲", show_alert=True)
          return
        await query.message.edit_text("<b>Oᴋ✅, ʏᴏᴜ ᴄΔɴ ᴄᴏɴᴛɪɴᴜᴇ ʏᴏᴜʀ ᴩʀᴏᴄᴇꜱꜱ.... Δɴᴅ Tʜᴀɴᴋꜱ ꜰᴏʀ ᴜꜱɪɴɢ ᴏᴜʀ ʙᴏᴛ... 🧭\nPʟᴇᴀꜱᴇ Rᴇ-Fᴏʀᴡᴀʀᴅ ʏᴏᴜʀ Ғɪʟᴇ Tᴏ ᴄᴏɴᴛɪɴᴜᴇ... 🪭</b>")


    elif data == "about":
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.ABOUT_TXT.format(client.mention),

            ),

            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("ᐊ ʙᴀᴄᴋ", callback_data="start"),
                InlineKeyboardButton("✘ ᴄʟᴏsᴇ", callback_data="close")
                
            ]])
        )

    elif data == 'stats':
        buttons = [[InlineKeyboardButton(
            '• ʙᴀᴄᴋ', callback_data='start'), InlineKeyboardButton('⟲ ʀᴇʟᴏᴀᴅ', callback_data='stats')]]
        reply_markup = InlineKeyboardMarkup(buttons)
        currentTime = time.strftime("%Hh%Mm%Ss", time.gmtime(
            time.time() - Config.BOT_UPTIME))
        total, used, free = shutil.disk_usage(".")
        total = humanbytes(total)
        used = humanbytes(used)
        free = humanbytes(free)
        cpu_usage = psutil.cpu_percent()
        ram_usage = psutil.virtual_memory().percent
        disk_usage = psutil.disk_usage('/').percent
        await query.message.edit_media(
            InputMediaPhoto(
                random.choice(Config.PICS),
                Txt.STATS_TXT.format(
                    currentTime, total, used, disk_usage, free, cpu_usage, ram_usage)
            ),
            reply_markup=reply_markup
        )

    elif data == 'userbot':
        userBot = await db.get_user_bot(query.from_user.id)

        text = f"Name: {userBot['name']}\nUserName: @{userBot['username']}\n UserId: {userBot['user_id']}"

        await query.message.edit(text=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('❌ ʀᴇᴍᴏᴠᴇ ❌', callback_data='rmuserbot')], [InlineKeyboardButton('✘ ᴄʟᴏsᴇ ✘', callback_data='close')]]))

    elif data == 'rmuserbot':
        try:
            await db.remove_user_bot(query.from_user.id)
            await query.message.edit(text='**User Bot Removed Successfully ✅**', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('✘ ᴄʟᴏsᴇ ✘', callback_data='close')]]))
        except:
            await query.answer(f'Hey {query.from_user.first_name}\n\n You have already deleted the user')

    elif data == 'season_false':
        await db.set_sydson(query.from_user.id, "False")
        await query.message.edit_text(
            text="Sᴇᴛ ᴛʀᴜᴇ ᴏʀ ꜰᴀʟꜱᴇ, ɪꜰ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ ɪꜱ ᴛᴏ ʙᴇ ɪɴ ꜰɪʟᴇ ᴇᴠᴇʀʏᴛɪᴍᴇ (ɪꜰ ꜰɪʟᴇ ᴅᴏɴᴛ ʜᴀᴠᴇ ꜱᴇᴀꜱᴏɴ ɴᴏ. ɪᴛ ᴡɪʟʟ ʙᴇ ᴅᴇꜰᴜᴀʟᴛ ᴛᴏ 1) ᴏʀ ꜰᴀʟꜱᴇ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴇᴀꜱᴏɴ ᴛᴀɢ",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Tʀᴜᴇ ✅", callback_data="season_true")
            ],[
                InlineKeyboardButton("✖️ Close", callback_data="close")
            ]])          
        )
            
    elif data == 'season_true':
        await db.set_sydson(query.from_user.id, "True")
        await query.message.edit_text(
            text="Sᴇᴛ ᴛʀᴜᴇ ᴏʀ ꜰᴀʟꜱᴇ, ɪꜰ ꜱᴇᴀꜱᴏɴ ɴᴜᴍʙᴇʀ ɪꜱ ᴛᴏ ʙᴇ ɪɴ ꜰɪʟᴇ ᴇᴠᴇʀʏᴛɪᴍᴇ (ɪꜰ ꜰɪʟᴇ ᴅᴏɴᴛ ʜᴀᴠᴇ ꜱᴇᴀꜱᴏɴ ɴᴏ. ɪᴛ ᴡɪʟʟ ʙᴇ ᴅᴇꜰᴜᴀʟᴛ ᴛᴏ 1) ᴏʀ ꜰᴀʟꜱᴇ ᴛᴏ ᴀᴠᴏɪᴅ ꜱᴇᴀꜱᴏɴ ᴛᴀɢ",
            reply_markup=InlineKeyboardMarkup([[
                InlineKeyboardButton("Fᴀʟꜱᴇ ✖️", callback_data="season_false")
            ],[
                InlineKeyboardButton("✖️ Close", callback_data="close")
            ]])          
        )
    elif data == "close":
        try:
            await query.message.delete()
            await query.message.reply_to_message.delete()
            await query.message.continue_propagation()
        except:
            await query.message.delete()
            await query.message.continue_propagation()
