from handlers import Update, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=
        f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! \n \n'
        'Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...)'
    )