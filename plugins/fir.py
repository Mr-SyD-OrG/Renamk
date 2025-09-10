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


from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid, UsernameNotOccupied
import re, asyncio

# Regex to catch @usernames and links like t.me/username
USERNAME_REGEX = re.compile(
    r"(?:@|(?:https?://)?t\.me/|(?:https?://)?telegram\.me/)([a-zA-Z0-9_]{5,32})",
    re.IGNORECASE
)

@Client.on_message(filters.command("search"))
async def search_usernames(bot: Client, message):
    try:
        args = message.text.split()
        if len(args) < 3:
            return await message.reply("⚠️ Usage:\n`/search {username} {last_message_id} {skip (optional)}`\n\nReply this to a forwarded msg from the group/channel.")

        username = args[1].lower()
        last_msg_id = int(args[2])
        skip = int(args[3]) if len(args) > 3 else 0

        # Get target chat
        if not message.reply_to_message or not message.reply_to_message.forward_from_chat:
            return await message.reply(
                "ℹ️ Forward **one message from the group/channel** you want to scan, "
                "then send `/search ...` as a reply to it."
            )

        target_chat = message.reply_to_message.forward_from_chat.id
        found = []

        await message.reply(f"🔎 Scanning `{username}` in {target_chat} from ID {last_msg_id} (skip {skip})...")

        count = 0
        for msg_id in range(last_msg_id, 0, -1):  # go backwards
            if count < skip:
                count += 1
                continue

            try:
                msg = await bot.get_messages(target_chat, msg_id)
            except Exception:
                continue

            if not msg or not msg.text:
                continue

            # find usernames in text
            for match in USERNAME_REGEX.finditer(msg.text):
                uname = match.group(1)
                if uname.lower().startswith(username):
                    try:
                        await bot.get_users(uname)  # exists
                    except (PeerIdInvalid, UsernameNotOccupied):
                        if uname not in found:
                            found.append(uname)
                            await message.reply(f"✅ Available: @{uname}")
                    except Exception as e:
                        print(f"[ERROR] checking {uname}: {e}")

            count += 1
            await asyncio.sleep(0.5)  # avoid flood

        if not found:
            await message.reply("❌ No available usernames found.")
        else:
            await message.reply(f"🎉 Finished! Found `{len(found)}` available usernames.")

    except Exception as e:
        await message.reply(f"⚠️ Error: {e}")
