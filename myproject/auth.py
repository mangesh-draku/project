from flask import Blueprint,render_template, request , flash ,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user , login_required ,logout_user , current_user


auth = Blueprint('auth',__name__)

@auth.route('/signup',methods=['GET','POST'])
def signup():
    if request.method == "POST":
        username = request.form.get('username')
        email = request.form.get('email')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(username=username).first()

        if len(username) < 3:
            flash('username must be greater then 3 character.',category='error')
        elif user :
            flash('username already exists',category='error')
        elif len(email) < 4:
            flash('username must be greater then 3 character.',category='error')
        elif len(password1) < 4:
            flash('password must be greater then 3 character.',category='error')
        elif password1 != password2:
            flash('password not matching',category='error')
        
        else:
            new_user = User(email=email,username=username,password=generate_password_hash(password1,method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("account created",category='success')
            return redirect(url_for('views.home'))
    
        return render_template("signup.html")
    else:
        return render_template("signup.html",user=current_user)    

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password,password):
                flash('loggedin successfully',category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('incorrect password, try again !!!',category='error')
        else:
            flash('incorrect username, try again !!!',category='error')

    else:
        return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('logged out successfully !!!',category='success')
    return redirect(url_for('auth.login'))