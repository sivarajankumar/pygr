# Introduction #

This article is an in-depth explanation of a script in which a genome and the accompanying annotations are manipulated in multiple ways,including in a MySQL table, and then stored in worldbase, a resource database. Storing the data this way enables it to be easily manipulated using pygr and prevents potential errors by allowing ease of access to the necessary genomic information.

**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


# Step-By-Step Example #

In this example the genome and annotations were downloaded from the NCBI database and stored in  two files, a .fna file and a .gff file. The .fna file is the actual genome, while the .gff file is comprised of the annotations.

The OptionParser class, taken from the optparse module, processes command line arguments. The filenames ( a .fna file and .gff file, in this case) are supplied by attributing them to an option name in the command line. If the attribute for either option is 'None', indicating there was no filename supplied, the help text for optparse will be printed, as well as the available option names. The option for each file was added, then given a name that would represent it during parsing.

In this step, the genome is loaded into a BLAST database. The BlastDB module establishes a BLAST database for the genome.

```
import sys
import csv
import os
from optparse import OptionParser
from pygr.seqdb import BlastDB
from pygr import seqdb
from pygr import cnestedlist
from pygr.sqlgraph import SQLTable

parser = OptionParser()
parser.add_option("-f", "--fna_file", dest="fna_filename")
parser.add_option("-g", "--gff_file", dest="gff_filename")
(options, args) = parser.parse_args()

if options.fna_filename is None or\
   options.gff_filename is None:
    parser.print_help()

genome = BlastDB(fna_filename)
```



In this next section, a connection to MySQL is established, and the basic frame work for the SQL databases is created. If a password is needed to connect to MySQL, it would be inserted after the user name in MySQLdb.connect. For example, if my password were “clover” the line of code would be:
conn = MySQLdb.connect(host='localhost', user='mccreary', passwd='clover')

Also, since I was creating a database for the E. coli genome, I named it 'ecoli', then dropped any current databases with that name. Next, I created a new database 'ecoli' for use.

A table (features2) is then created:

```
import MySQLdb

conn = MySQLdb.connect(host='localhost', user='mccreary')

In MySQL, a cursor is a named statement from which information from tables can be accessed easily and efficiently. 

c = conn.cursor()

c.execute('drop database if exists ecoli')

c.execute('create database ecoli')

c.execute('use ecoli')

c.execute('''

CREATE TABLE features2 (

   keyval INTEGER PRIMARY KEY AUTO_INCREMENT,

   start INTEGER NOT NULL,

   stop INTEGER NOT NULL,

   orientation INTEGER NOT NULL,

   chr TEXT NOT NULL,

   info TEXT NOT NULL

);

''')

c.execute('delete from features2')
```


In creating the dictionary for the annotations, the csv module can be used to read the .gff file. The csv module is able to differentiate the unique fields. Furthermore, the fields in the subsequent database are created and identified.

The following uses the csv dict reader to read the file. Since the annotations are seperated by white spaces, it can be difficult to differentiate the data in the separate fields, which is why DictReader is used.

```
annot_dict = {}

reader = csv.DictReader(open(gff_filename, "rb"),

                        fieldnames=['seqname',

                                    'source',

                                    'feature',

                                    'start',

                                    'end',

                                    'score',

                                    'strand',

                                    'frame',

                                    'group'],

                        delimiter='\t')

for row in reader:

    if row['seqname'][0:2] != '##': # Ignore comments 

        start = int(row['start'])

        stop = int(row['end'])

    

        if start == stop:

            continue

    

        if row['strand'] == '+':

            o = 1

        else:

            o = -1
```


Each row that is read is entered into the features2 table. 'Start' and 'stop' identify the beginning and end of each interval on the sequence (given with respect to the positive strand), 'orientation' is the orientation of the interval on the sequence (will return a value of 1 or -1, depending on whether it is the positive or negative strand), 'chr' is the identification of the sequence the intervals are contained within, and 'info' is the gene identifier.

```
        c.execute('''INSERT INTO features2 (start, stop, orientation, chr, info)

                  VALUES (%s, %s, %s, %s, %s)''',

                  (start, stop, o, row['seqname'], row['group']))

        

        n = reader.reader.line_num

    

        if n % 1000 == 0:

            print '...', n

            conn.commit()



conn.commit()
```

Finally, the MySQL database for the annotation is built, and saved as the supplied database name. conn.commit() closes the database and the transaction and makes the changes permanent.

Here, slicedb uses the annotation objects from the SQLTable, which correspond to the gene sequences in the BLAST database previously constructed that contains the genome. AnnotationDB uses the annotations as keys within a dictionary, and the values are the annotation objects, which are similar to sequence intervals in that they represent segments of the genome, but have annotation data associated with them. The two containers supplied for AnnotationDB are the slicedb, which contains the SQL table that holds the list of annotation objects, and sequence database for the E. coli sequence that holds the sequence intervals.

It should be noted that the sequence intervals and the annotation objects are NOT stored in the same database. The annotations and their corresponding IDs are stored within the annotation database, while the related sequence intervals are stored within the sequence database, also with their own IDs. However, the annotation objects have a sequence attribute that enables the annotation's matching sequence interval to be given as well.

Then, a dictionary is created to hold the annotations and the sequences they correspond to together. PrefixUnionDict provides a cohesive interface to access the data in the two databases.


Finally, an annotation map is created, with the annotations added. The nested list format for data structure shortens the time needed to scan the intervals by storing overlapping intervals in a more efficient and hierarchal format. The annotations are then mapped to the segment of the genome to which they correspond.

```
slicedb = SQLTable('ecoli.features2', c)

annots = seqdb.AnnotationDB(slicedb, genome,

                              sliceAttrDict=dict(id='chr'))


genomeUnion = seqdb.PrefixUnionDict({ 'CP000802' : genome,

                                      'annots' : annot_db })

annot_map = cnestedlist.NLMSA('annotationmap', 'w', genomeUnion,

                              pairwiseMode=True)


for n, k in enumerate(annot_db):

    if n % 1000 == 0:

        print 'adding...', n

    v = annot_db[k]

    annot_map.addAnnotation(v)



print 'building...'

annot_map.build()
```

Docstrings are then created for the genome, the annotations, and the annotation map so they may be stored in worldbase. worldbase requires docstrings to be assigned to every resources stored within, to allow a more descriptive storage of resources and to allow easier access.

Finally, the genome, the annotation, and the annotation map is stored in worldbase. Since the annotation map is a schema, its can be stored in worldbase as a schema. In order to store schema in worldbase, the relationship between the schema must be defined (Many-To-Many or One-To-Many). The annotation map is saved in pygr.Dara first, then again with the schema assignment. When saving the map as schema, the relationship between the schema and the resources it references must also be made clear, and the resources must be available in worldbase as well (you must save the genome and annotations along with the annotation map).

bindAttr can have up to three attribute names, although only one is used here. 'annots' is bound to the objects of the source database (the annotations are keys for the annotation map). The worldbase resources are then stored to worldbase using the save() command, which is essential for any session that modifies or adds worldbase resources.

```
genome.__doc__ = 'ecoli genome'
annots.__doc__ = 'ecoli annotations'
annot_map.__doc__ = 'annotation map'

worldbase.Bio.Seq.Genome.ecoli = genome 
worldbase.Bio.Annotation.ecoli.annotations = annots
worldbase.Bio.Annotation.ecoli.annotationmap = annot_map
worldbase.schema.Bio.Annotation.ecoli.annotationmap = \
    worldbase.ManyToManyRelation(genome,annots,bindAttrs=('annots',))

worldbase.save()
```