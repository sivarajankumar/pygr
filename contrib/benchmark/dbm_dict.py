# dbm based dictionary

# use this for windows
#import dumbdbm as dbm_lib

# uncomment this for unix
import gdbm as dbm_lib

def dbm_open( filename, mode='c'):
    db = DbmShelve(filename, mode=mode)
    return db

class DbmShelve( object ):

    def __init__ (self, filename, mode):
        # will switch modes of operation depending on the type of access
        self.db = dbm_lib.open( filename, mode) # ahem

    def create_index(self):
        pass

    def sync(self):
        if hasattr(self.db, 'sync'):
            self.db.sync()

    def close(self):
        if hasattr(self.db, 'close'):
            self.db.close()

    def __setitem__(self, key, value):            
        self.db[key] = value  
    
    def __getitem__(self, key):            
        return self.db[key]
   
    def __iter__(self):
        return iter( self.db.keys() )

    def keys(self):
        return self.db.keys()

if __name__ == '__main__':
    db = DbmShelve('test.db', mode='c')
