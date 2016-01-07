# Introduction #

We're trying to simplify Pygr's data models for the 0.8 release.  Here I'll propose how we might refactor the sequence database model a bit.  My main goals:
  * call the base class SequenceDB.  Put all BLAST support in a subclass.
  * define a standard, modular API to the actual storage, so no storage code is mixed up in the SequenceDB class.  It should be possible to use different storage classes with SequenceDB.
  * let users define / supply any sequence reading function they want.
  * start using the standard get\_bound\_subclass() system for handling itemClass, the same as in other parts of Pygr.

### What's New ###
The main change is modularizing the storage access mechanisms into the the **seqInfoDict** and `_init_subclass()` classmethod supplied by the **itemClass**.


## Proposed SequenceDB model ##

  * **itemClass** attribute: class to use for each top-level sequence object.  I propose that all functions for storage access (building and searching the index) be part of the itemClass, since it represents the storage interface.
  * **itemSliceClass** attribute: class to use for sequence sub-slice objects
  * **seqInfoDict** attribute: dictionary interface to sequence information from the storage mechanism.  Returns an object with attributes like **length**, **title** and possibly others like **offset**.  This is the official mechanism for getting some information about what's in the database without actually triggering the construction of a sequence object.  This interface is needed for things like NLMSA that will need to construct union coordinate systems that unify one or more sequence databases.
  * `__getitem__(seqID)`: get the sequence object with this ID
  * `__len__()`: get total number of sequences in this database
  * `__invert__()`: get reverse mapping object (maps sequence obj to its ID).
  * `__contains__(B)`: True if the argument is a sequence in this database
  * `__iter__()` etc.: all the standard dictionary iterators
  * `cacheHint(owner, ivalDict)`: save a cache hint dict of {id:(start,stop)} associated with owner
  * `strsliceCache(seq,start,stop)`: get strslice using cache hints, if any


## Sequence model ##
  * **id** attribute: gives the ID of the sequence (primary key within its database)
  * **db** attribute: points to the database object containing this sequence
  * **path**: the complete sequence object containing this sequence interval
  * **start**, **stop**: coordinates for this interval.  See docs for sign convention.
  * **orientation**: 1 if forward strand, -1 if negative strand
  * `__getitem__(slice)`: slice this sequence
  * `__len__()`: get this sequence's length
  * `__str__()`: get this sequence interval's sequence string
  * `__neg__()`: get reverse-complement of this sequence interval (ValueError if protein)
  * `__add__(B)`: get union with another sequence interval, i.e. A+B covers the interval [A.start,B.stop]. (ValueError if not in the same parent sequence).
  * `__contains__(B)`: True if the argument is a sub-interval of this sequence interval
  * `__mul__(B)`: get intersection with another sequence interval, i.e. A\*B is the largest interval contained both in A and in B.
  * `before()`: get the entire interval up to this sequence (adjacent on the left)
  * `after()`: get the entire interval after this sequence (adjacent on the right)
  * `seqtype()`: get type (nucleotide or protein) of this sequence
### Additional implementor methods ###
  * `strslice(start, stop)`: get string corresponding to sequence for interval [start,stop].  This is the primary interface to the actual storage.
  * `_init_subclass(seqReader=None)`: classmethod on the itemClass, that initializes connection to the storage, constructing the index if necessary, and adds a **seqInfoDict** attribute to the sequence database object.  Should accept a seqReader method argument that iterates all the sequences in the input file and returns all the IDs and sequences.