# Introduction #

The Ensembl database system is a central data repository for various eukaryotic genome sequences and their annotated information [Ensembl Home](http://www.ensembl.org).  The screen shots of schema diagrams for the four basic types of databases (core, compara, variation and funcgen) can be found at: [pygr-dev files](http://groups.google.com/group/pygr-dev/files?hl=en).  They were created using the files in the sql/
directory of the ensembl CVS module. The [table.sql](http://pygr-dev.googlegroups.com/web/table.sql?gda=M3ILbjoAAABJgcRQ_B738LYip0lXSox5BrGVnIRWNUQzXUPZ5KyWuGG1qiJ7UbTIup-M2XPURDTDvhSABxKrnfEc_FGQElaK) file gives the table
definitions and the [foreign\_keys.sql](http://pygr-dev.googlegroups.com/web/foreign_keys.sql?gda=K02TckEAAABJgcRQ_B738LYip0lXSox5BrGVnIRWNUQzXUPZ5KyWuGG1qiJ7UbTIup-M2XPURDRvOefWPvoIMlEIkd9UdRbQLTxVVTd9FLrlvrrz00ZndA) gives the foreign key definitions.  Being able to access its numerous large databases efficiently is indispensable to any genome research project. Currently, the Ensembl databases are mostly accessed through a Perl API or a (less developed) Java API. No equivalent Python API is yet available.

This project [GSoC 2008](http://code.google.com/soc/2008/psf/appinfo.html?csaid=16FD71A42C4B7B) aims to develop a Python API to access the Ensembl databases, using pygr.  Pygr is a Python database interface framework for bioinformatics that
makes it easy to supply a pythonic interface to genome, annotation and
alignment databases such as Ensembl.

By developing a Python Ensembl API, we hope to encourage the use of Python for programming in the field of Bioinfomatics.

# How will pygr make the development easier? #

The key advantages of choosing pygr over many other ORMs (object relational mappers, such as SqlAlchemy) are the followings:

**1.** it provides highly pythonic models for bioinformatics data based on
familiar Python constructs such as the mapping protocol (dictionaries) and sequence protocol;

**2.** these consistent interfaces allow the same client code to work transparently with many different "backend" implementations for how the data is actually stored;

**3.** the client code is insulated from the complexities of back-end database queries;

**4.** pygr works with a wide variety of backend storage systems that provide tremendous scalability for challenging bioinformatics database problems such as terabyte-size multigenome alignments;

**5.** pygr provides strong support for modeling database schemas, and greatly simplifies the problem of accessing and distributing complex database schemas (it transforms them into an "importable" python namespace).

These core capabilities will allow us to focus on problems that are
truly specific to the Ensembl data, rather than general
infrastructure, while delivering a solution that will be much easier
for bioinformatics researchers to use.

# Implementation Details #

Currently, we are in the process of trying pygr to access the dna and exon tables of the ensembl core database and build bi-directional mappings between the genome and the annotation.  For more information, please refer to the following thread http://groups.google.com/group/pygr-dev/browse_thread/thread/5d55fd9d071fbf4d?hl=en.

Stay tuned for further progress reports from us :)

# Approach #

Due to limited time frame, I am going to take on a minimalist approach in the first round, and then progressively add more functionality and features to the basic version.

# Requirements Specification #

Glenn Proctor, the head of the ensembl software team, kindly recommended some
tasks that a minimalist API should allow the user to perform, e.g.

**-** obtain the DNA sequence of a particular genomic region (defined by
chromosome, start, end, strand)

**-** find all the genes in a genomic region, and their transcripts and
translations

**-** retrieve all the genes that are associated with a particular
external reference, e.g. an HGNC symbol or GO term


# Design Decisions #

**Scope**

For now, the primary focus of this API is to provide means to retrieve information from the ensembl core databases.

**Framework**

**1.** the datamodel module (datamodel.py):

**-** a generic datamodel (BaseModel) class (super class).  It is a subclass of the Pygr's sqlgraph.TupleO.

**-** specialized datamodel classes (subclasses of BaseModel).  Each subclass represents a biological entity, or an Ensembl row/item object.

**-** a generic Feature class.  It represents a generic Ensembl feature.  An Ensembl feature refers to an object that has the attributes of seq\_region\_id, seq\_region\_start, seq\_region\_end and seq\_region\_strand.  The get\_sequence() method is implemented using Pygr's seqdb.AnnotationDB.

**-** specialized feature classes (subclasses of Feature).  The schema between features is implemented using Pygr's sqlgraph.SQLGraph.

**2.** the adaptor module (adaptor.py):

**-** a Registry class: provides a connection to the ensembl SQL server

**-** specialized adaptor classes (subclasses of Pygr's sqlgraph.SQLTable class): provides access to a specific sql table in an ensembl core database

**-** private module methods: provide automatic saving of the Ensembl database schema to worldbase

**3.** the featuremapping module (featuremapping.py): provides mapping between ensembl features

**4.** the supporting module (seqregion.py): provides mapping between a sequence slice and the set of Ensembl features in the slice

**Design Pattern**

The Registry class in the adaptor module is implemented as a singleton class, since making a connection to the server is expensive.

# Implemented Functionality #

The latest Ensembl API allows the user to perform the following tasks:

**General methods**

Create a connection to the ensembl MySQL server:

`serverRegistry = get_registry(host='ensembldb.ensembl.org', user='anonymous')`

Create access to an ensembl core database:

`coreDBAdaptor = serverRegistry.get_DBAdaptor('homo_sapiens', 'core', '47_36i')`

Retrieve a sequence object:


`coreDBAdaptor.fetch_slice_by_seqregion(coordSystemName, seqregionName)`

- coordSystemName: 'chromosome' or 'contig'

- seqreionName: a chromosome name, such as '1'
> or a contig name, such as 'AADC01095577.1.1.41877'

- optional arguments for this method: start, end, strand

Create access to any table in an ensembl core database:

e.g.
`transcriptAdaptor = coreDBAdaptor.get_adaptor('transcript')` will return a transcriptAdaptor object that can be used to access any record/item in the transcript table.

Create access to any record in an ensembl sql table:

e.g.
`transcript = transcriptAdaptor[1]` will return a transcript item with the unique dbID 1

Create access to any column of an ensembl sql table record:

e.g.
`transcript.seq_region_start` will return the seq\_region\_start value of the give transcript


**Methods for an ensembl feature object**

An ensembl feature refers to an object that has the attributes of seq\_region\_id, seq\_region\_start, seq\_region\_end and seq\_region\_strand.

Retrieve the sequence of an ensembl feature:

`get_sequence()`

e.g.
`gene.get_sequence()` will return a sequence object of the given gene.

optional argument for this method: the lengh of the flanking region on both sides of the feature sequence:

e.g.
`gene.get_sequence(500)` will return the sequence of the gene plus 500bp flanking regions on both sides of the gene.

Find all the feature objects in a particular slice:

`fetch_all_by_slice(slice)`

e.g.
`transcriptAdaptor.fetch_all_by_slice(slice)` will retrieve all the transcripts in the give slice.

Retrieve the stable\_id, created\_date, modified\_date or the version for a gene/transcript/translation/exon:

e.g.
`gene.get_stable_id()` will return the ensembl stable\_id for the given gene

Obtain a gene object:

`transcript.get_gene()`,
`geneAdaptor.fetch_by_stable_id(geneStableID)`

Obtain transcript objects:

`gene.get_transcripts()`,
`exon.get_all_transcripts()`,
`translation.get_transcript()`,
`transcriptAdaptor.fetch_by_stable_id(transcriptStableID)`

Obtain exon objects:

`transcript.get_all_exons()`,
`exonAdaptor.fetch_by_stable_id(exonStableID)`

Obtain a translation object:

`transcript.get_translation()`,
`translationAdaptor.fetch_by_stable_id(translationStableID)`

Obtain a spliced sequence object:

`transcript.get_spliced_seq()`

Obtain a five-prime untranslated region:

`transcript.get_five_utr()`

Obtain a three-prime untranslated region:

`transcript.get_three_utr()`

Obtain a prediction\_transcript object:

`predictionExon.get_prediction_transcript()`

Obtain prediction\_exon objects:

`predictionTranscript.get_all_prediction_exons()`


Additional sample code can be found under major methods in both the adaptor.py module and the datamodel.py module, in the form of doctests.

# Updates #

**1.** The latest Ensembl API tarball Qing\_Qian.tar.gz can be downloaded from http://code.google.com/p/google-summer-of-code-2008-psf/downloads/list#.
For the prerequisites and installation details, please refer to the README file.  The pygr version that works with this API can be downloaded here [pygr.tar.gz](http://groups.google.com/group/pygr-dev/files?hl=en)

Alternatively, the current ensembl API code, together with Pygr, can be retrieved from the public git repository.  To check out a copy, run the following instruction on the command line:

`git clone git://iorich.caltech.edu/git/public/pygr-jenny <dirname of your choice>`

(More information on Git can be found at [UsingGit](http://code.google.com/p/pygr/wiki/UsingGit))