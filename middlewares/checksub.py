import logging
from aiogram import types
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import InlineKeyboardMarkup,InlineKeyboardButton
#from data.config import CHANNELS
from utils.misc import subcription
from loader import bot,db
#from handlers.users.date import channelget
#from keyboards.inline.InlineKeyboards import til
#from handlers.users.date import user

#channelget = db.select_all_channels()
#channelget = ['-1002213884791']

class BigBrother(BaseMiddleware):
    async def on_pre_process_update(self, update: types.Update, data: dict):
        #oneuser = db.select_user(chat_id=update.from_user.id)
        if update.message:
            userr = update.message.from_user.id
            #userone = user(user_id=str(update.message.from_user.id))
            if update.message.text in ['/start', '/help']:
                return
            # if userone[-1] == None:
            #     await update.message.answer(f"🇺🇿 Tilni tanlang\n🇺🇸 Select a language\n🇷🇺 Выберите язык", reply_markup=til)

            # elif userone[-1] == 'uzbek':
            result = "Botdan to'liq foydalanish uchun quyidagi kanallarga obuna bo'ling!\n"
            final_status = True
            btn = InlineKeyboardMarkup(row_width=1)
            for channel in db.select_all_channels():
                status = await subcription.check(user_id=userr,
                                                      channel=channel[0])
                final_status *= status
                channel = await bot.get_chat(channel[0])
                if status:
                    invite_link = await channel.export_invite_link()
                    btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
                if not status:
                    invite_link = await channel.export_invite_link()
                    btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
            btn.add(InlineKeyboardButton(text="♻️Obunani tekshirish", callback_data="check_subs"))
            if not final_status:
                await update.message.answer(result, disable_web_page_preview=True, reply_markup=btn)
                raise CancelHandler()


            # elif userone[-1] == 'english':
            #     result = "Subscribe to the following channels to get the most out of the bot!\n"
            #     final_status = True
            #     btn = InlineKeyboardMarkup(row_width=1)
            #     for channel in CHANNELS:
            #         status = await subscription.check(user_id=user,
            #                                           channel=channel)
            #         final_status *= status
            #         channel = await bot.get_chat(channel)
            #         if status:
            #             invite_link = await channel.export_invite_link()
            #             btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
            #         if not status:
            #             invite_link = await channel.export_invite_link()
            #             btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
            #     btn.add(InlineKeyboardButton(text="♻️Check subscription", callback_data="check_subs"))
            #     if not final_status:
            #         await update.message.answer(result, disable_web_page_preview=True, reply_markup=btn)
            #         raise CancelHandler()


            # elif userone[-1] == 'rus':
            #     result = "Подпишитесь на каналы ниже, чтобы получить максимальную отдачу от бота!\n"
            #     final_status = True
            #     btn = InlineKeyboardMarkup(row_width=1)
            #     for channel in CHANNELS:
            #         status = await subscription.check(user_id=user,
            #                                           channel=channel)
            #         final_status *= status
            #         channel = await bot.get_chat(channel)
            #         if status:
            #             invite_link = await channel.export_invite_link()
            #             btn.add(InlineKeyboardButton(text=f"✅ {channel.title}", url=invite_link))
            #         if not status:
            #             invite_link = await channel.export_invite_link()
            #             btn.add(InlineKeyboardButton(text=f"❌ {channel.title}", url=invite_link))
            #     btn.add(InlineKeyboardButton(text="♻️Проверить подписку", callback_data="check_subs"))
            #     if not final_status:
            #         await update.message.answer(result, disable_web_page_preview=True, reply_markup=btn)
            #         raise CancelHandler()


        elif update.callback_query:
            userr = update.callback_query.from_user.id
            #if update.callback_query.data in ['check_subs','uzbek', 'english', 'rus']:
            if update.callback_query.data == "check_subs":
                return
        else:
            return