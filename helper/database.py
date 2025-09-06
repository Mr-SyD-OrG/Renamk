import motor.motor_asyncio
from config import Config
from .utils import send_log
import datetime
import aiohttp


async def download_image(url, save_path):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                with open(save_path, 'wb') as f:
                    f.write(await resp.read())
                return save_path
            else:
                raise Exception(f"Failed to download image, status code: {resp.status}")






db = None # Database(Config.DB_URL, Config.DB_NAME)
