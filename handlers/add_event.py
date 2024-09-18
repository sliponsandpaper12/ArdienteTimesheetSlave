from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime

# Define states for conversation
EVENT_DATE, START_TIME, END_TIME, ANOTHER_EVENT = range(4)

# In-memory storage for user data
user_states = {}
user_data = {}

async def add_event(update: Update, context: ContextTypes.DEFAULT_TYPE, user_states):
    user_id = update.effective_chat.id
    if user_states.get(user_id):
        await update.message.reply_text("Enter the date of the event (DDMMYYYY):")
        return EVENT_DATE
    else:
        await update.message.reply_text("Please use /start to activate the bot.")
        return ConversationHandler.END

async def receive_event_date(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Parse and validate date input
    try:
        event_date_str = update.message.text.strip()
        event_date = datetime.strptime(event_date_str, '%d%m%Y')
        user_data[update.effective_chat.id] = {'event_date': event_date}
        
        # Check if month page exists in Google Sheets
        month_year = event_date.strftime('%m%Y')
        sheet_exists = check_sheet_exists(month_year)  # Placeholder for actual sheet check
        
        if sheet_exists:
            await update.message.reply_text(f"Adding event on {event_date.strftime('%d/%m/%Y')} to Google Sheets.")
            await update.message.reply_text("Please enter class start time (HHMM):")
            return START_TIME
        else:
            last_month = get_last_month()  # Placeholder for getting last month of current schedule
            await update.message.reply_text(f"Your schedule is created only till {last_month}. Please use /generate_schedule to continue such schedule and record this event.")
            return ConversationHandler.END
    
    except ValueError:
        await update.message.reply_text("Invalid date format. Please enter the date as DDMMYYYY.")
        return EVENT_DATE  # Go back to asking for the event date

async def receive_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    start_time_str = update.message.text.strip()
    
    # Validate start time format
    try:
        start_time = datetime.strptime(start_time_str, '%H%M')
        user_data[update.effective_chat.id]['start_time'] = start_time
        await update.message.reply_text("Please enter class end time (HHMM):")
        return END_TIME
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time as HHMM.")
        return START_TIME  # Go back to asking for start time

async def receive_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    end_time_str = update.message.text.strip()
    
    # Validate end time format
    try:
        end_time = datetime.strptime(end_time_str, '%H%M')
        
        # Get stored data
        event_date = user_data[update.effective_chat.id]['event_date']
        start_time = user_data[update.effective_chat.id]['start_time']
        
        # Add event to Google Sheets (mock implementation)
        add_event_to_sheet(event_date, start_time.time(), end_time.time())
        
        await update.message.reply_text("Event added successfully! Would you like to add another event? (yes/no)")
        
        return ANOTHER_EVENT  # Move to the next state where we ask about another event
    
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time as HHMM.")
        return END_TIME  # Go back to asking for end time

async def handle_another_event(update: Update, context: ContextTypes.DEFAULT_TYPE):
    response = update.message.text.strip().lower()
    
    if response in ['yes', 'y']:
        await update.message.reply_text("Great! Let's add another event. Enter the date of the event (DDMMYYYY): \n \nYou can /cancel anytime if you change your mind too.")
        return EVENT_DATE  # Loop back to asking for the event date again
    elif response in ['no', 'n']:
        user_id = update.effective_chat.id
        user_states[user_id] = False  # Set user state to inactive
        await update.message.reply_text("Cancelled. You can start again with /start.")
        return ConversationHandler.END  # End the conversation
    else:
        await update.message.reply_text("Please respond with 'yes' or 'no'.")
        return ANOTHER_EVENT  # Stay in the same state and ask again

def check_sheet_exists(month_year):
    # Placeholder function to check if a month page exists in Google Sheets.
    return True  # Mock response

def add_event_to_sheet(event_date, start_time, end_time):
    # Placeholder function to add an event to Google Sheets.
    pass  # Implement your logic here

def get_last_month():
    # Placeholder function to get the last month of current schedule.
    return "MM/YYYY"  # Replace with actual logic

# Create and return the conversation handler
def get_add_event_handler(user_states):
    return ConversationHandler(
        entry_points=[CommandHandler('add_event', lambda update, context: add_event(update, context, user_states))],
        states={
            EVENT_DATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: receive_event_date(update, context))],
            START_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: receive_start_time(update, context))],
            END_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, lambda update, context: receive_end_time(update, context))],
            ANOTHER_EVENT: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_another_event)],
        },
        fallbacks=[CommandHandler('cancel', lambda update, context: cancel(update, context))]
    )

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_chat.id
    user_states[user_id] = False  # Set user state to inactive
    await update.message.reply_text("Cancelled. You can start again with /start.")
    return ConversationHandler.END  # End the conversation