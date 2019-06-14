from flask import (
    Blueprint, render_template, abort, session, g, request
)
from uuid import uuid1

from alignment.forms import InputForm, AlignForm
from alignment.db import insert_genes, get_gene_dict, wipe_genes, query_genes

from alignment.make_fasta import capture_alignment

bp = Blueprint('frontend', __name__)

@bp.route('/', methods=('GET', 'POST'))
def index():
    if 'user_id' not in session:
        session['user_id'] = str(uuid1())
    user_id = session['user_id']

    input_form = InputForm(request.form)
    align_form = AlignForm(request.form)
    #gene_data = "Please submit some genes for alignment"

    if input_form.gene_submit.data and input_form.validate():
        g.gene_name = input_form.gene_name.data
        g.gene_content = input_form.gene_content.data
        insert_genes(session, g)
    gene_data = gene_dict = get_gene_dict(session, 2)

    if align_form.align_submit.data and align_form.validate():
        gene_data = alignment = capture_alignment(gene_dict)
   
    return render_template('index.html', gene_data=gene_data, input_form=input_form, align_form = align_form)
    
