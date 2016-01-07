# Introduction #
This page explains how to build an NLMSA from the UCSC pairwise alignment format [AXT](http://genome.ucsc.edu/goldenPath/help/axt.html).

See http://www.doe-mbi.ucla.edu/~leec/newpygrdocs/reference/cnestedlist.html#nlmsa for full module documentation.

# Requirements #
In this example, the following are needed:
  1. Genomic sequences
    * [hg18](http://hgdownload.cse.ucsc.edu/goldenPath/hg18/bigZips/chromFa.zip)
    * [panTro2](http://hgdownload.cse.ucsc.edu/goldenPath/panTro2/bigZips/chromFa.tar.gz)
    * [mm8](http://hgdownload.cse.ucsc.edu/goldenPath/mm8/bigZips/chromFa.tar.gz)
    * [rn4](http://hgdownload.cse.ucsc.edu/goldenPath/rn4/bigZips/chromFa.tar.gz)
    * [canFam2](http://hgdownload.cse.ucsc.edu/goldenPath/canFam2/bigZips/chromFa.tar.gz)
  1. Pairwise alignments
    * [hg18\_self](http://hgdownload.cse.ucsc.edu/goldenPath/hg18/vsSelf/axtNet/)
    * [hg18\_panTro2](http://hgdownload.cse.ucsc.edu/goldenPath/hg18/vsPanTro2/axtNet/)
    * [hg18\_mm8](http://hgdownload.cse.ucsc.edu/goldenPath/hg18/vsMm8/axtNet/)
    * [hg18\_rn4](http://hgdownload.cse.ucsc.edu/goldenPath/hg18/vsRn4/axtNet/)
    * [hg18\_canFam2](http://hgdownload.cse.ucsc.edu/goldenPath/hg18/vsCanFam2/axtNet/)

# Details #
The steps are as follows:
  1. Download the axtNet alignments from UCSC website (for example, those listed above) and uncompress gzip archives. To easily get the pairwise alignment files, a script like the following is useful:
```
for species in Self PanTro2 Mm8 Rn4 CanFam2 ; do
wget --no-parent -A.axt.gz http://hgdownload.cse.ucsc.edu/goldenPath/hg18/vs${species}/axtNet/ ;
done

tar xvzf *.axt.gz
```
  1. The sequence name should be same as assembly name (i.e., save hg18 genome sequence as "hg18"). Most of the genomic sequences come split per chromosome. The files need to be concatenated into one file. For example:
```
unzip chromFa.zip
cat chr*.fa > hg18
```
  1. Then, to build them in pygr create a seqdb.SequenceFileDB for all of the genome assemblies:
```
from pygr import seqdb

genomes = {}
# list of filenames of genomic sequences
seqlist = ['hg18', 'panTro2', 'mm8', 'rn4', 'canFam2']

for orgstr in seqlist:
    genomes[orgstr] = seqdb.SequenceFileDB(orgstr)

  # Create the union of these SequenceFileDBs
genomeUnion = seqdb.PrefixUnionDict(genomes)
```
  1. Then, to build the alignment:
```
import os.path
import glob

from pygr import cnestedlist

msaname = 'hg18_pairwise5way'
# pathstem is where the NLMSA will be saved. 
pathstem = os.path.join('/my/path/to/output/', msaname)

# directory where the axt files are saved
axtdir = '/my/path/to/axtfiles'
axt_filelist = glob.glob(os.path.join(axtdir, '*/*.axt')

msa = cnestedlist.NLMSA(pathstem=pathstem, mode='w', seqDict=genomeUnion, axtFiles=axtlist)
```

Depending on your system, it may take several hours to finish. By default, 1GB of memory will be used. The amount of memory to use can be changed by passing arguments as follows:

```
# 500MB Version. It will use less than 750MB Memory at most.
cnestedlist.NLMSA(pathstem=pathstem, mode='w', seqDict=genomeUnion, axtFiles=axtlist, maxlen=536870912, maxint=22369620)
```

If you are planning to save NLMSA into worldbase and never open directly from file, you don't have to give additional options. For example:

```
from pygr import worldbase
msa.__doc__ = "5-way alignment using axt pairwise files"
worldbase.Bio.Alignment.HUMAN.hg18.hg18_pairwise5way = msa
worldbase.save()
```

However, if you are planning to open NLMSA directly from file, the seqDict should be saved into file by explicitly:
```
msa.save_seq_dict()
```

There is an important difference between a MAF NLMSA and a axtNet NLMSA: axtNet NLMSA alignments are always stored with in pairwise mode, while MAF alignments are not. MAF alignments are true multiple alignments. For example, assume we have alignments with hg18 as the reference species. With a NLMSA built from MAF files, if you query using hg18, you can get all alignments of other species (same as axtNet NLMSA). However, if you query using panTro2, you can only get hg18 alignments in axtNet (while with a MAF NLMSA all other hits from all other species could be retrieved).