### A collection of functions to interact with the Clustalo package to produce alignments from pythonic genomic data

from tempfile import mkstemp
import subprocess
import os

CLUSTALO_PATH = '/usr/local/bin/clustalo' # Location of Clustalo exec on machine
TEMP_DIR = '/tmp' # Temp file will be stored here

# Dictionary mapping command line output flags to more readable strings
OUTPUT_DICT = {
    "fasta": "--outfmt=fasta",
    "clustal": "--outfmt=clustal",
    "msf": "--outfmt=msf",
    "phylip": "--outfmt=phylip",
    "selex": "--outfmt=selex",
    "stockholm": "--outfmt=stockholm",
    "vienna": "--outfmt=vienna"}

### The following collection of functions should not be referenced outside of this module. They are merely helper functions. ###

def create_temp():
    temp_handle, temp_path = mkstemp(suffix=".fa", dir=TEMP_DIR)
    return temp_handle, temp_path

def create_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)        

def remove_temp(temp_path):
    os.unlink(temp_path)

def write_temp(gene_dict, temp_handle):
    """Take gene dictionary and construct a fasta file within the provided temporary file handle.
    """
    with open(temp_handle, 'wb') as f:
        for key, value in gene_dict.items():
            carrot = bytes('>', 'utf-8')
            newline = bytes('\n', 'utf-8')
            gene_name = bytes(key, 'utf-8')
            gene_bases = bytes(value, 'utf-8')
            f.writelines([carrot,
                           gene_name,
                           newline,
                           gene_bases,
                           newline
                           ])   
        f.close()

#################################################


def run_clustalo(temp_path, output_type, wrap_number):
    """This function opens up a new subprocess to run a clustalo command given the provided parameters as options to the command line executable.

    It is important that output_type should be one of the readable keys from the OUTPUT_DICT defined above. The wrap_number should be a valid postive integer. Any error will simply be returned as it would appear in the standard output.
    """
    assert os.path.exists(temp_path), "The provided fasta file does not exist."
    assert output_type in OUTPUT_DICT, "The provided output_type value must be a defined in OUTPUT_DICT"
    assert 0 < wrap_number and isinstance(wrap_number, int), "The provided wrap_number must be nonzeo, positive integer"
    try:
        output_arg = OUTPUT_DICT[output_type]
        wrap_arg = "--wrap=" + str(wrap_number)
        data = subprocess.run([CLUSTALO_PATH, "-i", temp_path, output_arg, wrap_arg, "--residuenumber"], capture_output=True, check=True)
        return data.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr 
 
def capture_alignment(session, gene_dict):
    """This function takes a dictionary of genes (gene_dict) and a session object from the Flask app that contains alignment options. The dictionary should have the following format:

        {'gene1': 'ATTT', 'gene2':'CCC'}

        Where both keys and values are strings, with values representing genes. It is up to the user to provide valid genomic data that can be aligned by Clustalo. 

        Dictionary information is converted to a temporary fasta file and passed to the Clustalo binary through a subprocess. The std output is collected and returned.
        """

    if len(gene_dict) < 2:
        return "Error: Need at least two genes for alignment!"
    assert isinstance(gene_dict, dict), "Gene_dict paramter must be a dictionary."
    output_format = session['output_format']
    wrap_number = session['wrap_num']

    create_temp_dir()
    temp_handle, temp_path = create_temp()
    write_temp(gene_dict, temp_handle)
    alignment_out = run_clustalo(temp_path, output_format, wrap_number)
    remove_temp(temp_path)
    return alignment_out.decode()

