from flask import Flask,render_template ,flash ,url_for , redirect
from forms import RegistrationForm,LoginForm
from sqlalchemy import create_engine
from flask_bcrypt import Bcrypt
from flask import request

app = Flask(__name__)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'

bcrypt =Bcrypt(app)
import cx_Oracle
password=''
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
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')

@app.route("/about")
def about():
    return render_template('about.html')

# @app.route("/account")
# def account():
#     return render_template('account.html')

@app.route("/login", methods=['GET', 'POST']) 
def login():
    form=LoginForm()
    if form.validate_on_submit():
        reg_password = engine.execute("select Password from Student_Tab where Roll_No = :a",{'a':form.rollNo.data})
        for row in reg_password:
            reg_pass=row
        print(reg_pass[0])
        if bcrypt.check_password_hash(reg_pass[0] , form.password.data) :
            print("xcb")
            flash('Login successful.', 'success')
        else:
            flash('Login Unsuccessful. Please check EnrollNo and password', 'danger')
            
    return render_template('login.html',title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        engine.execute("insert into Student_Tab(Name,Roll_No,Programme,Branch,Semester,Password) values(:a,:b,:c,:d,:e,:f)",{'a':form.name.data,'b':form.rollNo.data,'c':form.programme.data,'d':form.branch.data,'e':form.semester.data,'f':hashed_password})
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html',title='Register', form=form)



if __name__=='__main__':
    app.run(debug=True)