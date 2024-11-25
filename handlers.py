import config
import sqlite3

from aiogram import  F, Router, Bot
from aiogram.types import Message, CallbackQuery, InputFile, FSInputFile
from aiogram.filters import Command, CommandStart
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from inline_keyboards import (build_keyboard, accept_traning_callback_data, decline_traning_callback_data, accept_coach_traning_callback_data,sign_up_callback_data)

router = Router()
bot = Bot(token=config.BOT_TOKEN)

async def send_message_of_tranning(msg: Message):
    markup = build_keyboard()
    photo_post = FSInputFile(path='./photo/LilField.png')
    msg_to_pin = await msg.answer_photo(photo=photo_post, caption=f'{config.POST_INIT}', parse_mode='html', reply_markup=markup)
    # msg_to_pin = await msg.answer(f'{config.POST_INIT}', parse_mode='html', reply_markup=markup)
    await bot.pin_chat_message(chat_id = msg_to_pin.chat.id, message_id= msg_to_pin.message_id)

async def get_admins(chat_id):
    chat_admins = (await bot.get_chat_administrators(chat_id)).copy()
    result = []
    for admin in chat_admins:
        result.append(admin.user.id)
    return result

async def add_coach_to_ul(callback):
    old_message = callback.message.caption
    prefix_message = old_message.split('Тренера:')[0]
    message_split_coach = old_message.split('Тренера:')[1].split('\n')
    message_split_coach = [i for i in message_split_coach if i]
    add_accepted_list = f'{callback.from_user.first_name} {callback.from_user.last_name} (@{callback.from_user.username}) \n'
    check_in_list = False
    if (old_message.find(callback.from_user.username) != -1):
        check_in_list = True
    if (check_in_list):
        return ''
    else:
        message_split_coach.append(add_accepted_list)
        message_split_coach_str = (','.join(message_split_coach)).replace(',', '\n')
        return (prefix_message + "Тренера:\n\n" + message_split_coach_str)
    
async def add_player_accept_to_ul(callback):
    old_message = callback.message.caption
    prefix_message = old_message.split('Будут на тренировке: \n')[0]
    ul_accepted_player = old_message.split('Будут на тренировке: \n')[1].split('❌ Будут отсутствовать на тренировке:')[0].split('\n')
    ul_accepted_player = [i for i in ul_accepted_player if i]
    postfix_message = old_message.split('Будут на тренировке: \n')[1].split('❌ Будут отсутствовать на тренировке:')[1]
    add_accepted_list = f'{callback.from_user.first_name} {callback.from_user.last_name} (@{callback.from_user.username}) \n'
    check_in_list = False
    if (old_message.find(callback.from_user.username) != -1):
        check_in_list = True
    if (check_in_list):
        return ''
    else:
        ul_accepted_player.append(add_accepted_list)
        ul_accepted_player_str = (','.join(ul_accepted_player)).replace(',', '\n')
        return (prefix_message + "Будут на тренировке: \n" + ul_accepted_player_str + "\n❌ Будут отсутствовать на тренировке:" + postfix_message)
    
async def add_player_dicline_to_ul(callback):
    old_message = callback.message.caption
    prefix_message = old_message.split('Будут отсутствовать на тренировке: \n')[0]
    ul_diclined_player = old_message.split('Будут отсутствовать на тренировке: \n')[1].split('👤 Тренера:')[0].split('\n')
    ul_diclined_player = [i for i in ul_diclined_player if i]
    postfix_message = old_message.split('Будут отсутствовать на тренировке: \n')[1].split('👤 Тренера:')[1]
    add_accepted_list = f'{callback.from_user.first_name} {callback.from_user.last_name} (@{callback.from_user.username}) \n'
    check_in_list = False
    if (old_message.find(callback.from_user.username) != -1):
        check_in_list = True
    if (check_in_list):
        return ''
    else:
        ul_diclined_player.append(add_accepted_list)
        ul_diclined_player_str = (','.join(ul_diclined_player)).replace(',', '\n')
        return (prefix_message + "Будут отсутствовать на тренировке: \n" + ul_diclined_player_str + "\n👤 Тренера:" + postfix_message)
    
def create_tbl_users(connector):
    cursor = connector.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, \
                 login varchar(50),\
                 tg_id int,\
                 team varchar(50),\
                 position varchar(50),\
                 coach boolean\
                );')
    connector.commit()
    cursor.close()
    return True

def create_tbl_post_statics(connector):
    cursor = connector.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS post_statistic (id int auto_increment primary key, \
                 chat_id int,\
                 user_id int,\
                 option_selected int,\
                 date_traning datetime\
                );')
    connector.commit()
    cursor.close()
    return True

def check_registred(message: Message):
    tg_id = message.from_user.id
    connector = sqlite3.connect('bruinsTeam.sql')
    cursor = connector.cursor()
    result_select = cursor.execute("SELECT * FROM users where tg_id ='%d'" %(tg_id))
    cursor.close()
    if (result_select.row_factory == None):
        return False
    else:
        return True
    
    
@router.message(Command("createBD"))
async def create_bd_hendler(msg: Message):
    connector = sqlite3.connect('bruinsTeam.sql')
    create_tbl_users(connector)
    create_tbl_post_statics(connector)
    connector.close()
    await msg.answer(f"База данных создана")

@router.message(CommandStart("start"))
async def start_handler(msg: Message):
    print("++++++++++++++")
    print(msg)
    print("++++++++++++++")
    await msg.answer(f"Привет! {msg.from_user.first_name}")


@router.message(Command("job"))
async def job_handler(msg: Message):
    admins = await get_admins(msg.chat.id)
    if (msg.from_user.id in admins):
        scheduler = AsyncIOScheduler()
        # scheduler.add_job(send_message_of_tranning, 'cron', day_of_week='mon,sat', hour=4, minute=31, args=(msg,))
        scheduler.add_job(send_message_of_tranning, 'interval', seconds=4, args=(msg,))
        scheduler.start()
    else:
        await msg.answer(f"Нет прав на запуск данной команды. Обратитесь за правами к администратору")

@router.message(Command("sign_up"))
async def sing_up_handler(msg: Message):
    await msg.answer(f"Заполни информацию")

@router.callback_query(F.data == sign_up_callback_data)
async def sign_up(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me()
    if (check_registred(callback_query)):
        check_already_answer = await add_player_accept_to_ul(callback_query)
        if (check_already_answer == ''):
            await callback_query.answer(text="Уже голосовали", show_alert=True)
        else:
            await callback_query.answer(text="Красавчик! Каждая тренировка делает тебя сильнее💪", show_alert=True)
            await bot.edit_message_caption(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, caption=check_already_answer, inline_message_id=callback_query.inline_message_id)
            # await bot.edit_message_text(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=check_already_answer, inline_message_id=callback_query.inline_message_id)
    else:
        await callback_query.answer(url=f't.me/{bot_me.username}?start')

@router.callback_query(F.data == accept_traning_callback_data)
async def handle_accept_traning(callback_query: CallbackQuery):
    bot_me = await callback_query.bot.me()
    if (check_registred(callback_query)):
        check_already_answer = await add_player_accept_to_ul(callback_query)
        if (check_already_answer == ''):
            await callback_query.answer(text="Уже голосовали", show_alert=True)
        else:
            await callback_query.answer(text="Красавчик! Каждая тренировка делает тебя сильнее💪", show_alert=True)
            await bot.edit_message_caption(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, caption=check_already_answer, inline_message_id=callback_query.inline_message_id)
            # await bot.edit_message_text(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=check_already_answer, inline_message_id=callback_query.inline_message_id)
    else:
        await callback_query.answer(url=f't.me/{bot_me.username}?sign_up=0')

@router.callback_query(F.data == decline_traning_callback_data)
async def handle_decline_traning(callback_query: CallbackQuery):
    check_already_answer = await add_player_dicline_to_ul(callback_query)
    if (check_already_answer == ''):
        await callback_query.answer(text="Уже голосовали", show_alert=True)
    else: 
        await callback_query.answer(text="Причину об отсутсвие напиши ответом на сообщние ⬇️", show_alert=True)
        await bot.send_message(callback_query.message.chat.id, f'@{callback_query.from_user.username} напиши причину отсутсвия на тренировке!', parse_mode='html')
        await bot.edit_message_caption(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, caption=check_already_answer, inline_message_id=callback_query.inline_message_id)
        # await bot.edit_message_text(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=check_already_answer, inline_message_id=callback_query.inline_message_id)


@router.callback_query(F.data == accept_coach_traning_callback_data)
async def handle_accept_coach_traning(callback_query: CallbackQuery):
    check_already_answer = await add_coach_to_ul(callback_query)
    if (check_already_answer == ''):
        await callback_query.answer(text="Уже голосовали", show_alert=True)
    else:
        await callback_query.answer(text="Моё почтение 🦸‍♂️", show_alert=True)
        await bot.edit_message_caption(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, caption=check_already_answer, inline_message_id=callback_query.inline_message_id)
        # await bot.edit_message_text(reply_markup= callback_query.message.reply_markup, chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id, text=check_already_answer, inline_message_id=callback_query.inline_message_id)
  