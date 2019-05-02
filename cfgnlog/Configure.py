#!/usr/bin/python

# Exceptions are to be handled by caller.

import os, json
from Fun import env, mkdirs, die
import Defaults as DEFAULT
from Defaults import DAT, CACHE

# XDG Specification Compliance # <https://standards.freedesktop.org/basedir-spec/basedir-spec-latest.html>
DEFAULT_MODE = 0o700
CONFIGURATION_DIRECTORY_XDG = 'XDG_CONFIG_HOME'
CONFIGURATION_DIRECTORY_XDG_DEF = env( 'HOME' ) + '/.config' #TODO: use os.path.join
DATA_DIRECTORY_XDG = 'XDG_DATA_HOME'
DATA_DIRECTORY_XDG_DEF =  env( 'HOME' ) + '/.local/share' #TODO: use os.path.join
CACHE_DIRECTORY_XDG = 'XDG_CACHE_HOME'
CACHE_DIRECTORY_XDG_DEF = env( 'HOME' ) + '/.cache'

# Windows Compatibility #
CONFIGURATION_DIRECTORY_WIN = 'LOCALAPPDATA'	#Except XP

class Configure(  ):
	def __init__( self, config_file = None ):
		#Application is responsible for creation of DAT and CACHE directory
		if( config_file == None ):
			config_file = env( CONFIGURATION_DIRECTORY_XDG )
			if( config_file == '' ): config_file = env( CONFIGURATION_DIRECTORY_WIN );
			if( config_file == '' ): config_file = CONFIGURATION_DIRECTORY_XDG_DEF;
			config_file += DEFAULT.CONFIGURATION_DIRECTORY_NAME
			if not os.path.exists( config_file ): mkdirs( config_file, DEFAULT_MODE, 'Creating configuration directory' );
			config_file += DEFAULT.CONFIGURATION_FILENAME
		self.dirty = self.load( config_file )
		if( DAT not in self.param ):
			self.param[DAT] = env( DATA_DIRECTORY_XDG )
			if( self.param[DAT] == '' ): self.param[DAT] = env( CONFIGURATION_DIRECTORY_WIN );
			if( self.param[DAT] == '' ): self.param[DAT] = DATA_DIRECTORY_XDG_DEF;
			self.param[DAT] += DEFAULT.DATA_DIRECTORY_NAME
			self.dirty = True
		if( CACHE not in self.param ):
			self.param[CACHE] = env( CACHE_DIRECTORY_XDG )
			if( self.param[CACHE] == '' ): self.param[CACHE] = env( CONFIGURATION_DIRECTORY_WIN )
			if( self.param[CACHE] == '' ): self.param[CACHE] = CACHE_DIRECTORY_XDG_DEF + DEFAULT.CACHE_DIRECTORY_NAME;
			else: self.param[CACHE] += DEFAULT.CACHE_DIRECTORY_NAME + 'cache' + os.sep#TODO: use os.path.join
			self.dirty = True
		for key in DEFAULT.CONFIGURATION_PARAMETERS:
			if( key not in self.param ):
				self.param[key] = DEFAULT.CONFIGURATION_PARAMETERS[key]
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
			self.param = DEFAULT.CONFIGURATION_PARAMETERS
			print( 'Creating configuration file: ' + config_file )
			return True
		#TODO: except ValueError: malformed configuration file


if __name__ == '__main__':
	config = Configure(  )
	print config.param
