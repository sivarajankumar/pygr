**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.

# Why It's Useful #

pygr's data storage tools allow easy manipulation of the information they contain. In this example, I take the entire E. coli genome, as well as the corresponding annotations, and use AnnotationDB, BlastDB, as well as several modules within pygr to store the gene intervals and their corresponding sequences, and then count the number of nucleotides per gene by iterating over all of the genes. Finally, the average number of nucleotides per gene is calculated using the full count of the number of bases in the full genome sequence.

# Documenting the Code #

```
import sys
import csv
import os
from optparse import OptionParser
from pygr.seqdb import BlastDB
from pygr import seqdb
from pygr import cnestedlist
import re
```

Once everything is imported, the focus turns to interpreting the .gff file used in this example. One of the initial problems I had was defining the id. AnnotationDB needs at least an ID, as well as the start and stop values. However, the annotation ID is the same for each annotation, and something was needed to serve as a unique reference for each annotation that mapped to a different sequence. I noticed that the locus\_tag=EcHS\_A(number) was unique for each Genbank Gene, Regular Expression was used to search through the annotations, and store each annotation and its corresponding data if the locus tag was unique.

The class EcoliGene was defined to clarify each row and the information contained within. The orientation was specified by assigning a negative value to the start and stop values. If the start and stop values were 349 and 915 but the value of 'strand' was -1, the values assigned for start and stop would be-349 and -915.

```
re_locus_tag = re.compile('locus_tag=EcHS_A(\d+)')

class EcoliGene:
    def __init__(self, row):
        self.id = row['seqname']
        self.feature = row['feature']
        start = row['start']
        stop = row['stop']
        self.score = row['score']
        self.frame = row['frame']
        self.source = row['source']
        m = re_locus_tag.search(row['group'])
        if m:
            self.gene = m.group(1)
        else:
            pass

        if row['strand'] == -1:
            self.start = -stop
            self.stop = -start
        else:
            self.start = start
            self.stop = stop
        self.strand = row['strand']
```

The files were loaded using the simple OptionsParser module, which takes the command line arguments, stores them as the designated options, and loads them when called (like options.ecoli\_fna\_filename). The parser is populated with the command line arguments, and the unique options assigned to each argument differentiates between them.

The ecoli genome (ecoli\_fna\_filename) is stored in a BlastDB. The BlastDB unpacks the FASTA id and potentially several other ids potentially contained in the NCBI genome.

DictReader (from the csv module) opens the .gff file and reads the tab-separated entries, assigning each a string name. Since the entries are separated by tabs, the delimiter used to differentiate the fields is clearly a tab.

```
parser = OptionParser()
parser.add_option("-f", "--ecoli_fna_file", dest="ecoli_fna_filename")
parser.add_option("-g", "--ecoli_gff_file", dest="ecoli_gff_filename")

(options, args) = parser.parse_args()

ecgenome = BlastDB(options.ecoli_fna_filename)
ecgenome = genome['gi|157065147|gb|CP000802.1|']

reader = csv.DictReader(open(options.ecoli_gff_filename, "rb"),
                        fieldnames=['seqname',
                                    'source',
                                    'feature',
                                    'start',
                                    'stop',
                                    'score',
                                    'strand',
                                    'frame',
                                    'group'],
                        delimiter='\t')
```

Here comes the fun part. In order to perform our desired calculations on this genome, the various gene intervals denoted in the annotations must be linked to their corresponding sequence in the genome. In short, the specific nucleotides must be able to be retrieved. First, a dictionary is created, annots, which will hold the gene intervals found earlier in the code keyed by the locus\_tag. It will also store the corresponding values (start, stop, id, etc.) for the gene intervals.

The annots dictionary and E. coli genome are then both stored in seqDB, which, as mentioned earlier, is finicky about the sequence ID given, so ensure the field assigned to the id in the .gff file is actually the desired field that stores the id.

Next, another dictionary is created, this time to store the counts of each nucleotide per gene (ex: In the gene '1364', there are 226 As). iteritems() came in handy because it iterated over the dictionary, and returned the value for each gene. nucs was the key for the ec\_count, and each nucleotide base was a value (A, T, G, C,).

```
annots = {}
for row in reader:
    if row['seqname'][0:2] != '##': # Ignore comments
        if row['feature'] == 'gene':
            span = EcoliGene(row)
            annots[span.gene] = span

annot_db = seqdb.AnnotationDB(annots, ecgenome)

ecoli_nuc_count = {}

for gene, annot in annot_db.iteritems():
    nucs = str(annot.sequence)
    ec_count = dict(A=0, C=0, T=0, G=0)
    for nuc in nucs:
            ec_count[nuc] = ec_count[nuc] + 1
    ecoli_nuc_count[gene] = ec_count
```

I then create another dictionary, sum, to hold the counts of the number of nucleotides per genome. The intial sums are all set at 0.0 to initialize the count.

Next, we iterate over the genes and nucleotide counts, each instance of a nucleotide increasing the count for that base by one. And finally, the reason for the code: the sum of each base is divided by the total number (producing the average number of bases for that gene) and prints the values found for the calculations.

```
sum = {}
sum['A'] = 0.0
sum['G'] = 0.0
sum['C'] = 0.0
sum['T'] = 0.0

for gene, count_dict in ecoli_nuc_count.iteritems():
    for nuc, count in count_dict.iteritems():
        sum[nuc] += count
        
for nuc, count in sum.iteritems():
    sum[nuc] /= len(ecoli_nuc_count)
    print('The average %s nucleotide per gene is %f' % (nuc, sum[nuc]))
```