**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


One can easily download pre-built worldbase resources into your localdisk. Be sure to give writable path before XMLRPC server ('.' in WORLDBASEPATH).

```
  import os
  os.environ['WORLDBASEPATH'] = '.,http://biodb2.bioinformatics.ucla.edu:5000'
  from pygr import worldbase

  worldbase.dir('') # RETURNS ALL XMLRPC RESOURCES
  worldbase.dir('', download=True) # RETURNS ALL DOWNLOADABLE RESOURCES
```

For seqdb.BlastDB, you have to setup WORLDBASEDOWNLOAD path.

```
  os.environ['WORLDBASEDOWNLOAD'] = '/my/seqdb/path'

  hg18 = worldbase.Bio.Seq.Genome.HUMAN.hg18(download=True)
```

Above line will initiate downloading and saving hg18 into your WORLDBASEDOWNLOAD path.

For NLMSA, you have to setup WORLDBASEBUILDDIR path..

```
  os.environ['WORLDBASEBUILDDIR'] = '/my/nlmsa/path'

  hg18_multiz28way = worldbase.Bio.MSA.UCSC.hg18_multiz28way(download=True)
```

Above line will initiate downloading and saving hg18\_multiz28way into your WORLDBASEBUILDDIR path.

If you don't have huge disk space, don't forget to delete intermediate compressed files and text files.

Of course, if you delete download=True option, it will access biodb2 XMLRPC resources.

```
  hg18 = worldbase.Bio.Seq.Genome.HUMAN.hg18()
  hg18_multiz28way = worldbase.Bio.MSA.UCSC.hg18_multiz28way()
```