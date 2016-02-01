# -*- coding: utf-8 -*-
"""
YOUR HEADER COMMENT HERE

@author: YOUR NAME HERE

"""

import random
from amino_acids import aa, codons, aa_table   # you may find these useful
from load import load_seq


def shuffle_string(s):
    """Shuffles the characters in the input string
        NOTE: this is a helper function, you do not
        have to modify this in any way """
    return ''.join(random.sample(s, len(s)))

# YOU WILL START YOUR IMPLEMENTATION FROM HERE DOWN ###


def get_complement(nucleotide):
    """ Returns the complementary nucleotide

        nucleotide: a nucleotide (A, C, G, or T) represented as a string
        returns: the complementary nucleotide
    >>> get_complement('A')
    'T'
    >>> get_complement('C')
    'G'
    >>> get_complement('T')
    'A'
    >>> get_complement('G')
    'C'
    """
    # TODO: implement this
    if nucleotide == 'A':
        return 'T'
    elif nucleotide == 'T':
        return 'A'
    elif nucleotide == 'C':
        return 'G'
    else:
        return 'C'


def get_reverse_complement(dna):
    """ Computes the reverse complementary sequence of DNA for the specfied DNA
        sequence

        dna: a DNA sequence represented as a string
        returns: the reverse complementary DNA sequence represented as a string
    >>> get_reverse_complement("ATGCCCGCTTT")
    'AAAGCGGGCAT'
    >>> get_reverse_complement("CCGCGTTCA")
    'TGAACGCGG'
    >>> get_reverse_complement("ATCG")
    'CGAT'
    """
    # TODO: implement this
    reversed_dna = dna[::-1]
    result = '' #a string that will be appended with complements to be returned
    for letter in reversed_dna:
        result = result + get_complement(letter)
    return result


def divide_to_trips(dna):
    """Takes a DNA sequence and outputs a list of string triplets(codons) that makes up the sequence
       Last element might be incomplete codon with less then three letters
    >>> divide_to_trips("ATGTGAA")
    ['ATG', 'TGA', 'A']
    >>> divide_to_trips("ATGTGA")
    ['ATG', 'TGA']
    >>> divide_to_trips("ATGTGAAA")
    ['ATG', 'TGA', 'AA']
    """
    index = 0
    result = [] #list to be appended with codons
    while index< len(dna):
        result.append(dna[index:index+3])
        index += 3
    return result

def rest_of_ORF(dna):
    """ Takes a DNA sequence that is assumed to begin with a start
        codon and returns the sequence up to but not including the
        first in frame stop codon.  If there is no in frame stop codon,
        returns the whole string.

        dna: a DNA sequence
        returns: the open reading frame represented as a string
    >>> rest_of_ORF("ATGTGAA")
    'ATG'
    >>> rest_of_ORF("ATGAGATAGG")
    'ATGAGA'
    >>> rest_of_ORF("ATG")
    'ATG'
    >>> rest_of_ORF("AT")
    'AT'
    >>> rest_of_ORF("ATGASDASDWASDWADASDSAD")
    'ATGASDASDWASDWADASDSAD'
    >>> rest_of_ORF("ATGTGTTAAATGAAAAAATAGAA")
    'ATGTGT'
    """
    # TODO: implement this
    stop_codons = ['TAG', 'TAA', 'TGA']
    
    trips = divide_to_trips(dna) #lists of codons that the dna is made up of    

    result = "" #Empty string to be concatenated with codon sequence to be returned
    index = 0
    while index + 1 < len(trips):
        if trips[index+1] not in stop_codons: #If next codon is not one of stop codons, add the codon to result string and keep iterating
            result += trips[index]
            index += 1
        else:
            result += trips[index]
            return result #Add this codon before stop codon and return the resulting string
    return dna #If dna is shorter than 3 letters, it will just return dna itself.

def find_all_ORFs_oneframe(dna):
    """ Finds all non-nested open reading frames in the given DNA
        sequence and returns them as a list.  This function should
        only find ORFs that are in the default frame of the sequence
        (i.e. they start on indices that are multiples of 3).
        By non-nested we mean that if an ORF occurs entirely within
        another ORF, it should not be included in the returned list of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_oneframe("ATGCATGAATGTAGATAGATGTGCCC")
    ['ATGCATGAATGTAGA', 'ATGTGCCC']
    >>> find_all_ORFs_oneframe("ATGTGAA")
    ['ATG']
    >>> find_all_ORFs_oneframe('ASDASDAWSDSD')
    []
    >>> find_all_ORFs_oneframe('TATATGCATGAATGTAGATAGATGTGCTAAATAATAATGTTTTAAATT')
    ['ATGCATGAATGTAGA', 'ATGTGC', 'ATGTTT']
    """
    # TODO: implement this
    index = 0
    orf_list = [] #list of orfs that will be returned at the end
    while index < len(dna):
        if dna[index:index+3] == 'ATG':
            orf = rest_of_ORF(dna[index:]) #orf to be appended
            orf_list.append(orf)
            index += len(orf)
        else:
            index += 3
    return orf_list

def find_all_ORFs(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence in
        all 3 possible frames and returns them as a list.  By non-nested we
        mean that if an ORF occurs entirely within another ORF and they are
        both in the same frame, it should not be included in the returned list
        of ORFs.

        dna: a DNA sequence
        returns: a list of non-nested ORFs

    This unit testing would be enough because there isn't any special exceptions that needs to be tested. Also, this case tests this function's
    ability to grab orf from three different possible reading frames.
    >>> find_all_ORFs("ATGCATGAATGTAG")
    ['ATGCATGAATGTAG', 'ATGAATGTAG', 'ATG']
    """
    # TODO: implement this
    orf_list = [] #list of orfs in all frames that will be returned at the end
    orf_list = orf_list + find_all_ORFs_oneframe(dna) #zero offset frame
    orf_list = orf_list + find_all_ORFs_oneframe(dna[1:]) #1 char offset frame
    orf_list = orf_list + find_all_ORFs_oneframe(dna[2:]) #2 char offset frame
    return orf_list


def find_all_ORFs_both_strands(dna):
    """ Finds all non-nested open reading frames in the given DNA sequence on both
        strands.

        dna: a DNA sequence
        returns: a list of non-nested ORFs
    >>> find_all_ORFs_both_strands("ATGCGAATGTAGCATCAAA")
    ['ATGCGAATG', 'ATGCTACATTCGCAT']
    """
    # TODO: implement this
    reverse_complement = get_reverse_complement(dna)
    orf_list = find_all_ORFs(dna) + find_all_ORFs(reverse_complement)#orfs from both direction
    return orf_list

def longest_ORF(dna):
    """ Finds the longest ORF on both strands of the specified DNA and returns it
        as a string
    >>> longest_ORF("ATGCGAATGTAGCATCAAA")
    'ATGCTACATTCGCAT'
    """
    # TODO: implement this
    pass


def longest_ORF_noncoding(dna, num_trials):
    """ Computes the maximum length of the longest ORF over num_trials shuffles
        of the specfied DNA sequence

        dna: a DNA sequence
        num_trials: the number of random shuffles
        returns: the maximum length longest ORF """
    # TODO: implement this
    pass


def coding_strand_to_AA(dna):
    """ Computes the Protein encoded by a sequence of DNA.  This function
        does not check for start and stop codons (it assumes that the input
        DNA sequence represents an protein coding region).

        dna: a DNA sequence represented as a string
        returns: a string containing the sequence of amino acids encoded by the
                 the input DNA fragment

        >>> coding_strand_to_AA("ATGCGA")
        'MR'
        >>> coding_strand_to_AA("ATGCCCGCTTT")
        'MPA'
    """
    # TODO: implement this
    pass


def gene_finder(dna):
    """ Returns the amino acid sequences that are likely coded by the specified dna

        dna: a DNA sequence
        returns: a list of all amino acid sequences coded by the sequence dna.
    """
    # TODO: implement this
    pass

if __name__ == "__main__":
    import doctest
    #doctest.testmod()
    doctest.run_docstring_examples(find_all_ORFs_both_strands, globals())
