from flask import (
    Blueprint, render_template, abort, session, g, request, redirect
)
from uuid import uuid1

from alignment.forms import AlignForm, AnotherForm, SettingsForm 
from alignment.db import insert_genes, get_gene_dict, wipe_genes

from alignment.clustalo_align import capture_alignment

bp = Blueprint('frontend', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():

    # Generates unique User ID to associate multiple requests with a single user.
    if 'user_id' not in session:
        session['user_id'] = str(uuid1())
    user_id = session['user_id']
    
    # Session tracks whether genes have been submitted to decide which form template to render. Session also stores settings across requests.
    session['aligned'] = False
    session['output_format'] = 'clustal'
    session['wrap_num'] = 60

    # Genes for each request are retrieved from the g object.
    if 'gene_dict' not in g:
        g.gene_dict = {}

    align_form = AlignForm()
    another_form = AnotherForm()
    settings_form = SettingsForm()


    if align_form.align_button.data and align_form.validate_on_submit():
        gene1_name, gene1_content = align_form.gene1_name.data, align_form.gene1_content.data
        gene2_name, gene2_content = align_form.gene2_name.data, align_form.gene2_content.data

        g.gene_dict[gene1_name] = gene1_content
        g.gene_dict[gene2_name] = gene2_content
        
        session['aligned'] = True # This value will switch the form rendered in the template
        insert_genes(session, g)

    if another_form.wipe_button.data: 
        wipe_genes(session)
        session['aligned'] = False 
        return redirect('/')

    if another_form.another_button.data:
        session['aligned'] = True 
        if another_form.validate_on_submit():
            gene_name, gene_content = another_form.gene_name.data, another_form.gene_content.data

            g.gene_dict[gene_name] = gene_content
            insert_genes(session, g)


    if settings_form.apply_button.data:
        session['aligned'] = True 
        if settings_form.validate_on_submit():
            session['output_format'] = settings_form.output_type.data
            session['wrap_num'] = settings_form.wrap_number.data
            

    gene_dict = get_gene_dict(session)
    alignment_data = capture_alignment(session, gene_dict)   

    return render_template('index.html', 
                            aligned=session['aligned'],
                            alignment_data=alignment_data,
                            another_form=another_form,
                            align_form=align_form,
                            settings_form=settings_form)

