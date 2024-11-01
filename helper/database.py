import motor.motor_asyncio
from config import Config
from .utils import send_log
import datetime
import aiohttp


class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.db = self._client[database_name]
        self.col = self.db.user
        self.bot = self.db.bots
        self.req = self.db.requests

    async def find_join_req(self, id):
        return bool(await self.req.find_one({'id': id}))
        
    async def add_join_req(self, id):
        await self.req.insert_one({'id': id})
        
    async def del_join_req(self):
        await self.req.drop()
        
    def new_user(self, id):
        return dict(
            _id=int(id),
            file_id=None,
            caption=None,
            prefix=None,
            suffix=None,
            metadata=False,
            metadata_code=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- " -metadata author="@" -metadata:s:s title="Subtitled By :- @" -metadata:s:a title="By :- @" -metadata:s:v title="By:@""",
            dump=int(id),
            frm=int(id)
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)
            await send_log(b, u)

    async def add_user_bot(self, bot_datas):
        if not await self.is_user_bot_exist(bot_datas['user_id']):
            await self.bot.insert_one(bot_datas)

    async def get_user_bot(self, user_id: int):
        user = await self.bot.find_one({'user_id': user_id, 'is_bot': False})
        return user if user else None

    async def is_user_bot_exist(self, user_id):
        user = await self.bot.find_one({'user_id': user_id, 'is_bot': False})
        return bool(user)

    async def remove_user_bot(self, user_id):
        await self.bot.delete_many({'user_id': int(user_id), 'is_bot': False})

    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})

    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    async def set_dump(self, id, dump: int):
        await self.col.update_one({'_id': int(id)}, {'$set': {'dump': int(dump)}})

    async def get_dump(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('dump', int(id))

    async def set_syd(self, id, frm: int):
        await self.col.update_one({'_id': int(id)}, {'$set': {'frm': int(frm)}})

    async def get_syd(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('frm', int(id))
        
    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})

    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None)

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})

    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None)

    async def set_metadata(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata': bool_meta}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata', None)

    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def download_image(url, save_path):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(save_path, 'wb') as f:
                        f.write(await resp.read())
                    return save_path
                else:
                    raise Exception(f"Failed to download image, status code: {resp.status}")
                    
    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None)


db = Database(Config.DB_URL, Config.DB_NAME)
