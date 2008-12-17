# uses manual indexing

import sys, os, string, bsddb, random, sqlite3

def sq_dict2_open( filename, mode='c'):
    db = SqliteShelve(filename, mode=mode)
    return db

class SqliteShelve( object ):

    def __init__ (self, filename, mode='c'):
        """
        Mimics the bsdb shelve dictionary.
        Modes: n=new, c=create if necessary, r=read w=write
        """
        
        # new database, delete old
        if mode == 'n' and os.path.isfile(filename):
            os.remove(filename)

        # keeps cursor over the lifetime of the class
        self.conn = sqlite3.connect(filename)
        self.curs = self.conn.cursor()

        # create tables if necessary
        if mode in ('n', 'c') and not self._has_table():
            self._create_table()
    
    def _create_table(self):
        "Creates the table"
        self.curs.execute("""CREATE TABLE data (key BLOB, value BLOB)""")
    
    def _has_table(self):
        "Detects the existence of the data table"
        self.curs.execute("""SELECT name FROM sqlite_master WHERE type = 'table' AND name='data'""")
        count = len ( self.curs.fetchall() )
        assert count <= 1 # sanity check
        return count == 1

    def __setitem__(self, key, value):            
        stmt  = "REPLACE INTO data (key, value) VALUES (?, ?)" 
        self.curs.execute( stmt, (str(key), str(value) ) )

    def fast_loading( self, values):
        query  = "REPLACE INTO data (key, value) VALUES (?, ?)" 
        self.curs.executemany( query, values )

    def __getitem__(self, key):            
        stmt = "SELECT value FROM data WHERE key=?" 
        key, = self.curs.execute( stmt, (key,) )
        return key
    
    def __iter__(self):
        query  = "SELECT key FROM data" 
        for rowkey, in self.conn.execute( query):
            yield str(rowkey)

    def keys(self):
        stmt  = "SELECT key FROM data" 
        self.curs.execute( stmt )
        return [ str(r[0]) for r in self.curs.fetchall() ]
    
    def sync(self):
        self.conn.commit()

    def data_dump(self):
        stmt  = "SELECT * FROM data" 
        self.curs.execute( stmt )
        print len( self.curs.fetchall() )
    
    def close(self):
        self.conn.close()

    def create_index(self):
        self.conn.execute('''CREATE UNIQUE INDEX keyindex ON data (key)''')
        self.sync()

def btree_test():
    #db = bsddb.btopen(' test.btree', 'n')
    db = bsddb.hashopen(' test.btree', 'n')

    for count in xrange( ELEM_NUM):
        key = str(count)
        db[key] = ROW
    db.close() 

if __name__ == '__main__':
    #btree_test()
    db = SqliteShelve( 'test.sqlite' )

    db[1] = 123

    db.sync()
   
