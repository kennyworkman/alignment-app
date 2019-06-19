from flask import (
    Blueprint, render_template, abort, session, g, request, redirect
)
from uuid import uuid1

from alignment.forms import InputForm, WipeForm
from alignment.db import insert_genes, get_gene_dict, wipe_genes, query_genes

from alignment.make_fasta import capture_alignment

bp = Blueprint('frontend', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid1())
    user_id = session['user_id']

    input_form = InputForm(request.form)
    wipe_form = WipeForm(request.form)

    output_format = 'clustal'
    wrap_num = 60
    # Insert user gene information if form is validated
    if input_form.align_button.data and input_form.validate():
        g.gene_name = input_form.gene_name.data
        g.gene_content = input_form.gene_content.data
        output_format = input_form.output_type.data
        wrap_num = input_form.wrap_number.data
        insert_genes(session, g)

    # Wipe DB if form is validated
    if wipe_form.wipe_submit.data: 
        wipe_genes()
        return redirect('/')

    gene_dict = get_gene_dict(session)
    if len(gene_dict) == 0:
        db_message = "Enter some genes for alignment!"
    elif len(gene_dict) == 1:
        db_message = "Another gene please."
    else:
        db_message = "See aligned genes below! Submit more if you want. Press 'Wipe' to start over."
        
    alignment_data = capture_alignment(gene_dict, output_format, wrap_num)   
   
    return render_template('index.html', 
                                alignment_data=alignment_data, 
                                db_message=db_message,
                                input_form = input_form,
                                wipe_form = wipe_form)
    
