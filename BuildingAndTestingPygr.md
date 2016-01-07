To run the tests, 'cd tests && python runtest.py -B'; omit _-B_ to use in-place code instead of the build directory. runtest will fail out if it cannot import pygr from within the working directory, to avoid running the tests on the installed version.

## Overview ##

Generally speaking, the following steps must be taken to build and install Pygr on your machine:

  1. Install Python
  1. _(for Git sources only)_ Install Pyrex
  1. Install a C compiler and other development files
  1. _(optional)_ Install modules providing MySQL/SQLite support
  1. _(optional)_ Install BLAST tools
  1. Build/install Pygr
  1. Test your build


### Installing Python ###

This should be pretty straightforward. For ready-to-use binaries look to either your system's package repository (Linux, BSD, Fink, Cygwin, ...) or installers provided [at Python.org](http://www.python.org/download/) (Windows, Mac OS X). If all else fails, you can always try building Python from source.

Pygr should work correctly with any version of Python between 2.3 and 2.6, inclusive. Python 3.0 is **not** supported and no conversion has been planned yet, primarily because even its latest version (3.0.1) exhibits [visibly worse I/O performance](http://mail.python.org/pipermail/python-dev/2009-January/085590.html) than the 2.x branch.


### Installing Pyrex ###

Pygr extension code is written in [Pyrex](http://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/) rather than plain C, making it necessary to have Pyrex code translated into C before the compiler can do its job. **Official Pygr packages come with pre-build C files** so if you want to install one of these, you may **skip this step**. Conversely, you will need Pyrex installed to build Pygr using the code from our Git repository.

Pyrex hasn't been officially declared finished yet, which means two things to Pygr users: one is that you'll want the latest available version (as of now, 0.9.8.5) in order to avoid bugs, the other is that unless your system's software repositories contain new-enough Pyrex packages (many do - look for _pyrex_ or _python-pyrex_), you'll need to build the module by hand. Fortunately the latter is very easy:
  * download and unpack the archive;
  * launch a command-line interpreter and enter the newly-created directory;
  * run _python setup.py install_, possibly adding the option _-O_ if you want optimised files to be installed too. You may need to be more specific than saying just _python_ if multiple versions are present and/or the main executable is not in the path. Last but not least, _install_ copies files into sytem-wide Python directories so superuser privileges (or at least write access) might be needed to run it, in particular under Linux/Unix.

In case of Pygr Pyrex is only required at build time, it can safely be removed afterwards.


### The C Compiler etc. ###

Pygr is not a pure-Python module and a C compiler, along with possible assistant tools, must be present at build time for it to finish successfully. You will also need Python's header files. How all these should be obtained depends a lot on the system you use:

  * if you built Python from source, you should already have everything;

  * if under Linux/Unix/Fink/Cygwin/..., Python's header files may be distributed separately from its executables and other run-time files. Look for something similar to _python-devel_ in your package manager; installing it should automatically pull in all dependencies. As for the compiler, you will most likely use GCC - almost certainly available in your system's package repositories, if not already on your hard drive;

  * under Windows, your Python installation should come with all the required header files but things are more complicated when it comes to the compiler. There are two options available here, discussed in more details [here](PygrOnWindows.md):
    * use Microsoft Visual C++ and the official Microsoft Platform SDK; or
    * use [MinGW](http://www.mingw.org/), port of GCC and friends to Windows bundled with freely-distributable standard header files and import libraries.

Like Pyrex, both the compiler and the header files are build-time dependencies only. They can safely be removed afterwards.


### MySQL/SQLite Support ###

The following Python modules must be present in your system in order for Pygr to support accessing MySQL and SQLite databases:

  * SQLite - _sqlite3_ (part of the standard library) for Python 2.5 and newer, _pysqlite2_ ([pysqlite-2.x.y](http://pysqlite.org/)) for older versions;

  * MySQL - _MySQLdb_ (from the [MySQL-python](http://sourceforge.net/projects/mysql-python) package).

Both are fairly common in package repositories, and if all else fails they can be built from the source the same way as Pyrex (then again, note that building mysql-python is more complicated than most Python modules, especially under Windows - see [here](PygrOnWindows.md) for details of the latter case).

Note that Pygr only checks for SQL-related modules at run time - they needn't be present at the time of installation.


### BLAST Support ###

Pygr uses standard command-line BLAST tools to provide BLAST support. To have this work:

  * [Download the tools](http://www.ncbi.nlm.nih.gov/BLAST/download.shtml);

  * Unpack them somewhere;

  * Add the _bin_ subdirectory of wherever you unpacked the tools to to the search path.

Just like with SQL modules, Pygr only looks for BLAST tools at run time.


### Building and Installing Pygr ###

If you want your Pygr installation to be system-wide, the procedure is exactly the same as for Pyrex - obtain the sources, enter the directory and run _python setup.py install_ (possibly with _-Ox_). If however your installation is only to be local, you've got two options:

  * run _python setup.py build_. This will prepare a local directory containing a clean and complete build of Pygr but stop short of copying its contents to a system-wide location; you can then copy these contents by hand to wherever you want them to be and as long as you specify this directory in _sys.path_, Python will be able to find Pygr - and other modules which may be installed in it - there. You will find this build in the system-dependent directory **build/lib._OS_-_ARCH_-_PV_**, _e.g._ _build/lib.linux-x86\_64-2.5_. After you're done, the Pygr sources can safely be deleted;

  * run _python setup.py build\_ext -i_. This will perform a so-called in-place build, _i.e._ build C extensions of Pygr _in the source directory_. This approach is obviously not recommended for long-term use (one needs to keep the sources around, conflicts can arise between different Python versions, _etc._) but facilitates having a quick look at Pygr - in particular, if you launch your Python interpreter or script from the directory containing _setup.py_, in-place Pygr code should be imported automatically _i.e._ without having to set _sys.path_.


### Testing Your Build ###

Source packages of Pygr come with a test suite which allows one to verify that your build runs correctly. To run then, cd to the subdirectory _tests_ and run _python runtest.py -B_ if you ran _build_ or _install_ earlier, or _python runtest.py_ if you created an in-place build.

Note that the test suite will abort if it cannot find appropriate files locally, _i.e._ in either the _build_ subdirectory or in place - even if the very same version of Pygr is already present in Python path. This happens by design to avoid version mismatches between Pygr and the test suite.

Running the tests will display some information pertaining to their progress, followed by a summary. If everything is right, all tests should pass. Depending of what optional components are present in your system you may observe some test suites having been skipped.

For details about testing on Windows, see PygrOnWindows.


### Packaging ###

Instead of installing Pygr into the local Python package tree using _install_ one may opt to create an appropriate **package** and either install the package instead (e.g. to have Pygr under the control of a package manager) or share it with users who for either can't or don't want to build Pygr from source. A wide selection of binary packages of Pygr can be found on our Downloads page; to find out how to create packages of different formats or to learn more about how we build the provided ones, see the PackagingPygr Wiki page.


## Known Issues ##

The setup script fails to invoke Pyrex correctly under Python 2.3/2.4 if setuptools are installed. Specifically, the following condition must be met for this bug to trigger:
  * building Pygr for Python 2.3/2.4;
  * setuptools are installed and get imported correctly;
  * Pyrex-generated .c files are not present _or_ are older than respective .pyx files.
This appears to be a bug in setuptools; we have confirmed it to be present in version 0.6c9 of the package. Note that this problem should not affect users installing packaged releases of Pygr, as these are shipped with pre-built .c files and thus do not invoke Pyrex.