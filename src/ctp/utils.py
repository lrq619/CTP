import logging
import sys

# Step 1: Set up the logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Set the desired logging level here

# Step 2: Create handlers
file_handler = logging.FileHandler('ctp.log')  # You can replace 'logfile.log' with your desired log file name
stdout_handler = logging.StreamHandler(sys.stdout)

# Step 3: Set log levels and formats
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
stdout_handler.setFormatter(formatter)

file_handler.setLevel(logging.DEBUG)  # Set desired logging level for file handler
stdout_handler.setLevel(logging.DEBUG)  # Set desired logging level for stdout handler

# Step 4: Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(stdout_handler)