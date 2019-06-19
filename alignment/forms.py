from wtforms import Form, StringField, IntegerField, SubmitField, SelectField, validators

from wtforms.validators import input_required, optional, ValidationError


class InputForm(Form):
    gene_name = StringField('Gene Name', [input_required()])
    gene_content = StringField('Gene Content', [input_required()])
    output_type = SelectField('Alignment Format', choices=[('clustal', 'Clustal'),
      ('fasta', 'Fasta'),
      ('msf', 'Msf'),
      ('phylip', 'Phylip'),
      ('selex', 'Selex'),
      ('stockholm', 'Stockholm'),
      ('vienna', 'Vienna')])
    wrap_number = IntegerField('Wrap Length', [optional()])
    align_button = SubmitField('Align!')

    def validate_wrap_number(form, field):
            if field.data and field.data < 0:
                raise ValidationError(u'Must be Positive Number!')

class WipeForm(Form):
    wipe_submit = SubmitField('Wipe') 
    

        
        
            



