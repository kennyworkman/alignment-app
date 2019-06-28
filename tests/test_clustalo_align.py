from flask import session
from alignment.clustalo_align import *

def test_run_clustalo(app):
    """Ensure that clustalo library is correctly aligning genes. Assert that incorrect commands return a the error as a string
    """
    _, temp_path = create_temp()

    # No content in provided file, clustalo should error
    assert b'FATAL' in  run_clustalo(temp_path, "clustal", 5), "Clustalo is not displaying errors to the std_out or run_clustalo is not properly returning them."

    with open(temp_path, "wb") as f:
        f.writelines([b'>gene1', b'\nATTACTG'])

    assert b'nothing to align' in  run_clustalo(temp_path, "clustal", 5), "Clustalo should error when aligning a single sequence"
    
    with open(temp_path, "ab") as f:
        f.writelines([b'>gene2', b'\nATT', b'\n>gene3', b'\nTTAA'])

    assert b'multiple sequence alignment' in  run_clustalo(temp_path, "clustal", 5), "Clustalo alignment functionality not working properly" 
    # Ensure output formats work nicely
    assert b'CLUSTAL' in  run_clustalo(temp_path, "clustal", 5), "Clustalo alignment not printing proper output format"
    assert b'STOCKHOLM' in  run_clustalo(temp_path, "stockholm", 5), "Clustalo alignment not printing proper output format"

    
def test_capture_alignment(app, client):
    """Ensure interaction between the capture_alignment function and the session context is clean. Gene data should be parsed from the passed dictionary without error and options should be retrieved from the session object.
    """

    with client:
        client.get('/')
        gene_dict = {'gene1': 'ATT', 'gene2': 'TTA'}
        assert 'multiple sequence alignment' in capture_alignment(session, gene_dict), "capture_alignment not correctly processing data from its provided arguments." 
        assert 'CLUSTAL' in capture_alignment(session, gene_dict), "Incorrect output format; should be clustalo format." 
        # Test the line wrap option flag 
        session['wrap_num'] = 1
        assert 'ATT' not in capture_alignment(session, gene_dict), "Line wrap option isn't being expressed."
        
        # Test the outptut file type
        session['output_format'] = 'stockholm'
        assert 'STOCKHOLM' in capture_alignment(session, gene_dict), "Output type option isn't being expressed."
        
        gene_dict = {}
        assert 'Error' in capture_alignment(session, gene_dict), "Error isn't being handled internally by the function." 

