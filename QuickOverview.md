# Introduction #

Pygr is an open source software project used to develop graph database interfaces for the popular Python language, with a strong emphasis on bioinformatics applications ranging from genome-wide analysis of alternative splicing patterns, to comparative genomics queries of multi-genome alignment data.

# Documentation #

Please see our PygrDocumentation page for tutorials, module documentation, recipes, and forum.  Within the source code repository, you can build the documentation via `cd doc;make`, then point your browser at the file **doc/html/pygr/index.html**. You can also check out [the older documentation page](http://bioinfo.mbi.ucla.edu/pygr/docs/).

# Prerequisites #

  * Python >= 2.2: Pygr uses Python generators.
  * C compiler: Pygr includes several C extension modules (pygr.cnestedlist, pygr.cdict, pygr.seqfmt), coded in C for high performance.  To install Pygr from source code, you need a C compiler.  (If you don't have a C compiler, you may be able to find a binary installer for Pygr on your platform on this site).  Pygr uses the Python distutils module to build its extension modules, so any C compiler that distutils knows how to find and use is fine.

  * Pyrex: You do not need this if you are installing one of our source code releases, because these include the C source code compiled by Pyrex. However, if you are compiling from the git repository, you will need [Pyrex](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/), because (currently) the git repository does not include the Pyrex-compiled C files.

## Optional, Recommended ##
While pygr's core functionality only requires a sane python environment, some specific features require additional software:

  * MySQL support: allows Pygr to access MySQL databases using its pygr.sqlgraph module.  Also needed for worldbase module support for storage of worldbase resource databases in MySQL.  Requirements: **MySQL-python (MySQLdb module) >= 1.2.0; works with any server MySQL >= 3.23.x**

  * NCBI tools: used by the pygr.seqdb.BlastDB class to provide convenient blast/megablast search.  Requirements: **formatdb, blastall, megablast**, any recent version which you can [download from NCBI](http://www.ncbi.nlm.nih.gov/IEB/ToolBox/index.cgi); executables must be in your $PATH.

# Supported Platforms #

In theory, pygr should work on any platform that adequately supports python.  Here are the OS's we've successfully tested on:

  * Linux 2.2.x/2.4.x
  * Mac OS X
  * OpenBSD
  * Windows XP, Vista: please see our page on PygrOnWindows.

# Installation #

Installing pygr is quite simple.

```
cd pygr
python setup.py install 
```

Once the test framework has completed successfully, the setup script will install pygr into python's respective site-packages directory.  If you don't want to install pygr into your system-wide site-packages, replace the `python setup.py install` command with
`python setup.py build`.  This will build pygr but not install it in site-packages.

# Using Pygr #
Pygr contains several modules imported as follows:
```
from pygr import seqdb
```

If you did not install pygr in your system-wide site-packages, you must set your PYTHONPATH to the location of your pygr build. For example, if your top-level pygr source directory is $PYGRDIR then you'd type something like:
```
setenv PYTHONPATH $PYGRDIR/build/lib.linux-i686-2.3
```
where the last directory name depends on your specific architecture.

Pygr has a myriad of applications, however, providing a comprehensive description of its utility is out of the scope of this document (see PygrDocumentation).