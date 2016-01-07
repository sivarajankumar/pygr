# Introduction #

_Megatests_ is a special class of tests performed on Pygr code, which differ from regular tests in that they require significant amounts of input data, disc space and/or CPU time. As such, they are not run automatically by the test suite.

The aim of most existing megatests is to ensure adequate performance of Pygr under heavy load. Running such tests is particularly important during active development of code, as it allows one to quickly detect any changes negatively impacting performance; on the other hand, they can also be used to benchmark Pygr performance or, indirectly, observe performance-degrading system problems on a certain machine or machines.

The purpose of this page is to provide complete instructions for everyone wishing to run megatests on his/her system - from obtaining the necessary data through actual running of megatests to automatic periodic running and reporting.


# Details #

## Requirements ##

You will need the following to be able to run megatests:

  * A computer system you don't mind placing under heavy load, particularly I/O-wise, on a regular basis. Instructions on this page assume a box running Linux, which so far is the only operating system we have tried running megatests on; Unix(-based) systems should also be supported out of the box, Windows should in principle work but will need either Cygwin or a custom runner script. _Please let us know about the outcome of attempts of running on non-Linux boxes!_

  * A MySQL server (version 5 is recommended), with write access during set-up and read access during running. You'll probably want to use a local, dedicated instance to minimise security implications of the above as well as possible influence of database-access delays on test results;

  * A (relative) lot of disc space. At present megatests take up about 200 GB when idle and up to 600 GB while running;

  * Everything needed by Pygr itself;

  * _(optional)_ A local worldbase XML-RPC server, so that the data-download test is not affected by the quality of your connection to the UCLA one;

  * Sequence data, miscellaneous input and reference output used by megatests; obtaining and installing these will be described below.


## Downloading and preparing data ##

Data files need by Pygr megatests can be divided into three categories: sequence data in Pygr's _seqdb.BlastDB_ format, NLMSA files for different tests, and miscellaneous input/output files. The latter two are installed differently from the former one; both procedures will be described here.

Last but not least, since NLMSA-building megatests are run for both file and SQL storage back-ends it is necessary to import data from the last category above into a MySQL database. For your convenience we have provided MySQL dump-files which can be used for this purpose.

Presently there are two distinct classes of megatests, differing in what the primary genome used by each class is and therefore named after the genome in question: _dm2_ (_Drosophila melanogaster_, or common fruit fly) and _hg18_ (_Homo sapiens_, or human). Each class uses its own set of input and output data; it is recommended to keep them in separate directories.


### SequenceFileDB sequence files ###

The easiest way of obtaining SequenceFileDB sequence-data files is to fetch them using Pygr itself, from the UCLA XML-RPC server - that way downloaded files will automatically become registered into the local Pygr resource database. Information on how to do this can be found on the PygrResourceDownloader page; for your convenience, the lists below provide data-set names in the format understood by Pygr.

The following sequences must be obtained:

  1. For _dm2_ megatests
    * Bio.Seq.Genome.ANOGA.anoGam1
    * Bio.Seq.Genome.APIME.apiMel2
    * Bio.Seq.Genome.DROAN.droAna3
    * Bio.Seq.Genome.DROER.droEre2
    * Bio.Seq.Genome.DROGR.droGri2
    * Bio.Seq.Genome.DROME.dm2
    * Bio.Seq.Genome.DROMO.droMoj3
    * Bio.Seq.Genome.DROPE.droPer1
    * Bio.Seq.Genome.DROPS.dp4
    * Bio.Seq.Genome.DROSE.droSec1
    * Bio.Seq.Genome.DROSI.droSim1
    * Bio.Seq.Genome.DROVI.droVir3
    * Bio.Seq.Genome.DROWI.droWil1
    * Bio.Seq.Genome.DROYA.droYak2
    * Bio.Seq.Genome.TRICA.triCas2
  1. For _hg18_ megatests
    * Bio.Seq.Genome.ANOCA.anoCar1
    * Bio.Seq.Genome.BOVIN.bosTau3
    * Bio.Seq.Genome.CANFA.canFam2
    * Bio.Seq.Genome.CAVPO.cavPor2
    * Bio.Seq.Genome.CHICK.galGal3
    * Bio.Seq.Genome.DANRE.danRer4
    * Bio.Seq.Genome.DASNO.dasNov1
    * Bio.Seq.Genome.ECHTE.echTel1
    * Bio.Seq.Genome.ERIEU.eriEur1
    * Bio.Seq.Genome.FELCA.felCat3
    * Bio.Seq.Genome.FUGRU.fr2
    * Bio.Seq.Genome.GASAC.gasAcu1
    * Bio.Seq.Genome.HORSE.equCab1
    * Bio.Seq.Genome.HUMAN.hg18
    * Bio.Seq.Genome.LOXAF.loxAfr1
    * Bio.Seq.Genome.MACMU.rheMac2
    * Bio.Seq.Genome.MONDO.monDom4
    * Bio.Seq.Genome.MOUSE.mm8
    * Bio.Seq.Genome.ORNAN.ornAna1
    * Bio.Seq.Genome.ORYLA.oryLat1
    * Bio.Seq.Genome.OTOGA.otoGar1
    * Bio.Seq.Genome.PANTR.panTro2
    * Bio.Seq.Genome.RABIT.oryCun1
    * Bio.Seq.Genome.RAT.rn4
    * Bio.Seq.Genome.SORAR.sorAra1
    * Bio.Seq.Genome.TETNG.tetNig1
    * Bio.Seq.Genome.TUPGB.tupBel1
    * Bio.Seq.Genome.XENTR.xenTro2
  1. For the _restartIterator_ megatest (note significant overlap with _dm2_ megatests; also see the comment in the next section)
    * Bio.Seq.Genome.ANOGA.anoGam1
    * Bio.Seq.Genome.APIME.apiMel3
    * Bio.Seq.Genome.DROAN.droAna3
    * Bio.Seq.Genome.DROER.droEre2
    * Bio.Seq.Genome.DROGR.droGri2
    * Bio.Seq.Genome.DROME.dm3
    * Bio.Seq.Genome.DROMO.droMoj3
    * Bio.Seq.Genome.DROPE.droPer1
    * Bio.Seq.Genome.DROPS.dp4
    * Bio.Seq.Genome.DROSE.droSec1
    * Bio.Seq.Genome.DROSI.droSim1
    * Bio.Seq.Genome.DROVI.droVir3
    * Bio.Seq.Genome.DROWI.droWil1
    * Bio.Seq.Genome.DROYA.droYak2
    * Bio.Seq.Genome.TRICA.triCas2

Once the files have been downloaded they require no further attention.


### NLMSA and other files ###

Pygr megatests can be divided into two classes depending on whether they require NLMSA to be pre-built in a controlled environment or not. The first class consists of all _dm2_ and _hg18_ megatests, the second - of the _restartIterator_ megatest.

#### If pre-built NLMSA are required ####

The necessary files are available (as tar archives) on the Web, at http://biodb.bioinformatics.ucla.edu/MEGATEST/ . Download the archives and unpack them into directories of your choice. You need the following files:

  1. NLMSA for _dm2_ megatests
    * maf\_data.tar
    * maf\_test.tar
  1. NLMSA for _hg18_ megatests
    * axt\_data3.tar
    * maf\_data3.tar
    * maf\_test3.tar
  1. Miscellaneous files, needed by both classes
    * input\_and\_results.tar

This time some post-installation steps are necessary before the data can be used: the files _dm2\_multiz15way.seqDictP_ (from maf\_test.tar) and _hg18\_multiz28way.seqDictP_ (from maf\_test3.tar) contain hardcoded paths which will need to be changed to reflect your directory structure. Assuming the final path components are to stay the same (i.e. you keep the data in the directories in which they came in the archives), simply open the files in question using an ordinary text editor and replace all the occurrences of _result/pygr\_data_ and _/result/pygr\_megatest_ with the path(s) of your choice.


#### If pre-built NLMSA are not required ####

Simply download the _Bio.MSA.UCSC.dm3\_multiz15way_ alignment using Pygr, the same way you have downloaded all the sequence files. This has the added benefit of Pygr being able to resolve sequence dependencies of the alignment - in other words, should any required sequences be missing from the local resource database they shall be downloaded automatically.


#### The download test ####

Since version 0.8.1 Pygr uses a new version of the download megatest which uses a local HTTP server to provide the desired file, thus reducing the test's dependence on a fast and stable network connection. Of course that means you will have to download the necessary file, i.e. a text dump of an NLMSA, first... We recommend http://biodb.bioinformatics.ucla.edu/PYGRDATA/dm2_multiz9way.txt.gz - it's the same file as what the older versions of this test used, it's large but not too large and building it can take advantage of sequence data required by other megatests.


### MySQL data ###

You can find gzip-compressed MySQL dump files (produced with version 5) at http://biodb.bioinformatics.ucla.edu/MEGATEST/. Simply create a new database on your server, download all the _.sql.gz_ files and import them into the said database using e.g. the standard MySQL client (_mysql_).


## Configuration ##

### MySQL access ###

Megatests assume the database they use is located on the default MySQL server and accessed using default user name/password. If your system-wide defaults do not match the desired values of these parameters, you'll need to override them - using a standard MySQL option file. Under Linux/Unix you will most likely use the per-user option file _$HOME/.my.cnf_ file in your home directory

have it contain something like this:
```
[client]
port=3306
host=your_database_server
user=your_account
password=your_password
```

For more information on the subject of MySQL option files, see http://dev.mysql.com/doc/refman/5.1/en/option-files.html.


### The config file ###

Database access aside, configuration of Pygr megatests is performed entirely by setting appropriate keywords in appropriate files. At present, megatests and the associated tools search for their configuration the following files:

  1. _.pygrrc_ in the user's home directory;
  1. _pygr.cfg_ in the user's home directory;
  1. _.pygrrc_ in the current directory;
  1. _pygr.cfg_ in the current directory.

All of the keywords listed below can be found in any of these files. They are read in the order listed here, overriding old values with new ones should a keyword appear in more than one.

The config files follow standard syntax understood by Python's [ConfigParser module](http://docs.python.org/library/configparser.html), i.e. very similar to that of Windows INI files. Among other things this means keywords in a file are divided into sections. Megatests use keywords from four sections: _megatests_ for general configuration, _megatests\_dm2_ and _megatests\_hg18_ for settings pertaining to specific input data sets and _megatests\_download_ for downloader-specific options.


#### The download test ####

The version of the download megatest made available since Pygr 0.8.1 requires one to specify where the test's built-in HTTP server is to find the NLMSA file to serve for downloading. This can be done by setting the _httpdServedFile_ keyword in _megatest\_download_ to the path and name of that file. One can also optionally specify _httpdPort_ to override the default TCP port (28145) to be occupied by the built-in HTTP server.

**Note: the download megatest in 0.8.1 has a bug in parsing _httpdPort_ which prevents the test from running.** To work around that problem, set _httpdPort_ in the config file and change line 38 of _tests/downloadNLMSA\_megatest.py_ from

server\_addr = ('127.0.0.1', httpdPort)

to

server\_addr = ('127.0.0.1', int(httpdPort))


#### Choosing the variant ####

Both data sets used by megatests are quite large, making running tests over them in their entirely quite time consuming - for example, on a machine with a 2.8 GHz dual-core Opteron CPU and a SATA-2 RAID disc a single such run takes approximately 30 hours! Therefore, it may be desirable to run megatests only on subsets of the two data sets. In order to do this, specify appropriate subsets using the _smallSampleKey_ keyword in data set-specific sections. For example, to only use _chrYh_ in the _annotation\_dm2_ megatest, _chr4h_ in _nlmsa\_dm2_ and _chrY_ in _hg18_-based ones, specify:

```
[megatests_dm2]
smallSampleKey = chrYh
smallSampleKey_nlmsa = chr4h

[megatests_hg18]
smallSampleKey = chrY
```

On the aforementioned machine this reduces the running time of megatests to approximately 12 minutes per run.

In principle, any valid subsets could be used to have "quick" megatests. Then again, we only provide reference output files for the configuration shown above.


#### Location of input ####

Use the following keys to specify directories containing input data:

  1. In the _megatests_ section:
    * _testInputDB_ - name of the database on the server specified above containing data imported from our dump files;
    * _testInputDir_ - directory containing files from _input\_and\_results.tar_.
  1. In the _megatests\_SET_ sections:
    * _axtDir_ - directory containing files from _axt\_data_ archives (**hg18 only**);
    * _mafDir_ - directory containing files from _maf\_data_ archives;
    * _msaDir_ - directory containing files from _maf\_test_ archives;
    * _seqDir_ - directory containing BlastDB files downloaded using Pygr.

By definition, all of these keywords must be set for megatests to run.


#### Location of output ####

All files produced in the course of running megatests will be written in randomly-generated subdirectories of the directory pointed to by the _testOutputBaseDir_ keyword in the _megatests_ section; this keyword must be set for megatests to run. You will of course need write access there, along with enough free space. Note that all the files produced there are temporary and can safely be deleted after the end of a test run, if they are not deleted automatically (which they should).

In addition, log files from all stages of a run are written to the directory pointed to by the _logDir_ keywords in the _megatests_ section. These are not deleted automatically.


#### Timing ####

While running megatests on changing code it is helpful to keep an eye on how much time their execution takes. Out runner script (see below) makes it possible to automate this process by setting two keywords in the _megatests_ section:

  * _expectedRunningTime_ - how long the tests are expected to run, in minutes. Setting this to a negative value (default) disables this test;
  * _runningTimeAllowedDelay_ - allows one to specify the number of minutes or percentage of expected running time by which the latter can be exceeded without reporting the run as too long. The default value is 0, i.e. report every time expected time is exceeded.


#### Reporting ####

If you use our scripts (see below) for running megatests, each run should end with an e-mail being sent notifying its recipients of the outcome. The scripts attempt to determine the outcome of the test run and select appropriate recipients.

Presently, a test run is considered to have failed if one or more of the following statements are true at its end:

  * abnormal termination occurred in any of the phases of running;
  * any of the tests failed;
  * _(optional)_ running the tests took more than it should (see above).

The following keywords, all in the _megatests_ section, are used to control the reporting process:

  * _mailFrom_ - e-mail address to appear in the From: header of messages. Required if reports are to be sent;
  * _mailServer_ - name or IP address of the SMTP server to use to send the message. Leave unset to use the local (system or user) default, if available;
  * _mailTo\_failed_ - a comma-separated list of e-mail addresses to which a message will be sent if the tests failed. Leave unset to disable such reporting;
  * _mailTo\_ok_ - a comma-separated list of e-mail addresses to which a message will be sent if the tests succeeded. Leave unset to disable such reporting.


## Scripts ##

The directory _tests/tools_ in the Pygr source tree contains two scripts which can be used to facilitate the running of megatests:

  * **run\_megatests** - a Bourne-shell script, used to run the tests;
  * **send\_megatest\_email.py** - a Python script used by the former to mail test reports.

**run\_megatests** downloads Pygr sources using Git, builds Pygr and runs both standard tests and megatests, storing the output. At the end an e-mail is sent using **send\_megatest\_email.py** from downloaded sources, after which everything except output logs is deleted. The script has been designed for running via cron - if $HOME is not set, as it is often the case for cron jobs, it looks for MySQL and Pygr configuration files in a directory of user's choice.

**Note**: at present the script doesn't use the Pygr configuration file, as it is not trivial to parse such files in shell scripts. You'll need to specify appropriate settings in the file itself, near the beginning.