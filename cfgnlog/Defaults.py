#!/usr/bin/python

APP_NAME = 'Ymir'

VERSION = [0,0,0] #TODO: Begin incrementing once backwards compabibility is needed.

CONFIGURATION_FILENAME = 'settings.cfg'
CONFIGURATION_DIRECTORY_NAME = '/' + APP_NAME + '/'
DATA_DIRECTORY_NAME = '/' + APP_NAME + '/Data/'
LOG_FILENAME = APP_NAME + '.log' #TODO

DAT = 'DAT'

CONFIGURATION_PARAMETERS = {
	'V' : VERSION
}
#NOTE: Dynamically Included Default Configuration Parameters: { DATA_DIR, 'REV' } TODO: LOG
