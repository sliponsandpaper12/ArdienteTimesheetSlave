from telegram import Update
from telegram.ext import ApplicationBuilder, Updater, CommandHandler, ContextTypes

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...) ')


def main() -> None:
    application = ApplicationBuilder().token("7161948626:AAGVwolte2P36GTiNXzYq8TVpW9x6bb10FM").build()

    application.add_handler(CommandHandler("hello", hello))

    application.run_polling()