from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Add Event", callback_data='add_event')],
        [InlineKeyboardButton("Generate Report", callback_data='report_gen')],
        [InlineKeyboardButton("Help", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Please choose a command:', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # Acknowledge the button press

    if query.data == 'add_event':
        await query.edit_message_text(text="You selected to add an event.")
        # Call your add_event function here
    elif query.data == 'report_gen':
        await query.edit_message_text(text="You selected to generate a report.")
        # Call your report_gen function here
    elif query.data == 'help':
        await query.edit_message_text(text="Here are the available commands: /add_event, /report_gen")

if __name__ == '__main__':
    application = ApplicationBuilder().token("YOUR_BOT_TOKEN").build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CallbackQueryHandler(button_handler))  # Handle button presses
    
    application.run_polling()