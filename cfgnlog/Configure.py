#!/usr/bin/python

# Exceptions are to be handled by caller. #TODO: YAGNI IOErrorCallback

import os, json
from collections import OrderedDict
from Fun import mkdirs
from Global import die, log
from KeyStrings import DAT, CACHE, LOG

def env( var ):
    val = os.getenv( var );
    if( val == None ): return '';
    return val

# XDG Specification Compliance # <https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>
DEFAULT_MODE = 0o700
ENV_HOME = env( 'HOME' )
CONFIGURATION_DIRECTORY_XDG = 'XDG_CONFIG_HOME'
CONFIGURATION_DIRECTORY_XDG_DEF = os.path.join( ENV_HOME, '.config' )
DATA_DIRECTORY_XDG = 'XDG_DATA_HOME'
DATA_DIRECTORY_XDG_DEF =  os.path.join( ENV_HOME,  '.local', 'share' )
CACHE_DIRECTORY_XDG = 'XDG_CACHE_HOME'
CACHE_DIRECTORY_XDG_DEF = os.path.join( ENV_HOME, '.cache' )

# Windows Compatibility #
CONFIGURATION_DIRECTORY_WIN = 'LOCALAPPDATA'    #Except XP

class ConfigurationDefaults(  ):
#NOTE: Dynamically Included Default Configuration Parameters: { DAT, CACHE, LOG, } TODO: 'REV'?
    def __init__( self, config_filename, config_params, log_filename = None ):
        self.CONFIGURATION_FILENAME = config_filename
        self.CONFIGURATION_PARAMETERS = config_params
        self.LOG_FILENAME = log_filename;


class Configure(  ):
    def __init__( self, name, DEFAULT, config_file = None, IOErrorCallback = die ):
        # Application is responsible for just in time creation of DAT and CACHE directories
        if( config_file == None ):
            config_file = env( CONFIGURATION_DIRECTORY_XDG )
            if( config_file == '' ): config_file = env( CONFIGURATION_DIRECTORY_WIN );
            if( config_file == '' ): config_file = CONFIGURATION_DIRECTORY_XDG_DEF;
            if not os.path.exists( config_file ): mkdirs( config_file, DEFAULT_MODE, 'Creating configuration directory' );
            config_file = os.path.join( config_file, DEFAULT.CONFIGURATION_FILENAME )
        self.dirty = self.load( config_file, DEFAULT.CONFIGURATION_PARAMETERS )
        self.APP_NAME = name
        if( DAT not in self.param ):
            self.param[DAT] = env( DATA_DIRECTORY_XDG )
            if( self.param[DAT] == '' ): self.param[DAT] = env( CONFIGURATION_DIRECTORY_WIN );
            if( self.param[DAT] == '' ): self.param[DAT] = DATA_DIRECTORY_XDG_DEF;
            self.param[DAT] = os.path.join( self.param[DAT], self.APP_NAME )
            self.dirty = True
        if( LOG not in self.param ):
            if DEFAULT.LOG_FILENAME: self.param[LOG] = DEFAULT.LOG_FILENAME;
            else: self.param[LOG] = self.APP_NAME + ".log";
            self.param[LOG] = os.path.join( self.param[DAT], self.param[LOG] )#TODO: Use HOME/.filename by default ?
            self.dirty = True
        if( CACHE not in self.param ):
            self.param[CACHE] = env( CACHE_DIRECTORY_XDG )
            if( self.param[CACHE] == '' ): self.param[CACHE] = env( CONFIGURATION_DIRECTORY_WIN );
            if( self.param[CACHE] == '' ): self.param[CACHE] = os.path.join( CACHE_DIRECTORY_XDG_DEF, self.APP_NAME );
            else: self.param[CACHE] = os.path.join( self.param[CACHE], self.APP_NAME, 'cache' ); #WINDOWS
            self.dirty = True
        for key in DEFAULT.CONFIGURATION_PARAMETERS:
            if( key not in self.param ):
                self.param[key] = DEFAULT.CONFIGURATION_PARAMETERS[key]
                self.dirty = True
        if( self.dirty ): self.update( IOErrorCallback );
    def update( self, IOErrorCallback = die ):
        try:
            fh = open( self.config_file, 'w', DEFAULT_MODE )
            fh.write( json.dumps( self.param, indent=4, separators=(',', ': ') ) ) #TODO: Only write necessary parts
            fh.close(  )
            self.dirty = False
        except IOError as e: IOErrorCallback( e );
    def load( self, config_file, param ): # Returns true if needs (re)write.
        self.config_file = config_file
        try:
            fh = open( config_file )
            self.param = json.loads( fh.read(  ), object_pairs_hook=OrderedDict )
            fh.close(  )
            return False
        except IOError:
            self.param = param
            log.append( 'Creating configuration file: ' + config_file )
            return True
        #TODO: except ValueError: malformed configuration file to be handled by caller.


if __name__ == '__main__':
    default_params = { "Testing" : "123" }
    config = Configure( "YmirConfigureTest", ConfigurationDefaults( "Delete.me", default_params ) )
    print config.param
