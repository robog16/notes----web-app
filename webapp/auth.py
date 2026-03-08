from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')    
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category = 'success')
                login_user(user, remember = True) #je to funkcia ktora akoze hovori ze logni tohto juzra do keše a zapametaj si to, nahradza zrejme vsetky session funkcie
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again!', category = 'error')
        else:
            flash('Email does not exist!', category = 'error')
    
    return render_template('login.html', user = current_user)
    
@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', category='success')
    return redirect(url_for('auth.login'))

 
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password')
        password2 = request.form.get('confirm_password')

        if '@' not in email and len(email) < 5:
            flash('Email is too short or has incorrect format!', category = 'error')
        elif len(username) < 2:
            flash('Username needs to have at least 3 characters!', category = 'error')
        elif len(password1) < 5:
            flash('Password needs to have at least 6 characters!', category = 'error')
        elif password1 != password2:
            flash('Passwords doesn\'t match!', category = 'error')
        else:
            user = User.query.filter_by(email=email).first()  # Skontroluj, či e-mail existuje
            if user:
                flash('Email already exists!', category='error') # ak email existuje, vypis chybu.
            else:
                new_user = User(email=email, username=username, password=generate_password_hash(password1))
                db.session.add(new_user)
                db.session.commit()
                login_user(user, remember = True)
                flash('Account created!', category='success')
                return redirect(url_for('views.home'))
            
    return render_template('sign_up.html', user = current_user)