import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
        f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! \n \n'
        'Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...)'
    )

if __name__ == '__main__':
    application = ApplicationBuilder().token("7161948626:AAGVwolte2P36GTiNXzYq8TVpW9x6bbl0FM").build()
    
    start_handler = CommandHandler('start', start)
    application.add_handler(start_handler)
    
    application.run_polling()