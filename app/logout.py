from flask import Flask, render_template, request, redirect, url_for, session, Blueprint, flash
from flask_mysqldb import MySQL
import bcrypt
from app import mysql

# app = Flask(__name__)

# Configure MySQL
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'password'
# app.config['MYSQL_DB'] = 'swimmingPool'
# app.config['MYSQL_PORT'] = 3306

# app.secret_key = 'your_secret_key_here'

# mysql = MySQL(app)




bp = Blueprint('logout', __name__, )

@bp.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   session.pop('role',None)

   flash('Log out successful!', 'success'), 
   # Redirect to login page
   return redirect('/')