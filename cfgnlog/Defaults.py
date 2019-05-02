#!/usr/bin/python

import os

APP_NAME = 'Ymir'

VERSION = [0,0,0] #TODO: Begin incrementing once backwards compabibility is needed.

CONFIGURATION_FILENAME = 'settings.cfg'
CONFIGURATION_DIRECTORY_NAME = os.sep + APP_NAME + os.sep
DATA_DIRECTORY_NAME = os.sep + os.path.join( APP_NAME, 'Contacts' ) + os.sep
CACHE_DIRECTORY_NAME = os.sep + APP_NAME + os.sep
LOG_FILENAME = APP_NAME + '.log' #TODO

DAT = 'DAT'
CACHE = 'CACHE'

CONFIGURATION_PARAMETERS = {
	'V' : VERSION
}
#NOTE: Dynamically Included Default Configuration Parameters: { DATA_DIR, 'REV' } TODO: LOG
