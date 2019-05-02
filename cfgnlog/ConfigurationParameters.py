#!/usr/bin/python

APP_NAME = 'Ymir'

VERSION = [0,0,0] #TODO: Begin incrementing once backwards compabibility is needed.

DEFAULT_CONFIGURATION_FILENAME = 'config.txt' #XXX
DEFAULT_DATA_DIRECTORY_NAME = '/' + APP_NAME + '/Data/'
#TODO: DEFAULT_LOG_FILENAME = APP_NAME + '.log' #XXX

DATA_DIR = 'DAT'

DEFAULT_CONFIGURATION_PARAMETERS = { 'V' : VERSION }
#NOTE: Dynamically Included Default Configuration Parameters: { DAT_DIR_KEY, 'REV' }
