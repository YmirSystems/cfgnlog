#!/usr/bin/python

from Log import Log
from sys import exit

cfg = None
log = Log( )


def die( e ): log.append( 'ERROR: ' + e.strerror ); exit( e.errno );
