# Creates .fa (FASTA) files from dictonary mapping name to genomic info

from tempfile import NamedTemporaryFile
import subprocess
import os

CLUSTALO_PATH = '/usr/local/bin/clustalo' # Location of Clustalo exec on machine
TEMP_PATH = '/tmp' # Temp file will be stored here

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

# Dictionary mapping command line output flags to more readable strings
OUTPUT_DICT = {
    "fasta": "--outfmt=fasta",
    "clustal": "--outfmt=clustal",
    "msf": "--outfmt=msf",
    "phylip": "--outfmt=phylip",
    "selex": "--outfmt=selex",
    "stockholm": "--outfmt=stockholm",
    "vienna": "--outfmt=vienna"}


def run_clustalo(file, output_type, wrap_number):
    try:
        output_arg = OUTPUT_DICT[output_type]
        wrap_arg = "--wrap=" + str(wrap_number)
        data = subprocess.run([CLUSTALO_PATH, "-i", file.name, output_arg, wrap_arg, "--residuenumber"], capture_output=True, check=True)
        return data.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr 
 
def capture_alignment(session, gene_dict):
    """ Pass dictionary mapping gene names to genomic content. Converts data into fasta format and passes this temporary file to the clustero aligner. Output information captured from standard output and returned as a string.
    """
    if len(gene_dict) < 2:
        return "Error: Need at least two genes for alignment!"
    output_format = session['output_format']
    wrap_number = session['wrap_num']

    create_temp_dir()
    fp = create_temp()
    write_temp(gene_dict, fp)
    alignment_out = run_clustalo(fp, output_format, wrap_number)
    remove_temp(fp)
    return alignment_out.decode()

