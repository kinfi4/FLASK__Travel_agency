from wtforms import StringField, FloatField, DateField, SelectField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from datetime import date


class AddEditTourForm(FlaskForm):
    tour_name = StringField('Tour name', validators=[DataRequired()])
    hotel_name = StringField('Hotel name', validators=[DataRequired()])
    tour_includes = StringField('Tour includes', validators=[DataRequired()])
    day_cost = FloatField('Day cost', validators=[DataRequired()])
    submit = SubmitField('')


class AddEditClientForm(FlaskForm):
    first_name = StringField('First name', validators=[DataRequired()])
    second_name = StringField('Second name', validators=[DataRequired()])
    passport = StringField('Passport', validators=[DataRequired()])
    register_date = DateField('Register date', validators=[DataRequired()], default=date.today())
    submit = SubmitField('')


class AddEditOrderForm(FlaskForm):
    client_name = SelectField('Client name', validators=[DataRequired()])
    tour_name = SelectField('Tour name', validators=[DataRequired()])
    days = IntegerField('Days', validators=[DataRequired()], default=7)
    add_date = DateField('Add date', validators=[DataRequired()], default=date.today())
    submit = SubmitField('')
