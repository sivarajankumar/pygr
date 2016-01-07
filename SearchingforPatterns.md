# Introduction #

This straightforward script is a continuation of the article GenomeCalculationsUsingpygr (for the full code, see article). By quantifying the trinucleotide repeats found in the E. coli genome, as well as the number of repeats per gene, the underlying organizational structure of the genome sequence can be further studied.

**WARNING**: This is a code-example Wiki page and as such _may_ be out of sync with current versions of Pygr. It will be removed or refactored once our doctest infrastructure has been deployed.


# A Rundown of the Code #

First, the number of nucleotide bases per gene is counted and stored in the dictionary ec\_count. The gene sequences from the annotation db had to be converted to a string before they could be iterated through. The final count was assigned to the dictionary ecoli\_nuc\_count, which now holds both the genes and the number of bases per gene. For example, the gene'1869' will have this value: '1869': {'A': 512, 'C': 478, 'W': 0, 'G': 492, 'T': 452}.

```
ecoli_nuc_count = {}
for gene, annot in annot_db.iteritems():
    ec_count = dict(A=0, C=0, T=0, G=0, W=0)
    genes = str(annot.sequence)
    for nuc in genes:
            ec_count[nuc] = ec_count[nuc] + 1
    ecoli_nuc_count[gene] = ec_count
```

In order to search for each potential codon, the combinations of A,T,G, and C must be defined; however, by using xselections, I was able to simple specify the nucleotides and the length of each resulting string, and thus all 64 possible codons were identified. The E. coli genome sequence is turned into a string, and the occurrences of each codon within is counted and stored in the nucsum dictionary. Finally, the results are printed for the user to examine or record.

```
def xselections(items, n):
    if n==0: yield []
    else:
        for i in xrange(len(items)):
            for ss in xselections(items, n-1):
                yield [items[i]]+ss

nucsum = {}
for uc in xselections(['G','A','T','C'],3):
    triplet = "".join(uc)
    nucs = str(ecgenome)
    nuccount = nucs.count("".join(uc))
    nucsum[triplet] = nuccount
    print('The number of %s trinucleotide repeats\
 in the E. coli genome is %f' % (triplet, nuccount))
```

This segment is essentially the same as the preceding segment, except a structure is built to hold the values from the loop. The nucleotide triplets are defined, then each gene is searching for their presence. Once again, the results are printed.

```
genesum = {}
for gene, annot in annot_db.iteritems():
    nuc_in_gene = str(annot.sequence)
    triplet_count = {}
    for ge in xselections(['G','A','T','C'],3):
        triplet = "".join(ge)
        genecount = nuc_in_gene.count("".join(ge))
        triplet_count[triplet] = genecount
    genesum[gene] = triplet_count
    print('The number of %s trinucleotide repeats in E. coli gene %s is %d' % (triplet, gene, genesum[gene][triplet], ))
```

# Potential Future Uses #

By demonstrating simple ways to manipulate the data stored in the various containers available in pygr, more sophisticated uses for the data can be developed. For example, multiple human diseases, including Huntington's, Kennedy disease, or Fragile X syndrome, are caused by trinucleotide repeat expansion disorders. If a "normal" genome or gene is compared with a potentially mutated or diseased one, the counts of the various codons could show an excess of a particular codon, an altered reading frame (which would potentially change the number of each codon for the entire gene), or multiple other mutations.

# Note #

xselections is from the recipe "Generator for permutations, combinations, selections of a sequence " by Ulrich Hoffmann, found here: http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/190465 .