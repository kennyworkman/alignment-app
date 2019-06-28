from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SubmitField, SelectField 

from wtforms.validators import input_required, optional, ValidationError

class AlignForm(FlaskForm):
    """Initial alignment form. Takes a pair of genes.
    """
    gene1_name = StringField('First Gene Name', [input_required()])
    gene1_content = StringField('First Gene Content', [input_required()])
    gene2_name = StringField('Second Gene Name', [input_required()])
    gene2_content = StringField('Second Gene Content', [input_required()])
    align_button = SubmitField('Align!')

class AnotherForm(FlaskForm):
    """A form that will only take a single gene. Rendered after the initial form is submitted to avoid confusion and indiicate additional genes can be aligned.
    """
    gene_name = StringField('Gene Name')
    gene_content = StringField('Gene Content')
    another_button = SubmitField('Add Gene')
    wipe_button = SubmitField('Wipe') 

    def validate_gene_name(form, field):
        if field.data and not form.gene_content.data:
            raise ValidationError(u'Please fill out both forms!')
 
    def validate_gene_content(form, field):
        if field.data and not form.gene_name.data:
            raise ValidationError(u'Please fill out both forms!')

class SettingsForm(FlaskForm):
    """Form to change output settings, ie. file outputt type and number of base pairs per line
    """
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
            if field.data == 0:
                raise ValidationError(u'Must be Positive Nonzero Number!')
    

class WipeForm(FlaskForm):
    """ A form that is really a single button, indicating that the user wants to wipe all of his genes and start over.
    """
    wipe_button = SubmitField('Wipe') 
