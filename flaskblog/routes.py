import secrets
import os
from flask import  render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required
db.create_all()

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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
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
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful!. Please check your login details.', 'danger')
    return render_template('login.html', title='Login', form=form)

#LogOut
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

#Profile Picture
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)

    return picture_fn


#Account
@app.route('/account',  methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()  
    if form.validate_on_submit():
        
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file 
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your Account Has Been Updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static',filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', image_file=image_file, form=form)

