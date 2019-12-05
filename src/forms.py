from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, FieldList, FormField

class Field(FlaskForm):
    name = StringField()
    type = StringField()

class InsertForm(FlaskForm):
    """A form for one or more addresses"""
    fields = FieldList(FormField(Field), min_entries=1)
    submit = SubmitField('RUN')

class UpdateForm(FlaskForm):
    """A form for one or more addresses"""
    fields = FieldList(FormField(Field), min_entries=1)
    submit = SubmitField('RUN')
    value = StringField()

# class UpdateForm(FlaskForm):
#     def __init__(self, df):
#         self.fields = FieldList(StringField(row.name, validators=[DataRequired()]) for row in df.itertuples()
#         self.submit = SubmitField('Go')
