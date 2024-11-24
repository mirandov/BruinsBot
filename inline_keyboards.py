from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

accept_traning_callback_data = "accept_traning_callback_data"
decline_traning_callback_data = "decline_traning_callback_data"
accept_coach_traning_callback_data = "accept_coach_traning_callback_data"
def build_keyboard() -> InlineKeyboardMarkup:
    accept_traning_btn1 = InlineKeyboardButton(text= "✅ Буду на тренировке", callback_data=accept_traning_callback_data)
    decline_traning_btn1 = InlineKeyboardButton(text= "❌ Не будет на тренировке", callback_data=decline_traning_callback_data)
    accept_coach_traning_btn1 = InlineKeyboardButton(text= "🏈 Тренер", callback_data=accept_coach_traning_callback_data)
    row_first = [accept_traning_btn1, decline_traning_btn1]
    row_second = [accept_coach_traning_btn1]
    rows = [row_first,row_second]
    markup = InlineKeyboardMarkup(inline_keyboard=rows)
    return markup