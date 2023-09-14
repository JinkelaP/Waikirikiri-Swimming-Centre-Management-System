from flask import Flask, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
import bcrypt
from app import mysql

#The index page of the web app

# No, this is just a temporary one. When user is accessing the / page:
# If the user has logged in, redirect to the home page
# If not, redirect to login page

bp = Blueprint('temporaryIndex', __name__, )
@bp.route("/", methods=['GET'])
def index():    
    # check if logged in
    if 'loggedin' in session:
        if session['role'] == 1:
            return redirect(url_for('adminDashboardFunc.adminDashboard'))
        elif session['role'] == 2:
            return redirect(url_for('adminDashboardFunc.instructorDashboard'))
        elif session['role'] == 3:
            return redirect(url_for('adminDashboardFunc.memberDashboard'))
    
    else:
        return redirect(url_for('login.login'))