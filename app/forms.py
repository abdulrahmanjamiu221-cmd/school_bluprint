from flask_wtf import FlaskForm
from wtforms import BooleanField, FloatField, IntegerField, PasswordField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log in")


class SchoolForm(FlaskForm):
    name = StringField("School name", validators=[DataRequired(), Length(min=2, max=150)])
    code = StringField("School code", validators=[DataRequired(), Length(min=2, max=50)])
    address = StringField("Address", validators=[Optional(), Length(max=250)])
    contact_email = StringField("Contact email", validators=[Optional(), Email()])
    phone = StringField("Phone", validators=[Optional(), Length(max=50)])
    submit = SubmitField("Save school")


class StudentForm(FlaskForm):
    admission_number = StringField("Admission number", validators=[DataRequired(), Length(min=1, max=50)])
    first_name = StringField("First name", validators=[DataRequired(), Length(min=1, max=80)])
    last_name = StringField("Last name", validators=[DataRequired(), Length(min=1, max=80)])
    gender = SelectField("Gender", choices=[("male", "Male"), ("female", "Female")], validators=[DataRequired()])
    class_id = IntegerField("Class ID", validators=[DataRequired()])
    submit = SubmitField("Save student")


class ResultEntryForm(FlaskForm):
    ca = FloatField("CA", validators=[Optional(), NumberRange(min=0, max=100)])
    test = FloatField("Test", validators=[Optional(), NumberRange(min=0, max=100)])
    assignment = FloatField("Assignment", validators=[Optional(), NumberRange(min=0, max=100)])
    practical = FloatField("Practical", validators=[Optional(), NumberRange(min=0, max=100)])
    exam = FloatField("Exam", validators=[Optional(), NumberRange(min=0, max=100)])
    remarks = TextAreaField("Remarks", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Save result")


class PaymentForm(FlaskForm):
    student_id = IntegerField("Student ID", validators=[DataRequired()])
    reference = StringField("Payment reference", validators=[DataRequired(), Length(min=2, max=120)])
    amount = FloatField("Amount", validators=[DataRequired(), NumberRange(min=0)])
    method = SelectField("Method", choices=[("cash", "Cash"), ("bank", "Bank transfer"), ("pos", "POS"), ("other", "Other")], validators=[DataRequired()])
    notes = TextAreaField("Notes", validators=[Optional(), Length(max=500)])
    submit = SubmitField("Record payment")
