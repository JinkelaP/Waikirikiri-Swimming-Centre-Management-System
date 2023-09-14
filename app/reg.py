from flask import flash, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from datetime import datetime,date, timedelta
import MySQLdb.cursors
import bcrypt
from app import mysql
import re

bp = Blueprint('reg', __name__, )

@bp.route("/register", methods = ['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('userPassword')
        title = request.form.get('title')
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        position = request.form.get('position')
        phoneNumber = request.form.get('phoneNumber')
        email = request.form.get('userEmail')
        physicalAddress = request.form.get('userAddress')
        dateOfBirth = request.form.get('dateedit')
        healthInfo = request.form.get('healthInfo')

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()
        cursor.close()

        if account:
            msg = 'Account already exists!'
            return render_template('register.html', msg=msg)
        
        elif len(username) > 80:
            msg = 'Username is too long!'
            return render_template('register.html', msg=msg)
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
            return render_template('register.html', msg=msg)
        elif not username or not password:
            msg = 'Please fill out the form!'
            return render_template('register.html', msg=msg)
        elif len(password) < 6 or len(password) > 20:
            msg = 'Password must be between 6 and 20 characters!'
            return render_template('register.html', msg=msg)
        # Check is there any space in password
        elif re.search(r'\s', password):
            msg = 'Password cannot contain spaces!'
            return render_template('register.html', msg=msg)
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            
            # Just customer need to register, for staffs, admin add them to mysql
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s,%s)', ('3', username, hashed, '1'))
            mysql.connection.commit()
            # Get user_ID, then insert to table customer
            user_ID = cursor.lastrowid
            print (user_ID)
            cursor.execute('INSERT INTO memberinfo (userID, title, firstName, lastName, position, phoneNumber, email, physicalAddress, dateOfBirth, healthInfo) VALUES (%s, %s, %s, %s,  %s, %s, %s, %s, %s, %s)', (user_ID, title, firstName, lastName, position, phoneNumber, email, physicalAddress, dateOfBirth, healthInfo))
            mysql.connection.commit()
            cursor.close()
            flash('You have successfully registered. Please login to subscribe.', 'success')
            return redirect(url_for('login.login'))
    else:
        return render_template('register.html')

@bp.route('/viewSubscription')
def viewSubscription():
    # Check if member is logged in
    if 'loggedin' in session and session['role'] == 3:  # Ensure it's a member
        # Get member's userID
        user_id = session['id']
        
        # Connect to the database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get subscription details for the logged in member
        cursor.execute('SELECT startDate, endDate FROM subscriptions WHERE userID = %s', (user_id,))
        subscription = cursor.fetchone()
        
        # If member has an active subscription, show details
        if subscription:
            return render_template('viewSubscription.html', subscription=subscription)
        else:
            # If no active subscription, show a message
            msg = "You currently don't have an active subscription."
            return render_template('viewSubscription.html', msg=msg)
    else:
        # If not logged in or not a member, redirect to login
        return redirect(url_for('login.login'))
    
@bp.route('/subscription', methods=['GET', 'POST'])
def subscription():
    if request.method == 'POST':
        # Retrieve the specified username from the form
        username = request.form.get('userName')
        
        # Connect to the database and fetch the user with the specified username
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userName = %s', (username,))
        user = cursor.fetchone()

        # Return an error message if the specified user does not exist
        if not user:
            return render_template('subscription.html', msg="Username not found!")
        
        # Obtain the user's ID from the fetched user data
        userID = user['userID']

        # Retrieve the subscription duration from the form and calculate associated details
        duration_in_months = int(request.form.get('subscription_duration'))
        today = datetime.today()
        # Compute the subscription end date based on the chosen duration
        endDate = today + timedelta(days=30*duration_in_months)  # Using a 30-day approximation for month duration

        # Compute the subscription amount based on a fixed monthly rate
        amount = duration_in_months * 70

        # Update the subscriptions table with the new subscription details
        cursor.execute('INSERT INTO subscriptions (userID, startDate, endDate) VALUES (%s, %s, %s)', (userID, today.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d')))
        mysql.connection.commit()

        # Register the payment details in the payments table
        paymentTime = datetime.now()
        cursor.execute('INSERT INTO payments (customerID, paymentType, amount, paymentTime) VALUES (%s, %s, %s, %s)', (userID, 1, amount, paymentTime.strftime('%Y-%m-%d %H:%M:%S')))
        mysql.connection.commit()

        # Notify the user of the successful subscription and redirect to the login page
        flash('Subscription succeed! Congratulation!', 'success')
        return redirect(url_for('login.login'))
    
    # Render the subscription page for GET requests
    return render_template('subscription.html')

@bp.route('/subscriptionn')
def subscriptionn():
    if 'loggedin' in session and session['role'] == 3:
        user_id = session['id']
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE userID = %s', (user_id,))
        account = cursor.fetchone()
        cursor.execute('SELECT * FROM memberinfo WHERE userID = %s', (user_id,))
        member = cursor.fetchone()
        cursor.close()

        if account and member:
            username = account['userName']
            first_name = member['firstName']
            last_name = member['lastName']
            email = member['email']
            address = member['physicalAddress']
        else:
            flash('Account not found!', 'error')
            return redirect(url_for('login'))
        
        return render_template('subscription.html',current_date=datetime.now().strftime('%d/%m/%Y'),firstName=first_name,lastName=last_name,username=username,email=email,address=address)
    else:
        return redirect(url_for('login.login'))

@bp.route('/extendSubscription', methods=['GET', 'POST'])
def extendSubscription():
    msg = ''
    
    # Ensure user is logged in before proceeding
    if 'loggedin' not in session:
        return redirect(url_for('login.login'))
    
    # Check user role to ensure only members can access
    if session['role'] != 3:
        flash('Only members can access this page.', 'error')
        return redirect(url_for('login.login'))
    
    # Establish a connection with the database
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Retrieve the current subscription details for the logged-in user
    cursor.execute('SELECT * FROM subscriptions WHERE userID = %s', (session['id'],))
    subscription = cursor.fetchone()
    
    # Redirect if the user lacks an active subscription
    if not subscription:
        flash('You do not have an active subscription.', 'error')
        return redirect(url_for('reg.viewSubscription'))

    # Extract the current subscription end date
    current_end_date = subscription['endDate']

    # Handle form submission to extend subscription
    if request.method == 'POST':
        duration = int(request.form['subscription_duration'])
        # Calculate the new subscription end date
        new_end_date = current_end_date + timedelta(days=30*duration)
        
        # Update the subscription's end date in the database
        cursor.execute('UPDATE subscriptions SET endDate = %s WHERE userID = %s', (new_end_date, session['id']))
        # Compute the payment amount and insert the payment details
        amount = 70 * duration
        cursor.execute('INSERT INTO payments (customerID, paymentType, amount, paymentTime) VALUES (%s, %s, %s, %s)', 
                       (session['id'], 1, amount, date.today()))
        mysql.connection.commit()
        # Notify the user of the successful extension
        flash('Subscription extended successfully!', 'success')
        return redirect(url_for('reg.viewSubscription'))
    
    # Fetch user and member details for rendering
    cursor.execute('SELECT * FROM users WHERE userID = %s', (session['id'],))
    user = cursor.fetchone()
    cursor.execute('SELECT * FROM memberinfo WHERE userID = %s', (session['id'],))
    member_info = cursor.fetchone()

    # Format the current subscription end date for display
    current_end_date_str = current_end_date.strftime('%d/%m/%Y')
    
    # Render the extension page with appropriate data
    return render_template('extendSubscription.html', user=user, member_info=member_info, current_date=current_end_date_str, subscription=subscription)
