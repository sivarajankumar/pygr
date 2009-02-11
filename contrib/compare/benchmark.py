"""
Benchmarking various python based sequence manipulation 
frameworks
"""
import time, shelve, glob, os
from pygr import seqdb, logger
from Bio import SeqIO
from cogent import LoadSeqs, DNA
from bx.seq import fasta

NSLICE = 10**5

class Timer(object):
    """Timer decorator, prints timing information on a function call"""
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwds):
        start = time.time()
        try: 
            # first argument is the tested function, the others are arguments
            return self.func(*args, **kwds)
        finally:
            end = time.time()
            print '%20s\t%3.1fs' % ( self.func.__name__, end-start) 

def get_index( fname, tag='index', flag='c' ):
    fp = shelve.open( "%s-%s.db" % (fname, tag), flag=flag )
    return fp

def cleanup():
    "Cleans up index data"
    protected = [ 'dm.fasta', 'sacCer.fasta', '100K.fasta' ]
    for fname in glob.glob("data/*"):
        base = os.path.basename(fname)
        if base not in protected:
            os.remove(fname)

@Timer
def pygr_parse_fasta( fname ):
    fasta = seqdb.SequenceFileDB( fname )

@Timer
def bio_parse_fasta( fname ):
    handle = open( fname )
    index = get_index( fname, tag='bio', flag='c')
    for rec in SeqIO.parse(handle, "fasta") :
        index[rec.id] = rec
    index.close()                
    handle.close()


@Timer
def cogent_parse_fasta( fname ):
    index = get_index( fname, tag='cogent', flag='c')
    fasta = LoadSeqs(fname, moltype=DNA, aligned=False)
    for id, seq in fasta.items():
        index[id] =  seq
    index.close()

@Timer
def bx_parse_fasta( fname ):
    handle = open( fname )
    index = get_index( fname, tag='bx', flag='c')
    for rec in fasta.FastaReader( handle ) :
        # nuke open file handle
        rec.file = None
        index[rec.name] = rec
    index.close()                
    handle.close()


@Timer
def pygr_iter( fname ):
    fasta = seqdb.SequenceFileDB( fname )
    for rec in fasta:
        seq = fasta[rec]

@Timer
def bio_iter( fname ):
    fasta = get_index( fname, tag='bio', flag='c')
    for rec in fasta:
        seq = fasta[rec]
    fasta.close()                

@Timer
def bx_iter( fname ):
    fasta = get_index( fname, tag='bx', flag='c')
    for rec in fasta:
        seq = fasta[rec]
    fasta.close()     

@Timer
def cogent_iter( fname ):
    fasta = get_index( fname, tag='cogent', flag='c')
    for rec in fasta:
        seq = fasta[rec]
    fasta.close()  


@Timer
def pygr_slice( fname ):
    fasta = seqdb.SequenceFileDB( fname )
    for rec in fasta:
        seq = fasta[rec]
        for i in range(NSLICE):
            sub = str(seq[:100])
        break

@Timer
def bio_slice( fname ):
    fasta = get_index( fname, tag='bio', flag='c')
    for rec in fasta:
        seq = fasta[rec].seq
        for i in range(NSLICE):
            sub = seq[:100].tostring()
        break
    fasta.close()                

@Timer
def bx_slice( fname ):
    fasta = get_index( fname, tag='bx', flag='c')
    for rec in fasta:
        seq = fasta[rec]
        for i in range(NSLICE):
            sub = seq.get(0, 100)
        break
    fasta.close()     

@Timer
def cogent_slice( fname ):
    fasta = get_index( fname, tag='cogent', flag='c')
    for rec in fasta:
        seq = fasta[rec]
        for i in range(NSLICE):
            sub = str( seq[:100] )
        break
    fasta.close()  

@Timer
def pygr_reverse_comp( fname ):
    fasta = seqdb.SequenceFileDB( fname )
    keys = fasta.keys()
    keys.sort()
    for rec in keys:
        # force full reverse complement
        seq = str(-fasta[rec])
        sub = seq[:10]

@Timer
def bio_reverse_comp( fname ):
    fasta = get_index( fname, tag='bio', flag='c')
    keys = fasta.keys()
    keys.sort()
    for rec in keys:
        seq = fasta[rec].seq.reverse_complement()
        sub = seq.tostring()
    fasta.close()                

@Timer
def cogent_reverse_comp( fname ):
    fasta = get_index( fname, tag='cogent', flag='c')
    keys = fasta.keys()
    keys.sort()
    for rec in keys:
        seq = fasta[rec].reversecomplement()
        seq = str(seq)
        sub = seq[:10]
    fasta.close()

@Timer
def bx_reverse_comp( fname ):
    fasta = get_index( fname, tag='bx', flag='c')
    for rec in fasta:
        seq = fasta[rec]
        rev = seq.reverse_complement( seq.text )
        rev = str(rev)
        
    fasta.close()    

def run_benchmarks( fname ):
    print '%20s\t%s' % ( 'Test', 'Time') 
    
    logger.disable('DEBUG')
    
    if 1:
        cleanup()
        pygr_parse_fasta(fname )
        bio_parse_fasta(fname)
        bx_parse_fasta(fname)
        cogent_parse_fasta(fname )

    print '-' * 20

    if 1:
        pygr_iter(fname )
        bio_iter(fname)
        bx_iter(fname)
        cogent_iter(fname)

    print '-' * 20

    if 1:
        pygr_slice(fname )
        bio_slice(fname)
        bx_slice(fname)
        cogent_slice(fname)

    print '-' * 20
    
    if 1:
        pygr_reverse_comp(fname )
        bio_reverse_comp(fname)
        bx_reverse_comp(fname)
        cogent_reverse_comp(fname)

if __name__ == '__main__':
    fname = 'data/100K.fasta'
    
    fname = 'data/dm.fasta'

    print '*** benchmarking=%s' % fname
    run_benchmarks( fname )