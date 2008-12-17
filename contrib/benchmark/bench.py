import sys, os, bsddb, random, sqlite3, time
from itertools import *
import sq_dict
import sq_dict2

# number of elements
ELEM_NUM = 10**5

# data size
DATA_SIZE = 100

# the actual data row that will be stored
DATA_ROW = 'X' * DATA_SIZE

# key generators 
KEYS_FWD  = lambda : imap(str, xrange( ELEM_NUM ) )
KEYS_BACK = lambda : imap(str, reversed( xrange( ELEM_NUM )))

class Timer(object):
    """Timer decorator, prints timing information ona  function call"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwds):
        start = time.time()
        try: 
            f = args[0] # first argument is the tested function
            return self.func(*args, **kwds)
        finally:
            end = time.time()
            print 'elapsed=%5.1fs, test=%s, func=%s' % ( end-start, self.func.__name__, f.__name__ ) 

@Timer
def loading( func, fname ):
    "Loads rows into the database"
    db = func( fname, 'c')
    if hasattr(db, 'fast_loading'):
        data = izip( KEYS_FWD(), repeat(DATA_ROW) )
        db.fast_loading( data )
    else:
       for key in KEYS_FWD():
            db[key] = DATA_ROW
    db.sync()
    db.close() 

@Timer
def indexing( func, fname ):
    "Loads rows into the database"
    db = func( fname, 'w')
    if hasattr(db, 'create_index'):
        db.create_index()
        db.sync()
    db.close()

@Timer
def forward_iter( func, fname ):
    "Iterates over the entire database"
    db = func( fname, 'c')
    keys = db.keys()
    for key in db:
        value = db[key]
    db.close() 

@Timer
def reverse_iter( func, fname ):
    "Retrieves each element"
    db = func( fname, 'c')
    keys = db.keys()
    for key in KEYS_BACK():
        value = db[key]
    
    db.close() 

@Timer
def update( func, fname ):
    "Iterates over the database"
    db = func( fname, 'c')
    size1 = len( db.keys() )
    
    for key in KEYS_FWD():
        db[key] = DATA_ROW
    db.sync()

    size2 = len( db.keys() )
    assert size1 == size2 # sanity check
    db.close() 

def get_name( func ):
    "Returns the test database filename"
    return 'test-%s.db' % func.__name__ 

if __name__ == '__main__':
    
    #
    # enable the cdb benchmarks below 
    #
    #import cdb_dict
    #
    #func0 = cdb_dict.cdb_open
    
    func1 = bsddb.btopen
    func2 = bsddb.hashopen
    func3 = sq_dict.sq_dict_open
    func4 = sq_dict2.sq_dict2_open
    
    funcs = [ func1, func2, func3, func4 ]
    tests = [ loading, indexing, forward_iter, reverse_iter, update]
    
    print 
    
    # delete existing databases
    for func in funcs:
        fname = get_name( func )
        if os.path.isfile( fname ):
            os.remove( fname )

    # run each testcase for each function
    for testcase in tests:
        for func in funcs:
            fname = get_name( func )
            testcase( func, fname )
        print '-' * 10
