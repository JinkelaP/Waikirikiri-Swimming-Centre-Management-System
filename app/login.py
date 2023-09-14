from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from flask_mysqldb import MySQL
from .memberDashboardFunc import checkSubscription
import MySQLdb.cursors
import bcrypt
from datetime import datetime
from app import mysql

bp = Blueprint('login', __name__, )

def is_authenticated():
    return 'loggedin' in session

@bp.route('/login', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # logged in user cannot enter the page
    if 'loggedin' in session:
        return redirect("/")
    # Check if "username" and "password" POST requests exist (user submitted form)
    elif request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM users WHERE userName = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account['userPassword']
            # password = account[3]  
            if bcrypt.checkpw(user_password.encode('utf-8'), password.encode('utf-8')):
                # If account exists in accounts table in our database
                # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['role'] = account['userPermission']
                session['id'] = account['userID']
                # session['id'] = account[0]  # Assuming 'userID' is the first column in the result

                # Redirect to home page
                if session['role'] == 1:
                    return redirect(url_for('adminDashboardFunc.adminDashboard'))
                elif session['role'] == 2:
                    return redirect(url_for('adminDashboardFunc.instructorDashboard'))
                elif session['role'] == 3:
                    return redirect(url_for('adminDashboardFunc.memberDashboard'))
            else:
                # Password incorrect
                msg = 'Incorrect password!'
                return render_template('login.html', msg=msg, loginUsername = username)
        else:
            # Account doesn't exist or username incorrect
            msg = 'Incorrect username'
            return render_template('login.html', msg=msg, loginUsername = username)
    # Show the login form with message (if any)
    return render_template('login.html', msg=msg)