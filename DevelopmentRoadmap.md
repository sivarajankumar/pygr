# Planned Release Milestones #

## v0.9: NLMSA Joins ##
In a [number of discussions](http://groups.google.com/group/pygr-dev/browse_thread/thread/0d4d02149022e5a6?hl=en), we have already gone into some detail about new possible features for NLMSA.  The main idea is to define general purpose JOIN operations that execute in a high-speed, scalable way, obviating the need for researchers to write their own Python code (slow and possibly buggy) every time they need to find some intersection between two or more datasets.  The result of an NLMSA join will of course just be another NLMSA.  The goal is to make alignment and annotation query a killer app in terms of speed, query capabilities and ease of use.

New features:
  * ID standardization: adopting a convention for keeping IDs for sequence sets consistent across different NLMSAs will greatly speed up JOIN operations
  * JOIN operations implemented in C
  * more "Allen Logic" interval query operators for convenient query
  * Python interfaces for join operations, possibly as a graph query

## v1.0: Worldbase Extensions ##
[worldbase](http://www.doe-mbi.ucla.edu/~leec/newpygrdocs/tutorials/worldbase.html) is a powerful concept for sharing data, but needs additional tools and refinement.  Currently, it is not easy to manage worldbase resource databases, e.g. to copy resource or schema entries from one [metabase](http://www.doe-mbi.ucla.edu/~leec/newpygrdocs/reference/metabase.html) to another, group them, delete them etc.

New features:
  * worldbase makerules: initially this could be implemented as simple construction rules a la SCons for building some type of resource from some types of dependencies.
  * worldbase security via Signed Pickles: Python pickles create potential security vulnerabilities.  One simple and general solution is to create digitally signed pickles using OpenPGP that can be verified with the author's public key.  This would then integrate with standard tools (e.g. GnuPG) for listing sets of people whose content you trust.
  * metabase management tools for viewing, copying, organizing, deleting resource and schema entries between metabases.  These should work transparently with local resource metabases, SQL metabases, and remote XMLRPC metabases (all using authentication).
  * DNS-like framework for servers to share name lookup info with each other

# Past Milestones #

## Pygr 0.7 ##
new features added in the v0.7 release
  * pygr.Data
  * XMLRPC services (NLMSA, BlastDB)
  * in-memory NLMSA
  * many enhancements to NLMSA
  * switched all alignment cases to use NLMSA interface
  * many new features in other areas
  * many bug fixes

In short, an enormous number of different areas of new features were roped together under the "0.7" label.  This had a logical basis, namely that pygr.Data drove a wide-ranging unification of many different things so that they would all work seamlessly with pygr.Data.

## v0.8: Enhancement & Clean-up Release ##
**The 0.8 feature set is done**.  See the documentation for a list of its [new features](http://www.doe-mbi.ucla.edu/~leec/newpygrdocs/whatsnew.html).

V0.7 was very much a "developer release" in that it was a constant stream of new features.  I propose that v0.8 be more a "production release" that is less about new features and more about ensuring that the most used features -- alignment and annotation data -- work really smoothly and easily for a typical Python programmer.  I propose that this release would concentrate on the annotation and testing projects that we already have.  The goal for this release is to define several areas where developers other than myself can easily contribute to Pygr:
  * add new sources of annotation data (e.g. Ensembl)
  * add new sources of alignment data (e.g. programs like CLUSTAL etc.)
  * add new resources to worldbase
  * add web interfaces for searching / browsing contents of a worldbase server


New features:
  * pygr.Data auto-download capabilities (download=True mode) - _done_
  * SQL support for other databases besides MySQL, e.g. sqlite - _done_
  * support for read-write access to SQL databases - _done_
  * simple browsing / searching HTTP interface for worldbase server - _deferred_
  * simple management mechanism for XMLRPC services - _done_
  * XMLRPC annotation services - _done_
  * classes supporting Ensembl annotation (in support of Jenny & Rob's project) - _done_
  * additional UCSC alignment format(s), e.g. supporting hg18/hg17 mapping - _done_

API Clean-up:
  * define an "alignment parser API" that makes it simple to add a parser for an arbitrary alignment format, and have the results automatically loaded into an NLMSA. - _done_
  * ensure that dict-like interfaces in Pygr properly support all the standard Mapping Protocol methods - _done_
  * greatly expanded test suites courtesy of Rachel, Alex and Titus - _done_
  * other clean-up and bug fixes - _done_

For details on current status, search the Issues database for label [Milestone-Release0.8](http://code.google.com/p/pygr/issues/list?can=1&q=label%3AMilestone-Release0.8).