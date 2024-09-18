from telegram import Update
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, user_states):
    user_id = update.effective_chat.id
    user_states[user_id] = True  # Set the user state to active
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! \n\n'
            'Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...)'
        )
    )