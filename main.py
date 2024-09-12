from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, MessageHandler, filters
from handlers import *
from utils.logging_config import setup_logging
setup_logging()



if __name__ == '__main__':
    application = ApplicationBuilder().token("7161948626:AAGVwolte2P36GTiNXzYq8TVpW9x6bbl0FM").build()
    
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.COMMAND, unknown))
    application.add_handler(CommandHandler("report_gen",report_gen))
    # application.add_handler(InlineQueryHandler(inline_caps))
    
    application.run_polling() #check for new messages cnostantly 