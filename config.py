# This is the SQL Server Name
DATABASE_SERVER = 'BAYO-DELL'

# This is the database that will be created
DATABASE_NAME = 'pcard_db'

# The following identifies needed parameters. This can be changed to the desired folder path
UPLOAD_FOLDER = 'Uploads'
PROCESSED_FOLDER = 'Uploads/Processed'
UNPROCESSED_FOLDER = 'Uploads/Unprocessed'
LOG_FILE = 'event_log.txt'

# The debug value below will write important event based on the following settings:
# 0: Minimum information,  1: More information, 2: Maximum information
DEBUG = 2

# This is a time-out parameter when checking how often the code checks the UNPROCESSED_FOLDER for files to process.
WAIT_TIME = 60  # secs
