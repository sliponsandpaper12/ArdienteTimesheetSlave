import os
import pandas as pd
from telegram import Update
from telegram.ext import ContextTypes

# Flag to determine if running on a computer
IS_ON_COMPUTER = True  # Change this based on your environment

async def report_gen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    folder_name = 'Ardiente'
    file_name = 'report.xlsx'
    file_path = os.path.join(folder_name, file_name)

    # Check if running on a computer
    if IS_ON_COMPUTER:
        # Create the directory if it doesn't exist
        if not os.path.exists(
        ):
            os.makedirs(folder_name)
        
        # Create a simple DataFrame for the report
        data = {
            'Column1': [1, 2, 3],
            'Column2': ['A', 'B', 'C']
        }
        df = pd.DataFrame(data)

        # Save the DataFrame to an Excel file
        df.to_excel(file_path, index=False)

        # Respond to the user
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Your report is generated.")
    else:
        # If not on a computer, create the DataFrame and send it directly
        data = {
            'Column1': [1, 2, 3],
            'Column2': ['A', 'B', 'C']
        }
        df = pd.DataFrame(data)

        # Save the DataFrame to an Excel file in memory
        excel_file = f"{file_name}"
        df.to_excel(excel_file, index=False)

        # Send the Excel file to the user
        with open(excel_file, 'rb') as file:
            await context.bot.send_document(chat_id=update.effective_chat.id, document=file)

        # Notify the user
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Remember to download this on your computer later.")
