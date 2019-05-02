#!/usr/bin/python

APP_NAME = 'Ymir'

VERSION = [0,0,0] #TODO: Begin incrementing once backwards compabibility is needed.

CONFIGURATION_FILENAME = 'config.txt' #XXX
DATA_DIRECTORY_NAME = '/' + APP_NAME + '/Data/'
#TODO: LOG_FILENAME = APP_NAME + '.log' #XXX

DATA_DIR = 'DAT'

CONFIGURATION_PARAMETERS = { 'V' : VERSION }
#NOTE: Dynamically Included Default Configuration Parameters: { DATA_DIR, 'REV' }
