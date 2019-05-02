#!/usr/bin/python

import os
import Global

def mkdirs( path, mode, barf = None ):
    if( barf != None ): Global.log.append( barf + ': ' + path );
    os.makedirs( path, mode );
