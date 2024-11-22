import telegram
from telegram.ext import Updater
token = "7634177875:AAHhnscAJw-WvWobkWoyVVpLakpeXObUv1E"
USER_ID = 2370090966
def check_for_alert(context):
    bot.send_message(chat_id=USER_ID, text="Тест JOB", parse_mode="HTML")

# создание экземпляра бота
bot = telegram.Bot(token=token)
updater = Updater(token=token, use_context=True)
dispatcher = updater.dispatcher
job_queue = updater.job_queue
job_queue.run_repeating(check_for_alert, interval=10.0, first=0.0)
bot.infinity_polling()