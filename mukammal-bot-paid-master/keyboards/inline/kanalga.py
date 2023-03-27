from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
checker = InlineKeyboardMarkup(
    inline_keyboard=[
          [InlineKeyboardButton('➕1-kanal',url="https://t.me/testforbotp")],
          [InlineKeyboardButton('➕2-kanal',url="https://t.me/+MRXn6cPIspxlYThi")],
          [InlineKeyboardButton("Tekshirish",callback_data="check")]
    
    ])
    # return azobol
variantlar = InlineKeyboardMarkup(
    inline_keyboard=[
          [InlineKeyboardButton('A',callback_data="A"),InlineKeyboardButton("B",callback_data="B")],
          [InlineKeyboardButton('C',callback_data="C"),InlineKeyboardButton("D",callback_data="D")]
    
    ])
tasdiqlash = InlineKeyboardMarkup(
    inline_keyboard=[
    [InlineKeyboardButton("Tasdiqlash",callback_data="Tasdiqlash")],
    [InlineKeyboardButton("Bekor qilish",callback_data="Bekor qilish")]
    ]
)