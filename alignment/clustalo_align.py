"""
    clustalo_align
    ~~~~~~~~~~~~~~
    A collection of functions to interact with the Clustalo package to produce
    alignments from pythonic genomic data.
"""

from tempfile import mkstemp
import subprocess
import sys
import os

# TODO: Introduce a config file for these options
CLUSTALO_PATH = '../bin/clustalo'  # Location of binary within package
TEMP_DIR = '/tmp'  # Temp file will be stored here

# Dictionary mapping command line output flags to more readable strings
OUTPUT_DICT = {
    "fasta": "--outfmt=fasta",
    "clustal": "--outfmt=clustal",
    "msf": "--outfmt=msf",
    "phylip": "--outfmt=phylip",
    "selex": "--outfmt=selex",
    "stockholm": "--outfmt=stockholm",
    "vienna": "--outfmt=vienna"}

# The following collection of functions should not be referenced outside of
# this module. They are merely helper functions.


def create_temp():
    temp_handle, temp_path = mkstemp(suffix=".fa", dir=TEMP_DIR)
    return temp_handle, temp_path


def create_temp_dir():
    if not os.path.exists(TEMP_DIR):
        os.mkdir(TEMP_DIR)


def remove_temp(temp_path):
    os.unlink(temp_path)


def write_temp(gene_dict, temp_handle):
    """Take gene dictionary and construct a fasta file within the provided
    temporary file handle.
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

#############################################################################


def run_clustalo(temp_path, output_type, wrap_number):
    """Runs a clustalo command in a subprocess and captures the output.

    This function takes a fasta (.fa) file containing genomic information and
    performs an alignment on the data using the output_type and wrap_number
    parameters. The output of the process, whether it is functional alignment
    data or any error printed to the stderr, will be returned.

    :param temp_path: The file path with the .fa file containing the genomic
    information to align.
    :type temp_path: str
    :param output_type: A key in the OUTUPUT_DICT dictionary that corresponds to
    a clustalo output type.
    :type output_type: str
    :param wrap_number: A number that specifies how long each output line should
    be. Must be positive, nonzero.
    :type wrap_number: int
    :return: Binary data from the result of the process, either from the stdout
    or stderr
    """
    assert os.path.exists(temp_path), "The provided fasta file does not exist."
    assert output_type in OUTPUT_DICT, "The provided output_type value must be" \
                                       " defined in OUTPUT_DICT"
    assert 0 < wrap_number and isinstance(wrap_number, int), "The provided" \
                                                             " wrap_number must" \
                                                             " be nonzeo," \
                                                             " positive integer"

    try:
        output_arg = OUTPUT_DICT[output_type]
        wrap_arg = "--wrap=" + str(wrap_number)
        exec_path = os.path.join(os.path.abspath(sys.path[0]), CLUSTALO_PATH)
        data = subprocess.run([exec_path, "-i", temp_path,
                               output_arg, wrap_arg, "--residuenumber"],
                              capture_output=True, check=True)
        return data.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr


def capture_alignment(session, gene_dict):
    """Takes a dictionary of gene data and captures the alignment.

    The dictionary should have the following format::

        {'gene1': 'ATTT',
         'gene2':'CCC'}

    It's contents will be converted to fasta files and passed to a Clustalo
    binary through a subprocess. The stdout (or stderr) is collected and
    returned as binary data.

    The passed session object provides the command line options for the clustalo
    executable.

    :param session: A Flask session object
    :param gene_dict: A dictionary mapping gene names to data
    :type gene_dict: int
    :return: Binary alignment output data
    """
    if len(gene_dict) < 2:
        return "Error: Need at least two genes for alignment!"
    assert isinstance(
        gene_dict, dict), "Gene_dict paramter must be a dictionary."

    output_format = session['output_format']
    wrap_number = session['wrap_num']

    create_temp_dir()
    temp_handle, temp_path = create_temp()
    write_temp(gene_dict, temp_handle)
    alignment_out = run_clustalo(temp_path, output_format, wrap_number)
    remove_temp(temp_path)

    return alignment_out.decode()
