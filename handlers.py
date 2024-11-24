import config
import re

from aiogram import  F, Router, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from inline_keyboards import (build_keyboard, accept_traning_callback_data, decline_traning_callback_data, accept_coach_traning_callback_data)

router = Router()
bot = Bot(token=config.BOT_TOKEN)

async def send_message_to_test(msg: Message):
    markup = build_keyboard()
    await msg.answer(f'{config.POST_INIT}', parse_mode='html', reply_markup=markup)
async def get_admins(chat_id):
    chat_admins = (await bot.get_chat_administrators(chat_id)).copy()
    result = []
    for admin in chat_admins:
        result.append(admin.user.id)
    return result


@router.message(Command("start"))
async def start_handler(msg: Message):
    await msg.answer(f"Привет! {msg.from_user.first_name}")


@router.message(Command("job"))
async def job_handler(msg: Message):
    admins = await get_admins(msg.chat.id)
    if (msg.from_user.id in admins):
        scheduler = AsyncIOScheduler()
        # scheduler.add_job(send_message_to_test, 'cron', day_of_week='mon,sat', hour=4, minute=31, args=(msg,))
        scheduler.add_job(send_message_to_test, 'interval', seconds=5, args=(msg,))
        scheduler.start()
    else:
        await msg.answer(f"Нет прав на запуск данной команды. Обратитесь за правами к администратору")


@router.callback_query(F.data == accept_traning_callback_data)
async def handle_accept_traning_(callback_query: CallbackQuery):
    await callback_query.answer(text="Вы записаны на тренировку", show_alert=True)

@router.callback_query(F.data == decline_traning_callback_data)
async def handle_decline_traning_(callback_query: CallbackQuery):
    await callback_query.answer(text="Причину об отсутсвие оставьте в комментарии", show_alert=True)

@router.callback_query(F.data == accept_coach_traning_callback_data)
async def handle_accept_coach_traning(callback_query: CallbackQuery):
    old_message = callback_query.message.text
    prefix_message = old_message.split('Тренера:')[0]
    message_split_coach = old_message.split('Тренера:')[1].split('\n')
    add_accepted_list = f'{callback_query.from_user.first_name} {callback_query.from_user.last_name} (@{callback_query.from_user.username}) \n'
    check_in_list = False
    for i in message_split_coach:
        if (i!=''):
            username = i.split('@')[1].split(')')[0]
            if(username == callback_query.from_user.username):
                check_in_list = True
    if (check_in_list):
        await callback_query.answer(text="Уже голосовали", show_alert=True)
    else:
        message_split_coach.append(add_accepted_list)
        new_message = prefix_message + "Тренера:" + '\n'.join(message_split_coach)
        await bot.edit_message_text(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=new_message, inline_message_id=callback_query.inline_message_id)
  