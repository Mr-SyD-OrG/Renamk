import logging
import logging.config
import warnings
from pyrogram import Client, idle
from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from config import Config
from aiohttp import web
from plugins.web_support import web_server
from pytz import timezone
from datetime import datetime
import asyncio

import pyromod

logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("pymongo").setLevel(logging.ERROR)


class Bot(Client):

    def __init__(self):
        super().__init__(
            name="SnowRenamer",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=200,
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        app = web.AppRunner(await web_server())
        await app.setup()
        bind_address = "0.0.0.0"
        await web.TCPSite(app, bind_address, Config.PORT).start()
        logging.info(f"{me.first_name} ✅✅ BOT started successfully ✅✅")

        if Config.WOOK:
            syyd = Client(
                "SyDLnK",
                api_hash=Config.API_HASH,
                api_id=Config.API_ID,
                plugins={
                "root": "SyD"
                },
                workers=50,
                bot_token=Config.SYD_TOKEN
            )
            try:
                await syyd.start()
            except Exception as e:
                logging.info(f"{e}")
        for id in Config.ADMIN:
            try:
                await self.send_message(id, f"**__{me.first_name}  Iꜱ Sᴛᴀʀᴛᴇᴅ.....✨️__**")
            except:
                pass

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot Stopped 🙄")


bot = Bot()
bot.run()
