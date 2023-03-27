from loader import db
import random
from keyboards.inline.kanalga import *
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher import filters
from aiogram.dispatcher.filters import StateFilter
from aiogram.dispatcher.filters import state
from states.telefon_ism_state import *
from states.admin import *

async def salom (state , SavolgaStates,msg,num1):
    print(num1)
    savol = await db.select_all_savollar(num1)
    
    print(savol)
    print("#############################")
    jav=[savol[2],savol[3],savol[4],savol[5]]
    random.shuffle(jav)
    await state.update_data({
    "savol":savol[1],
    "togri":savol[5],
    "variant1":jav[0],
    "variant2":jav[1],
    "variant3":jav[2],
    "variant4":jav[3],
    "savol_idsi":num1
    })
    await SavolgaStates.togri_state.set()
    await msg.answer(f"{savol[1]}\n Variantlar: \nA) {jav[0]} \nB) {jav[1]} \nC) {jav[2]} \nD) {jav[3]}",reply_markup=variantlar)
