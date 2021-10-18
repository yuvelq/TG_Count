
#################################### Config Here ###############################################

# Path and and name of the log file, you can use also the 'lastheard.log' when using HBMon in a different server.
PATH_TO_LOG = "./"
LOG_NAME    = "freedmr.log"

# If the server is running in a Docker set this to True.
SERVER_IN_DOCKER = False

# Change this to False if you have been enabled the download option in the FReeDMR server.
DOWNLOAD_FILES = True

# Files and the time to update in "DAYS".
USER_URL     = "https://www.radioid.net/static/user.csv"
REFRESH_USER = 7

TG_NAME_URL     = "http://downloads.freedmr.uk/downloads/talkgroup_ids.json"
REFRESH_TG_NAME = 7

SUBSCRIBER_URL = "http://downloads.freedmr.uk/downloads/local_subscriber_ids.json"
REFRESH_LOCAL  = 15

# Path and file name of the template that we'll use to write PHP file.
PATH_TO_TEMPLATE = "./templates"
TEMPLATE_NAME    = "tgcount.php"

# Path and file name to where we'll write the PHP and the time in "MINUTES" to update the file. 
PATH_TO_WRITE = "./"
WRITE_FILE    = "count.php"
TIME_TO_WRITE = 3

# The IDs in this list won't be take into account for TG count.
VANISH = (1234567,)

################################## End of Config ################################################
