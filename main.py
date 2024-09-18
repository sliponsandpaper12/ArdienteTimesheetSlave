from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, MessageHandler, filters
from handlers.start import start
from handlers.generate_schedule import get_generate_training_schedule_handler
from handlers.add_event import get_add_event_handler
from handlers.add_repeated_event import get_add_repeated_event_handler
from handlers.unknown import unknown
from utils.logging_config import setup_logging


setup_logging()

user_states ={}

if __name__ == '__main__':
    application = ApplicationBuilder().token("7161948626:AAGVwolte2P36GTiNXzYq8TVpW9x6bbl0FM").build()
    
    application.add_handler(CommandHandler('start', lambda update, context: start(update, context, user_states)))
    # application.add_handler(CommandHandler("report_gen",report_gen))
    application.add_handler(get_add_event_handler(user_states))
    application.add_handler(get_add_repeated_event_handler(user_states))
    application.add_handler(get_generate_training_schedule_handler(user_states))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    
    # you can write the function straight if you wanna run this handler immediately after the start command is called
    # application.add_handler(get_add_event_handler())
    # application.add_handler(InlineQueryHandler(inline_caps))
    
    application.run_polling() #check for new messages constantly 