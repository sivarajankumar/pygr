# Introduction #

This tutorial introduces worldbase, which allows for easy access to multiple datasets by providing a consistent namespace or context for data. This method of data retrieval enables users to manipulate large quantities of data, potentially on multiple machines, without the added worry of ensuring each computer can directly access the various filepaths.  However, it should be noted that worldbase is intended for higher-level data resources, such as a MySQL table, BLAST sequence database, or a Python dictionary or shelve, because worldbase is purposed to be a “database of databases” rather than a substitute for a database.

**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


# A Walk Through the Code #

The E. coli genome sequence is stored in a BLAST database using seqdb. BLAST (Basic Local Alignment Search Tool) databases are designed for storing sequence alignments.

worldbase is then imported to allow access to the data namespace. This is an essential step, as worldbase must be previously imported in order to store or access data from or in it. WORLDBASEPATH must be set to the directory in which it is located.
In the following step, the data is stored in a container. There are many options for this, including a MySQL table or a BLAST database as seen here.

Furthermore, assigning a doc string is extremely important, as the data MUST have a doc string, which describes the kind of data it is, so that when a user looks at a directory listing of worldbase, he/she can quickly ascertain what data is stored. A docstring (documentation string) allows users to easily associate documentation with functions, classes, and modules, which is especially convenient for worldbase, since many databases could potentially be stored in it, and documentation ensures clarity and unambiguity.

Finally, the data is stored in worldbase using the save() function. In all worldbase sessions, it is essential to call the worldbase.save() function to ensure all new data that has been added that session is committed. Furthermore, it is imperative to observe the naming conventions for saving data to worldbase, since not only does it assign a unique and consistent name to the data, ensuring its easy import, but also since multiple users could be using one worldbase database and the data should be clearly organized.

```
from pygr import seqdb, worldbase 

ecoli = seqdb.BlastDB('/home/mccreary/Projects/pygr/data/CP000802.fna')

ecoli.__doc__ = 'ecoli genome sequence' 

worldbase.Bio.Seq.Genome.ECOLI.ecoli = ecoli 

worldbase.save()
```