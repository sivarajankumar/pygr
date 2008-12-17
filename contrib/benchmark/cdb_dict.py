"""
Coercing cdb into a shelve like interface

for python2.5 need to make this change this when compiling cdb:

http://www.notes.xythian.net/2007/10/24/python-cdb-032-52ubuntu2-with-python-25-causes-double-free-corruption-crash-on-dealloc/

"""
import cdb

def cdb_open( filename, mode='c'):
    db = CdbShelve(filename, mode=mode)
    return db

class CdbShelve( object ):

    def __init__ (self, filename, mode='c'):
        # will switch modes of operation depending on the type of access
        self.db = None
        self.fn= filename

    def create_index(self):
        pass

    def sync(self):
        try:
            self.db.finish()
        except:
            pass

    def close(self):
        pass

    def __setitem__(self, key, value):            
        
        try:
            self.db.add( key, value)  
        except:
            # cdb has two modes and if we're in the wrong mode, switch
            self.db = cdb.cdbmake(self.fn, self.fn + ".tmp")
            self.db.add( key, value )  
        
    def __getitem__(self, key):            
        
        try:
            return self.db.get( key ) 
        except:
            self.db = cdb.init( self.fn )
            return self.db.get( key ) 
   
    def __iter__(self):
        try:
            return iter( self.db.keys() )
        except:
            self.db = cdb.init( self.fn )
            return iter (self.db.keys() )

    def keys(self):
        try:
            return self.db.keys()
        except:
            self.db = cdb.init( self.fn )
            return self.db.keys()