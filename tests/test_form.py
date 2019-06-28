from alignment.forms import *

from flask import request, session, g

def post_gene_data(client, data):
    """Helper function that returns ReturnValue.data from a given post to the "/" endpoint
    """
    with client:
        rv = client.post('/', data=data, follow_redirects=True)
        return rv.data

def test_alignform(client):
    """Ensure that the initial alignment form properly handles POST requests, and raises appropriate errors if there are empty fields.
    """
    gene_data = {'gene1_name': '',
                 'gene1_content': 'ATT',
                 'gene2_name': 'gene2',
                 'gene2_content':'TAA',
                 'align_button': 'Align!'}

    rv = post_gene_data(client, gene_data)

    assert b'Enter some genes' in rv, "Alignment form doesn't validate input. It shouldn't accept empty forms."
   
    gene_data['gene1_name'] = 'gene1'
    
    rv = post_gene_data(client, gene_data)

    assert b'FATAL' not in rv, "Alignment form did not properly register data. Error displayed in aligned output when there shouldn't be."
    assert b'CLUSTAL' in rv, "Alignment default should be in CLUSTAL format"
    assert b'Add Gene' in rv, "After submitting intitial alignment form, the homepage should render the 'another_form' template."

def test_anotherform(client):
    """Ensure the AnotherForm class properly adds aligned genes and that one field cannot be submitted without the other. The wipe function should also remove aligned output and render the main form.
    """
    gene_data = {'gene1_name': 'gene1',
                 'gene1_content': 'ATT',
                 'gene2_name': 'gene2',
                 'gene2_content':'TAA',
                 'align_button': 'Align!'}

    # Submit initial post request to render this form 
    post_gene_data(client, gene_data)        
    
    gene_data = {'gene_name': 'gene3',
                 'gene_content': '',
                 'another_button': True}

    rv = post_gene_data(client, gene_data)
    assert b'Please fill out both forms!' in rv, "Shouldn't be able to submit a gene with its name, or a name with its content. Not displaying error."

    gene_data['gene_content'] = 'ATA'
    rv = post_gene_data(client, gene_data)
    assert b'CLUSTAL' in rv, "AnotherForm isn't displaying alignment data after a new gene is submitted."
    print(rv) 
    assert b'gene1' in rv and b'gene2' in rv and b'gene3' in rv, "AnotherForm doesn't doesn't add additional gene to existing alignment. Should be three genes present."

    gene_data['wipe_button'] = True
    rv = post_gene_data(client, gene_data)
    assert b'Enter some genes' in rv, "Wipe button should get rid of alignment output."
    assert b'First Gene Name' in rv, "Wipe button should render original AlignForm"
