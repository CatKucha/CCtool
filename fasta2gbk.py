#https://www.biostars.org/p/2492/
#modified by CottonZ 2019.08.28
"""Convert a GFF and associated FASTA file into GenBank format.

Usage:
fasta2genbank.py  <FASTA sequence file folder> 
"""
import sys
import os

from Bio import SeqIO
from Bio.Alphabet import generic_dna, generic_protein
from BCBio import GFF

genome_path = sys.argv[1]
if genome_path[:-1] == '/':
      genome_path = genome_path.rstrip('/')

fasta_file_list = []
for file in os.listdir(genome_path):
      if '.fna' in file:
            fasta_file_list.append(file)

def gff2gbk_parse_singlerecord(scaffold_gbk):
    scaffold_name = scaffold_gbk.id
    for cds in scaffold_gbk.features:
          cds_name = scaffold_name+'_'+cds.qualifiers['ID'][0].split('_')[-1]
          cds.qualifiers['translation'] = str(pep_input[cds_name].seq).strip('*')
          cds.qualifiers['transl_table'] = 11
    return scaffold_gbk

for fasta_file in fasta_file_list:
      fasta_500_file = "%s.500.fasta" % (genome_path+'/'+os.path.splitext(fasta_file)[0])
      gff_file = "%s.500.gff" % (genome_path+'/'+os.path.splitext(fasta_file)[0])
      pep_file = "%s.500.pep" % (genome_path+'/'+os.path.splitext(fasta_file)[0])
      gbk_file = "%s.500.gbk" % (genome_path+'/'+os.path.splitext(fasta_file)[0])
      embl_file = "%s.500.embl" % (genome_path+'/'+os.path.splitext(fasta_file)[0])

      os.system(f"seqkit seq -m 500 {fasta_file} > {fasta_500_file}")
      os.system(f"prodigal -a {pep_file} -f gff -i {fasta_500_file} -o {gff_file} ")


      fasta_input = SeqIO.to_dict(SeqIO.parse(fasta_500_file, "fasta", generic_dna))
      pep_input = SeqIO.to_dict(SeqIO.parse(pep_file, "fasta", generic_protein))
      gff_iter = GFF.parse(gff_file, base_dict= fasta_input)

      count = SeqIO.write((gff2gbk_parse_singlerecord(i) for i in gff_iter ) , gbk_file, "genbank")
      print("write %s records to gbk file" %count)

      count_embl = SeqIO.convert(gbk_file, 'genbank', embl_file, 'embl');
      print("write %s records to gbk file" %count_embl)


#############################################################################
def gff2gbk_parse(gff_iter):
      try:
            while True:
                  scaffold_gbk = next(gff_iter)
                  scaffold_name = scaffold_gbk.id
                  for cds in scaffold_gbk.features:
                        cds_name = scaffold_name+'_'+cds.qualifiers['ID'][0].split('_')[-1]
                        cds.qualifiers['translation'] = str(pep_input[cds_name].seq).strip('*')
                        cds.qualifiers['transl_table'] = 11
                  yield scaffold_gbk
      except StopIteration:
            return
# SeqIO.write(gff2gbk_parse(gff_iter), out_file, "genbank")


