from aiogram import executor

from loader import dp
import middlewares, filters, handlers
from utils.notify_admins import on_startup_notify
from utils.set_bot_commands import set_default_commands
from loader import db

async def on_startup(dispatcher):
    # Birlamchi komandalar (/star va /help)
    await set_default_commands(dispatcher)

    # Bot ishga tushgani haqida adminga xabar berish
    await on_startup_notify(dispatcher)
    
    print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    await db.create()
    print("============================================================= ochildi")
    
    
executor.start_polling(dp, on_startup=on_startup)

 
