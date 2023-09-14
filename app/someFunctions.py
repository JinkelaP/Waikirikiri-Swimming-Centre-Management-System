from app import mysql
from flask import flash, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import MySQLdb.cursors
import bcrypt
import os
import html

bp = Blueprint('someFunctions', __name__, )

def is_authenticated():
    return 'loggedin' in session

@bp.route('/writeNews')
def writeNews():
    return render_template('writeNews.html')

@bp.route('/submitNews', methods=['POST'])
def submitNews():
    if is_authenticated():
        if session['role'] == 1:  
            # Retrieve form data
            title = request.form['title'] 
            content = request.form['content']
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Insert news data into the database with current admin's ID and current date/time as publishDate
            cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, 0)', 
                           (title, content, datetime.now(), session['id']))
            mysql.connection.commit()
            cursor.close()

            # Redirect to the admin dashboard to confirm news submission
            return redirect(url_for('adminDashboardFunc.adminDashboard'))
        else:
            # Return an unauthorized error if the user isn't an admin
            return "Unauthorized", 403  
    else:
        # Redirect to login page if the user isn't authenticated
        return redirect(url_for('login.login'))

@bp.route('/news')
def displayNews():
    if is_authenticated():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT title, content, publishDate FROM news_updates WHERE newsTypeID=0 ORDER BY publishDate DESC')
        news = cursor.fetchall()
        cursor.close()
        return render_template('displayNews.html', news=news)
    else:
        # Redirect to login page if the user isn't authenticated
        return redirect(url_for('login.login'))
    
@bp.route('/msg')
def displayMsg():
    if is_authenticated():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT title, content, publishDate FROM news_updates WHERE newsTypeID=%s ORDER BY publishDate DESC',(session['id'],))
        news = cursor.fetchall()
        cursor.close()
        return render_template('displayMsg.html', news=news)
    else:
        # Redirect to login page if the user isn't authenticated
        return redirect(url_for('login.login'))
    
@bp.route('/admin/viewAllSubscriptions')
def viewAllSubscriptions():
    if is_authenticated() and session['role'] == 1:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM subscriptions INNER JOIN memberinfo ON subscriptions.userID = memberinfo.userID')
        subscriptions = cursor.fetchall()
        return render_template('viewAllSubscriptions.html', subscriptions=subscriptions)
    else:
        return "unauthorized"
    
@bp.route('/admin/fullReport')
def fullReport():
    if is_authenticated():
        if session['role'] == 1:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Query to get all the aerobics classes and their details
            query = '''
            SELECT a.*, CONCAT(i.firstName, ' ', i.lastName) AS instructorName, 
            COUNT(b.bookingID) AS totalBookings, 
            SUM(b.bookingAttend) AS totalAttended,
            CASE 
                WHEN a.bookingActive = FALSE THEN 'Deleted'
                WHEN DATE(a.sessionTime) < CURDATE() THEN 'Complete'
                ELSE 'Active'
            END AS sessionStatus
            FROM aerobics_schedule AS a
            LEFT JOIN aerobics_bookings AS b ON a.scheduleID = b.scheduleID
            INNER JOIN instructorinfo AS i ON a.instructorID = i.userID
            GROUP BY a.scheduleID
            ORDER BY totalBookings DESC;
            '''
            cursor.execute(query)
            classes = cursor.fetchall()

            return render_template('fullReport.html', classes=classes)
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))

