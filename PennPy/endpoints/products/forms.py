from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField, TextField, TextAreaField, SelectField
from wtforms.validators import DataRequired


class CreateListingForm(FlaskForm):
    title = TextField('Product Name', validators=[DataRequired()])
    category = SelectField('Product Category', choices=[
                           ('Pillow', 'Pillow'), ('Blanket', 'Blanket')])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    submit = SubmitField("Create Product")


class UpdateListingForm(FlaskForm):
    title = TextField('Product Name', validators=[DataRequired()])
    category = SelectField('Product Category', choices=[
                           ('Pillow', 'Pillow'), ('Blanket', 'Blanket')])
    price = IntegerField('Price', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    update = SubmitField("Update")
