#!/usr/bin/python

# Exceptions are to be handled by caller.

import os, json
from Fun import env, mkdirs
import Defaults as DEFAULT #TODO: remove reduntancy ie: DEFAULT.DEFAULT
from Defaults import APP_NAME, DATA_DIR #TODO: Transfer into Main module

# XDG Specification Compliance # <https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>
DEFAULT_MODE = 0o700
CONFIGURATION_DIRECTORY_XDG = 'XDG_CONFIG_HOME'
CONFIGURATION_DIRECTORY_XDG_DEF = env( 'HOME' ) + '/.config'
DATA_DIRECTORY_XDG = 'XDG_DATA_HOME'
DATA_DIRECTORY_XDG_DEF =  env( 'HOME' ) + '/.local/share'

# Windows Compatibility #
CONFIGURATION_DIRECTORY_WIN = 'LOCALAPPDATA'	#Except XP

class Configure(  ):
	def __init__( self, config_file = None ):
		#Application is responsible for creation of DATA_DIR
		if( config_file == None ):
			config_file = env( CONFIGURATION_DIRECTORY_XDG )
			if( config_file == '' ): config_file = env( CONFIGURATION_DIRECTORY_WIN );
			if( config_file == '' ): config_file = CONFIGURATION_DIRECTORY_XDG_DEF;
			config_file += '/' + APP_NAME + '/'
			if not os.path.exists( config_file ): mkdirs( config_file, DEFAULT_MODE, 'Creating configuration directory' );
			config_file += DEFAULT.DEFAULT_CONFIGURATION_FILENAME
		self.dirty = self.load( config_file )
		if( DATA_DIR not in self.param ):
			self.param[DATA_DIR] = env( DATA_DIRECTORY_XDG );
			if( self.param[DATA_DIR] == '' ): self.param[DATA_DIR] = env( CONFIGURATION_DIRECTORY_WIN );
			if( self.param[DATA_DIR] == '' ): self.param[DATA_DIR] = DATA_DIRECTORY_XDG_DEF;
			self.param[DATA_DIR] += DEFAULT.DEFAULT_DATA_DIRECTORY_NAME
			self.dirty = True
		for key in DEFAULT.DEFAULT_CONFIGURATION_PARAMETERS:
			if( key not in self.param ):
				self.param[key] = DEFAULT.DEFAULT_CONFIGURATION_PARAMETERS[key]
				self.dirty = True
		if( self.dirty ): self.update( config_file );
		self.f_ref = config_file #XXX
	def update( self, config_file ):
		try:
			fh = open( config_file, 'w', DEFAULT_MODE )
			fh.write( json.dumps( self.param ) ) #TODO: Only write necessary parts
			fh.close(  )
			self.dirty = False
		except IOError as e: die( e ); #TODO: Ask user to select a file. Delegate up.
	def load( self, config_file ): # Returns true if needs (re)write.
		try:
			fh = open( config_file )
			self.param = json.loads( fh.read(  ) )
			fh.close(  )
			#TODO: verify version and update when needed
			return False
		except IOError:
			self.param = DEFAULT.DEFAULT_CONFIGURATION_PARAMETERS
			print( 'Creating configuration file: ' + config_file )
			return True
		#TODO: except ValueError: malformed configuration file


if __name__ == '__main__':
	config = Configure(  )

