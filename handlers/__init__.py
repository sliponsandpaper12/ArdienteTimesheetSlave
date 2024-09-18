# __init__.py

# Importing submodules for easier access
from telegram import Update
from telegram.ext import ContextTypes
# from .start import start
# from .unknown import unknown
# from .report_gen import report_gen
# from .add_event import get_add_event_handler
# from .generate_training_schedule import get_generate_training_schedule

# from .inline_caps import inline_caps  # Uncomment if needed

# Defining package-level variables
__version__ = "1.0.0"

# Optional: Initialization code
print("Armed and Ready!")


# You can also define __all__ to specify what is imported with 'from your_bot import *'
__all__ = ['Update', 'ContextTypes', 'start', 'unknown', 'report_gen', 'get_add_event_handler', 'get_generate_training_schedule']  # Add other handlers as needed