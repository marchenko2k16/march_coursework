from flask_wtf import Form
from wtforms import StringField, SubmitField, HiddenField, DateField, IntegerField
from wtforms import validators
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=1, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
class UserForm(Form):
    __tablename__ = 'user'
   
    Username = StringField("User : ", [
        validators.DataRequired("Please, enter Username."),
        validators.Length(3, 20, "Username should be from 3 to 20 symbols")])
    
    Password = StringField("Password : ", [
        validators.DataRequired("Please enter the Password."),
        validators.Length(3, 20, "Password should be from 3 to 20 symbols")])
    
    Company = StringField("Company Name: ", [
        validators.DataRequired("Please enter the Company Name."),
        validators.Length(3, 20, "Company Name should be from 3 to 20 symbols")])
    Department = StringField("Department Name: ", [
        validators.DataRequired("Please enter the department name."),
        validators.Length(3, 20, "department name should be from 3 to 20 symbols")])

    old_name = HiddenField()
    submit = SubmitField("Save")


class CompaniesForm(Form):
    __tablename__ = 'company'
   
    Company = StringField("Company Name: ", [
        validators.DataRequired("Please enter Company Name."),
        validators.Length(3, 20, "Company Name should be from 3 to 20 symbols")])

    old_name = HiddenField()
    submit = SubmitField("Save")

class DepartmentForm(Form):
    __tablename__ = 'department'
   
    Department = StringField("Department Name: ", [
        validators.DataRequired("Please enter Department Name."),
        validators.Length(3, 20, "Department Name should be from 3 to 20 symbols")])

    old_name = HiddenField()
    submit = SubmitField("Save")

class MessagesForm(Form):
    __tablename__ = 'message'

    MessageContent = StringField("Message Content: ", [
        validators.DataRequired("Please enter Content of the message."),
        validators.Length(3, 80, "Message content should be from 1 to 2000 symbols")])

    old_name = HiddenField()
    submit = SubmitField("Save")
