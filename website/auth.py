from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Client, Nutritionist
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from datetime import datetime

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                if user.account_type == "client":
                    return redirect(url_for('views.client_profile'))
                else:
                    return redirect(url_for('views.nutritionist_profile'))
            else:
                flash('Incorrect password!', category='error')
        else:
            flash('Email does not exist', category='error')
    
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        dob = request.form.get('date_of_birth')
        date_of_birth=datetime.strptime(dob, '%Y-%m-%d').date()
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        gender = request.form.get('gender')
        account_type = request.form.get('account_type')
        default_profile_picture = url_for('static', filename='profile_pictures/avatar.jpg')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('This email is already registered.', category='error')
        elif len(email) < 4:
            flash('Email has to be longer than 4 characters', category='error')
            pass
        elif len(first_name) < 2:
            flash('First name has to be at least 2 characters long', category='error')
            pass 
        elif len(last_name) < 2:
            flash('Last name has to be at least 2 characters long', category='error')
            pass
        elif len(password1) < 6:
            flash('Password must contain at least 6 characters', category='error')
            pass
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
            pass
        elif account_type == "client":
            new_user = Client(email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, password=generate_password_hash(password1, method='sha256'), gender=gender, account_type=account_type, profile_picture='avatar.jpg')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.client_profile'))
        else:
            new_user = Nutritionist(email=email, first_name=first_name, last_name=last_name, date_of_birth=date_of_birth, password=generate_password_hash(password1, method='sha256'), gender=gender, account_type=account_type, profile_picture='avatar.jpg')
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.nutritionist_profile'))


    return render_template("sign_up.html", user=current_user)

