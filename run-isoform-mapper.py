import os
import sys
import json
import glob
import csvutil
from Bio import SeqIO
from isoform_mapper import map_isoform_pos
from optparse import OptionParser

import constants


def load_seq_dict(fasta_file):
    seq_dict = {}
    canon2isoforms = {}
    for record in SeqIO.parse(fasta_file, "fasta"):
        seq_id = record.id.split("|")[1]
        seq_dict[seq_id] = str(record.seq.upper())
    
    return seq_dict, canon2isoforms





def load_canon2isoforms(species):

    tmp_dict = {}
    in_file = "unreviewed/%s_protein_masterlist.csv" % (species)
    data_frame = {}
    csvutil.load_sheet(data_frame, in_file, ",")
    f_list = data_frame["fields"]
    for row in data_frame["data"]:
        canon = row[f_list.index("uniprotkb_canonical_ac")]
        for f in ["reviewed_isoforms", "unreviewed_isoforms"]:
            isoform_ac = row[f_list.index(f)]
            if isoform_ac == "":
                continue
            if canon not in tmp_dict:
                tmp_dict[canon] = {"reviewed":{}, "unreviewed":{}}
            ff = f.split("_")[0]
            tmp_dict[canon][ff][isoform_ac] = True

    return tmp_dict    



###############################
def main():

    usage = "\n%prog  [options]"
    parser = OptionParser(usage,version="%prog version___")
    parser.add_option("-i","--infile",action="store",dest="infile",help="")
    parser.add_option("-o","--outfile",action="store",dest="outfile",help="")
    (options,args) = parser.parse_args()

    for key in ([options.infile, options.outfile]):
        if not (key):
            parser.print_help()
            sys.exit(0)

    in_file = options.infile
    out_file = options.outfile


    DEBUG = False
    #DEBUG = True

    fasta_file_list = []
    log_file = "/data/shared/isoform-mapper/logs/logfile.txt"
    if DEBUG:
        fasta_file_list = glob.glob("/data/shared/isoform-mapper/db/*.fasta")
    else:
        db_dir = "/data/db/"
        if os.path.isdir(db_dir) == False:
            error_obj = {"error":"fasta directory not found"}
            print(error_obj)
            exit()
        fasta_file_list = glob.glob("/data/db/*.fasta")
        log_file = "/data/logs/logfile.txt"

    msg = "started loging ..."
    csvutil.write_log(log_file, msg, "w")
       
    if len(fasta_file_list) == 0:
        msg = "ERROR: no fasta files found"
        csvutil.write_log(log_file, msg, "a")
        exit()        

    seq_dict, isoform2canon = {}, {}
    for fasta_file in fasta_file_list:
        msg = "loading ... " + fasta_file
        csvutil.write_log(log_file, msg, "a")
        
        for record in SeqIO.parse(fasta_file, "fasta"):
            isoform_ac = record.id.split("|")[1]
            canon = record.description.split(" ")[-1].split("=")[1]
            seq_dict[isoform_ac] = str(record.seq.upper())
            isoform2canon[isoform_ac] = canon


    FW = open(out_file, "w")
    newrow = [
        "uniprotkb_isoform_ac","aa_pos_isoform","aa_isoform_user","aa_isoform_actual","glygen_canonical_ac",
        "aa_pos_canonical","aa_canonical","warning","error"
    ]
    FW.write("%s\n" % ("\t".join(newrow))) 

    with open(in_file, "r") as FR:
        f_list = []
        idx = 0
        for line in FR:
            idx += 1
            row = line[:-1].split(",")
            if idx == 1:
                f_list = row
            else:
                isoform_ac = row[f_list.index("isoform_ac")]
                isoform_pos = row[f_list.index("amino_acid_pos")]
                isoform_aa = row[f_list.index("amino_acid")]
                m_obj = {}
                if isoform_ac in isoform2canon and isoform_ac in seq_dict:
                    canon = isoform2canon[isoform_ac]
                    if canon in seq_dict:
                        canon_seq = seq_dict[canon]
                        isoform_seq = seq_dict[isoform_ac] 
                        m_obj = map_isoform_pos(canon_seq, isoform_seq, int(isoform_pos))
                        warning = "%s:%s is not %s" % (isoform_ac,isoform_pos,isoform_aa)
                        warning = "" if isoform_aa == m_obj["isoformaa"] else warning
                        error = ""
                        newrow = [isoform_ac,str(m_obj["isoformpos"]),isoform_aa,m_obj["isoformaa"]]
                        newrow += [canon,str(m_obj["canonpos"]), m_obj["canonaa"], warning, error]
                        FW.write("%s\n" % ("\t".join(newrow))) 
    FW.close() 
 
    return



if __name__ == '__main__':
    main()

