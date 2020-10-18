from flask_wtf import FlaskForm
from datetime import datetime
from flask_wtf.file import FileField, FileAllowed
from wtforms import (
    StringField,
    PasswordField,
    SubmitField,
    IntegerField,
)
from wtforms.validators import DataRequired, ValidationError

from Website.models import User

date_now = datetime.now()


class RegistrationForm(FlaskForm):
    first = StringField("First Name", validators=[DataRequired()])
    last = StringField("Last Name", validators=[DataRequired()])
    age = IntegerField("Age", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    phone = IntegerField("Phone #", validators=[DataRequired()])
    profile_pic = FileField("Profile Pic", validators=[FileAllowed(["jpg", "png"])])
    submit = SubmitField("Submit")


class ConfirmData(FlaskForm):

    email = StringField("Email", validators=[DataRequired()])
    phone = IntegerField("Phone #", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")

    def validate_phone(self, phone):

        phone_no = User.query.filter_by(phone=phone.data).first()

        if phone_no:
            raise ValidationError("")

    def validate_email(self, email):

        email = User.query.filter_by(email=email.data).first()

        if email:
            raise ValidationError("")


class YesandNoForm(FlaskForm):
    No = SubmitField("No")
    Yes = SubmitField("Yes")
