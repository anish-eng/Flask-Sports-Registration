
from schoolsports import db,login_manager,app
from werkzeug.security import check_password_hash,generate_password_hash
from flask_login import UserMixin,current_user
from datetime import datetime
from schoolsports.forms import *
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



usersport=db.Table("usersport",

db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
db.Column("sport_id",db.Integer,db.ForeignKey("sport.sport_id")))

userevent=db.Table("userevent",
db.Column("user_id",db.Integer,db.ForeignKey("user.id")),
db.Column("event_id",db.Integer,db.ForeignKey("events.event_id")))


sportevent=db.Table("sportevent",
db.Column("sport_id",db.Integer,db.ForeignKey("sport.sport_id")),
db.Column("event_id",db.Integer,db.ForeignKey("events.event_id")))


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    firstname=db.Column(db.String,nullable=False)
    
    lastname=db.Column(db.String,nullable=False)
    email=db.Column(db.String,unique=True,index=True,nullable=False)
    password_hash = db.Column(db.String(128))
    dob=db.Column(db.DateTime,nullable=False)
    mobileno=db.Column(db.String(10),nullable=False,unique=True)
    House=db.Column(db.String(10),nullable=True)
    Class=db.Column(db.Integer,nullable=False)
    Section=db.Column(db.String(1),nullable=False)
    Rollno=db.Column(db.Integer,nullable=False)
    aadharcard=db.Column(db.String(12),nullable=False,unique=True)
    gender = db.Column(db.Enum('male', 'female',name='gender' ))
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    grrno=db.Column(db.Integer,nullable=False,unique=True)
    sports=db.relationship("Sport",secondary=usersport, backref="player",lazy=True)
    events=db.relationship("Event",secondary=userevent, backref="participant",lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')


    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    def __repr__(self):
        return f"Firstname is{self.firstname}Email is {self.lastname}Date of birth is{self.dob}Class is {self.Class}Aadhar card is {self.aadharcard}"
            

    def check_password(self,password):
        
        return check_password_hash(self.password_hash,password)






class Sport(db.Model):
    __tablename__="sport"
    sport_id=db.Column(db.Integer,primary_key=True)
    sport_name=db.Column(db.String)
    sportevent=db.relationship("Event",secondary=sportevent,backref="sport",lazy=True)
    
    def __repr__(self):
        return f"{self.sport_name}"

def choice_query():
    return Sport.query.all()

def viewreportquery(data):
    mylist=[]
    finaleventlist=[]
    result=db.engine.execute("SELECT event_id from sportevent INNER JOIN sport ON sport.sport_id=sportevent.sport_id WHERE sport_name=? ",(data))
    for a in result:
        print("a is",a)
        if a==None:
            break
        else:
            mylist.append(a)
            print("mylist is",mylist)
    
        for item in mylist:
            print("item is",item)
            
            result2=db.engine.execute("SELECT event_title from events WHERE  events.event_id=?",(item))

            for n in result2:
                print("n is",n)
                
                finaleventlist.append(n)
                mylist=[]
                
    return( finaleventlist)

class Event(db.Model):
    __tablename__="events"
    event_id=db.Column(db.Integer,primary_key=True)
   
    event_title=db.Column(db.String,nullable=False)
    event_description=db.Column(db.Text,nullable=False)
    startdate=db.Column(db.Date,nullable=False)
    enddate=db.Column(db.Date,nullable=False)
    registrationstart=db.Column(db.Date,nullable=False)
    registrationend=db.Column(db.Date,nullable=False)
    status=db.Column(db.Enum('Active', 'Expired',name="Status",server_default="Active" ))
    organiser=db.Column(db.Text,nullable=False)
    venue=db.Column(db.Text,nullable=False)
    profilepic=db.Column(db.String(20), nullable=False, default='Eventprofile.png')
    eventsport=db.relationship("Sport",secondary=sportevent,backref="events",lazy=True)



@app.template_filter('datetimeformat')
def datetimeformat(value,format='%Y-%m-%d'):
    abc= datetime.strptime(value,format)
    return abc.strftime("%d-%B-%Y")
   





 
