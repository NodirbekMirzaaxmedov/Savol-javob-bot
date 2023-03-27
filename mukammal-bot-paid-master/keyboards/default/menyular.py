from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
menyular = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("❓Savol"),KeyboardButton("🤑Balans")],
        [KeyboardButton("💸Pul Chiqarish"),KeyboardButton("👥Referal")],
        [KeyboardButton("👨‍💻Dasturchi bilan aloqa")]
    ]
)
kontakt = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("📲Kontakt ulashish",request_contact=True)]
    ]
)
savol_ber = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("❓Savol berish"),KeyboardButton("📊Statistika")],
        [KeyboardButton("🗑Hamma eski savollarni o'chirish")],
        [KeyboardButton("👥Yangi savolar haqida bildirish")]
    ]
)

chiqish = ReplyKeyboardMarkup(
    resize_keyboard=True,
    keyboard=[
        [KeyboardButton("❌Testdan chiqish")]
    ]
)