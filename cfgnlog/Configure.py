#!/usr/bin/python

# Exceptions are to be handled by caller:
#   IOError     - Unable to update file
#   ValueError  - Malformed configuration file

import os, json
from collections import OrderedDict
from Fun import mkdirs
from Global import log
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

DEFAULT_CONFIGURATION_FILENAME_EXT = '.cfg'

class Configure(  ):
    def __init__( self, name, DEFAULT_CONFIGURATION_FILENAME = None, config_file = None ):
        if( config_file == None ):
            config_file = env( CONFIGURATION_DIRECTORY_XDG )
            if( config_file == '' ): config_file = env( CONFIGURATION_DIRECTORY_WIN );
            if( config_file == '' ): config_file = CONFIGURATION_DIRECTORY_XDG_DEF;
            if not os.path.exists( config_file ): mkdirs( config_file, DEFAULT_MODE, 'Creating configuration directory' );
            if DEFAULT_CONFIGURATION_FILENAME: self.config_file = os.path.join( config_file, DEFAULT_CONFIGURATION_FILENAME );
            else: self.config_file = os.path.join( config_file, name + DEFAULT_CONFIGURATION_FILENAME_EXT );
        else: self.config_file = config_file;
        self.dirty = False
        self.APP_NAME = name
    def add_dat( self ):
        ''' Add a data directory parameter to the loaded configuration. The application is responsible for creating it. '''
        if( DAT not in self.param ):
            self.param[DAT] = env( DATA_DIRECTORY_XDG )
            if( self.param[DAT] == '' ): self.param[DAT] = env( CONFIGURATION_DIRECTORY_WIN );
            if( self.param[DAT] == '' ): self.param[DAT] = DATA_DIRECTORY_XDG_DEF;
            self.param[DAT] = os.path.join( self.param[DAT], self.APP_NAME )
            self.dirty = True
    def add_log( self, DEFAULT_LOG_FILENAME = None, default_use_home = False ):
        ''' Add a log directory parameter to the loaded configuration. The application is responsible for creating it. '''
        if( LOG not in self.param ):
            if DEFAULT_LOG_FILENAME: self.param[LOG] = DEFAULT_LOG_FILENAME;
            else: self.param[LOG] = self.APP_NAME + ".log";
            if default_use_home:
                self.param[LOG] = os.path.join( ENV_HOME, '.'+self.param[LOG] );
            else: self.param[LOG] = os.path.join( self.param[DAT], self.param[LOG] );
            self.dirty = True
    def add_cache( self ):
        ''' Add a cache directory parameter to the loaded configuration. The application is responsible for creating it. '''
        if( CACHE not in self.param ):
            self.param[CACHE] = env( CACHE_DIRECTORY_XDG )
            if( self.param[CACHE] == '' ): self.param[CACHE] = env( CONFIGURATION_DIRECTORY_WIN );
            if( self.param[CACHE] == '' ): self.param[CACHE] = os.path.join( CACHE_DIRECTORY_XDG_DEF, self.APP_NAME );
            else: self.param[CACHE] = os.path.join( self.param[CACHE], self.APP_NAME, 'cache' ); #WINDOWS
            self.dirty = True
    def update( self ):
        fh = open( self.config_file, 'w', DEFAULT_MODE )
        fh.write( json.dumps( self.param, indent=4, separators=(',', ': ') ) ) #TODO: Only write necessary parts
        fh.close(  )
        self.dirty = False
    def load( self, DEFAULT_CONFIGURATION_PARAMETERS ): # Returns true if needs (re)write.
        try:
            fh = open( self.config_file )
            self.param = json.loads( fh.read(  ), object_pairs_hook=OrderedDict )
            fh.close(  )
            for key in DEFAULT_CONFIGURATION_PARAMETERS:
                if( key not in self.param ):
                    self.param[key] = DEFAULT_CONFIGURATION_PARAMETERS[key]
                    self.dirty = True
        except IOError:
            self.param = DEFAULT_CONFIGURATION_PARAMETERS
            self.dirty = True #TODO: YAGNI?
            log.append( 'Creating configuration file: ' + self.config_file )
        except ValueError as MalformedFileError:
            MalformedFileError.strerror = "Malformed configuration file"
            MalformedFileError.filename = self.config_file
            MalformedFileError.errno = 1
            raise MalformedFileError
        if( self.dirty ): self.update(  );


if __name__ == '__main__':
    default_params = { "Testing" : "123" }
    config = Configure( "ConfigureTest", "delete.me" )
    config.load( default_params )
    config.add_dat(  )
    config.add_cache(  )
    config.add_log( default_use_home = True )
    print config.param
