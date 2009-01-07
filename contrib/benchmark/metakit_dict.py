# metakit based dictionary

import metakit

def metakit_open(filename, mode='c'):
    db = MetakitShelve(filename, mode=mode)
    return db

class MetakitShelve( object ):

    def __init__ (self, filename, mode):
        self.db = metakit.storage( filename, 1) 
        view = self.db.getas("data[key:S,value:S]")
        hashvw = self.db.getas("__test_hash__[_H:I,_R:I]")
        self.view = view.hash(hashvw, 1)

    def create_index(self):
        pass

    def sync(self):
        self.db.commit()

    def close(self):
        pass

    def __setitem__(self, key, value):            
        self.view.append( (key, value))  
    
    def __getitem__(self, key):            
        return self.view.select(key=key)[0].value
   
    def __iter__(self):
        return iter( self.keys() )

    def keys(self):
        return [r.key for r in self.view]

if __name__ == '__main__':
    db = MetakitShelve('test.db', mode='c')
    for i in range(1000):
        db['1'] = '2'
    
    print db['1']
    for key in db:
        print key
