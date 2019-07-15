"""
    forms
    ~~~~~
    Implements forms based on WTForms.
"""

from flask_wtf import FlaskForm
from wtforms import Form, StringField, IntegerField, SubmitField, SelectField

from wtforms.validators import input_required, optional, ValidationError

class AlignForm(FlaskForm):
    """Initial alignment form that is rendered when the user first logs in.

    An instance of a WTForm that takes a pair of gene names and data.

    :cvar gene1_name: A WTForm StringField
    :cvar gene1_content: A WTForm StringField
    :cvar gene2_name: A WTForm StringField
    :cvar gene2_content: A WTForm StringField
    :cvar align_button: A WTForm SubmitField
    """
    gene1_name = StringField('First Gene Name', [input_required()])
    gene1_content = StringField('First Gene Content', [input_required()])
    gene2_name = StringField('Second Gene Name', [input_required()])
    gene2_content = StringField('Second Gene Content', [input_required()])
    align_button = SubmitField('Align!')

class AnotherForm(FlaskForm):
    """Secondary form that will only add a single gene to the existing stack.

    Rendered only after the initial form is submitted to avoid confusion and
    indicate that additional genes can be aligned.

    :cvar gene_name: A WTForm StringField
    :cvar gene_content: A WTForm StringField
    :cvar another_button: A WTForm SubmitField
    :cvar wipe_button: A WTForm SubmitField
    """

    gene_name = StringField('Gene Name')
    gene_content = StringField('Gene Content')
    another_button = SubmitField('Add Gene')
    wipe_button = SubmitField('Wipe')

    def validate_gene_name(form, field):
        """Ensures that gene_name and gene_content are submitted together.

        :raises ValidationError: If one of the StringFields is present on submit
        without the other.
        """
        if field.data and not form.gene_content.data:
            raise ValidationError(u'Please fill out both forms!')

    def validate_gene_content(form, field):
        """Ensures that gene_name and gene_content are submitted together.

        :raises ValidationError: If one of the StringFields is present on submit
        without the other.
        """
        if field.data and not form.gene_name.data:
            raise ValidationError(u'Please fill out both forms!')

class SettingsForm(FlaskForm):
    """Form to change output settings (file output type or line wrap number).

    :cvar output_type: A WTForm SelectField
    :cvar wrap_number: A WTForm IntegerField
    :cvar apply_button: A WTForm SubmitField
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
        """Ensures the wrap_number field has a positive number on submit.

        :raises ValidationError: If one of the StrinFields is negative or 0.
        """
        if field.data and field.data < 0:
            raise ValidationError(u'Must be Positive Number!')
        if field.data == 0:
            raise ValidationError(u'Must be Positive Nonzero Number!')
