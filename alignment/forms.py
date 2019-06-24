from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SubmitField, SelectField 

from wtforms.validators import input_required, optional, ValidationError

class AlignForm(FlaskForm):
    gene1_name = StringField('First Gene Name', [input_required()])
    gene1_content = StringField('First Gene Content', [input_required()])
    gene2_name = StringField('Second Gene Name', [input_required()])
    gene2_content = StringField('Second Gene Content', [input_required()])
    align_button = SubmitField('Align!')

class AnotherForm(FlaskForm):
    gene_name = StringField('Gene Name')
    gene_content = StringField('Gene Content')
    another_button = SubmitField('Add Gene')
    wipe_button = SubmitField('Wipe') 
 
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
    wipe_button = SubmitField('Wipe') 
