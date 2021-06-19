

import matplotlib

#import tkinter
from flask import render_template, url_for ,redirect,request,flash,session,abort
from schoolsports.forms import LoginForm,RegisterForm,AddSportForm,AddEventForm,UserAddForm,UpdateEventForm,UpdateUserForm,ChangePasswordForm,ResetRequestForm,ResetPasswordForm

from schoolsports import app,mail
from schoolsports.models import *
from schoolsports import db,migrate
from schoolsports.utils import save_picture,save_picture2
from werkzeug.security import check_password_hash,generate_password_hash
import  pandas as pd

#import pdfkit as pdf

#from tkinter import Tk, filedialog


#from tkinter import *
from jinja2 import Environment, FileSystemLoader
import os
from flask_mail import Message


import time

from datetime import date,datetime
from flask_login import current_user,login_user,logout_user,login_required



#matplotlib.use('Agg')
#config = pdf.configuration(wkhtmltopdf="C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

@app.route("/",methods=["GET","POST"])
def login():
   
    if "admin" in session:
        session.pop("admin",None)
    
   
    if current_user.is_authenticated:
        return redirect(url_for("maineventpage",name=current_user.firstname))
   
    form=LoginForm()
    
    if form.validate_on_submit():
        if form.email.data=="admin@gmail.com" and form.password.data=="admin123":
            
           
           

            
            
            
                
                
                
                
            session["admin"]=form.password.data 
            session.permanent=False  
            return redirect(url_for("admin"))
            
            
            
            
        else:
       
            user=User.query.filter_by(email=form.email.data).first()
            
            if user and user.check_password(form.password.data):
                login_user(user,remember=True)
                
                admin1=False
               
                next_page = request.args.get('next')
                return redirect(next_page) if next_page else redirect(url_for('login'))
                
               
            
                #return redirect(url_for('maineventpage',name=current_user.firstname))
            
            else:
                flash("Invalid credentials.Try again","danger")
           
    return render_template("login.html",form=form)


@app.route("/register",methods=["GET","POST"])
def register():
    
    
    form=RegisterForm()
    #print(form.aadharcard.data)
    #print(type(form.aadharcard.data))
    if form.validate_on_submit():
        if form.Myclass.data>5 and form.House.data=='NA':
            flash("Please enter your house correctly",'danger')
        else:
            if form.Myclass.data>4 and form.Section.data=='d':
                flash("Invalid Class","danger")
            else:
                user=User(firstname=form.firstname.data,lastname=form.lastname.data,
                email=form.email.data,password_hash=generate_password_hash(form.password.data),dob=form.DOB.data,
                mobileno=form.Mobile.data,House=form.House.data,Class=form.Myclass.data,Section=form.Section.data,
                Rollno=form.Rollno.data,aadharcard=str(form.aadharcard.data),gender=form.malefemale.data,grrno=form.Grrno.data,sports=form.sports.data)
                print("aadhardata is",form.aadharcard.data)
                print(type(form.aadharcard.data))
                db.session.add(user)
        # for item in form.sports.data:
            #   user.sports.append(item)
             
                db.session.commit()
            
        
            flash("Your account has been successfully created.You can now login.","success")
            time.sleep(2)
            return redirect(url_for("login"))
        
        
      
    
        
        
   
       
    return render_template("register.html",form=form)
   

@app.route("/maineventpage/<name>",methods=["GET","POST"])
@login_required
def maineventpage(name):
    
   
    return render_template("maineventpage.html",name=current_user.firstname)



@app.route("/logout")
def logout():
 
    logout_user()
    
    return redirect(url_for("login"))
   
@app.route("/admin",methods=["GET","POST"])


def admin():
    
  
    if "admin" not in session:
        
        abort(403)
        
    else:
        
        return render_template("admin.html")
    print(admin1)
    

@app.route("/adminlogout",methods=["GET","POST"])
def adminlogout():
    
    session.pop("admin", None)
    
    
    return redirect(url_for("login"))
    



@app.route("/adminhome",methods=["GET","POST"])
def adminhome():
    
    if "admin" not in session:
        abort(403)
    else:

        allevents=Event.query.all()
        
        return render_template("adminhome.html",allevents=allevents)

    print(admin1)
@app.route("/about",methods=["GET","POST"])
def about():
    
    if "admin" not in session:
        abort(403)
    else:
        return render_template("aboutadmin.html")

def savefileas(df):
    #root=Tk()
    
    #f = filedialog.asksaveasfile(mode='a',initialfile = "reports.xlsx",
    #defaultextension=".xlsx",filetypes=[("Excel Files","*.xlsx*")])
    #root.destroy()
    
    #root.mainloop()
    ab=3
    if ab==1:#if not f.name:
        try:
            writer = pd.ExcelWriter("reports.xlsx",engine='xlsxwriter')
            file=df.to_excel(writer)
            writer.save()
        except PermissionError:
            print(1)
            flash("Seems like you file is open",'danger')
    else:
        try:
            #print(f.name)
            #base=os.path.basename(f.name)
            #print(base)
            #out_path = f.name
            writer = pd.ExcelWriter(ab,engine='xlsxwriter')
            file=df.to_excel(writer)
            writer.save()
        except PermissionError:
            print(2)
            flash("Seems like you file is open",'danger')
    
    


@app.route("/viewreports",methods=["GET","POST"])
def viewreports():
    if "admin" not in session:
        abort(403)
    
        
    list2=[]
    mainlist=[]
    tables=""
    finalreportlist=[]
    excelbutton=False
    if request.method=='POST':
       
        
        sectionSelected=False
        classSelected= False
        houseselected=False
        sectionwithoutclass=False
        nostudentinlist=False
        nosport=False
            ###checking whether a a class is selected in the form. Part of form processing 
        if request.form["class1"]!='all':
            classSelected= True
                ##form data of class
            formclass=(request.form["class1"])
            ##checking whether a section is entered ###
        if request.form['section']!='all':
            sectionSelected = True
                ###form data of seciton
            formsection=(request.form["section"])

        if request.form["house"] !='all':
            houseselected= True
            formhouse=(request.form["house"])


        ##get sport form data in a loop example first badminton\
        if not request.form.getlist("sport"):
            nosport=True
        if request.form.getlist("sport") and (request.form.get("eventname")):
            flash("Select either the sport or event. Not both",'danger')
        else:
            
            for value in request.form.getlist("sport"):
                    ##getting user ids with given sport
                result1=db.engine.execute("SELECT user_id FROM usersport INNER JOIN sport ON usersport.sport_id=sport.sport_id WHERE sport_name = %(value)s",{"value":value})
                print("result 1 is",result1)
        
                    ##adding all user ids to a list
                for a in result1:
                    #print("a",a)            # for appending user ids to a list
                    list2.append(*a)
                    print("a  is",*a)
                    print("list2=",list2)
                            
                                #getting all details of the user from that user table
                    #query=db.session.query(User.grrno,User.firstname,User.lastname,User.House,User.Class,User.Section,User.Rollno).filter(User.id.in_(list2))
                    query=db.engine.execute("SELECT grrno,firstname,lastname,House,Class,Section,Rollno FROM user  WHERE user.id IN {}".format(1))
                            
                                
                                #iterating through users
                    #print("query is",query)
                    for j in query:
                        print(j)
                    


                        ######query is a list of all user details. b is going though each
                    for b in query:
                        #print("User id is",b)
                        #print("User name is",b.firstname)
                            ##abc contnains each user full object with details 1 by 1
                        abc=b.items()
                            ##contains dictionary of 1 isngle user   looping     
                        dictversion=(dict(abc))
                                    #print("Selected class dictversion is",dictversion["Class"])
                        
                                            
                            ##data in the students class reocrd lika 1,2,3,4
                        classdata=dictversion["Class"]
                            ##data in students secrion record like a,b,c,d
                        sectiondata=dictversion["Section"]
                        
                                    
                            

                        if classSelected==True and sectionSelected == True :

                            if int(classdata)==int(formclass) and formsection==sectiondata:
                                mainlist.append(dictversion)
                                print("Appended in both section and class",mainlist)
                                        

                        if classSelected==True and sectionSelected==False:
                            if int(classdata)==int(formclass) :
                                    mainlist.append(dictversion)
                                    print("Class true section false")

                                        
                        if classSelected==False and sectionSelected==True:
                                
                            sectionwithoutclass=True
                            
                        if classSelected==False and sectionSelected==False:
                            mainlist.append(dictversion)
                            print("Class false section false")
                            

                        #if (sectionSelected==False and classSelected== False) and houseselected==False:
                        #    mainlist.append(dictversion)
                          #  print("All false")
 

                            
                            
                print("\n^^^^^^MAIN LIST^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^",mainlist)                 
            if houseselected==True:
                for element in mainlist:
                    print("Element=",element)
                    print("Final list before if is",finalreportlist)
                                    #print("form data is",formhouse)
                        #print("dict data is",element['House'])
                    if element['House'] ==formhouse:
                        finalreportlist.append(element)
                        print("\nFinal list after if is",finalreportlist)
                            
                                    
            else:
                print("eneterd else")
                finalreportlist=mainlist
                                    
                
        print("\n&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&",finalreportlist)                        
                
        if not finalreportlist:
            nostudentinlist=True
        else:     
            df= pd.DataFrame.from_dict(finalreportlist)
            df.index += 1 
                            
            df.rename(columns={'grrno':"GRR NO",'firstname':'First name','lastname':'Last name'},inplace=True)
                            
                            
            tables=df.to_html(header=True,classes='table table-striped table-hover')
                            # pdf.from_string(tables, "report.pdf",configuration=config)
                    
            
                    
            if 'excelbutton' in request.form:
                print("df is",df)
               
                #root.withdraw()
                #tkt = TkThread(root)
                
                
                

                
                    #threading.Thread(target=savefileas).start()
                #root.update()
                savefileas(df)
                #root.mainloop()
                
                    
               
               
               
               
                
               
               
                
               
                #base=os.path.basename(f.name)
                #print(base)
                #f.write(str(df))
               
                #print("file is",file)
                    #end if excelbutton
                #end if finalreportlist
                        #mainloop()
            


                    
        if sectionwithoutclass==True:
                
            flash("You cannot select a section without a class",'danger')   
        if nostudentinlist==True: 
            flash("There are no students with your parameters.",'danger')              
        if nosport==True:
            flash("Please select a sport",'danger')     
        # end if request ==POST        
   
        
            
                
    events=Event.query.all()
    sports=Sport.query.all()
    return render_template("viewreports.html",events=events,sports=sports,tables=tables)
  



@app.route("/About",methods=["GET","POST"])
def about2():
    
    return render_template("aboutmain.html")


@app.route("/addsport",methods=["GET","POST"])
def addsport():
    sportlist=[]
    
    if "admin" not in session:
        abort(403)
    else:
        form=AddSportForm()
        
       
        
        
        
        
        if form.validate_on_submit():
            
            sports=form.sportsfield.data
            
            
            
            
            #if sport not in form.sportsfield.data and len(sport.events) or len(sport.player) ==0:
              #  issue=True
              #  flash("You cannot remove a sport which has existing events or users. Please select the missing sport.") 
            
            
                
            if not len(Sport.query.all()) :     
                for a in sports:
                    sport=Sport(sport_name=a)
                    
                    
                    db.session.add(sport)
                    db.session.commit()
                
                flash("The sports have been added successfully!","light")
                
                #if sport.query.all has data;
            
                
                    #if a not in sportlist and len(sport.events)!=0 or len(sport.player) !=0:
                    #    sportnotthere.append(a)
                    #    if sportnotthere is not []:
                     #       flash("You cannot remove a sport which has existing events or users. Please select the missing sport.","danger")
                    #else:
                        
                    
            elif len(Sport.query.all()):
               
               
                invalid_selection=False
                invalid_sport=[]
                for sport in Sport.query.all():        
                    print("sport from database is",sport)
                    if str(sport) not in form.sportsfield.data and len(sport.events)!=[] :

                        print("form data is",form.sportsfield.data)
                        print("sport event is",sport.events)
                        invalid_selection = True
                        invalid_sport.append(sport)
                        
                if  invalid_selection==False : 
                    db.session.query(Sport).delete()
                    db.session.commit()     
                    for i in form.sportsfield.data:

                        sport=Sport(sport_name=i)
                        
                        
                        db.session.add(sport)
                        db.session.commit()
                        

                print("Invalid sport is",invalid_sport)
                print (invalid_selection)
                if invalid_selection==True:
                    
                    flash("You cannot remove a sport which has existing events or users. Please check the sports. ","danger")
                    
                else:
                    
                    flash("The sports have been added successfully!","light")
            
            #else:
                #db.session.query(Sport).delete()
               # for a in sports:
                #    sport=Sport(sport_name=a)
                #    db.session.add(sport)
                #    db.session.commit()
                        
               # flash("The sports have been updated successfully!","light")
           


       
       

    return render_template("addsport.html",form=form)


@app.route("/addevent",methods=["GET","POST"])
def addevent():
    
   
    if "admin" not in session:
        abort(403)
    else:

        form=AddEventForm()
        if form.validate_on_submit():
            
            admin1=True
            error=False
            if form.eventstartdate.data>form.eventenddate.data:
               flash("End date of the event cannot be earlier than the start date.","danger")
               error=True
            if form.registrationstartdate.data>form.registrationenddate.data:
                flash("Registration end date of the event cannot be earlier than the  Registration start date.","danger")
                error=True
            if form.registrationstartdate.data <= date.today() or  form.registrationenddate.data <= date.today() or form.eventstartdate.data  <= date.today() or form.eventenddate.data <= date.today():
       
               error=True
               flash("Date cannot be a past date.","danger")

            if form.registrationenddate.data >= form.eventstartdate.data:
                error=True
                flash("Last date of registration must be before event starting date","danger")
            if form.registrationstartdate.data >= form.eventstartdate.data:
                error=True
                flash("Beginning of registration must be before event starting date","danger")    
            else:
               if form.eventpic.data:
                   picture_file = save_picture(form.eventpic.data)

                   if error==False:
                        event=Event(event_title=form.eventtitle.data,event_description=form.eventdescription.data,startdate=form.eventstartdate.data,enddate=form.eventenddate.data
                        ,registrationstart=form.registrationstartdate.data,registrationend=form.registrationenddate.data,organiser=form.Organiser.data,venue=form.venue.data,profilepic=picture_file,status="Active")
                        db.session.add(event)
                        db.session.commit()
                        event.sport.append(form.sports.data)
                        db.session.commit()
                        flash("Event successfully added","success")

                    

               else: 
                    if error==False:
                        event=Event(event_title=form.eventtitle.data,event_description=form.eventdescription.data,startdate=form.eventstartdate.data,enddate=form.eventenddate.data
                        ,registrationstart=form.registrationstartdate.data,registrationend=form.registrationenddate.data,organiser=form.Organiser.data,venue=form.venue.data,status="Active")
                        db.session.add(event)
                        db.session.commit()
                        event.sport.append(form.sports.data)
                        db.session.commit()
                        flash("Event successfully added","success")
               
               

        return render_template("addevent.html",form=form)



@app.route("/AddUserSport",methods=["GET","POST"])
@login_required
def addsportuser():
    
   
    
        
    form=UserAddForm()
        
        
        
    if form.validate_on_submit:
        if form.sport.data is None:
            pass
            
        else:
            print("1")
                
            if form.sport.data in current_user.sports:
                flash("The sport already exists","danger")
            #sportname=Sport(sport_name=form.sport.data)
           
            #print("type of the sport object created is",type(sportname))
            #print(sportname)    
            else:
                current_user.sports.append(form.sport.data)
                print("current user.sports after appending is",current_user.sports)
                    
                db.session.commit()
                flash("Sport successfully added. Submit the form again to add another sport.","success")

    
    
        
    
    return render_template("addsportsuser.html",form=form)



@app.route("/<name>/home",methods=["GET","POST"])
@login_required
def home(name):
    mylist=[]
    eventset=[]
    a=current_user.id 
    
    query=db.session.query(usersport.c.sport_id).join(User).filter(User.id==current_user.id) 
    
   
    for z in query:
        print("z=",z)
        querymain=db.engine.execute("SELECT sportevent.event_id FROM sportevent WHERE  sportevent.sport_id IN (?)",(z))

        for abc in  querymain:
            mylist.append(abc)
        
   
    for event in mylist:
        fulleventdetail=db.engine.execute("SELECT * FROM events WHERE events.event_id=?",(event))
        for realevent in fulleventdetail:
           eventset.append(realevent)
           

   
    
 
    
    #queryevent=db.session.query(sportevent).join(usersport).filter(sport.c.sport_id==1)
    #for z in queryevent:
     #   print(z)
    
    return render_template("userhome.html",eventset=eventset)




@app.route("/Info/<int:eventid>",methods=["GET","POST"])
def info(eventid):
    
    
    wantedevent=Event.query.get_or_404(eventid)
    datenow=date.today()
    if request.method=='POST':
        if not wantedevent in current_user.events:
            current_user.events.append(wantedevent)

            db.session.commit()
            flash("You have successfully registered for this event.",'success')
        else:
                
            flash("You have already registered for this event",'danger')


   
    return render_template("eventinfo.html",wantedevent=wantedevent,datenow=datenow)

# print the dates

@app.route("/Admin/<int:eventid>/info",methods=["GET","POST"])

def admininfo(eventid):
    
    if "admin" not in session:
        abort(403)
    else:
        
        wantedevent=Event.query.get_or_404(eventid)
        datenow=date.today()
    


   
    return render_template("admineventinfo.html",wantedevent=wantedevent,datenow=datenow)

@app.route("/admin/edit/<int:eventid>",methods=["GET","POST"])
 
def editevent(eventid):
    
    if "admin" not in session:
        abort(403)
    else:
        
       
        theevent=Event.query.get_or_404(eventid)
        datenow=date.today()
        form=UpdateEventForm()
        error=False
        if form.validate_on_submit():
            
            if request.form['bday3']>request.form['bday4']:
               error=True
               flash("End date of the event cannot be earlier than the start date.","danger")
               
            if request.form['bday1']>request.form['bday2']:
                error=True
                flash("Registration end date of the event cannot be earlier than the  Registration start date.","danger")
                
            if datetime.strptime(request.form['bday1'],'%Y-%m-%d').date() <= date.today() or  datetime.strptime(request.form['bday2'],'%Y-%m-%d').date() <= date.today() or datetime.strptime(request.form['bday3'],'%Y-%m-%d').date()  <= date.today() or datetime.strptime(request.form['bday4'],'%Y-%m-%d').date() <= date.today():
       
               error=True
               flash("Date cannot be a past date.","danger")

            if request.form['bday2'] >=request.form['bday3']:
                error=True
                flash("Last date of registration must be before event starting date","danger")
            if request.form['bday1'] >= request.form['bday3']:
                error=True
                flash("Beginning of registration must be before event starting date","danger")  
            
           
            
            if form.eventpic.data and error==False:
               
                picfile=save_picture(form.eventpic.data)
                theevent.profilepic=picfile
                theevent.event_title=form.eventname.data
                theevent.event_description=form.eventinstructions.data
                theevent.organiser=form.eventorganiser.data
                theevent.venue=form.eventvenue.data
                theevent.registrationstart= datetime.strptime(request.form['bday1'],'%Y-%m-%d')
                theevent.registrationend=datetime.strptime(request.form['bday2'],'%Y-%m-%d')
                theevent.startdate=datetime.strptime(request.form['bday3'],'%Y-%m-%d')
                theevent.enddate=datetime.strptime(request.form['bday4'],'%Y-%m-%d')
                db.session.commit()
            
                
                flash("Event successfully updated.",'success')
            if not form.eventpic.data and error==False:
                theevent.event_title=form.eventname.data
                theevent.event_description=form.eventinstructions.data
                theevent.organiser=form.eventorganiser.data
                theevent.venue=form.eventvenue.data
                theevent.registrationstart= datetime.strptime(request.form['bday1'],'%Y-%m-%d')
                theevent.registrationend=datetime.strptime(request.form['bday2'],'%Y-%m-%d')
                theevent.startdate=datetime.strptime(request.form['bday3'],'%Y-%m-%d')
                theevent.enddate=datetime.strptime(request.form['bday4'],'%Y-%m-%d')
                db.session.commit()
            
                
                flash("Event successfully updated.",'success')
        elif request.method=="GET":
            form.eventname.data=theevent.event_title
            form.eventorganiser.data=theevent.organiser
            form.eventinstructions.data=theevent.event_description
            form.eventvenue.data=theevent.venue
            
            #form.registrationstartdate=theevent.registrationstart
            
        return render_template("editevent.html",theevent=theevent,form=form)

#@app.route()

#def registermain(eventid):
  #  print("Reacheds")
    #event=Event.query.get_or_404(eventid)
    #if event in current_user.events:
    #    pass
    #else:
    #    current_user.events.append(event)
    #    db.session.commit()



    
#app.jinja_env.globals.update(toexcel=toexcel )


@app.route("/<name>/profile",methods=["GET","POST"])
@login_required
def useraccount(name):
    form=UpdateUserForm()
    if form.validate_on_submit():
       if form.profile.data:
           image=save_picture2(form.profile.data)
           current_user.image_file=image
           current_user.email=form.email.data
           current_user.mobileno=form.Mobile.data
           current_user.House=form.House.data
           current_user.Class=form.Myclass.data
           current_user.Section=form.Section.data
           current_user.aadharcard=form.aadharcard.data
           current_user.Rollno=form.Rollno.data
           db.session.commit()
           flash("You successfully updated your profile",'success')
       if not form.profile.data:
           
           current_user.email=form.email.data
           current_user.mobileno=form.Mobile.data
           current_user.House=form.House.data
           current_user.Class=form.Myclass.data
           current_user.Section=form.Section.data
           current_user.aadharcard=form.aadharcard.data
           current_user.Rollno=form.Rollno.data
           db.session.commit()
           flash("You successfully updated your profile",'success')

    elif request.method=="GET":
        form.email.data=current_user.email
        form.Mobile.data=current_user.mobileno
        form.House.data=current_user.House
        form.Myclass.data=current_user.Class
        form.Section.data=current_user.Section
        form.aadharcard.data=current_user.aadharcard
        form.Rollno.data=current_user.Rollno
    return render_template("useraccount.html",form=form)


@app.route("/change_password/<name>",methods=["GET","POST"])
@login_required
def changepassword(name):
    form=ChangePasswordForm()
    if form.validate_on_submit():
        current_user.password_hash=generate_password_hash(form.newpassword.data)
        db.session.commit()
        flash("Password changed successfully",'success')
       

    return render_template("Changepassword.html",form=form)

def send_reset_email(user):
    token=user.get_reset_token()
    msg=Message("Password  Reset Request",sender='anish.kamath2005@gmail.com',recipients=[user.email])
    msg.body=f'''To reset your password visit the following link:
    {url_for('reset_password',token=token,_external=True)}
    If you did not make this request please ignore this message.
    '''
    mail.send(msg)
@app.route("/reset_request",methods=["GET","POST"])
def reset_request():
    form=ResetRequestForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.emailmain.data).first()
        if user is None:
            flash("No account exists with this email. Pls register first.",'danger')
        else:
            send_reset_email(user)
            flash("An email has been sent with instructions to reset your password",'success')
            time.sleep(2)
            return redirect(url_for('login'))

    return render_template("resetrequest.html",form=form)

@app.route("/reset_password/<token>",methods=["GET","POST"])
def reset_password(token):
    user=User.verify_reset_token(token)
    
    if user is None:
        flash("Invalid or expired token",'warning')
        return redirect(url_for('reset_request'))
    form=ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password=generate_password_hash(form.newpassword.data)
        user.password_hash=hashed_password
        db.session.commit()
        flash("Your password has been updated",'success')
        return redirect(url_for("login"))

    


    return render_template("resetpassword.html",form=form)

@app.route("/events/<name>")
def myevents(name):
    events=current_user.events
    print(events)
    return render_template("myevents.html",events=events)
