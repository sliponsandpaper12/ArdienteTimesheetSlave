# import logging
# from telegram import Update, InlineQueryResultArticle, InputTextMessageContent
# from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, InlineQueryHandler, MessageHandler, filters

# # from uuid import uuid4


# logging.basicConfig(
#     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#     level=logging.INFO
# )

# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=
#         f'Hello {update.effective_user.first_name}! Welcome to Ardiente Exco! \n \n'
#         'Thanks for serving the club :D You\'ve earned yourself a slave working under you (me...)'
#     )

# #error handling
# async def unknown(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text="Sorry, I didn't understand that command.")

# # async def inline_caps(update: Update, context: ContextTypes.DEFAULT_TYPE):
# #     query = update.inline_query.query #retrieve text of inline query
# #     if not query:
# #         return
# #     results = []
# #     results.append(
# #         InlineQueryResultArticle(
# #             id=str(uuid4()),
# #             title='Caps',
# #             input_message_content=InputTextMessageContent(query.upper()), #the message to return. can be formula liek get hours, then we retrieve from excel
# #         )
# #     )
# #     await context.bot.answer_inline_query(update.inline_query.id, results) #  This sends the results back to the Telegram client, displaying them as options for the user to select.

# if __name__ == '__main__':
#     application = ApplicationBuilder().token("7161948626:AAGVwolte2P36GTiNXzYq8TVpW9x6bbl0FM").build()
    
#     start_handler = CommandHandler('start', start)
#     unknown_handler = MessageHandler(filters.COMMAND, unknown)
#     # inline_caps_handler = InlineQueryHandler(inline_caps)

    
#     application.add_handler(start_handler)
#     application.add_handler(unknown_handler) # this one must be the last so the code can run through all handlers before returning error message
#     # application.add_handler(inline_caps_handler)
    
#     application.run_polling()