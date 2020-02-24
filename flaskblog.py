#Imports
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm
from models import User, Post
app = Flask(__name__)

#Hash Security Key
app.config['SECRET_KEY'] = '44ad1670c8d8186ca39190bb09f6a781'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

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
        flash(f'Account Created for {form.username.data}!','success')
        return redirect(url_for('home'))
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

#Server Startup
if  __name__ == "__main__":
    app.run(debug=True)

