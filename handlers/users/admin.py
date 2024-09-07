import asyncio
import logging

from aiogram import types
from aiogram.types import CallbackQuery

from data.config import ADMINS
from aiogram.dispatcher import FSMContext
from loader import dp, db, bot
from keyboards.default.adminKey import adminusers,admincommands
from keyboards.inline.inlinekey import rek
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import ContentType





class Channel(StatesGroup):
    name = State()
    channel_idi = State()


class Delete_channels(StatesGroup):
    name = State()



class Kino(StatesGroup):
    cod = State()
    name = State()
    file_id = State()
    



@dp.message_handler(text="🚫 Bekor qilish",state='*')
async def habar_end(message: types.Message, state: FSMContext):

    current_state = await state.get_state()
    if current_state is None:
        return
    logging.info('Cancelling state %r', current_state)

    await state.finish()

    await message.answer("Kerakli bo'limni tanlashingiz mumkun!")



@dp.message_handler(text="Kanallar", user_id=1363350178)
async def kanal_qoshish(message: types.Message):
    kanallar = db.select_all_channels()
    text =  f"Kanallar!\n\n"
    for kanal in kanallar:
        text+= f"{kanal[1]} || {kanal[0]} \n"
    await message.answer(text)
    

@dp.message_handler(text="Kinolar", user_id=1363350178)
async def kinolar(message: types.Message):
    kinolar = db.select_all_kino()[:50]
    text =  f"Kinolar!  || KINOLAR SONI: {len(kinolar)}\n\n"
    for kino in kinolar:
        text+= f"KINO KODI: {kino[0]} || KINO NOMI: {kino[2]} \n"
    await message.answer(text)



@dp.message_handler(text="Kanal qo'shish", user_id=1363350178)
async def kanal_qoshish(message: types.Message):
    await message.answer("Kanal nomini yozing")
    await Channel.name.set()



@dp.message_handler(state=Channel.name)
async def channel_name(message: types.Message,state: FSMContext):
    name = message.text

    await state.update_data(
        {"name": name}
    )
    
    await message.answer("Kanal Id sini kiriting")
    await Channel.next()




@dp.message_handler(state=Channel.channel_idi)
async def channel_id(message: types.Message,state: FSMContext):
    channe_id = message.text

    await state.update_data(
        {"channe_id": channe_id}
    )

    data = await state.get_data()
    name = data.get("name")
    channelId = data.get("channe_id")

    try:
        db.add_channels(channelId,name)
        await bot.send_message(chat_id=1363350178,text="Kanal qo'shildi")
    except Exception as e:
        await bot.send_message(chat_id=1363350178,text=e)

    await state.finish()




@dp.message_handler(text="Kino qo'shish", user_id=1363350178)
async def kino_qoshish(message: types.Message):
    await message.answer("Kino codini yozing")
    await Kino.cod.set()



@dp.message_handler(state=Kino.cod)
async def kino_cod(message: types.Message,state: FSMContext):
    cod = message.text

    await state.update_data(
        {"cod": cod}
    )
    
    await message.answer("Kino nomini yuboring!")
    await Kino.next()


@dp.message_handler(state=Kino.name)
async def kino_name(message: types.Message,state: FSMContext):
    name = message.text

    await state.update_data(
        {"name": name}
    )
    
    await message.answer("Kinoni yuboring!")
    await Kino.next()



@dp.message_handler(content_types=types.ContentTypes.VIDEO,state=Kino.file_id)
async def file_id(message: types.Message,state: FSMContext):

    file_id = message.video.file_id

    await state.update_data(
        {"file_id": file_id}
    )

    data = await state.get_data()
    cod = data.get("cod")
    name = data.get("name")
    fileid = data.get("file_id")

    try:
        db.add_kino(cod,fileid,name)
        await bot.send_message(chat_id=1363350178,text="Kino qo'shildi")
    except Exception as e:
        await bot.send_message(chat_id=1363350178,text=e)

    await state.finish()



@dp.message_handler(text="Kanal o'chirish", user_id=1363350178)
async def kanal_qoshish(message: types.Message):
    await message.answer("Kanal nomini yozing")
    await Delete_channels.name.set()



@dp.message_handler(state=Delete_channels.name)
async def channel_name(message: types.Message,state: FSMContext):
    name = message.text

    await state.update_data(
        {"name": name}
    )
    data = await state.get_data()
    name = data.get("name")


    try:
        db.delete_channels(name=name)
        await bot.send_message(chat_id=1363350178,text="Kanal o'chirildi")
    except Exception as e:
        await bot.send_message(chat_id=1363350178,text=e)

    await state.finish()
    


@dp.message_handler(text="/start", user_id=ADMINS)
async def get_all_users(message: types.Message):

    #await message.answer('admin panel',reply_markup=admincommands)
    await bot.send_message(chat_id=ADMINS[0],text='Siz adminsiz',reply_markup=admincommands)




@dp.message_handler(text="admin panel", user_id=ADMINS)
async def get_all_users(message: types.Message):

    await message.answer('admin panel',reply_markup=adminusers)




@dp.message_handler(text="users", user_id=ADMINS)
async def get_all_users(message: types.Message):
    count = db.count_users()
    users = db.select_all_users()[:50]
    text = f"instabot || Foydalanuvchilar soni: {count[0]}\n\n"
    for user in users:
        text+= f"{user[0]}). || {user[2]} || @{user[3]}\n"
    await message.answer(text)


@dp.message_handler(text="back", user_id=ADMINS)
async def back_button(message: types.Message):

    await message.answer('Bosh menyu',reply_markup=admincommands)


class Reklama(StatesGroup):
    message = State()




@dp.message_handler(text="reklama",user_id=ADMINS)
async def bot_start(message: types.Message):
    await message.answer("reklama yuboring")
    await Reklama.message.set()


@dp.message_handler(content_types=ContentType.ANY,state=Reklama.message)
async def answer_fullname(message: types.Message, state: FSMContext):
    habar = message.text

    await state.update_data(
        {"habar": habar}
    )
    data = await state.get_data()
    reklama = data.get("habar")

    msg = reklama
    
    for user in db.select_all_users():
        user_id = user[1]
        try:
            await message.send_copy(chat_id=user_id)
            await asyncio.sleep(0.05)
        except Exception as e:
            await bot.send_message(chat_id=ADMINS[0],text=f"{e}")
    await bot.send_message(chat_id=ADMINS[0],text=f"Reklama yuborildi! ✅")
    await state.finish()
