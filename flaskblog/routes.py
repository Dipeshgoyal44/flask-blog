from flask import  render_template, url_for, flash, redirect
from flaskblog import app,db,bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post


#Dummy Data
posts = [
    {
        'author':'Dipesh Goyal',
        'title':'Blog Post 1',
        'content':'First Post Content',
        'date_posted': 'April 20, 2018',
    },
    {
        'author':'Abhay Goyal',
        'title':'Blog Post 2',
        'content':'Second Post Content',
        'date_posted': 'Febrauary 16,2020'
    },

]

#Routes
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

#About
@app.route('/about')
def about():
    return render_template('about.html', title='About')  

#Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your Account has been created!','success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Sign Up', form=form)

#Login
@app.route('/login',  methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'admin' and form.password.data =='password':
            flash('You Have Been Logged In!','success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful!. Please check your login details.', 'danger')
    return render_template('login.html', title='Login', form=form)
