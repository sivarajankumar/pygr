# Introduction #

This code, which utilizes some of pygr's numerous storage databases (seqdb and AnnotationDB), demonstrates a way in which intergenic regions are located within a genome, then stored and maniuplated using pygr.

**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


# A Guide to the Script #

First, once the necessary modules are imported, the yeast genome (the .fna file) is stored in a BLAST database through the seqdb module in pygr. The BlastDB unpacks the FASTA id and potentially several other ids potentially contained in the NCBI genome. The ID is obtained from the genome by splicing the key located at the beginning of the genome sequence. The key looks like this: gi|50593115|ref|NC\_001134.7|, but the desired ID is merely NC\_001134.7, necessitating the split. Next, the search for the intergenic region continues by creating the class Intergenic, which defines the characteristics of each regions, including before\_gene (the gene preceding the region), after\_gene, start and stop (the integers at which the sequence starts and concludes), orientation (which strand the region is located upon), length, and id.

```
import csv
import string
from pygr.seqdb import BlastDB
from pygr import seqdb
from pygr import cnestedlist
import cogs2


# Load up the genome into a BlastDB
genome = BlastDB(data/NC_001134.fna)
# Get the ID from the genome
for key, val in genome.iteritems():
    genome_id = key.split('|')[3]
    break # We only have one 

# Create a class for the intergenic region
class Intergenic(object):
    def __init__(self, before_gene, after_gene, start, stop, orientation, id, length):
        self.before_gene = before_gene
        self.after_gene = after_gene
        self.start = start
        self.stop = stop
        self.orientation = orientation
        self.id = id
        self.length = length
Intergenic_Regions = {}

```

Next, the cogs2 module provides several handy classes for iterating through the various regions between known genes, including CogsFileContent. This class reads the .ptt file and converts the gene coordinates to integers, throughout the length of the yeast genome stored in the BlastDB. The function return\_intergenic\_regions returns a dictionary of the intergenic regions consisting of the start and stop coordinates of the intergenic regions and the gene names for the previous and subsequent gene.

The start and stop coordinates for each region interval is defined and saved, and the dictionary Intergenic\_Regions now holds all of the pertinent data for the intergenic sequences.

```
yeastregions = cogs2.CogsFileContent(data/NC_001134.ptt, len(genome))

def return_intergenic_regions(ptt_info):
    intergenic = cogs2.IntergenicRegionsByFootprint(ptt_info)
    yeast_between = {}
    for(start, end, name) in intergenic:
        if "-" in name:
            continue
        key = tuple(name)
        if end - start > 0:
            yeast_between[key] = (start, end)
    return yeast_between


yeast = return_intergenic_regions(yeastregions)
id = genome.seqLenDict.keys()[0]
yeast_genome = genome[id]


for i, (gene,site) in enumerate(yeast.iteritems()):
    regions = str(yeast_genome[site[0]:site[1]])
    start = site[0]
    stop = site[1]
    Intergenic_Regions[i] = Intergenic(gene[0] ,gene[1], start, stop, 1, genome_id, stop - start + 1)
```

An annotation database is created to store the intergenic regions and the yeast genome. Annotation databases are especially useful because they can be utilized in several different ways. For example, a simple use shown here is to assign the first intergenic region to intergenic\_region\_1, then print out the preceding gene, the following gene, and the actual sequence of the region. Obviously, AnnotationDB has many more complex uses, but the ease with which it finds and stores information makes it handy to do simple tasks as well.

Finally, a reverse mapping is built, tying the intergenic regions to the genome and storing them as representations of aligned intervals using nestedlist, allowing the pairs to takes up very little storage space but providing ease of search and function. The sequences can be easily and simply queried. The start and stop coordinates of the desired region are provided, as well as the genome id, and, using the keys method, relevant data can be quickly produced.

```
# Create a pygr AnnotationDB
annot_db = seqdb.AnnotationDB(Intergenic_Regions, genome)
# Do cool things with it
intergenic_region_1 = annot_db[1] # The key is the order
print(intergenic_region_1.before_gene) # The gene that comes before
print(intergenic_region_1.after_gene) # The gene that comes after
print(intergenic_region_1.sequence) # The intergenic sequence
# And so on

# Build a reverse mapping
annot_map = cnestedlist.NLMSA('genes', mode='memory', use_virtual_lpo=True)
for v in annot_db.values():
    annot_map.addAnnotation(v)
annot_map.build()
query_sequence = genome[genome_id][intergenic_region_1.start:intergenic_region_1.stop]
annotations = annot_map[query_sequence]
annotation = annotations.keys()[0]
print(annotation.before_gene)
```

# Conclusion #

While this script is fairly simple, it can be modified to serve varied purposes. For example, an intergenomic region of interest can be quickly found and iterated through, so concentrating on a small portion of a large genome can become an easy task. Furthermore, AnnotationDB can be manipulated in various ways, according to the user's skill level and desired use.


## Note ##

cogs2.py and return\_intergenic\_regions are based upon code Dr. C. Titus Brown wrote, and can be found and used in the article "Using pygr to study orthologous binding sites in bacterial genomes". found here: http://bio.scipy.org/wiki/index.php/Using_pygr_to_study_orthologous_binding_sites_in_bacterial_genomes.