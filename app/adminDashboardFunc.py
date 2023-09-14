from app import mysql
from flask import flash, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from datetime import datetime
from werkzeug.utils import secure_filename
from .memberDashboardFunc import checkSubscription
import MySQLdb.cursors
import bcrypt
import os
import math
from datetime import date, datetime, timedelta, time
from decimal import Decimal
from .memberDashboardFunc import getHistoryBookings, getUpcomingBookings
from .instructorDashboardFunc import getInstructorHistoryBookings, getInstructorUpcomingBookings, getInstructorByUserId

bp = Blueprint('adminDashboardFunc', __name__, )

def is_authenticated():
    return 'loggedin' in session

# function to get all the account information by userid
def get_account(userId):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = '''SELECT * FROM
                (SELECT 
                users.userID,
                users.userName,
                users.userPassword,
                users.userPermission,
                users.userActive,
                COALESCE(instructorinfo.introduction, NULL, NULL) AS introduction,
                COALESCE(memberinfo.healthInfo, NULL, NULL) AS healthInfo,
                COALESCE(memberinfo.dateOfBirth, NULL, NULL) AS dateOfBirth,
                COALESCE(memberinfo.physicalAddress, NULL, NULL) AS physicalAddress,
                COALESCE(admininfo.title, instructorinfo.title, memberinfo.title) AS title,
                COALESCE(admininfo.firstName, instructorinfo.firstName, memberinfo.firstName) AS firstName,
                COALESCE(admininfo.lastName, instructorinfo.lastName, memberinfo.lastName) AS lastName,
                COALESCE(admininfo.position, instructorinfo.position, memberinfo.position) AS position,
                COALESCE(admininfo.phoneNumber, instructorinfo.phoneNumber, memberinfo.phoneNumber) AS phoneNumber,
                COALESCE(admininfo.email, instructorinfo.email, memberinfo.email) AS email
                FROM users
                LEFT JOIN admininfo ON users.UserID = admininfo.UserID
                LEFT JOIN instructorinfo ON users.UserID = instructorinfo.UserID
                LEFT JOIN memberinfo ON users.UserID = memberinfo.UserID) AS user_admin_instructor_customer       
                WHERE userActive = True and userID = %s;'''
    cursor.execute(sql,(userId,))
    account = cursor.fetchone()
    return account  

# function to check if username already exist in database
def userNameCrash(userName):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users WHERE userActive = True and userName = %s', (userName,))
    exist_account = cursor.fetchone()
    if exist_account:
        return 1
    else:
        return 0

# encapsulate the passwordEncrypt function
def passwordEncrypt(userPassword):
    bytes = userPassword.encode('utf-8')
    salt = bcrypt.gensalt()
    hashedPsw = bcrypt.hashpw(bytes, salt)
    return hashedPsw

def labelAvailable(userID, date, startTime, lessonDuration):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM time_slots WHERE startTime = '{startTime}';")
    firstTimeSlot = cursor.fetchone()
    firstSlotID = firstTimeSlot['slotsID']
    numOfSlots = math.ceil(int(lessonDuration)/15)
    for i in range(numOfSlots):
        # cursor.execute("UPDATE user_availability SET availability = True WHERE userID = %s AND date = %s AND slotsID = %s;",(userID,date,firstSlotID+i) )
        cursor.execute("DELETE FROM user_availability WHERE userID = %s AND date = %s AND slotsID = %s;",(userID,date,firstSlotID+i) )
    cursor.connection.commit()

def checkUserAvailability(userId, date, startTime, lessonDuration):
    flag = True
    numOfSlots = math.ceil(int(lessonDuration)/15)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM time_slots WHERE startTime = '{startTime}';")
    firstTimeSlot = cursor.fetchone()
    firstSlotID = firstTimeSlot['slotsID']
    for i in range(numOfSlots):
        cursor.execute("SELECT availability FROM user_availability WHERE userID = %s AND date = %s AND slotsID = %s;",(userId,date,firstSlotID+i) )
        availability = cursor.fetchone()
        if availability and availability['availability'] == False:
            flag = False
    return flag

def labelUnavailable(userId, date, startTime, lessonDuration):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(f"SELECT * FROM time_slots WHERE startTime = '{startTime}';")
    firstTimeSlot = cursor.fetchone()
    firstSlotID = firstTimeSlot['slotsID']
    numOfSlots = math.ceil(int(lessonDuration)/15)
    for i in range(numOfSlots):
        cursor.execute("SELECT * FROM user_availability WHERE userID = %s AND date = %s AND slotsID = %s;",(userId,date,firstSlotID+i) )
        availability = cursor.fetchone()
        if availability:
            availabilityID = availability['availabilityID']
            cursor.execute("UPDATE user_availability SET availability = False WHERE availabilityID = %s",(availabilityID,))
            cursor.connection.commit()
        else:
            cursor.execute("INSERT INTO user_availability (userID, slotsID, date, availability) VALUES (%s,%s,%s,False)",(userId,firstSlotID+i,date))
            cursor.connection.commit()


def timedeltaToTime(delta):
    hours, remainder = divmod(delta.total_seconds(), 3600)
    minutes, seconds = divmod(remainder, 60)
    return time(int(hours), int(minutes), int(seconds))

# redirect all 404 pages to my bootstrapped one.
@bp.errorhandler(404)
def pageNotFound(error):
    session['loggedin'] = False
    return render_template('404.html',session=session), 404

# admin dashboard
@bp.route('/admin/home')
def adminDashboard():
    if is_authenticated():
        if session['role'] == 1:           
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

            # Get total members
            cursor.execute('SELECT COUNT(*) FROM memberinfo LEFT JOIN users ON users.userID = memberinfo.userID WHERE users.userActive = True;')
            row = cursor.fetchone()
            totalMember = row['COUNT(*)']

            # Query to get total subscription count
            cursor.execute('SELECT COUNT(*) as totalSubscription FROM subscriptions')
            totalSubscription = cursor.fetchone()['totalSubscription']

            # Query to get subscriptions due in one month
            one_month_from_now = (datetime.now() + timedelta(days=30)).date()
            cursor.execute('SELECT COUNT(*) as SubsIn1Month FROM subscriptions WHERE endDate <= %s', [one_month_from_now])
            SubsIn1Month = cursor.fetchone()['SubsIn1Month']

            #Query to get monthly payment in current month
            month_names = {
                1: 'Jan',
                2: 'Feb',
                3: 'Mar',
                4: 'Apr',
                5: 'May',
                6: 'Jun',
                7: 'Jul',
                8: 'Aug',
                9: 'Sep',
                10: 'Oct',
                11: 'Nov',
                12: 'Dec'
                }
            cursor.execute('SELECT SUM(amount) as monthlyPayment FROM payments WHERE MONTH(paymentTime) = MONTH(NOW()) AND YEAR(paymentTime) = YEAR(NOW())')
            monthlyPayment = cursor.fetchone()['monthlyPayment']
            if monthlyPayment is None:
                monthlyPayment = Decimal(0)
            if datetime.now().month == 1:
                cursor.execute('SELECT SUM(amount) as lastMonthPayment FROM payments WHERE MONTH(paymentTime) = 12 AND YEAR(paymentTime) = YEAR(NOW())-1')
                lastMonthPayment = cursor.fetchone()['lastMonthPayment']
            else:
                cursor.execute('SELECT SUM(amount) as lastMonthPayment FROM payments WHERE MONTH(paymentTime) = MONTH(NOW())-1 AND YEAR(paymentTime) = YEAR(NOW())')
                lastMonthPayment = cursor.fetchone()['lastMonthPayment']
            if lastMonthPayment is None:
                lastMonthPayment = Decimal(0)
            if lastMonthPayment and  lastMonthPayment != 0:
                paymentIncreasePercentage  = round((monthlyPayment - lastMonthPayment) / lastMonthPayment * 100)
            else:
                paymentIncreasePercentage = 100
            current_datetime = datetime.now()
            month = month_names.get(current_datetime.month)

            #Query to get subscription and swimming lessons payment 
            cursor.execute('SELECT SUM(amount) as totalPayment FROM payments GROUP BY paymentType')            
            subPayment =  cursor.fetchone()
            if (subPayment):
                subPayment = subPayment['totalPayment']
            individualPayment =  cursor.fetchone()
            if (individualPayment):
                individualPayment = individualPayment['totalPayment']
            
            #Query to get monthly attendance 
            cursor.execute('SELECT COUNT(attendanceID) as attendanceCount FROM attendance WHERE MONTH(attendanceTime) = MONTH(NOW()) AND YEAR(attendanceTime) = YEAR(NOW())')
            attendanceCount = cursor.fetchone()['attendanceCount']

            if attendanceCount is None:
                attendanceCount = Decimal(0)
            if datetime.now().month == 1:
                cursor.execute('SELECT COUNT(attendanceID) as lastMonthAttendance FROM attendance WHERE MONTH(attendanceTime) = 12 AND YEAR(attendanceTime) = YEAR(NOW())-1')
                lastMonthAttendance = cursor.fetchone()['lastMonthAttendance']
            else:
                cursor.execute('SELECT COUNT(attendanceID) as lastMonthAttendance FROM attendance WHERE MONTH(attendanceTime) = MONTH(NOW())-1 AND YEAR(attendanceTime) = YEAR(NOW())')
                lastMonthAttendance = cursor.fetchone()['lastMonthAttendance']
            if lastMonthAttendance is None:
                lastMonthAttendance = Decimal(0)
            if lastMonthAttendance and  lastMonthAttendance != 0:
                attendanceIncreasePercentage  = round((attendanceCount - lastMonthAttendance) / lastMonthAttendance * 100)
            else:
                attendanceIncreasePercentage = 0

            # Fetching instructor list
            cursor.execute('SELECT * FROM instructorinfo \
                        LEFT JOIN users ON users.userID = instructorinfo.userID \
                        WHERE users.userActive = TRUE')
            instructorList = cursor.fetchall()

            # Fetching pool list
            cursor.execute('SELECT * FROM pools WHERE poolType LIKE "Hydro%" OR poolType LIKE "Training%";')
            poolList = cursor.fetchall()

            # Fetching aqua list and enriching it with instructor name
            current_date2 = datetime.now().date()
            cursor.execute('SELECT * FROM aerobics_schedule WHERE bookingActive = "1" AND sessionTime >= %s;', [current_date2])
            aquaList = cursor.fetchall()
            for c in aquaList:
                cursor.execute('SELECT userName FROM users WHERE userID = %s;', (c['instructorID'],))
                instructorName = cursor.fetchall()[0]['userName']  
                c['instructorName'] = instructorName

            # Query to select top 3 aerobics classes in descending order
            cursor.execute('SELECT aerobics_schedule.sessionName FROM aerobics_schedule LEFT JOIN aerobics_bookings ON aerobics_schedule.scheduleID = aerobics_bookings.scheduleID WHERE aerobics_bookings.bookingActive = TRUE GROUP BY aerobics_schedule.sessionName, aerobics_schedule.scheduleID ORDER BY COUNT(aerobics_bookings.bookingID) DESC LIMIT 3;')
            top_classes = cursor.fetchall()   


            # --------------------------------------------------------
            # below is for printing the table of instructors schedule
            cursor.execute("SELECT * from time_slots;")
            timeSlots = cursor.fetchall()
            organizedTimeSlots = {}
            for timeSlot in timeSlots:
                organizedTimeSlots[timeSlot['slotsID']] = (timeSlot['startTime'], timeSlot['endTime'])
            
            # get instructor list data and restructure to dictionary
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM instructorinfo LEFT JOIN users ON users.userID = instructorinfo.userID WHERE userActive = 1;")
            instructorList = cursor.fetchall()

            organizedInstructors = {}
            instructorAvailability = {}
            for instructor in instructorList:
                bookings = getInstructorHistoryBookings(instructor['userID']) + getInstructorUpcomingBookings(instructor['userID'])
                organizedInstructors[instructor['userID']] = (bookings, instructor)

                query = '''SELECT availabilityID, userID, user_availability.slotsID, date, availability, startTime, endTime 
                            FROM user_availability
                            LEFT JOIN time_slots 
                            ON user_availability.slotsID = time_slots.slotsID
                            WHERE userID = %s AND availability = FALSE;'''
                cursor.execute(query,(instructor['userID'],))
                availableSlots = cursor.fetchall()
                organizedAvailability = {}
                startDate = date.today()
                for timeSlot in timeSlots:
                    organizedAvailability[timeSlot['slotsID']] = {startDate + timedelta(days=i): 1 for i in range(14)}
                for availableSLot in availableSlots:
                    if availableSLot['slotsID'] in organizedAvailability and availableSLot['date'] in organizedAvailability[timeSlot['slotsID']]:
                        organizedAvailability[availableSLot['slotsID']][availableSLot['date']]=0
                    # print(organizedAvailability)
                    # print(organizedAvailability.values())
                instructorAvailability[instructor['userID']] = organizedAvailability


            # --------------------------------------------------------
            # below is for printing the group class time table
            timeSlots = ["05:00 AM","06:00 AM","07:00 AM","08:00 AM","09:00 AM","10:00 AM","11:00 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM","06:00 PM","07:00 PM","08:00 PM","09:00 PM","10:00 PM"]

            query = '''SELECT * FROM
                (SELECT  aerobics_schedule.scheduleID,
                instructorID, 
                aerobics_schedule.bookingActive AS classActive,
                sessionName, 
                maxParticipants, 
                sessionTime,
                lessonDuration,
                TIMESTAMPADD(MINUTE,lessonDuration,sessionTime) AS endTime,
                aerobics_schedule.poolID, 
                bookingID,
                title,
                firstName,
                lastName,
                position,
                phoneNumber,
                email,
                introduction,
                (SELECT COUNT(bookingID) FROM aerobics_bookings WHERE scheduleID = aerobics_schedule.scheduleID AND aerobics_bookings.bookingActive = 1) AS bookingCount,
                poolType,
                description,
                aerobics_bookings.bookingActive AS bookingActive
                FROM aerobics_schedule 
                LEFT JOIN pools ON aerobics_schedule.poolID = pools.poolID
                LEFT JOIN aerobics_bookings ON aerobics_bookings.scheduleID = aerobics_schedule.scheduleID AND aerobics_bookings.customerID = %s 
                LEFT JOIN instructorinfo ON aerobics_schedule.instructorID = instructorinfo.userID) AS schedule
                WHERE DATE(sessionTime) BETWEEN %s AND %s ORDER BY sessionTime ASC;'''
            
            endDate = date.today() + timedelta(days=6)

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(query,(session['id'],startDate,endDate))
            classes = cursor.fetchall()
            organizedClasses = {}
            for timeSlot in timeSlots:
                organizedClasses[timeSlot] = {startDate + timedelta(days=i): [] for i in range(7)}
            for aquaClass in classes:
                classTime = aquaClass['sessionTime']
                classDate = classTime.date()
                classTimeSlot = classTime.replace(minute=0,second=0).strftime('%I:%M %p')
                if classTimeSlot in organizedClasses and classDate in organizedClasses[timeSlot]:
                    # print(organizedClasses[timeSlot])
                    organizedClasses[classTimeSlot][classDate].append(aquaClass)
            # print(organizedClasses)
            return render_template('admin_dashboard.html', session=session, totalMember=totalMember, totalSubscription=totalSubscription, SubsIn1Month=SubsIn1Month, month=month, monthlyPayment=monthlyPayment, paymentIncreasePercentage=paymentIncreasePercentage, subPayment=subPayment, individualPayment=individualPayment, attendanceCount=attendanceCount, attendanceIncreasePercentage=attendanceIncreasePercentage,instructorList=instructorList, poolList=poolList, aquaList=aquaList, instructorDict = organizedInstructors, instructorAvailability=instructorAvailability, timeSlots=organizedTimeSlots, top_classes=top_classes, classes=organizedClasses)

        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))

        


# member dashboard
@bp.route('/member/home')
def memberDashboard():
    if is_authenticated():
        if session['role'] == 3:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM instructorinfo LEFT JOIN users ON users.userID = instructorinfo.userID WHERE userActive = 1;")
            instructorList = cursor.fetchall()
            cursor.execute("SELECT * FROM memberinfo LEFT JOIN users ON users.userID = memberinfo.userID WHERE memberinfo.userID = %s",(session['id'],))
            memberInfo = cursor.fetchone()

            hasSubscription = checkSubscription(session['id'])
            historyBookings = getHistoryBookings()
            upcomingBookings = getUpcomingBookings()
            startDate = date.today()
            endDate = date.today() + timedelta(days=6)  
            timeSlots = ["05:00 AM","06:00 AM","07:00 AM","08:00 AM","09:00 AM","10:00 AM","11:00 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM","06:00 PM","07:00 PM","08:00 PM","09:00 PM","10:00 PM"]    
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('''SELECT * FROM
                (SELECT  aerobics_schedule.scheduleID,
                instructorID, 
                sessionName, 
                maxParticipants, 
                sessionTime,
                lessonDuration,
                TIMESTAMPADD(MINUTE,lessonDuration,sessionTime) AS endTime,
                aerobics_schedule.poolID, 
                bookingID,
                title,
                firstName,
                lastName,
                position,
                phoneNumber,
                email,
                introduction,
                (SELECT COUNT(bookingID) FROM aerobics_bookings WHERE scheduleID = aerobics_schedule.scheduleID) AS bookingCount,
                poolType,
                description
                FROM aerobics_schedule 
                LEFT JOIN pools ON aerobics_schedule.poolID = pools.poolID
                LEFT JOIN aerobics_bookings ON aerobics_bookings.scheduleID = aerobics_schedule.scheduleID AND aerobics_bookings.customerID = %s 
                LEFT JOIN instructorinfo ON aerobics_schedule.instructorID = instructorinfo.userID) AS schedule
                WHERE DATE(sessionTime) BETWEEN %s AND %s ORDER BY sessionTime ASC;''',(session['id'],startDate,endDate))
            classes = cursor.fetchall()
            

            organizedClasses = {}
            for timeSlot in timeSlots:
                organizedClasses[timeSlot] = {startDate + timedelta(days=i): [] for i in range(7)}
            # print(organizedClasses)
            for aquaClass in classes:
                classTime = aquaClass['sessionTime']
                classDate = classTime.date()
                classTimeSlot = classTime.replace(minute=0,second=0).strftime('%I:%M %p')
                if classTimeSlot in organizedClasses and classDate in organizedClasses[timeSlot]:
                    # print(organizedClasses[timeSlot])
                    organizedClasses[classTimeSlot][classDate].append(aquaClass)
            return render_template('member_dashboard.html',session=session,instructorList=instructorList, memberInfo=memberInfo,  hasSubscription=hasSubscription, historyBookings=historyBookings, upcomingBookings=upcomingBookings, classes=organizedClasses)
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))
    
# instructor dashboard
@bp.route('/instructor/home')
def instructorDashboard():
    if is_authenticated():
        if session['role'] == 2:
            upcomingBookings = getInstructorUpcomingBookings(session['id'])
            historyBookings = getInstructorHistoryBookings(session['id'])
            instructor = getInstructorByUserId(session['id'])
            return render_template('instructor_dashboard.html', session=session, upcomingBookings=upcomingBookings, historyBookings=historyBookings, instructor=instructor)
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))

    

# list all active members 
@bp.route('/admin/members')
def memberList():
    if is_authenticated():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM memberinfo LEFT JOIN users ON users.userID = memberinfo.userID WHERE users.userActive = TRUE')
        customerList = cursor.fetchall()
        if session['role'] == 1:
            return render_template('member_list.html', customerList=customerList, session=session) 
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))
    
# list all active tutors 
@bp.route('/admin/instructors')
def instructorList():
    if is_authenticated():        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM instructorinfo LEFT JOIN users ON users.userID = instructorinfo.userID WHERE users.userActive = TRUE')
        instructorList = cursor.fetchall()
        if session['role'] == 1:
            return render_template('instructor_list.html', instructorList=instructorList, session=session) 
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))

# check user's profile page by userid
@bp.route('/profile/<userId>')
def checkProfile(userId):
    if is_authenticated():        
        account = get_account(userId)        
        if account and (session['role'] == 1 or (session['role']==2 and account['userPermission']==3) or session['id']==account['userID']):            
            return render_template('user_profile.html',account=account, session=session)
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))

# update profile information on profile page
@bp.route('/profile/update', methods=['GET', 'POST'])
def updateProfile():
    if is_authenticated():
        userId = request.form.get('userId')
        account = get_account(userId)        
        if account and (session['role'] == 1 or session['id'] == account['userID']):
            userName = request.form.get('userName')
            title = request.form.get('title')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            phoneNumber = request.form.get('phoneNumber')
            position = request.form.get('position')
            email = request.form.get('email')
            userPassword = request.form.get('userPassword')            
            if account['userPermission'] == 3:
                dateOfBirth = request.form.get('dateOfBirth')
                physicalAddress = request.form.get('physicalAddress')
                healthInfo = request.form.get('healthInfo')
            elif account['userPermission'] == 2:
                introduction = request.form.get('introduction')

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #if username is changed:
            if userName != account['userName']:
                #check if username already exists in database
                if userNameCrash(userName):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    return redirect(url_for('adminDashboardFunc.checkProfile',userId=account['userID']))
                else:
                    cursor.execute('UPDATE users SET userName=%s WHERE userID=%s',(userName, userId))
                    mysql.connection.commit()
                    flash('Username changed successfully!','success')

            # check if the password is changed by comparing the input password with the password stored in database

            if userPassword.encode('utf-8') !=  account['userPassword'].encode('utf-8'):
                if userPassword != "********" and not bcrypt.checkpw(userPassword.encode('utf-8'), account['userPassword'].encode('utf-8')):
                    print (userPassword)
                    print(account['userPassword'])

                    # if password is changed, then the new password needs to be encrypted before inserting into databse
                    hashed = passwordEncrypt(userPassword)
                    cursor.execute('UPDATE users SET userPassword=%s WHERE userID=%s',(hashed, userId))
                    mysql.connection.commit()
                    flash('Password changed successfully!','success')
            
            if 'avatar' in request.files and request.files['avatar'].filename != '':
                avatar = request.files.get('avatar')                
                avatarName = f"{userId}.jpg"                
                filePath = os.path.join('app', 'static', 'uploadAvatar', avatarName)
                avatar.save(filePath)
            # else:
            #     flash('Failed. Uploaded avatar file type is incorrect.')
            #     return redirect(url_for('dashboardFunc1.checkProfile',userId=userId))

            # update the other data to the database

            if account['userPermission']== 3 and (email != account['email'] or firstName != account['firstName'] or lastName != account['lastName'] or phoneNumber != account['phoneNumber'] or physicalAddress != account['physicalAddress'] or title != account['title'] or position != account['position'] or healthInfo != account['healthInfo'] or dateOfBirth != str(account['dateOfBirth'])):
                cursor.execute('UPDATE memberinfo SET email=%s,firstName=%s,lastName=%s,phoneNumber=%s,physicalAddress=%s, title=%s, position=%s, healthInfo=%s, dateOfBirth=%s WHERE memberinfo.userID=%s', (email,firstName,lastName,phoneNumber,physicalAddress,title,position,healthInfo, dateOfBirth,userId))
                mysql.connection.commit()
                flash('Profile information updated successfully!','success')
                return redirect(url_for('adminDashboardFunc.checkProfile',userId=userId))
            elif account['userPermission'] == 2 and (email != account['email'] or firstName != account['firstName'] or lastName != account['lastName'] or phoneNumber != account['phoneNumber'] or title != account['title'] or position != account['position'] or introduction != account['introduction']):
                cursor.execute('UPDATE instructorinfo SET email=%s,firstName=%s,lastName=%s,phoneNumber=%s,title=%s, position=%s,introduction=%s WHERE instructorinfo.userID = %s', (email,firstName,lastName,phoneNumber,title,position,introduction,userId))
                mysql.connection.commit()
                flash('Profile information updated successfully!','success')
                return redirect(url_for('adminDashboardFunc.checkProfile',userId=userId))

            elif account['userPermission'] == 1 and (email != account['email'] or firstName != account['firstName'] or lastName != account['lastName'] or phoneNumber != account['phoneNumber'] or title != account['title'] or position != account['position']):
                cursor.execute('UPDATE admininfo SET email=%s,firstName=%s,lastName=%s,phoneNumber=%s,title=%s, position=%s WHERE admininfo.userID = %s', (email,firstName,lastName,phoneNumber,title,position,userId))
                mysql.connection.commit()
                flash('Profile information updated successfully!','success')
                return redirect(url_for('adminDashboardFunc.checkProfile',userId=userId))
            else:
                return redirect(url_for('adminDashboardFunc.checkProfile',userId=userId))
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))


# update profile information on member list page
@bp.route('/admin/update/user', methods=['GET', 'POST'])
def updateUser():
    if is_authenticated():
        userId = request.form.get('userId')
        account = get_account(userId)
        if session['role'] == 1:
            userName = request.form.get('userName')
            title = request.form.get('title')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            phoneNumber = request.form.get('phoneNumber')
            email = request.form.get('email')
            userPassword = request.form.get('userPassword')
            position = request.form.get('position')
            if account['userPermission'] == 3:
                dateOfBirth = request.form.get('dateOfBirth')
                physicalAddress = request.form.get('physicalAddress')
                healthInfo = request.form.get('healthInfo')
            elif account['userPermission'] == 2:
                introduction = request.form.get('introduction')

            
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #if username is changed:
            if userName != account['userName']:
                #check if username already exists in database
                if userNameCrash(userName):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    if account['userPermission']== 3:
                        return redirect(url_for('adminDashboardFunc.memberList'))
                    elif account['userPermission'] == 2:
                        return redirect(url_for('adminDashboardFunc.instructorList'))
                    else:
                        return 404
                else:
                    cursor.execute('UPDATE users SET userName=%s WHERE userID=%s',(userName, userId))
                    mysql.connection.commit()
                    flash('Username updated successfully!', 'success')

            # check if the password is changed by comparing the input password with the password stored in database
            if userPassword.encode('utf-8') != account['userPassword'].encode('utf-8'):
                if userPassword != "********" and not bcrypt.checkpw(userPassword.encode('utf-8'), account['userPassword'].encode('utf-8')):
                    # if password is changed, then the new password needs to be encrypted before inserting into databse
                    hashed = passwordEncrypt(userPassword)
                    cursor.execute('UPDATE users SET userPassword=%s WHERE userID=%s',(hashed, userId))
                    mysql.connection.commit()
                    flash('Password updated successfully!', 'success')  

            # update the other data to the database
            if account['userPermission']== 3:
                cursor.execute('UPDATE memberinfo SET email=%s,firstName=%s,lastName=%s,phoneNumber=%s,physicalAddress=%s, title=%s, position=%s, healthInfo=%s, dateOfBirth=%s WHERE memberinfo.userID=%s', (email,firstName,lastName,phoneNumber,physicalAddress,title,position,healthInfo, dateOfBirth,userId))
                mysql.connection.commit()
                flash('Profile information updated successfully!','success')
                return redirect(url_for('adminDashboardFunc.memberList'))
            elif account['userPermission'] == 2:
                cursor.execute('UPDATE instructorinfo SET email=%s,firstName=%s,lastName=%s,phoneNumber=%s,title=%s, position=%s, introduction=%s WHERE instructorinfo.userID=%s', (email,firstName,lastName,phoneNumber,title,position,introduction,userId))
                mysql.connection.commit()
                flash('Profile information updated successfully!','success')
                return redirect(url_for('adminDashboardFunc.instructorList'))
            else:
                return render_template('unauthorized.html')
        else:
             return "unauthorized"
    else:
        return redirect(url_for('login.login'))


# delete a member on member list page
@bp.route('/admin/delete/user/<userId>')
def deleteUser(userId):
    if is_authenticated():
        if session['role'] == 1:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM users WHERE userID=%s and userActive = True',(userId,))
            userToDelete = cursor.fetchone()
            current_time = datetime.now()

            # delete a user
            if userToDelete['userPermission'] == 3:
                # Check if the customer has booked lessons, 
                cursor.execute('SELECT lessonDate, lessonTime FROM individual_lesson_bookings WHERE customerID=%s',(userId,))
                lessons = cursor.fetchall()
                
                cursor.execute('SELECT aerobics_schedule.sessionTime FROM aerobics_schedule INNER JOIN aerobics_bookings ON aerobics_schedule.scheduleID = aerobics_bookings.scheduleID WHERE aerobics_bookings.customerID = %s', (userId,))
                sessionTimes = cursor.fetchall()
                canBedelete = True
                
                for (course_dateDict, course_timeDict) in lessons:
                    course_date = course_dateDict['course_date']
                    course_time = course_timeDict['course_time']
                    if course_date >= current_time.date() and course_time >= current_time.time():
                        canBedelete = False                
              
                for sessionDict in sessionTimes:
                    sessionTime = sessionDict['sessionTime']                  
                    if sessionTime >= current_time:
                        canBedelete = False                           

                if not canBedelete:
                    flash('Cannot delete user who has booked classes or lessons.','error')
                    return redirect(url_for('adminDashboardFunc.memberList'))
                else:
                    cursor.execute('UPDATE users SET userActive=False WHERE userID=%s',(userId,))
                    mysql.connection.commit()
                    flash('Delete successfully!','success')
                    return redirect(url_for('adminDashboardFunc.memberList'))

            # delete a staff
            elif userToDelete['userPermission'] == 2:
                # check if the instructor has booked lessons
                cursor.execute('SELECT lessonDate, lessonTime FROM individual_lesson_bookings WHERE instructorID=%s',(userId,))
                lessons=cursor.fetchall()
                cursor.execute('SELECT sessionTime FROM aerobics_schedule WHERE instructorID=%s',(userId,))
                sessionTimes=cursor.fetchall()
                canBedelete = True
                
                # for (course_dateDict, course_timeDict) in lessons:
                #     course_date = course_dateDict['course_date']
                #     course_time = course_timeDict['course_time']
                for i in lessons:
                    course_date = i['lessonDate']
                    course_time = i['lessonTime']
                    course_time = timedeltaToTime(course_time)

                    course_datetime = datetime.combine(course_date, course_time)
                    
                    if course_datetime >= current_time:
                        canBedelete = False                
              
                for sessionDict in sessionTimes:
                    sessionTime = sessionDict['sessionTime'] 
                           
                    if sessionTime >= current_time:
                        canBedelete = False     
                        

                if not canBedelete:
                    flash('Cannot delete a user who has booked classes or lessons.','error')
                    return redirect(url_for('adminDashboardFunc.instructorList'))
                else:
                    cursor.execute('UPDATE users SET userActive=False WHERE userID=%s',(userId,))
                    mysql.connection.commit()
                    flash('Delete successfully!','success')
                return redirect(url_for('adminDashboardFunc.instructorList'))
            else:
                return 404
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))
    
     
# add a member on member list page
@bp.route('/admin/add/user', methods=['Get', 'POST'])
def addUser():
    if is_authenticated():
        userType = int(request.form.get('userType'))
        if session['role'] == 1:
            userName = request.form.get('userName')
            title = request.form.get('title')
            firstName = request.form.get('firstName')
            lastName = request.form.get('lastName')
            phoneNumber = request.form.get('phoneNumber')
            email = request.form.get('email')
            userPassword = request.form.get('userPassword')
            position = request.form.get('position')
            if userType == 3:
                dateOfBirth = request.form.get('dateOfBirth')
                physicalAddress = request.form.get('physicalAddress')
                healthInfo = request.form.get('healthInfo')
            elif userType == 2:
                introduction = request.form.get('introduction')
            
            if userNameCrash(userName):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    if userType == 3:
                        return redirect(url_for('adminDashboardFunc.memberList'))
                    elif userType == 2:
                        return redirect(url_for('adminDashboardFunc.instructorList'))
                    else:
                        return 404
            # insert the data to the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if userType == 2:
                cursor.execute('INSERT INTO users (userName, userPassword, userPermission) VALUES (%s, %s, %s)',(userName, passwordEncrypt(userPassword), 2))
                userId = cursor.lastrowid
                cursor.execute('INSERT INTO instructorinfo (email,firstName,lastName,phoneNumber,title, position, introduction,userID) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)',(email,firstName,lastName,phoneNumber,title,position,introduction,userId))
                mysql.connection.commit()
                flash("You have successfully added a staff!",'success')
                return redirect(url_for('adminDashboardFunc.instructorList'))
            elif userType == 3:
                cursor.execute('INSERT INTO users (UserName, userPassword, userPermission) VALUES (%s, %s, %s)',(userName, passwordEncrypt(userPassword), 3))
                userId = cursor.lastrowid
                cursor.execute('INSERT INTO memberinfo (userID,email,firstName,lastName,phoneNumber,physicalAddress,title,position,healthInfo,dateOfBirth) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)',(userId,email,firstName,lastName,phoneNumber,physicalAddress,title,position,healthInfo,dateOfBirth))
                mysql.connection.commit()
                flash("You have successfully added a member!",'success')
                return redirect(url_for('adminDashboardFunc.memberList'))
            else:
                return 404
        else:
            return "unauthorized"
    else:
        return redirect(url_for('login.login'))
    

@bp.route('/admin/delete/<lessonID>')
def deleteAquaClass(lessonID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM aerobics_schedule WHERE scheduleID = %s',(lessonID,))
    originalClass = cursor.fetchall()
    instructor = originalClass[0]['instructorID']
    originalClassDate = originalClass[0]['sessionTime'].date()
    originalClassTime = originalClass[0]['sessionTime'].time()
    originalDuration = originalClass[0]['lessonDuration']
    originalClassName = originalClass[0]['sessionName']
    labelAvailable(instructor, originalClassDate, originalClassTime, originalDuration)


    cursor.execute('UPDATE aerobics_schedule SET bookingActive = 0 WHERE scheduleID = %s;',(lessonID,))
    mysql.connection.commit()

    #Send news

    title = f"[CANCELLED] {originalClassName} has been cancelled."
    content = f"""{originalClassName} has been cancelled. Please re-book a new class or contact admin."""

    cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, 0)', 
                    (title, content, datetime.now(), session['id']))
    
    cursor.execute('SELECT * FROM aerobics_bookings JOIN memberinfo ON memberinfo.userID=aerobics_bookings.customerID WHERE scheduleID = %s;', (lessonID,))
    classAttendee = cursor.fetchall()
    if classAttendee:
        for p in range(0, len(classAttendee)):
            cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
                    (title, content, datetime.now(), session['id'], classAttendee[p]['userID']))
    mysql.connection.commit()
    
    flash('Schedule deleted!','success')
    return redirect(url_for('adminDashboardFunc.aqua'))

@bp.route('/admin/delete/aquaBooking', methods=['POST'])
def deleteAquaClassAttendee():
    originalAquaBookingID = request.form.get('originalAquaBookingID')
    originalClassName = request.form.get('originalClassName')
    originalUserID = request.form.get('originalUserID')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE aerobics_bookings SET bookingActive=False WHERE bookingID=%s',(originalAquaBookingID,))

    title = f"[REMOVED] You have been removed from {originalClassName}."
    content = f"""You have been removed from {originalClassName}. Please re-book a new class or contact admin."""
    cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
                    (title, content, datetime.now(), session['id'], originalUserID))

    mysql.connection.commit()
    
    flash('Booking deleted!','success')
    return redirect(url_for('adminDashboardFunc.aqua'))

@bp.route('/admin/aqua/checkin', methods=['POST'])
def attendanceAquaClass():
    AquaBookingID = request.form.get('originalAquaBookingID2')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('UPDATE aerobics_bookings SET bookingAttend=True WHERE bookingID=%s',(AquaBookingID,))
    mysql.connection.commit()
    flash('checkin successful','success')
    return redirect(url_for('adminDashboardFunc.aqua'))



@bp.route('/admin/individual', methods=['Get', 'POST'])
def individual():

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM instructorinfo \
                   LEFT JOIN users ON users.userID = instructorinfo.userID \
                   WHERE users.userActive = TRUE')
    instructorList = cursor.fetchall()

    cursor.execute('SELECT * FROM pools;')
    poolList = cursor.fetchall()

    cursor.execute('SELECT * FROM individual_lesson_bookings;')
    individualList = cursor.fetchall()

    if individualList:
        for c in individualList:
            cursor.execute('SELECT * FROM instructorinfo WHERE userID = %s;', (c['instructorID'],))
            instructorName = cursor.fetchall()[0]['firstName']
            c['instructorName'] = instructorName

            cursor.execute('SELECT * FROM memberinfo WHERE userID = %s;', (c['customerID'],))
            customerName = cursor.fetchall()[0]['firstName']
            c['customerName'] = customerName

            cursor.execute('SELECT poolType FROM pools WHERE poolID = %s;', (c['poolID'],))
            poolName = cursor.fetchall()[0]['poolType']
            c['poolName'] = poolName


    return render_template('individualClass.html', instructorList=instructorList, poolList=poolList, individualList=individualList)

@bp.route('/admin/delete/individual/<bookingID>')
def deleteIndividualClass(bookingID):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM individual_lesson_bookings WHERE bookingID = %s',(bookingID,))
    originalClass = cursor.fetchall()
    customer = originalClass[0]['customerID']
    instructor = originalClass[0]['instructorID']
    originalClassDate = originalClass[0]['lessonDate']
    originalClassTime = originalClass[0]['lessonTime']
    originalDuration = originalClass[0]['lessonDuration']
    labelAvailable(instructor, originalClassDate, originalClassTime, originalDuration)


    cursor.execute('UPDATE individual_lesson_bookings SET bookingActive = 0 WHERE bookingID = %s;',(bookingID,))
    mysql.connection.commit()

    #Send news

    title = f"[REMOVED] Your individual lesson on {originalClassDate.strftime('%Y-%m-%d')} has been cancelled."
    content = f"""Your individual lesson on {originalClassDate.strftime('%Y-%m-%d')} has been cancelled. Please re-book a new class or contact admin."""
    


    cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
            (title, content, datetime.now(), session['id'], customer))
    cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
            (title, content, datetime.now(), session['id'], instructor))
    mysql.connection.commit()
    
    flash('Schedule deleted!','success')
    return redirect(url_for('adminDashboardFunc.individual'))

@bp.route('/admin/aqua', methods=['Get', 'POST'])
def aqua():
    className = request.form.get('sessionName')
    instructor = request.form.get('instructor')
    duration = request.form.get('duration')
    maxP = request.form.get('maxParticipants')
    dateClass = request.form.get('sessionTime')
    timeClass = request.form.get('sessionTime2')
    poolID = request.form.get('pool')
    originalID = request.form.get('originalID')

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM instructorinfo \
                   LEFT JOIN users ON users.userID = instructorinfo.userID \
                   WHERE users.userActive = TRUE')
    instructorList = cursor.fetchall()

    cursor.execute('SELECT * FROM pools WHERE poolType LIKE "Hydro%" OR poolType LIKE "Training%";')
    poolList = cursor.fetchall()

    cursor.execute('SELECT * FROM aerobics_schedule;')
    aquaList = cursor.fetchall()

    if aquaList:
        for c in aquaList:
            cursor.execute('SELECT * FROM instructorinfo WHERE userID = %s;', (c['instructorID'],))
            instructorName = cursor.fetchall()[0]['firstName']
            c['instructorName'] = instructorName

            cursor.execute('SELECT poolType FROM pools WHERE poolID = %s;', (c['poolID'],))
            poolName = cursor.fetchall()[0]['poolType']
            c['poolName'] = poolName

            cursor.execute('SELECT * FROM aerobics_bookings JOIN memberinfo ON memberinfo.userID=aerobics_bookings.customerID WHERE scheduleID = %s;', (c['scheduleID'],))
            classAttendee = cursor.fetchall()
            c['classAttendee'] = classAttendee
    

    if className:
        # convert to datetime in database
        classTimeString = f'{dateClass} {timeClass}'
        sessionTimeMix = datetime.strptime(classTimeString, '%Y-%m-%d %H:%M')

        timeClass = datetime.strptime(timeClass, '%H:%M')

        if int(duration) == 30:
            timeClassEndTime = timeClass + timedelta(minutes = 30)
        elif int(duration) == 60:
            timeClassEndTime = timeClass + timedelta(hours = 1)

        timeClass = timeClass.strftime("%H:%M:%S")
        timeClassEnd = timeClassEndTime.strftime("%H:%M:%S")


        if originalID:
            cursor.execute('SELECT * FROM aerobics_schedule WHERE scheduleID = %s',(originalID,))
            originalClass = cursor.fetchall()
            originalClassDate = originalClass[0]['sessionTime'].date()
            originalClassTime = originalClass[0]['sessionTime'].time()
            originalDuration = originalClass[0]['lessonDuration']
            originalInstructor = originalClass[0]['instructorID']

            # do not check time if time did not change.
            if dateClass != originalClassDate.strftime('%Y-%m-%d') or timeClass != originalClassTime.strftime('%H:%M:%S'):
                checkInstructorAvailability = checkUserAvailability(instructor, dateClass, timeClass, duration)
                if checkInstructorAvailability == False:
                    flash("The instructor is not available in the time slot!",'success')
                    return redirect(url_for('adminDashboardFunc.aqua'))
                else:
                    labelAvailable(originalInstructor, originalClassDate, originalClassTime, originalDuration)
                    labelUnavailable(instructor, dateClass, timeClass, duration)
                    
            else:
                labelAvailable(originalInstructor, originalClassDate, originalClassTime, originalDuration)
                labelUnavailable(instructor, dateClass, timeClass, duration)
                
            
            cursor.execute('UPDATE aerobics_schedule SET \
                        instructorID = %s, sessionName = %s, maxParticipants = %s, sessionTime = %s, lessonDuration = %s, poolID = %s \
                        WHERE scheduleID = %s',\
                            (instructor, className, maxP, sessionTimeMix, duration, poolID, originalID))
            
            #Send news
            cursor.execute('SELECT * FROM instructorinfo WHERE userID = %s;', (instructor,))
            instructorName = cursor.fetchall()[0]['firstName']

            cursor.execute('SELECT poolType FROM pools WHERE poolID = %s;', (poolID,))
            poolName = cursor.fetchall()[0]['poolType']
            
            title = f"[CHANGE] {className}'s schedule has changed."
            content = f"""The schedule of {className} has been changed. Please check the new details.
                        Status: Active
                        Instructor: {instructorName}
                        Duration: {duration} min
                        Date: {sessionTimeMix}
                        Max Capacity: {maxP}
                        Pool: {poolName}
                        """

            cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, 0)', 
                           (title, content, datetime.now(), session['id']))
            
            cursor.execute('SELECT * FROM aerobics_bookings JOIN memberinfo ON memberinfo.userID=aerobics_bookings.customerID WHERE scheduleID = %s;', (originalID,))
            classAttendee = cursor.fetchall()
            if classAttendee:
                for p in range(0, len(classAttendee)):
                    if classAttendee[p]['bookingActive'] == 1:
                        cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
                                (title, content, datetime.now(), session['id'], classAttendee[p]['userID']))
            mysql.connection.commit()
            flash("You have successfully edited a group class!",'success')
        
        else:
            # check if time in working time and availability

            checkInstructorAvailability = checkUserAvailability(instructor, dateClass, timeClass, duration)

            if checkInstructorAvailability == False:
                flash("The instructor is not available in the time slot!",'success')
                return redirect(url_for('adminDashboardFunc.aqua'))
            else:
                labelUnavailable(instructor, dateClass, timeClass, duration)
                cursor.execute('INSERT INTO aerobics_schedule \
                            (instructorID, sessionName, maxParticipants, sessionTime, lessonDuration, poolID) \
                            VALUES (%s,%s,%s,%s,%s,%s)',\
                                (instructor, className, maxP, sessionTimeMix, duration, poolID))
                mysql.connection.commit()

            #Send news
            cursor.execute('SELECT * FROM instructorinfo WHERE userID = %s;', (instructor,))
            instructorName = cursor.fetchall()[0]['firstName']

            cursor.execute('SELECT poolType FROM pools WHERE poolID = %s;', (poolID,))
            poolName = cursor.fetchall()[0]['poolType']

            title = f"[NEW] Welcome to our new class: {className}"
            content = f"""Please see details below. 
                        Status: Active
                        Instructor: {instructorName}
                        Duration: {duration} min
                        Date: {sessionTimeMix}
                        Max Capacity: {maxP}
                        Pool: {poolName}
                        """

            cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, 0)', 
                           (title, content, datetime.now(), session['id']))
            
            
            mysql.connection.commit()

            flash("You have successfully added a group class!",'success')
        return redirect(url_for('adminDashboardFunc.aqua'))

    return render_template('aquaClass.html', instructorList=instructorList, poolList=poolList, aquaList=aquaList)


@bp.route('/admin/financialReport', methods=['Get', 'POST'])
def financialReport():
    startDateStr = request.form.get('startDate')
    endDateStr = request.form.get('endDate')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('''    
        WITH RecentYears AS (
            SELECT YEAR(CURRENT_DATE) AS year
            UNION SELECT YEAR(CURRENT_DATE) - 1
            UNION SELECT YEAR(CURRENT_DATE) - 2
            UNION SELECT YEAR(CURRENT_DATE) - 3
            UNION SELECT YEAR(CURRENT_DATE) - 4
        )
        SELECT 
            ry.year AS paymentYear,
            COALESCE(SUM(p.amount), 0) AS yearlyPayment,
            COALESCE(SUM(CASE WHEN p.paymentType = 1 THEN p.amount ELSE 0 END), 0) AS subscriptionsYearlyPayment,
            COALESCE(SUM(CASE WHEN p.paymentType = 2 THEN p.amount ELSE 0 END), 0) AS classYearlyPayment
        FROM RecentYears ry
        LEFT JOIN payments p ON ry.year = YEAR(p.paymentTime)
        GROUP BY ry.year
        ORDER BY ry.year ASC;
                   ''')
    yearlyPayments = cursor.fetchall()

    cursor.execute('''    
    WITH Months AS (
        SELECT 1 AS month
        UNION SELECT 2
        UNION SELECT 3
        UNION SELECT 4
        UNION SELECT 5
        UNION SELECT 6
        UNION SELECT 7
        UNION SELECT 8
        UNION SELECT 9
        UNION SELECT 10
        UNION SELECT 11
        UNION SELECT 12
    )
    SELECT    
        Months.month as paymentMonth,
        COALESCE(YEAR(p.paymentTime), YEAR(NOW())) as paymentYear,
        COALESCE(SUM(p.amount), 0) as monthlyPayment,
        COALESCE(SUM(CASE WHEN p.paymentType = 1 THEN p.amount ELSE 0 END), 0) as subscriptionsMonthlyPayment,
        COALESCE(SUM(CASE WHEN p.paymentType = 2 THEN p.amount ELSE 0 END), 0) as classMonthlyPayment
    FROM
        Months    
    LEFT JOIN
    payments p
    ON Months.month = MONTH(p.paymentTime) AND YEAR(p.paymentTime) = YEAR(NOW())
    GROUP BY        
        Months.month, paymentYear
    ORDER BY        
        paymentYear, Months.month;            
    ''')
    monthlyPayments = cursor.fetchall()      


    if startDateStr and endDateStr:
        startDate = datetime.strptime(startDateStr, '%Y-%m-%d')    
        endDate = datetime.strptime(endDateStr, '%Y-%m-%d')

        query = '''SELECT
        SUM(p.amount) as totalPayment,  
        SUM(CASE WHEN p.paymentType = 1 THEN p.amount ELSE 0 END) as subscriptionsPayment, 
        SUM(CASE WHEN p.paymentType = 2 THEN p.amount ELSE 0 END) as classPayment
        FROM
        payments p
        WHERE DATE(paymentTime) BETWEEN %s AND %s'''
        
        cursor.execute(query, (startDate, endDate))
        selectAmount = cursor.fetchone()   
    else:
        selectAmount = {}   

    return render_template('financialReport.html', start_date=startDateStr, end_date=endDateStr,selectAmount=selectAmount, monthlyPayments=monthlyPayments, yearlyPayments=yearlyPayments)


@bp.route('/admin/paymentList', methods=['GET', 'POST'])
def paymentList():      
    customerFilter = request.form.get('customerFilter')
    paymentTypeFilter = request.form.get('paymentTypeFilter')  
    
    query = """SELECT m.userID, m.title, m.firstName, m.lastName, m.phoneNumber, p.paymentType, p.amount, p.paymentTime, s.startDate, s.endDate 
    FROM memberinfo m 
    INNER JOIN payments p ON m.userID = p.customerID 
    INNER JOIN subscriptions s ON p.customerID = s.userID 
    WHERE 1=1 """    
    if customerFilter:
        query += f" AND p.customerID = {customerFilter}"
    if paymentTypeFilter:
        query += f" AND p.paymentType = {paymentTypeFilter}"
    query += " ORDER BY m.userID, p.paymentTime "
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query)
    payments = cursor.fetchall()
    totalAmount = 0
    for payment in payments:
        totalAmount += payment['amount']
    
    

    cursor.execute("SELECT userID, firstName, lastName FROM memberinfo")
    member_list = cursor.fetchall()

    currentDate = datetime.now().date()
    
    return render_template('paymentList.html', payments=payments, member_list=member_list, totalAmount=totalAmount, currentDate=currentDate)
    

@bp.route('/admin/attendanceReport', methods=['GET', 'POST'])
def attendanceReport():
    startDateStr = request.form.get('startDate')
    endDateStr = request.form.get('endDate')

    selected_member = request.form.get('selected_member')
    selected_attendanceType = request.form.get('selected_attendanceType')

    query = "SELECT memberinfo.firstName, memberinfo.lastName, attendance.userID, attendance.attendanceType, COUNT(*) as count FROM attendance INNER JOIN memberinfo ON memberinfo.userID = attendance.userID WHERE 1=1"
    params = []

    if startDateStr:
        startDate = datetime.strptime(startDateStr, '%Y-%m-%d')
        query += " AND DATE(attendance.attendanceTime) >= %s"
        params.append(startDate)

    if endDateStr:
        endDate = datetime.strptime(endDateStr, '%Y-%m-%d')
        query += " AND DATE(attendance.attendanceTime) <= %s"
        params.append(endDate)

    if selected_member:
        query += " AND attendance.userID = %s"
        params.append(selected_member)
    
    if selected_attendanceType:
        query += " AND attendance.attendanceType = %s"
        params.append(selected_attendanceType)

    query += " GROUP BY userID, attendanceType"

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query, params)
    attendance_data = cursor.fetchall()

    cursor.execute('''
    WITH Months AS (
        SELECT 1 AS month
        UNION SELECT 2
        UNION SELECT 3
        UNION SELECT 4
        UNION SELECT 5
        UNION SELECT 6
        UNION SELECT 7
        UNION SELECT 8
        UNION SELECT 9
        UNION SELECT 10
        UNION SELECT 11
        UNION SELECT 12
    )
    SELECT    
        Months.month as attendanceMonth,
        COALESCE(YEAR(a.attendanceTime), YEAR(NOW())) as attendanceYear,
        COALESCE(COUNT(a.attendanceID), 0) as monthlyAttendanceCount,
        COALESCE(SUM(CASE WHEN a.attendanceType = 1 THEN 1 ELSE 0 END), 0) as usingPoolCount,
        COALESCE(SUM(CASE WHEN a.attendanceType = 2 THEN 1 ELSE 0 END), 0) as individualClassCount,
        COALESCE(SUM(CASE WHEN a.attendanceType = 3 THEN 1 ELSE 0 END), 0) as aquaClassCount
    FROM
        Months    
    LEFT JOIN
    attendance a
    ON Months.month = MONTH(a.attendanceTime) AND YEAR(a.attendanceTime) = YEAR(NOW())
    GROUP BY        
        Months.month, attendanceYear
    ORDER BY        
        attendanceYear, Months.month;           
    ''')
    monthlyAttendanceData = cursor.fetchall() 
    
    cursor.execute("SELECT userID, firstName, lastName FROM memberinfo")
    member_list = cursor.fetchall()

    return render_template('attendanceReport.html', attendance_data=attendance_data,monthlyAttendanceData=monthlyAttendanceData, member_list=member_list, startDateStr=startDateStr, endDateStr=endDateStr)
  
@bp.route('/admin/checkin', methods=['GET', 'POST'])
def checkin():
    userID = request.form.get('userID')
    attendanceType = request.form.get('attendanceType')
    timeNow = datetime.now()

    if userID:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM memberinfo WHERE userID = %s',(userID,))
        userInfo = cursor.fetchall()

        if userInfo:
            cursor.execute('INSERT into attendance (userID, attendanceType, attendanceTime) VALUES (%s, %s, %s)', (userID, attendanceType, timeNow))
            cursor.connection.commit()

            # For Individual class
            if attendanceType == '2':
                today = timeNow.date()
                cursor.execute('UPDATE individual_lesson_bookings SET bookingAttend = TRUE WHERE customerID = %s AND lessonDate = %s', (userID, today))
                cursor.connection.commit()
            
            # For Aqua aerobics class
            elif attendanceType == '3':
                today = timeNow.date()
                cursor.execute('UPDATE aerobics_bookings SET bookingAttend = TRUE WHERE customerID = %s AND bookingTime = %s', (userID, today))
                cursor.connection.commit()

            flash('User is checked in!', 'success')
            return redirect(url_for('adminDashboardFunc.checkin'))
        
        else:
            flash('Did not find the member in the record!', 'success')
            return redirect(url_for('adminDashboardFunc.checkin'))

    return render_template('checkin.html')


