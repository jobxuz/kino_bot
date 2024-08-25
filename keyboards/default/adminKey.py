from aiogram.types import ReplyKeyboardMarkup,KeyboardButton


admincommands = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="admin panel")
        ],
        
    ],
    resize_keyboard=True
)

adminusers = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="users"),
        ],
        [
            KeyboardButton(text="reklama"),
        ],
          [
            KeyboardButton(text="Kanal qo'shish"),
            KeyboardButton(text="Kanal o'chirish")
        ],
          [
            KeyboardButton(text="Kino qo'shish")
        ],
         [
            KeyboardButton(text="Kinolar")
        ],
          [
            KeyboardButton(text="Kanallar")
        ],
          [
            KeyboardButton(text="🚫 Bekor qilish")
        ],
        [
            KeyboardButton(text="back")
        ],
    ],
    resize_keyboard=True
)