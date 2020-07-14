import os

BASE_DIR = os.path.dirname(os.path.dirname(__name__))

DEBUG = True
FIREFOX_PROFILES_PATH = r'C:\Users\%s\AppData\Roaming\Mozilla\Firefox\Profiles' % os.getlogin()
ACCOUNTS_FILE = 'accounts.csv'
DEFAULT_PORT = '3738'
EXECUTABLE_PATH = 'bin/geckodriver.exe'
LOGS_DIR = os.path.join(BASE_DIR, 'logs')

APP_NAME = 'YahooBot'
APP_VERSION = '0.1.0'
POWRED_BY = 'Omega Capital'
DEVELOPED_BY = 'Mohammed Ramouchy'
CONTACT_ME = 'https://github.com/medram'
