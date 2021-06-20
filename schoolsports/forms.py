
from schoolsports.models import viewreportquery
from wtforms.fields.simple import TextAreaField
from schoolsports.models import *


from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField,PasswordField, BooleanField,IntegerField,SelectField,RadioField,SelectMultipleField,widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError,AnyOf,NumberRange,Optional,InputRequired
from flask_login import current_user
from wtforms.fields.html5 import DateField,DateTimeField
from wtforms.fields.html5 import EmailField
from wtforms.ext.sqlalchemy.fields import QuerySelectField,QuerySelectMultipleField
import datetime
from wtforms_alchemy import PhoneNumberField

#data=viewreportquery(form.eventnames.data)




class LoginForm(FlaskForm):
    email = StringField(
                        validators=[DataRequired(), Email()],render_kw={"placeholder": "Email"})
    password = PasswordField( validators=[DataRequired()],render_kw={"placeholder": "Password"},id="password")
    check = BooleanField('Show password',id="check")
    
    submit = SubmitField('Login')






def check_class_section(form,field):
        if Myclass.data>=5 and Section.data==D:
            raise ValidationError("There is no section for this class")
def check_email_domain(form,field):
    string=field.data
    if "@" in field.data:
        domain=string.split("@")[1]
        if domain!="vidyavalley.com":
            raise ValidationError("Email must be a vidyavalley email.") 
    else:
       pass 

    
                    

def check_aadharcard(form ,field):
    
    if len(field.data)!=12 :
        
        raise ValidationError("Aadhar card number must be a 12 digit number ")

def check_first_last(form,field):
   
    
    abc= any(char.isdigit() for char in field.data)
    if abc==True:
        raise ValidationError("Please enter a valid name without a number.")
    #if abc==int:

def check_mobile(form,field):
   if  len((field.data))!=10:
       raise ValidationError("Enter a valid mobile number")

def check_datetime(form,field):
    
 

    x=datetime.datetime.now()
    y=x.strftime("%d-%m-%y")
    date_time_obj = datetime.datetime.strptime(y, '%d-%m-%y')
    abc=date_time_obj.date()
    
    if field.data>abc:
        raise ValidationError("Your date of birth cannot be a future date. ")
def pass_length(form,field):
    if len(field.data)<8:
        raise ValidationError("The password must be minimum 8 characters long.")

def check_len_grr(form,field):
    
  if len(str(field.data))!=4:
    raise ValidationError("GRR No must be a 4 digit number")
      
      
    
    
   # if len(field.data)>4:
    #    raise ValidationError("GRR Number must be maximum 4 digits")


class RegisterForm(FlaskForm):
    firstname=StringField(validators=[InputRequired(),check_first_last],render_kw={"placeholder":"First name"})
    lastname=StringField(validators=[InputRequired(),check_first_last],render_kw={"placeholder":"Last name"})
    email = StringField(validators=[InputRequired(), Email(),check_email_domain],render_kw={"placeholder": "Email(School email only)"})
    password = PasswordField( validators=[InputRequired(),pass_length],render_kw={"placeholder": "Password(Min 8 characters)"})
    DOB=DateField("Date of Birth",validators=[check_datetime,InputRequired()],format='%Y-%m-%d',render_kw={"placeholder": "DOB"})
    Mobile=StringField(validators=[InputRequired(),check_mobile],render_kw={"placeholder": "Mobile No"})
    House=SelectField(u'House', validators=[Optional()], choices=[('puma', 'Puma'), ('cheetah', 'Cheetah'), ('sher', 'Sher'),("jaguar","Jaguar"),("NA","Not applicable")])
    Myclass=IntegerField(validators=[InputRequired(),AnyOf(values=[1,2,3,4,5,6,7,8,9,10])],render_kw={"placeholder": " Class"})
   # language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    Section=SelectField(u'Section', choices=[('a', 'A'), ('b', 'B'), ('c', 'C'),("d","D")])
    Rollno=IntegerField(validators=[InputRequired(),NumberRange(min=1,max=40,message="Roll no must be between 1 and 40")],render_kw={"placeholder": "Roll no"})
    aadharcard=StringField(validators=[InputRequired(),check_aadharcard],render_kw={"placeholder": "Aadhar card no"})
   
    Grrno=IntegerField(validators=[InputRequired(), check_len_grr],render_kw={"placeholder":"GRRNO"})
    malefemale = RadioField(label="Gender",validators=[InputRequired(message="Please choose one option")], choices=[('male','Male'),('female','Female')],default="male")
    confirmpassword = PasswordField( validators=[DataRequired(),EqualTo("password")],render_kw={"placeholder": "Confirm Password"})
    sports= QuerySelectMultipleField("Choose sports by clicking CTRL Key and selecting the options",validators=[InputRequired()],query_factory=choice_query,allow_blank=False,get_label="sport_name")
    #sport=MultiCheckboxField(u"CHOOSE SPORT",choices=tag, render_kw={"style": "font-weight:bolder;"})#


    submit = SubmitField('Register')



    def validate_Grrno(self, Grrno):
        user = User.query.filter_by(grrno=Grrno.data).first()
        if user:
            raise ValidationError('That GRRNO is already in use. Please choose a different one.')
   

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

    def validate_Mobile(self, Mobile):
        user = User.query.filter_by(mobileno=Mobile.data).first()
        if user:
            raise ValidationError('That Phone number  is taken. Please choose a different one.')

    def validate_aadharcard(self, aadharcard):
        user = User.query.filter_by(aadharcard=aadharcard.data).first()
        if user:
            raise ValidationError('That Aadharcard number is already taken. Please choose a different one.')


    #def validate_
class MultiCheckboxField(SelectMultipleField):
    widget = widget=widgets.TableWidget(with_table_tag=True)
    option_widget = widgets.CheckboxInput()

            
class AddSportForm(FlaskForm):
   sports = [('badminton','Badminton'), ('tennis','Tennis'), ('taekwondo','Taekwondo'),('swimming','Swimming'),('handball','Handball'),('volleyball','Volleyball')
   ,('basketball','Basketball'),('chess','Chess'),('athletics','Athletics'),('tabletennis','Table tennis')]
   sportsfield = MultiCheckboxField('Select all the sports', choices=sports,validators=[DataRequired()]) 

   submit = SubmitField('Add Sports')


def verify_date(form,field):
    pass
class AddEventForm(FlaskForm):
    eventtitle=StringField(validators=[InputRequired()],render_kw={"placeholder": "Event Title"})
    eventstartdate=DateField("Starting date of event",validators=[InputRequired()],format='%Y-%m-%d',render_kw={"placeholder": "Start Date"})
    eventenddate=DateField("Ending date of event",validators=[InputRequired()],format='%Y-%m-%d',render_kw={"placeholder": "End Date"})
    registrationstartdate=DateField("Registration Start Date",validators=[InputRequired()],format='%Y-%m-%d',render_kw={"placeholder": "Start date"})
    registrationenddate=DateField("Registration End Date",validators=[InputRequired()],format='%Y-%m-%d',render_kw={"placeholder": "End date"})
    eventdescription=TextAreaField(validators=[InputRequired()],render_kw={"placeholder": "Event description"})
    sports=QuerySelectField(query_factory=choice_query,allow_blank=False,get_label="sport_name")
    venue=TextAreaField(validators=[InputRequired()],render_kw={"placeholder": "Event Venue"})
    Organiser=StringField(validators=[InputRequired()],render_kw={"placeholder": "Organiser name"})
    eventpic=FileField('Upload Optional Event Form or Image', validators=[Optional(), FileAllowed(['jpg', 'png',"Jpeg","JPEG","jpeg"])])
    submit = SubmitField('Add Event')


    
class UserAddForm(FlaskForm):
    sport= QuerySelectField(query_factory=choice_query,allow_blank=False,get_label="sport_name")
    
    submit = SubmitField('Add Sport')

class UpdateEventForm(FlaskForm):
    eventname=StringField()
    eventinstructions=TextAreaField()
    eventorganiser=StringField()
    eventvenue=StringField()
    eventstartdate=DateField("If no change is needed keep this field blank",validators=[Optional()])
    eventenddate=DateField("If no change is needed keep this field blank",validators=[Optional()])
    registrationstartdate=DateField("If no change is needed keep this field blank",validators=[Optional()])
    registrationenddate=DateField("If no change is needed keep this field blank",validators=[Optional()])
    eventpic=FileField('Update Image', validators=[Optional(), FileAllowed(['jpg', 'png',"Jpeg","JPEG","jpeg"])])
    submit=SubmitField("Update")

3#3lass ViewReportForm(FlaskForm):
    
  #  myclass=SelectField(u'Class', validators=[Optional()], choices=[('all', 'All '), ('1st', '1'), ('2nd', '2'),("3rd","3")],default=('all','All ') )
  #  Section=SelectField(u'Section', choices=[("all ","All "),('a', 'A'), ('b', 'B'), ('c', 'C'),("d","D")],default=('all ',"All "))
  #  House=SelectField(u'House', validators=[Optional()], choices=[("all ","All "),('puma', 'Puma'), ('cheetah', 'Cheetah'), ('sher', 'Sher'),("jaguar","Jaguar")],default=('all ',"All "))
  #  sports=QuerySelectMultipleField("Sports",query_factory=choice_query,allow_blank=False,get_label="sport_name")
 #   eventnames=QuerySelectMultipleField("Event names",query_factory=Eventquery,allow_blank=False,get_label="event_title")
 #   submit=SubmitField("Generate excel report")
def check_Mobile_data_form_(form,field):
    if type(field.data)!=int or len(str(field.data))!=10:
        raise ValidationError("Enter a valid mobile number")

class UpdateUserForm(FlaskForm):
    profile=FileField("Update profile", validators=[Optional(), FileAllowed(['jpg', 'png',"Jpeg","JPEG","jpeg"])])
    email = StringField("Email",validators=[InputRequired(), Email(),check_email_domain])
    Mobile=IntegerField("Mobile no",validators=[InputRequired(),check_Mobile_data_form_])
    House=SelectField( "House",validators=[Optional()], choices=[('puma', 'Puma'), ('cheetah', 'Cheetah'), ('sher', 'Sher'),("jaguar","Jaguar")])
    Myclass=IntegerField("Class",validators=[InputRequired(),AnyOf(values=[1,2,3,4,5,6,7,8,9,10])])
   # language = SelectField(u'Programming Language', choices=[('cpp', 'C++'), ('py', 'Python'), ('text', 'Plain Text')])
    Section=SelectField("Section", choices=[('a', 'A'), ('b', 'B'), ('c', 'C'),("d","D")])
    Rollno=IntegerField("Rollno",validators=[InputRequired(),NumberRange(min=1,max=40,message="Roll no must be between 1 and 40")])
    aadharcard=StringField("Aadharcard no",validators=[InputRequired(),check_aadharcard])
    submit=SubmitField("Update details")
    #password = PasswordField( validators=[InputRequired(),pass_length])
  
    
class ChangePasswordForm(FlaskForm):
    newpassword=PasswordField("New Password")  
    confpassword=PasswordField("Confirm Password",validators=[EqualTo('newpassword',message="Confirm password must be equal to Password"),pass_length])        
    submit=SubmitField("Change Password") 


class ResetRequestForm(FlaskForm):
    emailmain=StringField(validators=[InputRequired(),check_email_domain],render_kw={"placeholder": "Email"})
    submit=SubmitField("Send email ")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        print(user)
        if user is None:
            raise ValidationError('That is no account with that email. Please register first.')

class ResetPasswordForm(FlaskForm):
    newpassword=PasswordField("New Password",render_kw={"placeholder": "Enter new Password"})  
    confpassword=PasswordField("Confirm Password",validators=[EqualTo('newpassword',message="Confirm password must be equal to Password"),pass_length],render_kw={"placeholder": "Confirm Password"})        
    submit=SubmitField("Change Password") 

