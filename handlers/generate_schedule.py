from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
import calendar

# Define states for conversation
MONTH, DAYS_OF_WEEK, START_TIME, END_TIME = range(4)

# Handler for generating schedule
async def generate_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE, user_states):
    user_id = update.effective_chat.id
    if user_states.get(user_id):
        await update.message.reply_text("Enter month (1-12):")
        return MONTH
    else:
        await update.message.reply_text("Please use /start to activate the bot.")
        return ConversationHandler.END

async def receive_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        context.user_data['month'] = int(update.message.text)
        await update.message.reply_text("Enter days of week (1=Monday to 7=Sunday) separated by commas:")
        return DAYS_OF_WEEK
    except ValueError:
        await update.message.reply_text("Please enter a valid month (1-12).")
        return MONTH

async def receive_days_of_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        days_input = update.message.text.split(',')
        context.user_data['days_of_week'] = list(map(int, days_input))
        await update.message.reply_text("Enter class start time (HHMM):")
        return START_TIME
    except ValueError:
        await update.message.reply_text("Please enter valid days of the week.")
        return DAYS_OF_WEEK

async def receive_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['start_time'] = update.message.text
    await update.message.reply_text("Enter class end time (HHMM):")
    return END_TIME

async def receive_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['end_time'] = update.message.text
    
    # Ensure start_time and end_time are properly parsed
    try:
        start_time = datetime.strptime(context.user_data['start_time'], '%H%M')
        end_time = datetime.strptime(context.user_data['end_time'], '%H%M')
        
        # Calculate duration
        duration = (end_time - start_time).seconds / 60  # Duration in minutes
        
        # Generate schedule using collected data
        schedule = generate_training_schedule(
            context.user_data['month'],
            context.user_data['days_of_week'],
            context.user_data['start_time'],
            context.user_data['end_time']
        )
        
        # Send schedule back to user
        response_message = "Here is your training schedule:\n"
        
        for session in schedule:
            response_message += f"{session['Date']} - Start Time: {session['Start Time']}, End Time: {session['End Time']}, Duration: {session['Duration (minutes)']} minutes\n"
        
        await update.message.reply_text(response_message)
    
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time as HHMM.")
        return END_TIME  # Go back to asking for end time

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# Function to generate training schedule
def generate_training_schedule(int_month, days_of_week, class_start_time, class_end_time):
    training_sessions = []
    year = datetime.now().year
    total_days = calendar.monthrange(year, int_month)[1]

    for day in range(1, total_days + 1):
        date_obj = datetime(year, int_month, day)
        if date_obj.weekday() in [day - 1 for day in days_of_week]:  # Adjusting for 0-based index
            start_time = datetime.strptime(class_start_time, '%H%M')
            end_time = datetime.strptime(class_end_time, '%H%M')
            duration = (end_time - start_time).seconds / 60

            training_sessions.append({
                'Date': date_obj.strftime('%d/%m/%Y'),
                'Start Time': start_time.strftime('%H:%M'),
                'End Time': end_time.strftime('%H:%M'),
                'Duration (minutes)': duration
            })

    return training_sessions

def get_generate_training_schedule_handler(user_states):
    return ConversationHandler(
        entry_points=[CommandHandler('generate_schedule', lambda update, context: generate_schedule(update, context, user_states))],
        states={
            MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_month)],
            DAYS_OF_WEEK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_days_of_week)],
            START_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_start_time)],
            END_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_end_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )