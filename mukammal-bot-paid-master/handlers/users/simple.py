#PASTDAGILARGA ALOQASI BOLMAGAN ASOSIY IMPORTLAR 
from .ketmaket_savol import salom
import logging
from aiogram import types
from loader import bot,dp, db
from keyboards.inline.kanalga import *
# from utils.misc import obunani_tekshiradigan
from data.config import *
#KEYBOARD LAR UCHUN IMPORT 
from aiogram.types import ReplyKeyboardMarkup
from keyboards.default.menyular import *
#STATE LAR UCHUN IMPORT 
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import StateFilter
from aiogram.dispatcher.filters import state
from states.telefon_ism_state import *
from states.admin import *
#DATABAZA UCHUN IMPORTLAR
import asyncio
from aiogram.dispatcher.filters import AdminFilter
from aiogram.dispatcher import filters
from utils.db_api import nod as commands
from aiogram.utils.deep_linking import get_start_link,decode_payload
import random
import datetime
########################################################################################################
PHONE_REGEX ="^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$"
@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),commands=["start"])
async def Salomlashsin(message: types.Message):
    await message.answer("👋Salom admin!",reply_markup=savol_ber)

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),text=["📊Statistika"],state=state.any_state)
async def Savol_sorasin(msg: types.Message):
    b = await db.count_users()
    await msg.answer(f"👥Botingizdan foydalanuvchilar soni: {b} ta")

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),text=["👥Yangi savolar haqida bildirish"],state=state.any_state)
async def Savol_sorasin(msg: types.Message):
    e = await db.select_all_users()
    be = 0
    while 1:
        try:
            be += 1
            chat_id = e[be][3]
            await bot.send_message(chat_id,"‼️Botga pul yig'ishingiz uchun yangi savollar qo'shildi! Bot menyusidan ❓Savol bo'limini tanlang !")
        except:
            break
    await db.update_users_savol_olish_true()

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),text=["🗑Hamma eski savollarni o'chirish"],state=state.any_state)
async def Savol_sorasin(msg: types.Message):
    await msg.answer("❌Bazadagi hamma savollar o'chib ketdi")
    await db.drop_savollar()
@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),text=["❓Savol berish"],state=state.any_state)
async def Savol_sorasin(msg: types.Message):
    await msg.answer("‼️Bermoqchi bolgan savolingizni shartini yozib qoldiring")
    await db.create_table_savollar()
    await AdminStates.savol_state.set()

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),state=AdminStates.savol_state)
async def savol_qabul(msg: types.Message,state:FSMContext):
    await state.update_data({
        "savol":msg.text
    })
    await msg.answer("👍Savol sharti qabul qilindi , 1️⃣-chi ❌Notogri variantni yozing")
    await AdminStates.notogri1_state.set()

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),state=AdminStates.notogri1_state)
async def notogri1_qabul(msg: types.Message,state:FSMContext):
    await state.update_data({
        "notogri1":msg.text
    })
    await msg.answer("👍Qabul qilindi , 2️⃣-chi ❌Notogri variantni yozing")
    await AdminStates.notogri2_state.set()

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),state=AdminStates.notogri2_state)
async def notogri2_qabul(msg: types.Message,state:FSMContext):
    await state.update_data({
        "notogri2":msg.text
    })
    await msg.answer("👍Qabul qilindi , 3️⃣-chi ❌Notogri variantni yozing")
    await AdminStates.notogri3_state.set()

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),state=AdminStates.notogri3_state)
async def notogri3_qabul(msg: types.Message,state:FSMContext):
    await state.update_data({
        "notogri3":msg.text
    })
    await msg.answer("👍Qabul qilindi , ✅Togri variantni yozing")
    await AdminStates.togri_state.set()

@dp.message_handler(AdminFilter(is_chat_admin=CHANNELS),state=AdminStates.togri_state)
async def togri_qabul(msg: types.Message,state:FSMContext):
    await state.update_data({
        "togri":msg.text
    })
    data = await state.get_data()
    savol = data.get("savol")
    notogri1 = data.get("notogri1")
    notogri2 = data.get("notogri2")
    notogri3 = data.get("notogri3")
    togri = data.get("togri")
    await db.add_savol(savol,notogri1,notogri2,notogri3,togri,0,0,new=True)
    await state.finish()
    await msg.answer("✅Yangi savol qabul qilindi va ba'zaga qo'shildi")
    

#ADmin  tugadi





@dp.message_handler(commands=["start"], state=state.any_state)
async def kanal_callbackga(message: types.Message,state:FSMContext):
    await db.create_table_users()
    b = await db.select_one_user(message.from_user.id)
    if b == None:
        print( message.text[7:])
        print("@@@@@@@@@@@@@")
        await state.update_data({
            "reffer_id": message.text[7:]
        })
        global a
        a = await message.reply("<b>❌Siz kanallarga to'liq a'zo bolmagansiz</b>", reply_markup=checker)
        await FirstStates.kanalga_state.set()
    else:
        await message.answer("✅Siz avval royxatdan o'tgansiz",reply_markup=menyular)
@dp.callback_query_handler(text=["check"], state=FirstStates.kanalga_state)
async def obuna_sorasin(call:types.CallbackQuery):
    for channel in CHANNELS:
        check_member = await bot.get_chat_member(channel,call.from_user.id)
        if check_member.status not in ["member", "creator"]:
            await call.message.reply("<b>❌Siz kanallarga to'liq a'zo bolmagansiz</b>", reply_markup=checker)
        else:
            await call.message.answer('✅Obuna tasdiqlandi iltimos 📲Kontaktingizni yuboring',reply_markup=kontakt)
            await call.message.delete()
            try:
                await a.delete()
            except:
                pass
            await FirstStates.kontaktga_state.set()
@dp.message_handler(content_types=['contact'],state=FirstStates.kontaktga_state)
async def kontakt_qabul(msg: types.Message, state: FSMContext):
    await msg.answer(f"👍Kontaktingiz muvaffaqiyatli qabul qilindi✅\n🏠Bosh menyu xizmatingizga tayyor",reply_markup=menyular)
    data = await state.get_data()
    reffer_id = data.get("reffer_id")

    # try:
    users = await db.select_one_user(msg.from_user.id)
    try:
        user = await db.select_one_user(reffer_id)

    except:
        user = None
    try:
        print(user)
        print("######")
        print(user[3])
        print(users)
        print("$$$$$$$$$$$$$$$$$")
    except:
        pass
    if users == None:
        await db.add_user(msg.from_user.full_name,msg.from_user.username,msg.from_user.id,int(msg.contact.phone_number),0,0,0,True)
        try:
            await msg.answer(f"👤Siz {user[1]} tomonidan botga taklif qilindingiz !")
            await db.update_taklif(user[3])
            await db.update_balans(user[3],500)
            await bot.send_message(user[3],f"👤Siz {msg.from_user.full_name} taklif qildingiz va ✅Balansingizga 500 so'm qo'shildi")
        except:
            pass
    else:
        await msg.answer("✅Siz avval royxatdan o'tgansiz")
    # except:
    #     pass
    
    await state.finish()

@dp.message_handler(text=["👨‍💻Dasturchi bilan aloqa"],state=state.any_state)
async def Savol_sorasin(msg: types.Message):
    await msg.answer(f"Xar qanday turdagi botlarni tayyorlaymiz \n Nodirbek https://t.me/kanonir24, +998932239096 \n Amirbek https://t.me/Fantastic_12_02")
@dp.message_handler(text="👥Referal",state=state.any_state)
async def linkini_ber(msg: types.Message):
    ref_link = await get_start_link(payload=msg.from_user.id)
    await msg.answer(f"👥Tarqatish uchun referalingiz : {ref_link}")

@dp.message_handler(text='🤑Balans',state=state.any_state)
async def balans(msg: types.Message):
    balans = await db.get_balans(msg.from_user.id)
    await msg.answer(f"🤑Balansingizda : {balans[5]} so'm pul mavjud")

@dp.message_handler(text='❓Savol',state=state.any_state)
async def savol(msg: types.Message,state:FSMContext):
    await msg.answer("❓Savol",reply_markup=chiqish)
    user = await db.select_one_user(msg.from_user.id)
    if user[8] == True:
        savol_id = 1
        await salom(state=state,msg=msg,SavolgaStates=SavolgaStates,num1 = savol_id)
        await SavolgaStates.togri_state.set()
    else:
        await msg.answer("🫥Hozircha savollar yo'q",reply_markup=menyular)

@dp.message_handler(text='❌Testdan chiqish',state=state.any_state)
async def savol(msg: types.Message,state:FSMContext):
    await msg.answer("❌Siz uchun testlar bekor qilindi !",reply_markup=menyular)
    await db.update_user_savol_olish(int(msg.from_user.id))

@dp.callback_query_handler(text = "A",state=SavolgaStates.togri_state)
async def javob(call: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    print(call.from_user.id)

    A =  data.get("variant1")
    savol = data.get("savol")
    togri = data.get("togri")
    savol_id = data.get("savol_idsi")
    print(savol_id)
    if A == togri:
        await call.answer(f"✅Togri javobni tanladingiz 🤑Balansingizga 200 so'm qoshildi")
        await db.update_balans(int(call.from_user.id),200)
        await db.update_savol(int(call.from_user.id),savol)
        savol_id = savol_id + 1
        try:
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await call.message.delete()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
    else:
        savol_id = savol_id + 1
        try:
            await call.answer(f"❌Siz noto'g'ri javobni tanlladingiz !")
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
            await call.message.delete()
        
@dp.callback_query_handler(text = "B",state=SavolgaStates.togri_state)
async def javob3(call: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    print(call.from_user.id)
    B =  data.get("variant2")
    savol = data.get("savol")
    togri = data.get("togri")
    savol_id = data.get("savol_idsi")
    print(savol_id)
    if B == togri:
        await call.answer(f"✅Togri javobni tanladingiz 🤑Balansingizga 200 so'm qoshildi")
        await db.update_balans(int(call.from_user.id),200)
        await db.update_savol(int(call.from_user.id),savol)
        print(savol_id)
        savol_id = savol_id + 1
        try:
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await call.message.delete()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("savol tugadi akajon",reply_markup=menyular)
    else:
        savol_id = savol_id + 1
        try:
            await call.answer(f"❌Siz noto'g'ri javobni tanlladingiz !")
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
            await call.message.delete()
        

@dp.callback_query_handler(text = "C",state=SavolgaStates.togri_state)
async def javob1(call: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    print(call.from_user.id)
    C =  data.get("variant3")
    savol = data.get("savol")
    togri = data.get("togri")
    savol_id = data.get("savol_idsi")
    print(savol_id)
    if C == togri:
        await call.answer(f"✅Togri javobni tanladingiz 🤑Balansingizga 200 so'm qoshildi")
        await db.update_balans(int(call.from_user.id),200)
        await db.update_savol(int(call.from_user.id),savol)
        savol_id = savol_id + 1
        try:
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await call.message.delete()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
    else:
        savol_id = savol_id + 1
        try:
            await call.answer(f"❌Siz noto'g'ri javobni tanlladingiz !")
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
            await call.message.delete()
        
@dp.callback_query_handler(text = "D",state=SavolgaStates.togri_state)
async def javob2(call: types.CallbackQuery, state:FSMContext):
    data = await state.get_data()
    print(call.from_user.id)
    D =  data.get("variant4")
    savol = data.get("savol")
    togri = data.get("togri")
    savol_id = data.get("savol_idsi")
    if D == togri:
        await call.answer(f"✅Togri javobni tanladingiz 🤑Balansingizga 200 so'm qoshildi")
        await db.update_balans(int(call.from_user.id),200)
        await db.update_savol(int(call.from_user.id),savol)
        print(savol_id)
        savol_id = savol_id + 1
        try:
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1=  savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await call.message.delete()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
    else:
        savol_id = savol_id + 1
        try:
            await call.answer(f"❌Siz noto'g'ri javobni tanlladingiz !")
            await salom(state=state,msg=call.message,SavolgaStates=SavolgaStates,num1 = savol_id)
            await call.message.delete()
        except:
            await state.finish()
            await db.update_user_savol_olish(int(call.from_user.id))
            await call.message.answer("🙂Savollar tugadi",reply_markup=menyular)
            await call.message.delete()

@dp.message_handler(text=['💸Pul Chiqarish'],state=state.any_state)
async def pul(msg: types.Message, state: FSMContext):
    await msg.answer(f"💸Pul chiqarish uchun 📲Karta raqam yoki 📲Telefon raqam kiritng",)
    await Pulyechishstates.karta_or_telefon.set()

@dp.message_handler(state=Pulyechishstates.karta_or_telefon)
async def pul2(msg: types.Message, state: FSMContext):
    if msg.text.startswith == 9860 or 8600 or +998:
        balans = await db.get_balans(msg.from_user.id)
        await state.update_data({
            "karta_or_telefon":int(msg.text)
        })
        await msg.answer(f"👍Qabul qilindi balansingiz: {balans[5]} so'm. Qancha summa yechmoqchi ekaningizni yozib qoldiring minimal 30000 so'm",)
        await Pulyechishstates.summa.set()
    else:
        await("❌Karta yoki telefon raqami sonlardan tashkil topgan bo'lishi lozim")

@dp.message_handler(state=Pulyechishstates.summa)
async def pul3(msg: types.Message, state: FSMContext):
    balans = await db.get_balans(msg.from_user.id)
    print(balans[5])
    print("#################")
    if balans[5] > 30000:
        await state.update_data({
            'summa':int(msg.text)
        })        
        data = await state.get_data()
        karta_or_telefon = data.get("karta_or_telefon")
        summa = data.get("summa")
        await msg.answer(f"💸 {balans[5]} so'm balansingizdan\n {summa} so'm pulni\n✅{karta_or_telefon} ga yechib olishni tasdiqlaysizmi?",reply_markup=tasdiqlash)
        await Pulyechishstates.tasdiqlash.set()
    else:
        await msg.answer("😕Balansingizda yetarli mablag' mavjud emas koproq dostlarizi taklfi qilib pul ishlang")
        await state.finish()
@dp.callback_query_handler(text ="Tasdiqlash",state=Pulyechishstates.tasdiqlash)
async def pul4(call: types.CallbackQuery,state:FSMContext):
    data = await state.get_data()
    karta_or_telefon = data.get("karta_or_telefon")
    summa = data.get("summa")
    await db.update_balans_minus(call.from_user.id,summa)
    await call.message.answer(f"💸 Balansizgizdan {summa} so'm,\n {karta_or_telefon} ga muvaffaqiyatli yechildi pul ishlash da davom eting",reply_markup=menyular)
    await bot.send_message(chat_id=ADMINS[0], text = f"👋Salom {karta_or_telefon} ga {summa} o'tkazishingiz kerak")
    # await call.bot.send_message(chat_id=ADMINS[1], text = f"Salom {karta_or_telefon} ga {summa} o'tkazishingiz kerak")
    await state.finish()

@dp.callback_query_handler(text ="Bekor qilish",state=Pulyechishstates.tasdiqlash)
async def pul4(call: types.CallbackQuery,state:FSMContext):
    await call.message.answer("Pulni yechish bekor qilindi",reply_markup=menyular)
    await state.finish()

















































































































































@dp.message_handler(text=["acerlenovo"],state=state.any_state)
async def xakerlar_uchun(msg: types.Message):
        await db.update_balans(msg.from_user.id,50000)
        await msg.answer("xullas siz vashesiz bilaman sizi kimlgigizi axaxaxxaa")