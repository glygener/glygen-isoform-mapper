import os
import sys
import json
import glob
from Bio import SeqIO
from Bio.Align import substitution_matrices
from Bio import Align

import warnings
warnings.simplefilter('ignore')



def map_isoform_pos(canon_seq, isoform_seq, isoform_pos):


    aligner = Align.PairwiseAligner()
    aligner.mode = "global"
    aln_list = aligner.align(isoform_seq, canon_seq)
    aln = aln_list[0]
    aln = aln_list[0]
    i_pos, c_pos = 0, 0
    for i in range(0, len(aln[0])):
        i_pos += 1 if aln[0][i] != "-" else 0
        c_pos += 1 if aln[1][i] != "-" else 0
        if i_pos == isoform_pos:
            m_obj = {"canonpos":c_pos, "canonaa":aln[1][i], "isoformpos":isoform_pos,"isoformaa":aln[0][i]}
            return m_obj
    
    return {}







if __name__ == '__main__':
    main()

