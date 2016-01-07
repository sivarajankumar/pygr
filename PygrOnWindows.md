# Building Pygr under Windows #

While [the build procedure](BuildingAndTestingPygr.md) itself is the same under Windows as under other systems, the former demands more attention because of the multitude of possible build set-ups - at present, Python extensions can be build in any of the following ways:
  * under Cygwin
  * natively, using Microsoft Visual C++
  * natively, using MinGW

## Cygwin ##

Possibly the best choice for users with Unix background, as the POSIX environment provided by Cygwin is very similar (up to and including familiar shells) to what is offered by Linux/Unix systems - making it unnecessary to deal with the native command-line interface of Windows and all its quirks. The fact the environment is based entirely on Open Source software may be important to some as well. Last but not least, Cygwin comes with a package manager which makes it a breeze to install (almost) all the software needed to build and run Pygr.

The primary (yet hardly major) disadvantage of Cygwin is that it must of course be installed everywhere you want to run Cygwin applications. Moreover, applications built under it do not necessarily work when called "from the outside". This leaves us with only one issue - getting Python-MySQL to work under Cygwin is at present a bit of a bother.


### Details ###

Make sure the following packages are installed, along with whatever they pull in:
  * always: _gcc_, _python_;
  * for Git versions: _python-pyrex_;
  * for SQLite support: _libsqlite3\_0_ (note: this is required even for Python 2.5 and newer - even then it isn't automatically pulled in by the _python_ package), _libsqlite3-devel_ (Python older than 2.5 only).
Follow the standard building procedure. Build the _pysqlite2_ module by hand if you want SQLite support under Python versions older than 2.5.

The problem with MySQL under Cygwin is that there are presently no Cygwin packages of MySQL. Rumour has it it is possible to link Python-MySQL against a native Windows installation of the MySQL client, then again since the procedure involves some serious cross-platform voodoo it is generally easier to build the MySQL client from sources. While doing this, keep the following in mind:
  * make sure you pass _--without-server_ (or similar, different versions used different options) to _configure_ - building the server is not necessary and usually fails anyway;
  * depending on the version of MySQL and/or Cygwin packages, the compiler may complain about missing header files not present anywhere in the Cygwin repository. For example, MySQL-5.1.33 built on an up-to-date Cygwin installation in April 2009 couldn't find _sys/ttydefaults.h_. In many cases this can be worked around by locating such files on any relatively modern Linux box and copying them into the MySQL source tree.


## Microsoft Visual C++ ##

Since all official Python distributions so far have been built using different versions of Visual C++, it is the de-facto standard way - and, for now anyway, the **only** stable way in case of 64-bit builds - of building Python extensions for this operating system. That said, there is an important issue to keep in mind regarding this approach: due to limitations of Visual C++, extensions must be built with **exactly the same** version of the compiler as your Python distribution! In case of official distributions from Python.org, these are:
  * 2.3 - 6
  * 2.4/2.5 - 2003
  * 2.6 - 2008
  * 2.7 - 2008 (i.e. same VS version works for both 2.6 and 2.7)
The fact old versions of Microsoft software may be difficult and/or expensive to obtain aside, this makes it more-or-less impossible to perform builds for different Python version under a single instance of the operating system.

The easiest way of obtaining Visual C++ is to find (download from microsoft.com if it's the latest edition, elsewhere - e.g. on CDs attached to programming books at a library - if not) and install Microsoft Visual Studio Express Edition - it's free and takes up _much_ less disc space than the full-blown edition. Unfortunately the earliest Express-Edition version of Visual Studio was 2005, meaning this option is not viable for any official Python builds older than 2.6. Note that in case of VS 2003 there is an alternative to spending time and money on hunting down a copy - in 2004 Microsoft made available free of charge _Visual C++ Toolkit 2003_, a full version of Visual C++ 2003 optimizing compiler. This will give you no GUI or anything fancy, just the compiler, but it is enough to build Pygr. The Toolkit is no longer available on microsoft.com but can quite easily be found elsewhere on the Web. Once you've got a copy, follow [these instructions](http://www.vrplumber.com/programming/mstoolkit/) to set everything up.

**Note for Visual C++ Express Edition and 64-bit builds**: express editions at least up to and including 2008 only contain the tools for building 32-bit binaries. Fortunately, they can easily (at least in case of command-line use) be made to support 64-bit systems by installing the standalone Windows SDK, available for free [at microsoft.com](http://msdn.microsoft.com/en-us/windows/bb980924.aspx). You'll generally want the latest stable version of the SDK; if in doubt, consult the "Which SDK is right for me?" table provided by Microsoft. Using the on-line installer is recommended, as it saves one from downloading the whole SDK only to install its small part (look for features specifically referring to the x64 architecture, under _Developer Tools_). With that taken care of, Python should correctly invoke the 64-bit compiler.

### Details ###

Building Pygr with Visual C++ should work out of the box as long as all of its dependencies have been met.

At the beginning of Visual Studio installation you may be informed that certain Windows components, namely the IIS and its FrontPage Server extensions, are not installed. Adding these would require having an appropriate Windows installation disc handy, then again they are not required in order to build Pygr so you can safely skip this step using an appropriately-labelled button.

When prompted to choose the components to be installed, one ought to be able to safely uncheck everything except Visual C++. Some pruning of the C++ tree is possible as well but lies beyond the scope of this document.

If installing an older version of Visual Studio, don't bother telling it to look for updates as the final step of installation - it will likely not find them, even if they're still on microsoft.com. Just finish installation, then download and run update installers (_e.g._ Visual Studio 2003 Service Pack 1) by hand. At this point it should be safe to click the Exit button without rolling back the installation.


## MinGW ##

[MinGW](http://www.mingw.org/) along with its companion project [MinGW-w64](http://mingw-w64.sourcefore.net/) port the GNU development chain (gcc, binutils and so on) to Windows and provide it with freely-distributable header files and import libraries. With MinGW one should be able to build native Windows applications the same way one would invoke gcc in a POSIX environment.

There are four advantages of using MinGW to build Python extensions. To begin with, taking this approach allows one to rely entirely on free and Open Source software. Secondly, MinGW is lighter on resources (both disc space and CPU/memory requirements) than the Microsoft development environment. Next, MinGW can be used as a cross-compiler, making it in principle possible to build Windows packages under Linux/Unix. Last but not least, in fact this may be the most important advantage of MinGW, it hasn't got the version-related limitation of Visual C++ - making it possible to use _one_ compiler to build Python extensions for different Python versions.

Unfortunately, at present Pygr's extension libraries built with stable versions of MinGW (5.1.4 and older) **DO NOT RUN CORRECTLY** despite no problems during compilation or linking. We are investigating this problem and will hopefully come up with a solution soon. With that out of the way, the only real disadvantage of using MinGW is that some Python modules, when built from source, get confused if compilers other than MSVC++ are to be used under Windows and/or require a bit of tweaking to get the build process going - especially if external libraries are used.


### Details ###

**1.** After installing MinGW make sure its _bin_ directory is present in your search path: open System Properties from the Control Panel, go to the tab "Advanced" and click "Environment Variables". If "PATH" contains something along the lines of _C:\MinGW\bin_, appropriate for where you installed MinGW on your system, you are okay; otherwise, click "Edit" and add it by hand.

**2.** Oddly enough, Windows packages of Python versions older than 2.5 doen't come with MinGW-compatible import libraries in spite of their distutils being MinGW-aware. Fortunately, it is quite easy to produce such import libraries:
  * download [PExports](http://www.emmestech.com/software/pexports-0.43/pexports-0.43.zip) and extract the executable file somewhere you can run it (the MinGW _bin_ directory is not a bad place, since it's already in the paths and you will likely want to keep pexports.exe around);
  * locate _python2X.dll_, where X is the relevant Python branch number, on your hard drive; it will likely be in the _system32_ subdirectory of your Windows directory;
  * launch the Windows command prompt and run (make sure you've got write access to where the .def file is to be stored)
```
pexports \path\to\python2X.dll > python2X.def
```
to extract symbols from the DLL;
  * create the import library by running
```
dlltool --dllname python2X.dll --def \path\to\python2X.def --output-lib c:\python2X\libs\libpython2X.a
```
making sure your destination directory is correct (it should be the same one as where _python2X.lib_, the Microsoft Visual C++ import library, is. Note that the argument of _--dllname_ should **not** contain the path, even if the DLL is not in your current directory. In case you were wondering, _dlltool_ is bundled with MinGW.

By the way, the same procedure can be used to create import libraries for other packages you may need while building Windows software with MinGW.

**3.** All that remains now is to tell distutils we want to use MinGW. To make it the system-wide default, create or edit the file _C:\Python2X\Lib\distutils\distutils.cfg_ and make it contain the following option:
```
[build]
compiler = mingw32
```
Conversely, you can just specify the command-line option _-c mingw32_ whenever you run _python setup.py build_, _build\_ext_ and the likes. Note that using the command-line option means you must always run _build_ and the likes before you run _install_, as the latter doesn't understand the _-c_ option.

**4.** With everything set up, follow the [standard build procedure](BuildingAndTestingPygr.md) to get Pygr ready. If you want to create an installer package of Pygr instead of having install itself, run the following:
```
python setup.py bdist_wininst
```
to produce an EXE file or, if you use Python 2.6 or newer,
```
python setup.py bdist_msi
```
to produce a Microsoft Installer package.

### Testing on Windows ###

After building Pygr as usual (for example, for Python 2.6):
```
\Python26\python setup.py build
```

you can test by setting the PYTHONPATH to the appropriate build subdirectory, e.g.
```
cd tests
set PYTHONPATH=C:\cygwin\home\Administrator\projects\pygr\build\lib.win32-2.6
\Python26\python runtest.py
```

In some cases this doesn't work for me (I suspect that runtest.py is overriding my PYTHONPATH for some reason).  In that case I force it to build the extension modules in the pygr source directory, and then running the tests that way seems to work.  I first make sure there are no extension module libs leftover from old builds:
```
del pygr\*.pyd
```
Now build and test:
```
\Python27\python setup.py build_ext -i
cd tests
set PYTHONPATH=C:\cygwin\home\Administrator\projects\pygr
\Python27\python runtest.py
```