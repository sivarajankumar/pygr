# Introduction #

This is work in progress.


# Details #

Packages - generally binary, also source. Many available formats, most but not all supported directly by the setup script (usually with both distutils and setuptools, then again the latter add some metadata to resulting packages).

Source packages: 'setup.py sdist'. Uses information from MANIFEST.in to build a tarball containing Pygr sources. NOTE: At the moment sdist doesn't automatically invoke generating C code from Pyrex files (which our source-package policy includes), make sure you do that beforehand or the resulting package will depend on Pyrex! The resulting file by is a gzipped tarball under a POSIX system or a ZIP archive under Windows, can be changed using command-line options.

"Dumb" binary packages: 'setup.py bdist' or 'setup.py bdist\_dumb'. Just archives (see above for default formats) containing Pygr files contained in site-packages of appropriate Python. Typically include the path of local Python installation (e.g. /usr/local/lib/python2.5), which limits portability (unless one copies files to the right location by hand).

Python Eggs: 'setup.py bdist\_egg' with setuptools installed. Easy to manage and portable but installing these requires either easy\_install or the whole setuptools. In practice - a ZIP with defined internal directory structure.

Two formats of Windows packages:
  * 'setup.py bdist\_msi' (Windows Installer packages)
  * 'setup.py bdist\_wininst' (same but self-executable)
Functionally the two are identical. Using MSI packages is recommended, especially under 64-bit Windows or Vista/Windows 7 (due to the way the self-executable bit is designed, it produces a lot of overhead on such systems) - unfortunately building them with vanilla distutils only works with Python-2.6 and newer.

Linux RPM packages: 'setup.py bdist\_rpm', on a system containing the program 'rpmbuild' (on RPM-based distributions, usually in the 'rpm-build' package). One snag for more complicated set-up - the .spec file produced by distutils/setuptools refers to Python as 'python' rather than pointing to the Python executable used by setup.py. This makes auto-building for multiple Python versions impossible (one can work around this by stopping after generating the .spec file, editing it and running rpmbuild by hand). That said, most users shouldn't be bothered by this issue.


**Packages etc. not supported by setup.py**

Linux DEB packages: all files are in misc/debian/. Move/copy/symlink that directory out of misc (i.e. to where setup.py is), make sure the 'dpkg-buildpackage' program is available (under Debian/Ubuntu it is in the package 'dpkg-dev') and run 'dpkg-buildpackage -b -uc -us' ('-b' for building only the binary package, '-uc -us' disable cryptographic signing of the package which would require extra setting-up effort). If everything goes well, the resulting .deb file will be in the parent directory (**not** in dist!)

Portage (Gentoo): there are two ebuilds under misc/portage, one for building official releases (while copying that file, replace VER with the desired version number), one from pulling sources from Git. Create a local Portage overlay if you haven't got one yet, copy the ebuild(s) into it and run 'emerge pygr'. At the moment the only keywords in the files are ~amd64 and ~x86 but the ebuilds should work on any Portage system with working Python, including FreeBSD. Check the ebuilds' USE flags for customisation options.

Fink: Pygr is in the official Fink repository so all you have to do is run 'fink install pygr-pyXX' (where XX is 25 or 26 - in other words, the Python branch you want to use Pygr with).


**Miscellaneous**

Side note regarding Windows: as long as we can't build Pygr using MinGW we are more-or-less forced to have multiple Win build boxes - having several versions of Visual C++ coexist on one system is tricky at best. On the other hand, once MinGW is supported we could not only build for different Python versions with the same compiler but actually use a Linux/Unix box to build Win32 (Win-AMD64 unclear, depending on status of 64-bit MinGW) packages!

Under Mac OS X, a naming conflict exists between binary packages (both dumb ones and Python eggs) created using Python from Fink and those using Apple-shipped Python; it's up to you to rename some of these files to avoid this conflict.

OS X again: under 10.5/10.6, setup executed by Apple-shipped Python builds dual-arch extension libraries (i.e. x86 and PPC); don't get deceived by the name of the resulting package in dist. This behaviour can be altered by passing appropriate CFLAGS/LDFLAGS. On the other hand, under 10.4 extensions are always built for the local architecture (apparently 10.4 doesn't support building universal binaries).


# Building official Pygr packages #

This is how official Pygr packages are built.

**sources**
  * build system: Linux/x86, Fedora Core 6, Python 2.5 built from source
  * Pyrex version: 0.9.8.5
  * setup.py targets: _sdist_

**Mac OS X 10.6, Apple-shipped Python 2.6**
  * architecture: x86 **or** PPC (packages are dual-architecture)
  * compiler: default
  * setup.py targets: _bdist\_egg_, _bdist\_dumb_
  * note: produced packages must be renamed to match our convention (see the Downloads page)

**Mac OS X 10.5/10.6, Apple-shipped Python 2.5**
  * architecture: x86 **or** PPC (packages are dual-architecture)
  * compiler: default
  * setup.py targets: _bdist\_egg_, _bdist\_dumb_
  * note: produced packages must be renamed to match our convention (see the Downloads page)

**Mac OS X 10.3/10.4, Apple-shipped Python 2.3**
  * architectures: x86, PPC
  * compiler: default
  * setup.py targets: _bdist\_egg_, _bdist\_dumb_
  * note: produced packages must be renamed to match our convention (see the Downloads page)

**Microsoft Windows XP, Python 2.6**
  * architectures: x86, amd64
  * compiler: Visual Studio 2008 (Express)
  * setup.py targets: _bdist\_egg_, _bdist\_msi_

**Microsoft Windows XP, Python 2.5**
  * architecture: x86
  * compiler: Visual Studio 2003
  * setup.py targets: _bdist\_egg_, _bdist\_wininst_

**Cygwin (the latest available version)**
  * setup.py targets: _bdist\_egg_

**Linux**
  * architectures: x86, amd64
  * build systems: Ubuntu 10.04 (x86), Fedora Core 6 (amd64); all Python versions built from source
  * Python versions: 2.4, 2.5, 2.6
  * setup.py targets: _bdist\_egg_, _bdist\_dumb_

**documentation**
  * output formats: HTML, PDF
  * Sphinx version: 0.6.4
  * Epydoc version: 2.1