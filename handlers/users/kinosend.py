from aiogram import types

from loader import dp,db,bot


# Echo bot
@dp.message_handler()
async def kino_send(message: types.Message):

    try:
        kino_cod = int(message.text)
        try:
            kino = db.select_kino(cod=kino_cod)
            try:
                await bot.send_video(chat_id=message.chat.id, video=kino[1], 
                                     caption=f"#KINO_KODI {kino[0]}\n\n🧾 KINO NOMI: {kino[2]}\n\n\n🤖 Bizning bot: @newkino01bot")
            except:
                await message.answer("Kino yuborishda xatolik")
        except:
            await message.answer('Kino topilmadi!')
        
    except:
        await message.answer("Kino kodini yuboring!")