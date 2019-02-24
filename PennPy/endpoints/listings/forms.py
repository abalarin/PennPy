from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateListingForm(FlaskForm):
    title = TextField('Listing Name', validators=[DataRequired()])
    category = SelectField('Listing Category', choices=[
                           ('Pillow', 'Pillow'), ('Blanket', 'Blanket')])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField("Create Listing")


class UpdateListingForm(FlaskForm):
    title = TextField('Listing Name', validators=[DataRequired()])
    category = SelectField('Listing Category', choices=[
                           ('Pillow', 'Pillow'), ('Blanket', 'Blanket')])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    update = SubmitField("Update")
