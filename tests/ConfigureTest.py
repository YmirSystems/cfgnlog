#!/usr/bin/python

from cfgnlog import Configure

if __name__ == '__main__':
    default_params = { "Testing" : "123" }
    config = Configure( "ConfigureTest", "delete.me" )
    config.load( default_params )
    config.add_dat(  )
    config.add_cache(  )
    config.add_log( default_use_home = True )
    print config.options
