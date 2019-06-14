from wtforms import Form, StringField, BooleanField, SubmitField, validators

class InputForm(Form):
    gene_name = StringField('Gene Name', validators=[validators.input_required()])
    gene_content = StringField('Gene Content', validators=[validators.input_required()])
    gene_submit = SubmitField('Submit Gene')

class AlignForm(Form):
    do_alignment = BooleanField('Align?', validators=[validators.input_required()])
    align_submit = SubmitField('Align!')
