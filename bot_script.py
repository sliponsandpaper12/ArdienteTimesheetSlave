from telegram import Update
from telegram.ext import Application, CommandHandler

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     await update.message.reply_text(f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...) ')

async def start(update: Update, context):
    await update.message.reply_text(
        f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! '
        f'Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...)'
    )

# def main() -> None:
#     application = ApplicationBuilder().token("7161948626:AAGVwolte2P36GTiNXzYq8TVpW9x6bb10FM").build()
#     application.add_handler(CommandHandler("hello", hello))
#     application.run_polling()

def main() -> None:
    application = Application.builder().token("YOUR_TOKEN_HERE").build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()