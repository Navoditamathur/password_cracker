import hashlib
import re
from config import auth_list
from config import auth_details
from flask import Flask, render_template, request, Blueprint, session, redirect, url_for, flash
from flask_session import Session
from password_cracker import crack_pwd
auth = Blueprint('auth', __name__)


@auth.route('/index', methods=['GET', 'POST'])
def index():
    if session.get("user_name"):
        return redirect(url_for('auth.get_details'))
    return render_template("index.html", authenticated=False)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == "POST":
        error_msg = ''
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        user_name = request.form.get('user_name').lower()
        email = request.form.get('email')
        password = request.form.get('psw')
        password_conf = request.form.get('psw-repeat')
        with open(auth_list) as f:
            for line in f:
                if line.split("\t")[0] == user_name:
                    flash('Account already exists with this user name!! Please Login or choose another username')
                    return redirect(url_for('auth.sign_up'))
        match = re.search(r'[A-Z]+', password)
        num_numbers = len(re.findall('\d', password))
        if count_special_char(password) > 2 or num_numbers > 2 or match:
            error_msg += "Passwords must contain only lowercase letters with max two digits repetition amd max two special characters ('@', '#', '$', '%', '&') with no repetition"
        if password != password_conf:
            error_msg += 'Passwords do not match'
        if error_msg:
            flash(error_msg)
            return redirect(url_for('auth.sign_up'))
        else:
            hash_pwd = hashlib.md5(password.encode()).hexdigest()
            fl = open(auth_list, "a+")
            fl.write(user_name + "\t" + str(hash_pwd) + "\n")
            fl.close()

            fd = open(auth_details, "a+")
            fd.write(user_name + "\t" + first_name + "\t" + last_name + "\t" + email + "\n")
            fd.close()
            return redirect(url_for('auth.login'))
    return render_template("sign_up.html", title="Sign Up", authenticated=False)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        user_name = request.form.get('user_name').lower()
        password = request.form.get('psw')
        hash_pwd = hashlib.md5(password.encode()).hexdigest()
        user_found = False
        with open(auth_list) as f:
            for line in f:
                if line.split("\t")[0] == user_name:
                    user_found = True
                    if line.split("\t")[1].strip() != str(hash_pwd):
                        flash('Invalid Login Credentials!!')
                        return redirect(url_for('auth.login'))
        if not user_found:
            flash('Invalid Login Credentials!!')
            return redirect(url_for('auth.sign_up'))
        session["user_name"] = user_name
        return redirect(url_for('auth.get_details'))
    return render_template("login.html", title="Login", authenticated=False)

@auth.route("/get_details")
def get_details():
    if not session.get("user_name"):
        return redirect(url_for("auth.index"))
    user_name = session["user_name"]
    with open(auth_details) as f:
        for line in f:
            details = line.split("\t")
            if details[0] == user_name:
                session["user_name"] = user_name
                return render_template("home.html", title="User Details", authenticated=True, first_name=details[1], last_name=details[2],
                                       user_name=details[0], email=details[3])


@auth.route("/logout")
def logout():
    session["user_name"] = None
    return redirect(url_for("auth.index"))

@auth.route('/crack_password', methods=['GET', 'POST'])
def crack_password():
    authenticated = True
    if not session.get("user_name"):
        authenticated = False
    if request.method == "POST":
        user_name = request.form.get('user_name').lower()
        password = ""
        password_strength = ""
        time_taken = ""
        detailed = request.form.get('detailed') == 'detailed'
        pwd_details = crack_pwd(user_name, detailed)
        if pwd_details[0]:
            msg = "Password cracked Successfully!!"
            password = pwd_details[1]
            password_strength = pwd_details[2]
            time_taken = pwd_details[3]
        else:
            if len(pwd_details) == 5 and len(pwd_details[4]) > 0:
                msg = "Account not found with username "+user_name+"!!"
            else:
                msg = "Unable to crack Password!!"
        return render_template("crack_password.html", title="Password Details of User", cracked=pwd_details[0], user_name=user_name, password=password, password_strength=password_strength, time_taken=time_taken, msg=msg, authenticated=authenticated)
    return render_template("crack_password.html", title="Crack Password",authenticated=authenticated)

@auth.route('/validate_password', methods=['GET', 'POST'])
def validate_password():
    if not session.get("user_name"):
        flash("Either Sign up or Login to validate password")
        return redirect(url_for("auth.index"))
    user_name = session["user_name"]
    with open(auth_details) as f:
        for line in f:
            details = line.split("\t")
            if details[0] == user_name:
                pwd_details = crack_pwd(user_name)
                password_strength = pwd_details[2]
                time_taken = pwd_details[3]
                return render_template("validate_password.html", title="Password Validation Details of User", validated="True", authenticated=True, first_name=details[1], last_name=details[2],
                                       user_name=details[0], email=details[3], cracked=pwd_details[0], password_strength=password_strength, time_taken=time_taken)


def count_special_char(s):
    n = 0
    for c in s:
        if not (c.isalpha() or c.isdigit() or c == ' '):
            n += 1
    return n
