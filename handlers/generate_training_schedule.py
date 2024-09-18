from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, ConversationHandler
from datetime import datetime
import calendar

# Define states for conversation
MONTH, REPEATED_TRAINING, DAYS_OF_WEEK, START_TIME, END_TIME = range(5)

def generate_training_schedule(int_month, bool_repeatedtraining, days_of_week, class_start_time, class_end_time):
    # Prepare output list
    training_sessions = []

    # Get current year
    year = datetime.now().year

    # Create a mapping for days of week
    day_map = {1: 0, 2: 1, 3: 2, 4: 3, 5: 4, 6: 5, 7: 6}  # Monday=0 to Sunday=6

    # Get total number of days in the month
    total_days = calendar.monthrange(year, int_month)[1]

    # Iterate through each day of the month
    for day in range(1, total_days + 1):
        date_obj = datetime(year, int_month, day)
        if date_obj.weekday() in [day_map[day] for day in days_of_week]:
            # Calculate duration
            start_time = datetime.strptime(class_start_time, '%H%M')
            end_time = datetime.strptime(class_end_time, '%H%M')
            duration = (end_time - start_time).seconds / 60  # Duration in minutes

            # Append session details to output list
            training_sessions.append({
                'Date': date_obj.strftime('%d/%m/%Y'),
                'Start Time': start_time.strftime('%H:%M'),
                'End Time': end_time.strftime('%H:%M'),
                'Duration (minutes)': duration
            })

    return training_sessions

# Handler for generating schedule
async def generate_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Enter month (1-12):")
    return MONTH

async def receive_month(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['month'] = int(update.message.text)
    await update.message.reply_text("Is training repeated? (yes/no):")
    return REPEATED_TRAINING

async def receive_repeated_training(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['repeated_training'] = update.message.text.lower() == 'yes'
    await update.message.reply_text("Enter days of week (1=Monday to 7=Sunday) separated by commas:")
    return DAYS_OF_WEEK

async def receive_days_of_week(update: Update, context: ContextTypes.DEFAULT_TYPE):
    days_input = update.message.text.split(',')
    context.user_data['days_of_week'] = list(map(int, days_input))
    
    await update.message.reply_text("Enter class start time (HHMM):")
    return START_TIME

async def receive_start_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['start_time'] = update.message.text
    await update.message.reply_text("Enter class end time (HHMM):")
    return END_TIME

async def receive_end_time(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data['end_time'] = update.message.text
    
    # Generate schedule using collected data
    schedule = generate_training_schedule(
        context.user_data['month'],
        context.user_data['repeated_training'],
        context.user_data['days_of_week'],
        context.user_data['start_time'],
        context.user_data['end_time']
    )
    
    # Send schedule back to user
    response_message = "Here is your training schedule:\n"
    
    for session in schedule:
        response_message += f"{session['Date']} - Start Time: {session['Start Time']}, End Time: {session['End Time']}, Duration: {session['Duration (minutes)']} minutes\n"
    
    await update.message.reply_text(response_message)
    
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Cancelled.")
    return ConversationHandler.END

def generate_training_schedule():
    return ConversationHandler(
        entry_points=[CommandHandler('generate_schedule', generate_schedule)],
        states={
            MONTH: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_month)],
            REPEATED_TRAINING: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_repeated_training)],
            DAYS_OF_WEEK: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_days_of_week)],
            START_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_start_time)],
            END_TIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, receive_end_time)],
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
