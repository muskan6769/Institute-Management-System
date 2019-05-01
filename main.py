from flask import Flask,render_template ,flash ,url_for , redirect,jsonify
from forms import RegistrationForm,CourseRegisterForm,StudLoginForm,FacLoginForm,AdminLoginForm,FacRegisterForm,ProgrammeRegisterForm
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask import request
import json
# from __init__ import current_user

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

bcrypt =Bcrypt(app)
import cx_Oracle
password='Sweet130118'
host='localhost'
port=1522
sid='orcl1'
user='system'

sid = cx_Oracle.makedsn(host,port,sid=sid)

cstr = 'oracle://{user}:{password}@{sid}'.format(
    user=user,
    password=password,
    sid=sid
)

engine =  create_engine(
    cstr,
    convert_unicode=False,
    pool_recycle=10,
    pool_size=50,
    echo=True
)

class User:
    def __init__(self,Name,isFac,isStud):
        self.Name = Name
        self.isFac = isFac
        self.isStud = isStud

u= User("muskan",True,False)

@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/account")
def account():
    return render_template('account.html')

@app.route("/logout")
def logout():
    return redirect(url_for('home'))

@app.route("/Studlogin", methods=['GET', 'POST']) 
def Studlogin(): 
    form=StudLoginForm()
    if form.validate_on_submit():
        reg_password = engine.execute("select Name,Password from Student_Tab where Roll_No = :a",{'a':form.rollNo.data})
        for row in reg_password:
            reg_details=row
        print(reg_details)
        if bcrypt.check_password_hash(reg_details[1] , form.password.data) :
            flash('Login successful.', 'success')
            current_user = reg_details[0]
            return redirect(url_for('profile',current_user= current_user,Type_of_User="Student"))
        else:
            flash('Login Unsuccessful. Please check EnrollNo and password', 'danger')  
    return render_template('Studlogin.html',title='StudLogin', form=form)

@app.route("/Faclogin", methods=['GET', 'POST']) 
def Faclogin():     
    form=FacLoginForm()
    if form.validate_on_submit():
        reg_password = engine.execute("select Fac_Code,Password from Faculty_Tab where Fac_Code = :a",{'a':form.facCode.data})
        for row in reg_password:
            reg_details=row
        if bcrypt.check_password_hash(reg_details[1] , form.password.data) :
            flash('Login successful.', 'success')
            current_user = reg_details[0]
            return redirect(url_for('profile',current_user= current_user,Type_of_User="Faculty"))
        else:
            flash('Login Unsuccessful. Please check EnrollNo and password', 'danger')  
    return render_template('Faclogin.html',title='FacLogin', form=form)

@app.route("/adminlogin", methods=['GET', 'POST']) 
def adminlogin(): 
    form=AdminLoginForm()
    if form.validate_on_submit():
        reg_password = engine.execute("select Password from Admin_Tab where Name = :a",{'a':form.name.data})
        for row in reg_password:
            reg_details=row
        print(reg_details)
        if bcrypt.check_password_hash(reg_details[0] , form.password.data) :
            flash('Login successful.', 'success')
            current_user = form.name.data
            return redirect(url_for('profile',current_user= current_user,Type_of_User="Admin"))
        else:
            flash('Login Unsuccessful. Please check EnrollNo and password', 'danger')  
    return render_template('adminlogin.html',title='adminLogin', form=form)


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_password)
        engine.execute("insert into Student_Tab(Name,Roll_No,Programme,Branch,Semester,Password) values(:a,:b,:c,:d,:e,:f)",{'a':form.name.data,'b':form.rollNo.data,'c':form.programme.data,'d':form.branch.data,'e':form.semester.data,'f':hashed_password})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Studlogin'))
    return render_template('register.html',title='Register', form=form)

@app.route("/<Type_of_User>/<current_user>/addStudent", methods=['GET', 'POST'])
def addStudent(Type_of_User,current_user):
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_password)
        engine.execute("insert into Student_Tab(Name,Roll_No,Programme,Branch,Semester,Password) values(:a,:b,:c,:d,:e,:f)",{'a':form.name.data,'b':form.rollNo.data,'c':form.programme.data,'d':form.branch.data,'e':form.semester.data,'f':hashed_password})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('profile',current_user= current_user,Type_of_User="Admin"))
    return render_template('register.html',title='AddStudent', form=form,current_user=current_user,Type_of_User=Type_of_User)


@app.route("/<Type_of_User>/<current_user>/addFaculty", methods=['GET', 'POST'])
def addFaculty(Type_of_User,current_user):
    form = FacRegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        print(hashed_password)
        engine.execute("insert into Faculty_Tab(NAME,FAC_CODE,ROOM_NO,PHONE_NO,EMAIL_ID,OFFICE,PASSWORD) values(:a,:b,:c,:d,:e,:f,:g)",{'a':form.name.data,'b':form.facCode.data,'c':form.room_no.data,'d':form.phone_no.data,'e':form.email_id.data,'f':form.office.data,'g':hashed_password})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('profile',current_user= current_user,Type_of_User="Admin"))
    return render_template('AddFac.html',title='AddFac', form=form,current_user=current_user,Type_of_User=Type_of_User)

@app.route("/<Type_of_User>/<current_user>/addCourse", methods=['GET', 'POST'])
def addCourse(Type_of_User,current_user):
    form = CourseRegisterForm()
    if form.validate_on_submit():
        engine.execute("insert into Course_Tab(NAME,CODE,PROGRAMME,BRANCH,SEMESTER) values(:a,:b,:c,:d,:e)",{'a':form.course_name.data,'b':form.courseCode.data,'c':form.programme.data,'d':form.branch.data,'e':form.semester.data})
        engine.execute("insert into Fac_Course_Tab(FAC_CODE,COURSE_CODE) values(:a,:b)",{'a':form.faculty.data,'b':form.courseCode.data})
        # flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('profile',current_user= current_user,Type_of_User="Admin"))
    return render_template('AddCourse.html',title='AddCourse', form=form,current_user=current_user,Type_of_User=Type_of_User)

@app.route("/<Type_of_User>/<current_user>/addProgramme", methods=['GET', 'POST'])
def addProgramme(Type_of_User,current_user):
    form = ProgrammeRegisterForm()
    if form.validate_on_submit():
        engine.execute("insert into Programme_Tab(PROGRAMME,BRANCH) values(:a,:b)",{'a':form.programme.data,'b':form.branch.data})
        return redirect(url_for('profile',current_user= current_user,Type_of_User="Admin"))
    return render_template('AddProgramme.html',title='AddProgramme', form=form,current_user=current_user,Type_of_User=Type_of_User)


@app.route("/profile/<Type_of_User>/<current_user>")
def profile(Type_of_User,current_user):
    if Type_of_User == "Faculty" :
        courses=[]
        course_list = engine.execute("select Course_Code from Fac_Course_Tab where Fac_Code = :a",{'a' : current_user})
        for row in course_list:
            courses.append(row[0])
        return render_template('Facprofile.html',title='Profile',courses=courses,current_user=current_user,Type_of_User=Type_of_User)
    elif  Type_of_User == "Student" :
        stud=engine.execute("select Roll_No,Branch,Semester from Student_Tab where Name = :a",{'a':current_user})
        for i in stud:
            stud_details=[i[0],i[1],i[2]]
        print(stud_details)
        currentSem = stud_details[2]
        stud_course_perf = {}
        sem_list=[]
        for sem in range(1,currentSem+1):
            sem_list.append(sem)
            courses = engine.execute("select Code from Course_Tab where Semester = :a and Branch =:b",{'a' :sem,'b':i[1]})
            course_perf = {}
            for course in courses:
                stud_perf = engine.execute("select QUIZ1_MARKS_OF_15,MIDSEM_MARKS_OF_30,QUIZ2_MARKS_OF_15,ENDSEM_MARKS_OF_75,LAB_TEST_MARKS,ATTENDANCE_IN_PERC from Stud_Perf_Tab where Course_Code = :a and Student_Id = :b",{'a' : course[0],'b':stud_details[0]})
                for perf in stud_perf:
                    # print()
                    course_perf[course[0]]=[perf[0],perf[1],perf[2],perf[3],perf[4],perf[5]] 
            stud_course_perf[sem] = course_perf
        return render_template('Studprofile.html',title='Profile', stud_details=stud_details,current_user=current_user,Type_of_User=Type_of_User,stud_course_perf = stud_course_perf,currentSem = currentSem,sem_list = sem_list)
    else :
        return render_template('AdminProfile.html',title='Profile',current_user=current_user,Type_of_User=Type_of_User)

@app.route("/<Type_of_User>/<current_user>/<Table>")
def showTablesToAdmin(Type_of_User,current_user,Table):
    if Table=="Student":    
        colnames=['NAME','ROLL_NO','PROGRAMME','BRANCH','SEMESTER']
        slist = engine.execute('select NAME,ROLL_NO,PROGRAMME,BRANCH,SEMESTER from Student_Tab')
        stable=[]
        for stud in slist:
            stable.append([stud[0],stud[1],stud[2],stud[3],stud[4]])
    elif Table=="Faculty":
        colnames=['NAME','FAC_CODE','ROOM_NO','PHONE_NO','EMAIL_ID','OFFICE']
        slist = engine.execute('select NAME,FAC_CODE,ROOM_NO,PHONE_NO,EMAIL_ID,OFFICE from Faculty_Tab')
        stable=[]
        for stud in slist:
            stable.append([stud[0],stud[1],stud[2],stud[3],stud[4],stud[5]])
    elif Table=="Course":
        colnames=['NAME','CODE','PROGRAMME','BRANCH','SEMESTER']
        slist = engine.execute('select NAME,CODE,PROGRAMME,BRANCH,SEMESTER from Course_Tab')
        stable=[]
        for stud in slist:
            stable.append([stud[0],stud[1],stud[2],stud[3],stud[4]])
    else :
        colnames=['PROGRAMME','BRANCH','NO_OF_STUDENTS']
        slist = engine.execute('select PROGRAMME,BRANCH,NO_OF_STUDENTS from programme_Tab')
        stable=[]
        for stud in slist:
            stable.append([stud[0],stud[1],stud[2]])

    return render_template('showStudTable.html',current_user=current_user,Type_of_User=Type_of_User,stable=stable,Table=Table,colnames=colnames)
        

@app.route("/List/<Type_of_User>/<current_user>/<course>")
def showList(course,Type_of_User,current_user):
    stud_perf = {}
    stud_details = engine.execute("select STUDENT_ID, QUIZ1_MARKS_OF_15,MIDSEM_MARKS_OF_30,QUIZ2_MARKS_OF_15,ENDSEM_MARKS_OF_75,LAB_TEST_MARKS,ATTENDANCE_IN_PERC from Stud_Perf_Tab where Course_Code = :a",{'a' : course})
    for i in stud_details:
        student_name = engine.execute("select Name from Student_Tab where Roll_No = :a ",{'a' :i[0]})
        for j in student_name:
            stud_perf[i[0]] = [j[0],i[1],i[2],i[3],i[4],i[5],i[6]]
    print(stud_perf)

    return render_template('list.html',title='Stud_List',stud_perf=stud_perf,course=course,current_user=current_user,Type_of_User=Type_of_User)



@app.route("/updated",methods=['POST'])  
def updated():
    # values = request.get_json()
    
    param = {                      
                    'a'  : int(request.form['ATTENDANCE_IN_PERC']),                                
                    'b'  : int(request.form['QUIZ1_MARKS_OF_15']),                               
                    'c' :  int(request.form['MIDSEM_MARKS_OF_30']),                              
                    'd'  : int(request.form['QUIZ2_MARKS_OF_15']),                             
                    'e'  : int(request.form['ENDSEM_MARKS_OF_75']),  
                    'g'  : request.form['ENROLL_NO'],
                    'h'  : request.form['COURSE_CODE'],    
                   
    }
    print(param)
    engine.execute("update stud_perf_tab set ATTENDANCE_IN_PERC = :a,QUIZ1_MARKS_OF_15 = :b,MIDSEM_MARKS_OF_30 = :c,QUIZ2_MARKS_OF_15 = :d,ENDSEM_MARKS_OF_75= :e where Student_ID = :g and COURSE_CODE = :h",param)
    if request.form['LAB_TEST_MARKS'] != 'None':    
        request.form['LAB_TEST_MARKS'] = float(request.form['LAB_TEST_MARKS'])
        engine.execute('update stud_perf_tab set LAB_TEST_MARKS = :f where Student_ID = :g and COURSE_CODE = :h',{'f':request.form['LAB_TEST_MARKS'],'g'  : request.form['ENROLL_NO'],'h'  : request.form['COURSE_CODE']})
    
@app.route("/updateStudTables/<table>",methods=['POST'])  
def updateStudTables(table):
    # values = request.get_json()
    if table == "Student":
        param = {                      
                        'a'  : request.form['NAME'],                                
                        'b'  : request.form['PROGRAMME'],                               
                        'c' :  request.form['BRANCH'],                              
                        'd'  : int(request.form['SEMESTER']),                             
                        'e'  : request.form['ROLL_NO'],                  
        }
        engine.execute("update student_tab set NAME = :a,PROGRAMME = :b,BRANCH = :c,SEMESTER = :d where ROLL_NO = :e",param)
    elif table == "Faculty":                   
        param = {                      
                        'a'  : request.form['NAME'],                                
                        'b'  : request.form['FAC_CODE'],                               
                        'c' :  int(request.form['ROOM_NO']),                              
                        'd'  : int(request.form['PHONE_NO']),                             
                        'e'  : request.form['EMAIL_ID'], 
                        'f'  : request.form['OFFICE'],                  
        }
        engine.execute("update faculty_tab set NAME = :a,ROOM_NO = :c,PHONE_NO = :d,EMAIL_ID = :e,OFFICE = :f where FAC_CODE = :b",param)
    elif table == "Course":                   
        param = {                      
                        'a'  : request.form['NAME'],                                
                        'b'  : request.form['CODE'],                               
                        'c' :  request.form['PROGRAMME'],                              
                        'd'  : request.form['BRANCH'],                             
                        'e'  : int(request.form['SEMESTER']), 
                                        
        }
        engine.execute("update course_tab set NAME = :a,PROGRAMME = :c,BRANCH = :d,SEMESTER = :e where CODE = :b",param)
    else  :                
        param = {                      
                                                       
                        'a' :  request.form['PROGRAMME'],                              
                        'b'  : request.form['BRANCH'],                             
                        'c'  : int(request.form['NO_OF_STUDENTS']), 
                                        
        }
        engine.execute("update programme_tab set NO_OF_STUDENTS = :c where BRANCH = :b and PROGRAMME = :a",param)



@app.route("/up/<table>",methods=['POST'])  
def deleteInStudTable(table):
    if table == "Student":
        param={ 'a'  : request.form['ROLL_NO']}
        engine.execute("delete from stud_perf_tab where STUDENT_ID = :a",param)
        engine.execute("delete from student_tab where ROLL_NO = :a",param)
    elif table == "Faculty":
        param={ 'a'  : request.form['FAC_CODE']}
        engine.execute("delete from fac_course_tab where FAC_CODE = :a",param)
        engine.execute("delete from faculty_tab where FAC_CODE = :a",param)
    elif table == "Course":
        param={ 'a'  : request.form['CODE']}
        engine.execute("delete from stud_perf_tab where  COURSE_CODE= :a",param)
        engine.execute("delete from fac_course_tab where COURSE_CODE = :a",param)
        engine.execute("delete from course_tab where CODE = :a",param)
    else  :                
        param = {                      
                        'a' :  request.form['PROGRAMME'],
                        'b' :  request.form['BRANCH'],                              
                                        
        }
        c = engine.execute("select CODE from course_tab where PROGRAMME = :a AND BRANCH =:b",param)
    
        for i in c:
            engine.execute("delete from stud_perf_tab where STUDENT_ID = :a",{'a':i[0]})
            engine.execute("delete from student_tab where ROLL_NO = :a",{'a':i[0]})

        s = engine.execute("select ROLL_NO from student_tab where PROGRAMME = :a AND BRANCH =:b",param)
        
        for i in s:
            engine.execute("delete from stud_perf_tab where  COURSE_CODE= :a",{'a':i[0]})
            engine.execute("delete from fac_course_tab where COURSE_CODE = :a",{'a':i[0]})
            engine.execute("delete from course_tab where CODE = :a",{'a':i[0]})
        engine.execute("delete from programme_tab where PROGRAMME = :a AND BRANCH =:b",param)



   
if __name__=='__main__':
    app.run(debug=True)