from pyrogram import Client, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, Message)

from bot import bot
from bot.config import OWNER_USERID, SUDO_USERID
from bot.database import database


@Client.on_message(filters.command(["start"]))
async def start(_, message: Message):
    await database.saveUser(message.from_user)
    return await message.reply_text("Hello! I am a simple bot that can download files from the internet. Send me a link to get started.")


@Client.on_message(filters.new_chat_members, group=1)
async def newChat(_, message: Message):
    """
    Get notified when someone add bot in the group, then saves that group chat_id
    in the database.
    """
    chatid = message.chat.id
    for new_user in message.new_chat_members:
        if new_user.id == bot.me.id:
            await database.saveChat(chatid)
