from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField

class GetCountryDataForm(FlaskForm):
    name = SelectField(label="Country", coerce=int)
    submit = SubmitField('Submit') 