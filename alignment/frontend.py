from flask import (
    render_template, abort, session, g, request, redirect
)
from uuid import uuid1

from alignment.forms import AlignForm, AnotherForm, SettingsForm 
from alignment.db import insert_genes, get_gene_dict, wipe_genes

from alignment.make_fasta import capture_alignment

@app.route('/', methods=('GET', 'POST'))
def index():
    # Generates unique User ID to associate multiple requests with a single user.
    if 'user_id' not in session:
        session['user_id'] = str(uuid1())
    user_id = session['user_id']
    # Genes for each request are retrieved from the g object.
    if 'gene_dict' not in g:
        g.gene_dict = {}

    align_form = AlignForm()
    another_form = AnotherForm()
    settings_form = SettingsForm()

    output_format = 'clustal'
    wrap_num = 60
    aligned = False

    if align_form.align_button.data and align_form.validate_on_submit():
        gene1_name, gene1_content = align_form.gene1_name.data, align_form.gene1_content.data
        gene2_name, gene2_content = align_form.gene2_name.data, align_form.gene2_content.data

        g.gene_dict[gene1_name] = gene1_content
        g.gene_dict[gene2_name] = gene2_content
        
        aligned = True # This value will switch the form rendered in the template
        insert_genes(session, g)

    if another_form.wipe_button.data: 
        wipe_genes()
        aligned = False # This value will swtich form rendered in tempalte to the original
        return redirect('/')

    if another_form.another_button.data:
        aligned = True # Maintain changed form
        # Manually check fields are not empty to allow seperate behavior among Submit Fields
        if another_form.gene_name.data and another_form.gene_content.data: 
            gene_name, gene_content = another_form.gene_name.data, another_form.gene_content.data

            g.gene_dict[gene_name] = gene_content
            insert_genes(session, g)


    if settings_form.apply_button.data and settings_form.validate_on_submit():
        output_format = settings_form.output_type.data
        wrap_num = settings_form.wrap_number.data
        aligned = True  

    gene_dict = get_gene_dict(session)
    alignment_data = capture_alignment(gene_dict, output_format, wrap_num)   

    return render_template('index.html', 
                            aligned=aligned,

                            alignment_data=alignment_data,
                            another_form=another_form,
                            align_form=align_form,
                            settings_form=settings_form)

