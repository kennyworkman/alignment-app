from alignment.frontend import *

DATA = {'gene1_name': 'gene1',
        'gene1_content': 'ATT',
        'gene2_name': 'gene2',
        'gene2_content':'TAA',
        'align_button': 'Align!'}

MORE_DATA = {'gene_name': 'gene3',
             'gene_content': 'CCC',
             'another_button': True}

SETTINGS_DATA = {'output_type': 'stockholm',
                 'wrap_number': 10,
                 'apply_button': True}

def test_unique_uuid(client, new_client):
    """Ensure unique UUID is generated for different clients, but that the same UUID persists across all requests for that client.
    """

    with client:
        client.get('/')
        first_uuid = session['user_id']
        assert len(first_uuid) == 36 and isinstance(first_uuid, str), "The value of the User ID stored in the session is incorrect." 

        client.post('/',data=DATA) 
        second_uuid = session['user_id']
        assert first_uuid == second_uuid, "The UserID value needs to be the same across requests."
    
    with new_client:
        new_client.get('/')
        third_uuid = session['user_id']
        assert third_uuid != first_uuid, "New client should have a distinct UserID"

def test_rendered_form(client):
    """Ensure correct input form is rendered depending on where user is in alignment workflow. Rendered behavior is determined by the 'aligned' variable stored in the session object; should be initially False, and set to True whenever genes are aligned and displayed in the ouptut.
    """
    with client:
        rv = client.get('/')
        #Each action will test variable and form rendering behavior simultaneously
        assert not session.get('aligned', None), "The app should always assume no genes are aligned with an initial request."
        assert b'First Gene Name' in rv.data, "The app should initially render the default input form."

        rv = client.post('/', data=DATA)
        assert session['aligned'] is True, "The value of session.aligned should be True if valid genes have been submitted."
        assert b'Add Gene' in rv.data, "The app should initially render the additional form upon successful alignment."

        rv = client.post('/', data=MORE_DATA)
        assert session['aligned'] is True, "The value of session.aligned should be True if additional genes have been submitted." 
        assert b'Add Gene' in rv.data, "The app should initially render the additional form upon successful alignment."
        
        rv = client.post('/', data=SETTINGS_DATA)
        assert session['aligned'] is True, "The value of session.aligned should be True if the settings have been changed."
        assert b'Add Gene' in rv.data, "The app should initially render the additional form upon successful alignment."

        rv = client.post('/', data={'wipe_button': True}, follow_redirects=True)
        assert session['aligned'] is False, "The value of session.aligned should be False if the wipe button is pressed."
        assert b'First Gene Name' in rv.data, "The app should render default intake form when the Wipe button is pressed."
        
def test_options_in_session(client):
    """Ensure session object is updated with user selected alignment options. Also ensure changes to the session actually make their way to the alignment info.
    """
    with client:
        client.get('/')
        assert session['output_format'] == 'clustal' and session['wrap_num'] == 60, "Incorrect option defaults stored in the session object."

        client.post('/', data=DATA)
        assert session['output_format'] == 'clustal' and session['wrap_num'] == 60, "Option defaults should remain the same when genes are aligned, unless explicitly changed."
        
        rv = client.post('/', data=SETTINGS_DATA)
        assert session['output_format'] == 'stockholm' and session['wrap_num'] == 10, "Option defaults should change when the user updates them."
        assert b'STOCKHOLM' in rv.data, "Option changes should be applied to alignment information when user changes them."


def test_gene_dict(client):
    """Ensure g.gene_dict functions correctly within the scope of a request. User data submissions should be reflected in this dictionary.
    """
    with client:
        client.get('/')
        assert not g.gene_dict, "g.gene_dict should only be empty if no requests are made."

        client.post('/', data=DATA)
        assert len(g.gene_dict) == 2 and 'gene1' in g.gene_dict, "g.gene_dict should reflect the request made by the user. If two genes are posted, there should be two things in the dictionary"


        client.post('/', data=MORE_DATA)
        assert len(g.gene_dict) == 1 and 'gene3' in g.gene_dict, "g.gene_dict should contain one gene if one gene is posted."

        client.post('/', data={'wipe_button': True}, follow_redirects=True)
        assert not g.gene_dict, "Wiping should remove any content from g.gene_dict"

def test_alignment_data(client):
    """Ensure alignment_data is what it should be depending on user request/post. 
    """
    with client:
        rv = client.get('/')
        assert b'Enter some genes to get started!' in rv.data, "With no genes to align, the app should prompt the user to to do enter some."

        rv = client.post('/', data=DATA)
        assert b'CLUSTAL' in rv.data, "When genes are aligned, the output should display on the webpage."

        rv = client.post('/', data=MORE_DATA)
        assert b'CLUSTAL' in rv.data, "When additional genes are aligned, the output should display on the webpage."
        assert b'gene1' in rv.data and b'gene3' in rv.data, "Additional genes should be added to the present alignment stack."

        rv = client.post('/', data={'wipe_button': True}, follow_redirects=True)
        
        assert b'Enter some genes to get started!' in rv.data, "Wipe button should get rid of the alignment data."
