import config

from aiogram import types, F, Router, methods, Bot
from aiogram.types import Message
from aiogram.filters import Command
from apscheduler.schedulers.asyncio import AsyncIOScheduler

router = Router()
bot = Bot(token=config.BOT_TOKEN)

async def send_message_to_test(msg: Message):
    await msg.answer_poll(question="Пример тренировки по шедуллеру",is_anonymous=False, options=["буду", "не буду"])

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
        scheduler.add_job(send_message_to_test, 'interval', seconds=3, args=(msg,))
        scheduler.start()
    else:
        await msg.answer(f"Нет прав на запуск данной команды. Обратитесь за правами к администратору")
