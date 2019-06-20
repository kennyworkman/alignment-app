from flask import (
    Blueprint, render_template, abort, session, g, request, redirect
)
from uuid import uuid1

from alignment.forms import GeneForm, SettingsForm, WipeForm
from alignment.db import insert_genes, get_gene_dict, wipe_genes, query_genes

from alignment.make_fasta import capture_alignment

bp = Blueprint('frontend', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():

    if 'user_id' not in session:
        session['user_id'] = str(uuid1())
    user_id = session['user_id']

    gene_form = GeneForm()
    settings_form = SettingsForm()
    wipe_form = WipeForm()

    output_format = 'clustal'
    wrap_num = 60

    if gene_form.validate_on_submit():
        g.gene_name = gene_form.gene_name.data
        g.gene_content = gene_form.gene_content.data

        insert_genes(session, g)

    if settings_form.validate_on_submit():
        output_format = settings_form.output_type.data
        wrap_num = settings_form.wrap_number.data

    if wipe_form.wipe_submit.data: 
        wipe_genes()
        return redirect('/')

    gene_dict = get_gene_dict(session)
    alignment_data = capture_alignment(gene_dict, output_format, wrap_num)   

    if len(gene_dict) == 0:
        db_message = "Enter some genes for alignment!"
    elif len(gene_dict) == 1:
        db_message = "Another gene please."
    else:
        db_message = "See aligned genes below! Submit more if you want. Press 'Wipe' to start over."
        
    return render_template('index.html', 
                            db_message=db_message,

                            alignment_data=alignment_data, 
                            gene_form=gene_form,
                            settings_form=settings_form,
                            wipe_form=wipe_form)

