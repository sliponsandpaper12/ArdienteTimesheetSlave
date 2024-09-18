from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Dictionary to hold user states
user_states = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user_states[user_id] = True  # Set user state to active
    await context.bot.send_message(chat_id=user_id, text="Welcome! You can now use commands like /add_event.")

async def add_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_states.get(user_id):
        await context.bot.send_message(chat_id=user_id, text="Enter the date of the event (DDMMYYYY):")
        # Proceed with adding event logic...
    else:
        await context.bot.send_message(chat_id=user_id, text="Please use /start to activate the bot.")

async def report_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_states.get(user_id):
        await context.bot.send_message(chat_id=user_id, text="Generating report...")
        # Proceed with report generation logic...
    else:
        await context.bot.send_message(chat_id=user_id, text="Please use /start to activate the bot.")

async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    if user_states.get(user_id):
        await context.bot.send_message(chat_id=user_id, text="Sorry, I didn't understand that command.")
    else:
        await context.bot.send_message(chat_id=user_id, text="Please use /start to activate the bot.")

if __name__ == '__main__':
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    
    # Add handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler("add_event", add_event))
    application.add_handler(CommandHandler("report_gen", report_gen))
    
    # Handle unknown commands
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    # Start polling for updates
    application.run_polling()  # Check for new messages constantly