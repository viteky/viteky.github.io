from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import TextAreaField, StringField, PasswordField, SubmitField, BooleanField, DateField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import email_validator
from credits.models import User, Claim, Role, Item


class registrationForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    first_name = StringField("First Name",
                            validators=[DataRequired(), Length(min=2)])
    last_name = StringField("Last Name",
                        validators=[DataRequired(), Length(min=2)])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField("Confirm Password",
                            validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("Username is taken.")
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("Email is taken.")


class loginForm(FlaskForm):
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    password = PasswordField("Password",
                             validators=[DataRequired(), Length(min=6)])
    remember = BooleanField("Remember Me")
    submit = SubmitField("Log In")


class updateAccountForm(FlaskForm):
    username = StringField("Username", 
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField("Email",
                        validators=[DataRequired(), Email()])
    picture = FileField("Update Profile Picture", validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField("Update")

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("Username is taken.")
    
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("Email is taken.")
            

class newClaimForm(FlaskForm):
    customer_id = StringField("Customer ID", validators=[DataRequired()])
    invoice_num = StringField("Invoice No.", validators=[DataRequired()])
    invoice_date = DateField("Invoice Date", validators=[DataRequired()])
    run_num = StringField("Run No.", validators=[DataRequired()])
    notify_date = DateField("Notified Date", validators=[DataRequired()])
    driver = StringField("Driver")
    notes = TextAreaField("Notes")
    submit = SubmitField("Log Claim")

    def validate_invoice_num(self, invoice_num):
        invoice = Claim.query.filter_by(invoice_num=invoice_num.data).first()
        if invoice:
            raise ValidationError("Claim already exists for this invoice")
