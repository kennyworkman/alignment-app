# Creates .fa (FASTA) files from dictonary mapping name to genomic info

from tempfile import NamedTemporaryFile
import subprocess
import os

CLUSTALO_PATH = '/usr/local/bin/clustalo' # Location of Clustalo exec on machine
TEMP_PATH = './instance' # Temp file will be stored here

def create_temp():
    temp = NamedTemporaryFile(suffix=".fa", dir=TEMP_PATH, delete=False)  
    return temp

def create_temp_dir():
    if not os.path.exists(TEMP_PATH):
        os.mkdir(TEMP_PATH)        

def remove_temp(temp):
    os.unlink(temp.name)

def write_temp(gene_dict, file):
        for key, value in gene_dict.items():
            carrot = bytes('>', 'utf-8')
            newline = bytes('\n', 'utf-8')
            gene_name = bytes(key, 'utf-8')
            gene_bases = bytes(value, 'utf-8')
            file.writelines([carrot,
                           gene_name,
                           newline,
                           gene_bases,
                           newline
                           ])   
        file.close()

def run_clustalo(file):
    try:
        data = subprocess.run([CLUSTALO_PATH, "-i", file.name, "--outfmt=clustal", "--residuenumber"], capture_output=True, check=True)
        return data.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr 
        
def capture_alignment(gene_dict):
    """ Pass dictionary mapping gene names to genomic content. Converts data into fasta format and passes thistemporary file to the clustero aligner. Output information captured from standard output and returnded as a string.
    """
    
    create_temp_dir()
    fp = create_temp()
    write_temp(gene_dict, fp)
    alignment_out = run_clustalo(fp)
    remove_temp(fp)
    return alignment_out.decode()
