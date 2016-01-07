# Goals #

This page is for assembling information about needs and possible solutions for working with Solexa and other high-throughput sequencing data.  Please use this page to list:
  * describe datasets you need to work with: numbers of sequences, length, etc.
  * describe types of analysis you want to perform, ideally in the form of some kind of pseudocode that makes clear how the data would be used
  * Experiments you've tried
  * Problems you've run into and need solved
  * Ideas for how to solve them
  * Tools that could be useful for this effort

# Datasets #

**Namshin Kim**: Here is the situation. I have 1G, a billion, reads of 36bp.

# Analyses #
**Namshin Kim**:  I want to scan the alignments by genomic coordinates, and then I can see genomic variations in detail. I can make variation calling module or basic module for genome browser. I am already working on it.For the solexa data processing, I am trying to save them into axtNet format in pairwiseMode. Of course I can save as annotation database, but I thought it would be much useful. Correct me if there is another way to do, maybe combination of annotation database and seqdb?

# Problems We Must Solve #
**Namshin Kim**: Here are the problems. Assume that I decided to save them as pygr-aware
axtNet format. Usually, sequence ID is long, average 20 characters. It means
I need 40GB memory (if python saves them by unicode) to build prefixUnion.
We have hundreds of 8-core machines with 16GB memory, but not 40GB memory.
My conclusion is to split them into smaller pieces, maybe 100M reads or
smaller.

# Tools we should consider #

## Mapping Methods ##
Shawn Cokus in Matteo Pellegrini's lab has developed a probabilistic mapping algorithm that is fast, scalable, and accurate.  We've used this for an alternative splicing Solexa analysis.  I've mentioned to Shawn that it would be interesting to incorporate this into Pygr with an NLMSA-like interface.

## Database Classes ##
**Chris Lee**: I think we should consider having a sequence database class optimized for huge numbers of fixed length reads (like Solexa).

  * each sequence would have a int ID assigned in ascending order
  * you would initialize the DB by specifying a max length per sequence.  It would then store sequences in a disk file as fixed length blocks of exactly that size.  It can then fseek() directly to the right block just based on the numerical ID of the sequence.
  * if we wanted we could eventually develop flavors that store the data using 2 bit or other reduced representation to save space.
  * you can add more sequences at any time, and I guess you could remove sequences as well, although I don't know what use that would be.
  * the Solexa assigned string ID of each sequence could be kept in a  separate file on more or less the same principle, so that one can map from number ID to string ID quickly and easily.  The reverse mapping implies using shelve or some equivalent.

  * the interface to the SolexaDB would be the same as BlastDB, of course.  Or maybe this would just be another subclass of BlastDBbase...