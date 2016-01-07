### General development ###

Starts with: new-version Git branch merged with the master, if one existed

Allowed commits to Git master: all

Ends with: an arbitrary decision of the team, preferably with no **FixedNeedsReview** enhancement requests in the tracker


### Feature freeze ###

Starts with: tagging the Git master with an "alpha" tag

Allowed commits in Git master: all but implementation of new features

Ends with: no conflicts between documentation and current state of code, no open tracker issues pertaining to this version

Note: parallel development of new features for future versions is allowed, as long as no such changes are committed to the Git master.


### Beta-testing ###

Starts with: tagging the Git master with a "beta" tag (with appropriate number), creation of a "beta" package of Pygr (tarball at the least, other formats as wanted/needed). If the UCLA XML-RPC server is based on Git code and not the last release, it should be switched to the new beta code at this point as well.

Allowed commits in Git master: bug fixes and documentation updates only

Ends with: current state of code fully covered by documentation; no open tracker issues pertaining to this version for at least X days **or** no open tracker issues pertaining to this version + an arbitrary decision of the team

Note: new "beta" packages and Git-master tags should be introduced every time an issue filed after the previous one is fixed, but no more frequently than every Y days.


### Release ###

Starts with: updating the version number in pygr/init.py and doc/rest/conf.py, adding a new version entry to misc/debian/changelog; tagging the Git master with a "release" tag

Allowed commits in Git master: none

Ends with: packages (all agreed-upon formats) created and published on the Web site, UCLA XML-RPC server updated to use current release code.

Also:

pygr.org documentation updated so that latest-release pointer is correct (see make.sh on http://github.com/ctb/www-pygr.org)