from aiogram.dispatcher.filters.state import StatesGroup,State

class FirstStates(StatesGroup):
    kanalga_state = State()
    kontaktga_state = State()
    ismga_state = State()
    
class SavolgaStates(StatesGroup):
    togri_state = State()
class Pulyechishstates(StatesGroup):
    karta_or_telefon = State()
    summa = State()
    tasdiqlash = State()