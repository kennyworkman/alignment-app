from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SubmitField, SelectField 

from wtforms.validators import input_required, optional, ValidationError


class GeneForm(FlaskForm):
    gene_name = StringField('Gene Name', [input_required()])
    gene_content = StringField('Gene Content', [input_required()])
    submit_gene = SubmitField('Submit!')

class SettingsForm(FlaskForm):
    output_type = SelectField('Alignment Format', choices=[('clustal', 'Clustal'),
      ('fasta', 'Fasta'),
      ('msf', 'Msf'),
      ('phylip', 'Phylip'),
      ('selex', 'Selex'),
      ('stockholm', 'Stockholm'),
      ('vienna', 'Vienna')], default="clustal")
    wrap_number = IntegerField('Wrap Length', [optional()], default=60)
    apply_button = SubmitField('Apply Changes')

    def validate_wrap_number(form, field):
            if field.data and field.data < 0:
                raise ValidationError(u'Must be Positive Number!')

    
class WipeForm(FlaskForm):
    wipe_submit = SubmitField('Wipe') 
    align_button = SubmitField('Align!')
