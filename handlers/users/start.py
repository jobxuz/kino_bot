import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton

from data.config import ADMINS
from loader import dp, db, bot
from keyboards.inline.inlinekey import til
from utils.misc import subcription
from keyboards.default.adminKey import admincommands


#channelget = db.select_all_channels()
#channelget = ['-1002213884791']


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    chat_id = message.from_user.id
    username = message.from_user.username
    fulname = message.from_user.first_name
    date = str(message.date)
    # Foydalanuvchini bazaga qo'shamiz
    try:
        db.add_user(chat_id=chat_id,first_name=fulname,username=username,date=date)
        for admin in ADMINS:
            await bot.send_message(chat_id=admin,text=f" {message.from_user.first_name} bazaga qoshildi")
    except sqlite3.IntegrityError as err:
        for admin in ADMINS:
            await bot.send_message(chat_id=admin, text=err)

    user1 = db.select_user(chat_id=chat_id)

    if user1[4] == None:
        await message.reply(f"🇺🇿 Tilni tanlang\n🇺🇸 Select a language\n🇷🇺 Выберите язык", reply_markup=til)
    else:
        await message.answer('salom')

    user = message.from_user.id
    final_status = True
    btn = InlineKeyboardMarkup(row_width=1)
    for channel in db.select_all_channels():
        status = await subcription.check(user_id=user, channel=channel[0])
        final_status *= status
        chat = await bot.get_chat(channel[0])
        if status:
            invite_link = await chat.export_invite_link()
            btn.insert(InlineKeyboardButton(text=f"✅ {chat.title}", url=invite_link))
        if not status:
            invite_link = await chat.export_invite_link()
            btn.insert(InlineKeyboardButton(text=f"❌ {chat.title}", url=invite_link))
    btn.add(InlineKeyboardButton(text="♻️Obunani tekshirish", callback_data="check_subs"))
    if final_status:
        if message.from_user.id == 1363350178:
            await bot.send_message(chat_id=message.from_user.id,
                                       text=f"Assalomu alaykum {message.from_user.first_name} siz adminsiz",
                                       reply_markup=admincommands)
        else:
            await message.answer(f"Assalomu alaykum {message.from_user.full_name}!\n"
                                     f"Botdan foydalanish uchun kerakli bo'limni tanlang!")
    if not final_status:
        await message.answer("Botdan to'liq foydalanish uchun quyidagi kanallarga obuna bo'ling!",
                                 disable_web_page_preview=True, reply_markup=btn)





    
