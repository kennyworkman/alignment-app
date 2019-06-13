from wtforms import Form, StringField, validators

class InputForm(Form):
    gene_name = StringField('Gene Name', validators=[validators.input_required()])
    gene_content = StringField('Gene Content', validators=[validators.input_required()])

class AlignForm(Form):
    pass
