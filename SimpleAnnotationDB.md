# Introduction #

Sometimes it's nice to know exactly what behavior you need to implement to get
something minimal going.  Here are some notes on doing that with an AnnotationDB-a-like
object that doesn't support pickling or anything fancy; it just acts as an AnnotationDB.

**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


# Details #

Here's the basic code:

```
class MyAnno(SeqPath):
    step = 1
  
    def __init__(self,id,db,parent,start,stop):
        self.id = id                    # unique name of this feature
        self.db = db                    # annotation database for lookups
        # self.start -> 0
        self.stop = stop-start          # reset to start at 0
        self._anno_seq = parent         # actual sequence
        self._anno_start = start        # offset within sequence
        self.path = self                # simple SeqPath obj

class MyAnnoDB(object):
    def __init__(self, seqDB):
        self.d = {}
        self.seqDB = seqDB

    def add(self, f):
        self.d[f.id] = f

    def __getitem__(self, k):
        return self.d[k]

```

OK, a few notes:

> - MyAnnoDB.seqDB is necessay for lookups, e.g. annotation.sequence will look for annodb.seqDB.

> - apart from that, MyAnnoDB really only needs to implement the getitem protocol for retrieving values by key.  The 'add' function is just to add annotations; it doesn't need to be there if MyAnnoDB is retrieving annotations from somewhere else.

> - even though it's not explicit in the code, MyAnnoDB should return objects of type MyAnno!