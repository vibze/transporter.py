import os

PROJECT_ROOT = os.path.dirname(os.path.realpath(__file__))
LOG_ROOT = os.path.join(PROJECT_ROOT, 'logs')
TMP_ROOT = os.path.join(PROJECT_ROOT, 'tmp')

# Login and password for web monitor
# TODO: Change these!
#
MONITOR_LOGIN = 'admin'
MONITOR_PASSWORD = 'password'

DATABASE = os.path.join(PROJECT_ROOT, 'transporter.sqlite3')