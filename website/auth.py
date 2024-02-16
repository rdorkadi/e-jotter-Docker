from flask import Blueprint, redirect, render_template, request,flash, session, url_for, abort 
from .input_validation import *
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user, UserMixin
from io import BytesIO
import pyqrcode

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # check if the user exist already in DB
        user = User.query.filter_by(email=email).first()
        print(password)
        print(request.form.get('password'))

        # if  the user exists check if the password enterd and stored are same
        if user :
            email = request.form.get('email')
            password = request.form.get('password')
            token = request.form.get('token')
            user = User.query.filter_by(email=email).first()
            # check for password and OTP too
            print("email:",email)
            print("Token",token) 
            print("OTP check", user.verify_totp(token))
            if check_password_hash(user.password,password) and user.verify_totp(token):
                flash('Logged in Successfully!', category='success')
                
                # when the browser closes, if the user is logged in, it will remember
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password or OTP Token', category='error')
        # if the user doesnt exists
        else:
            flash('User not found in our Database', category='error')
            return redirect(url_for("auth.sign_up"))

    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Bye,you have been logged out!",category="success")
    return redirect(url_for('auth.login'))



@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    # we are diff GET and POST request
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        # check if we are grabbing the values from UI correctly
        #print(email,firstName,password1,password2)



        # Before creating a new account, check if the user(email) already exists in our DB
        user = User.query.filter_by(email=email).first()
        print("Sign-up 1st occ user", user)
        
        if user and user.is_active:
           flash('Email already exists in our Database',category='error')
        # basic checks, and flash for showing messages on UI
        # email length check
        elif len(email) < 4:
            flash ('Email must be greater than 4 characters', category='error')
        # firstname check
        # 1. length
        # 2. shouldnt start with numbers or special chrs
        elif len(firstName) < 3:
            flash('Fist Name must be greater than 3 characters',category='error')
        # password check
        # 1. min length = 8
        # 2. 1 uppercase 1 lowercase 1 specialchr
        elif len(password1) < 7:
            flash("Password must be at least 7 characters",category='error')
        elif not contains_chr(password1):
            flash("Password must contains at least 1 special characters",category='error')
        elif not contains_upper(password1):
            flash("Password must contain atleast 1 uppercase letter",category="error")
        elif not contains_lower(password1):
            flash("Password must contain atleast 1 lowercase alphabet",category="error")
        elif password1 != password2:
            flash("Password not maching",category='error')
        else:


            # creating a new user
            new_user = User(email=email, firstName=firstName, password=generate_password_hash(password1, method="sha256"))
                
            # adding this new user to staging area
            db.session.add(new_user)

            # adding this user to DB
            db.session.commit()
            user = User.query.filter_by(email=email).first()
            print("Sign-up 2nd occ user", user)
            login_user(user, remember=True)

            session['email'] = email
            print(session['email']) 
            return redirect(url_for('auth.qr'))

        
        flash(f"Account Created, Welcome {firstName}",category='success')
        return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

@auth.route('/qr', methods=['GET','POST'])
def qr():
    if 'email' not in session:
        return redirect(url_for('auth.sign_up'))
    email = session['email']
    print("/qr - email",email)
    user = User.query.filter_by(email=email).first()
    print("/qr - user",user)
    # if user is None:
    #     return redirect(url_for('auth.sign_up'))
    return render_template("qr.html", user=current_user)


# Generate QR code
@auth.route('/generate_qr', methods=['GET','POST'])
def generate_qr():
    if 'email' not in session:
        return redirect(url_for('auth.sign_up'))
    email = session['email']
    email = 'user100@email.com'
    user = User.query.filter_by(email=email).first()

    if user is None:
        abort(404)

    del session['email']

    print("current_user=",current_user)
    url = pyqrcode.create(current_user.get_totp_uri())
    stream = BytesIO()
    url.svg(stream, scale=5)
    return stream.getvalue(), 200, {
        'Content-Type': 'image/svg+xml',
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'
        }


