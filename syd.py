import logging
import asyncio
import pytz
import random 
import re
import os
from helper.database import db
from config import Config
#from info import AUTH_CHANNEL
from pyrogram.types import Message
from pyrogram.errors import InputUserDeactivated, UserNotParticipant, FloodWait, UserIsBlocked, PeerIdInvalid

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

async def is_req_subscribed(bot, query):
    if await db.find_join_req(query.from_user.id):
        return True
  #  try:
      #  user = await bot.get_chat_member(AUTH_CHANNEL, query.from_user.id)
    #except UserNotParticipant:
       # pass
   # except Exception as e:
      #  logger.exception(e)
   # else:
      #  if user.status != enums.ChatMemberStatus.BANNED:
        #    return True

    return False
