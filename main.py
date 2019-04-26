from flask import Flask,render_template ,flash ,url_for , redirect
from forms import RegistrationForm,StudLoginForm,FacLoginForm
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask import request
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

@app.route("/")
@app.route("/home")
def home():
    # print(current_user)
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


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        engine.execute("insert into Student_Tab(Name,Roll_No,Programme,Branch,Semester,Password) values(:a,:b,:c,:d,:e,:f)",{'a':form.name.data,'b':form.rollNo.data,'c':form.programme.data,'d':form.branch.data,'e':form.semester.data,'f':hashed_password})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('Studlogin'))
    return render_template('register.html',title='Register', form=form)

@app.route("/profile/<Type_of_User>/<current_user>")
def profile(Type_of_User,current_user):
    if Type_of_User == "Faculty" :
        courses=[]
        course_list = engine.execute("select Course_Code from Fac_Course_Tab where Fac_Code = :a",{'a' : current_user})
        for row in course_list:
            courses.append(row[0])
        return render_template('Facprofile.html',title='Profile',courses=courses)
    else:
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

    


@app.route("/List/<course>")
def showList(course):
    stud_perf = {}
    stud_details = engine.execute("select STUDENT_ID, QUIZ1_MARKS_OF_15,MIDSEM_MARKS_OF_30,QUIZ2_MARKS_OF_15,ENDSEM_MARKS_OF_75,ATTENDANCE_IN_PERC from Stud_Perf_Tab where Course_Code = :a",{'a' : course})
    for i in stud_details:
        student_name = engine.execute("select Name from Student_Tab where Roll_No = :a ",{'a' :i[0]})
        for j in student_name:
            stud_perf[i[0]] = [j[0],i[1],i[2],i[3],i[4],i[5]]
    print(stud_perf)

    return render_template('list.html',title='Stud_List',stud_perf=stud_perf)
    

if __name__=='__main__':
    app.run(debug=True)