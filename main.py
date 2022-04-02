import openpyxl
import xlrd

from scripts import check_setup_data, import_excel_data, write_to_file
from datetime import datetime, timedelta
from models import metadata
from database_conn import engine
from config import DEBUG, PROCESSED_FOLDER, UNPROCESSED_FOLDER, WAIT_TIME
import time


# initialise local variables
today = datetime.today().date()
debug = DEBUG
unprocessed_filepath = UNPROCESSED_FOLDER
processed_filepath = PROCESSED_FOLDER

start_time = datetime.now()
if debug >= 0:
    write_to_file('Starting program...')
    print(f'*** Starting program at {start_time.strftime("%d-%b-%Y %I:%M:%S.%f %p")} ***')

# db = SessionLocal()
metadata.create_all(engine)

# initialize setup data
check_setup_data(debug)

while True:
    # import excel data
    import_excel_data(debug)








finish_time = datetime.now()

if debug >= 0:
    print(f'*** Finished program at {finish_time.strftime("%d-%b-%Y %I:%M:%S.%f %p")} ***')
    print(f'*** Time to complete - {finish_time - start_time} ***')
