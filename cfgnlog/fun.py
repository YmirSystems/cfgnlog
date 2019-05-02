#!/usr/bin/python

import os
from sys import exit

def die( e ): print( 'ERROR: ' + e.strerror ); exit( e.errno );
def env( var ):
	val = os.getenv( var );
	if( val == None ): return '';
	return val
def mkdirs( path, mode, barf = None ):
	if( barf != None ): print( barf + ': ' + path );
	os.makedirs( path, mode );
#TODO: Add mesage dilivery callback to Configuration, default to print. Use to pass to a logfile.


