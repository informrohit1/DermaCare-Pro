from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, NumberRange

class SkinForm(FlaskForm):
    # Ask for skin issue (you can change this to a SelectField if there are predefined issues)
    skin_issue = StringField('What skin issue are you experiencing?', validators=[DataRequired()])

    # Ask for severity, but this might be better as a SelectField with predefined options
    severity = SelectField('Severity of issue', choices=[('Mild', 'Mild'), ('Moderate', 'Moderate'), ('Severe', 'Severe')], validators=[DataRequired()])

    # Ask for symptoms (good choice for a TextAreaField)
    symptoms = TextAreaField('Symptoms', validators=[DataRequired()])

    # Additional fields that might be useful
    age = IntegerField('Age', validators=[DataRequired(), NumberRange(min=0, max=120)])
    weight = IntegerField('Weight (in kg)', validators=[DataRequired(), NumberRange(min=30, max=200)])
    blood_group = StringField('Blood Group', validators=[DataRequired()])

    # Submit button
    submit = SubmitField('Submit')
