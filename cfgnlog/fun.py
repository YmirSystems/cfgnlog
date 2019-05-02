#!/usr/bin/python

import os
import Global
from sys import exit

def die( e ): Global.log.append( 'ERROR: ' + e.strerror ); exit( e.errno );
def env( var ):
	val = os.getenv( var );
	if( val == None ): return '';
	return val
def mkdirs( path, mode, barf = None ):
	if( barf != None ): Global.log.append( barf + ': ' + path );
	os.makedirs( path, mode );


