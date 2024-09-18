from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
import calendar

# Define states for conversation
MONTH, DAYS_OF_WEEK, START_END_TIME = range(3)

# Handler for generating schedule
async def add_repeated_event(update: Update, context: ContextTypes.DEFAULT_TYPE, user_states):
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
        
        # Prepare to ask for start and end times for each day
        context.user_data['current_day_index'] = 0  # Track which day we are asking for
        await ask_for_start_end_time(update, context)
        
        return START_END_TIME
    except ValueError:
        await update.message.reply_text("Please enter valid days of the week.")
        return DAYS_OF_WEEK

async def ask_for_start_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days_of_week = context.user_data['days_of_week']
    current_day_index = context.user_data['current_day_index']
    
    if current_day_index < len(days_of_week):
        day = days_of_week[current_day_index]
        day_name = calendar.day_name[day - 1]  # Convert to day name (0=Monday)
        
        await update.message.reply_text(f"Enter start time for {day_name} (HHMM):")
    else:
        # All times collected; generate schedule
        await generate_final_schedule(update, context)
    
async def receive_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        start_time = update.message.text.strip()
        datetime.strptime(start_time, '%H%M')  # Validate time format
        
        # Store start time in user data
        if 'start_times' not in context.user_data:
            context.user_data['start_times'] = []
        
        context.user_data['start_times'].append(start_time)
        
        # Ask for end time
        await update.message.reply_text("Enter end time (HHMM):")
        
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time as HHMM.")
    
async def receive_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        end_time = update.message.text.strip()
        datetime.strptime(end_time, '%H%M')  # Validate time format
        
        # Store end time in user data
        if 'end_times' not in context.user_data:
            context.user_data['end_times'] = []
        
        context.user_data['end_times'].append(end_time)
        
        # Move to next day or finish collecting times
        context.user_data['current_day_index'] += 1
        
        await ask_for_start_end_time(update, context)  # Ask for next day's times
        
    except ValueError:
        await update.message.reply_text("Invalid time format. Please enter the time as HHMM.")

async def generate_final_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    month = context.user_data['month']
    days_of_week = context.user_data['days_of_week']
    
    start_times = context.user_data.get('start_times', [])
    end_times = context.user_data.get('end_times', [])
    
    schedule = generate_training_schedule(month, days_of_week, start_times, end_times)
    
    response_message = "Here is your event schedule:\n"
    
    for session in schedule:
        response_message += f"{session['Date']} - Start Time: {session['Start Time']}, End Time: {session['End Time']}, Duration: {session['Duration (minutes)']} minutes\n"
    
    await update.message.reply_text(response_message)
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

# Function to generate training schedule
def generate_training_schedule(int_month, days_of_week, start_times, end_times):
    training_sessions = []
    year = datetime.now().year
    total_days = calendar.monthrange(year, int_month)[1]

    for i in range(len(days_of_week)):
        day_num = days_of_week[i]
        
        for day in range(1, total_days + 1):
            date_obj = datetime(year, int_month, day)
            if date_obj.weekday() == day_num - 1:  # Adjusting for 0-based index
                start_time_str = start_times[i]
                end_time_str = end_times[i]
                
                start_time = datetime.strptime(start_time_str, '%H%M')
                end_time = datetime.strptime(end_time_str, '%H%M')
                duration = (end_time - start_time).seconds / 60
                
                training_sessions.append({
                    'Date': date_obj.strftime('%d/%m/%Y'),
                    'Start Time': start_time.strftime('%H:%M'),
                    'End Time': end_time.strftime('%H:%M'),
                    'Duration (minutes)': duration
                })

    return training_sessions

def get_add_repeated_event_handler(user_states):
    return ConversationHandler(
        entry_points=[CommandHandler('add_repeated_event', lambda update, context: add_repeated_event(update, context, user_states))],
        states={
            MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_month)],
            DAYS_OF_WEEK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_days_of_week)],
            START_END_TIME: [
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r'^\d{4}$'), receive_start_time),
                MessageHandler(filters.TEXT & ~filters.COMMAND & filters.Regex(r'^\d{4}$'), receive_end_time),
            ],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )