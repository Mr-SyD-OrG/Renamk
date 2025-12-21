import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait

@Client.on_message(filters.command("forward", prefixes="/"))
async def forward_messages(client, message):
    try:
        # /forward from_chat to_chat start_id end_id pause_seconds
        parts = message.text.split()
        if len(parts) < 5:
            return await message.reply(
                "Usage: `/forward {from} {to} {start_id} {end_id} {pause_seconds}`",
                quote=True
            )

        from_chat = parts[1]
        to_chat = parts[2]
        start_id = int(parts[3])
        end_id = int(parts[4])
        pause_seconds = float(parts[5]) if len(parts) > 5 else 1.0

        sent_count = 0
        total_messages = end_id - start_id + 1
        progress_msg = await message.reply("Forwarding started...")

        for msg_id in range(start_id, end_id + 1):
            try:
                msg = await client.get_messages(from_chat, msg_id)
                if not msg:
                    continue

                while True:
                    try:
                        await msg.copy(to_chat)
                        sent_count += 1
                        break
                    except FloodWait as e:
                        print(f"FloodWait: Sleeping {e.value} seconds for message {msg_id}")
                        await asyncio.sleep(e.value)
                    except Exception as e:
                        print(f"Failed to copy message {msg_id}: {e}")
                        break

                if sent_count % 100 == 0:
                    try:
                        await progress_msg.edit_text(
                            f"📤 Forwarded {sent_count}/{total_messages} messages..."
                        )
                    except Exception as e:
                        print(f"Progress edit failed: {e}")

                await asyncio.sleep(pause_seconds)

            except Exception as e:
                print(f"Error fetching message {msg_id}: {e}")

        await progress_msg.edit_text("✅ Forwarding completed.")

    except Exception as e:
        await message.reply(f"❌ Error: {e}")
        
from pyrogram import Client, filters
from pyrogram.errors import FloodWait
import asyncio

SOURCE_CHANNEL = -1003583073724   # channel to listen
TARGET_CHANNEL = -1003342276289   # channel to copy into


@Client.on_message(filters.chat(SOURCE_CHANNEL))
async def copy_incoming_message(client: Client, message):
    while True:
        try:
            await message.copy(TARGET_CHANNEL)
            break  # ✅ copied successfully

        except FloodWait as e:
            await asyncio.sleep(e.value + 1)  # ⏳ wait & retry SAME message

        except Exception as e:
            # ❌ real error → skip message
            print(f"Copy failed for msg {message.id}: {e}")
            break
