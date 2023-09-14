from app import mysql
from flask import flash, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from datetime import date, datetime, timedelta
import MySQLdb.cursors
import bcrypt
import math
import os
import calendar

bp = Blueprint('memberDashboardFunc', __name__, )

def is_authenticated():
    return 'loggedin' in session

startDate = date.today()
endDate = date.today() + timedelta(days=6)

timeSlots = ["05:00 AM","06:00 AM","07:00 AM","08:00 AM","09:00 AM","10:00 AM","11:00 AM","12:00 PM","01:00 PM","02:00 PM","03:00 PM","04:00 PM","05:00 PM","06:00 PM","07:00 PM","08:00 PM","09:00 PM","10:00 PM"]

def checkSubscription(userId):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM subscriptions WHERE userID = %s", (userId,))
    subscriptionToCheck = cursor.fetchone()
    current_date = datetime.now()
    threshold_date = current_date + timedelta(days=30)  # 30 days from now

    if subscriptionToCheck:
        # Convert date to datetime for comparison
        subscription_end_datetime = datetime.combine(subscriptionToCheck['endDate'], datetime.min.time())
        
        # Check if subscription is active
        if subscription_end_datetime >= current_date:
            # Check if subscription ends within 30 days
            if subscription_end_datetime <= threshold_date:
                return -1  # Subscription is active but ends within 30 days
            else:
                return True  # Subscription is active and does not end within 30 days
        else:
            return False  # Subscription has ended
    else:
        return False  # No active subscription




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

@bp.route('/member/timetable/aqua_aerobics_class')
def aquaAerobicsClassTimetable():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(query,(session['id'],startDate,endDate))
    classes = cursor.fetchall()
    # print(classes)
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
    # print(organizedClasses)

    return render_template("timetable_aquaAerobicsClass.html", classes=organizedClasses)


@bp.route('/member/book/aqua_aerobics_class/<scheduleId>')
def bookClass(scheduleId):
    if checkSubscription(session['id']):
        # print(scheduleId)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"SELECT * FROM aerobics_schedule WHERE sessionTime > NOW() AND scheduleID = '{scheduleId}';")
        classToBook = cursor.fetchone()
        # print(classToBook)
        if classToBook:
            cursor.execute("SELECT COUNT(bookingID) FROM aerobics_bookings WHERE scheduleID = %s",(scheduleId,))
            numberOfBooking = cursor.fetchone()['COUNT(bookingID)']
            availableSpace = classToBook['maxParticipants'] - numberOfBooking
            if availableSpace > 0:
                date = classToBook['sessionTime'].date()
                startTime = classToBook['sessionTime'].time()
                lessonDuration = classToBook['lessonDuration']
    
                # check member's time availability in case time crash
                if checkUserAvailability(session['id'], date, startTime, lessonDuration):
                    cursor.execute("SELECT * FROM aerobics_bookings WHERE scheduleID = %s AND bookingActive=0",(classToBook['scheduleID'],))
                    bookedAndCanceled = cursor.fetchone()
                    if bookedAndCanceled:
                        cursor.execute("UPDATE aerobics_bookings SET bookingTime = now(), bookingActive = 1 WHERE scheduleID = %s", (classToBook['scheduleID'],) )
                        cursor.connection.commit()
                    else:
                        cursor.execute("INSERT INTO aerobics_bookings (scheduleID, customerID, bookingTime) VALUES (%s,%s,now())",(scheduleId,session['id']))
                        cursor.connection.commit()
                    labelUnavailable(session['id'], date, startTime, lessonDuration)
                    flash("Booking successfully!","success")
                    return redirect(url_for('memberDashboardFunc.aquaAerobicsClassTimetable'))     
                else:
                    flash("Ooops! Time crash! Already booked other classes in this time frame.","error")
                    return redirect(url_for('memberDashboardFunc.aquaAerobicsClassTimetable'))      
            else:
                flash("Class is full. Unable to book.","error")
                return redirect(url_for('memberDashboardFunc.aquaAerobicsClassTimetable'))
        else:
            return "404"
    else:
        flash("Unable to book class, need to subscribe first.","error")
        return redirect(url_for('memberDashboardFunc.aquaAerobicsClassTimetable'))
    

@bp.route('/member/instructors')
def instructorList():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM instructorinfo LEFT JOIN users ON users.userID = instructorinfo.userID WHERE userActive = 1;")
    instructorList = cursor.fetchall()
    return render_template("instructor_list_for_members.html",instructorList=instructorList)



@bp.route('/member/timetable/individual_lessons/<instructorId>')
def individualLessonsTimetable(instructorId):

    # get instructor list data and restructure to dictionary
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM instructorinfo LEFT JOIN users ON users.userID = instructorinfo.userID WHERE userActive = 1;")
    instructorList = cursor.fetchall()
    organizedInstructors = {}
    for instructor in instructorList:
        organizedInstructors[instructor['userID']] = instructor
    # print(organizedInstructors)

    # get time slots data and restructure to nested dictionary
    cursor.execute("SELECT * from time_slots WHERE startTime BETWEEN '08:00:00' AND '17:59:00';")
    timeSlots = cursor.fetchall()
    organizedTimeSlots = {}
    for timeSlot in timeSlots:
        organizedTimeSlots[timeSlot['slotsID']] = (timeSlot['startTime'], timeSlot['endTime'])
    # print(organizedTimeSlots)
    
    # get instructors' availability data and restructure to nested dictionary
    # instructorAvailability = {}
    # for instructor in instructorList:
    query = '''SELECT availabilityID, userID, user_availability.slotsID, date, availability, startTime, endTime 
                FROM user_availability
                LEFT JOIN time_slots 
                ON user_availability.slotsID = time_slots.slotsID
                WHERE userID = %s AND availability = FALSE;'''
    cursor.execute(query,(instructorId,))
    availableSlots = cursor.fetchall()
        
        # timeSlotsID = []
        # for timeSlot in timeSlots:
        #     timeSlotsID.append(timeSlot['slotsID'])
    organizedAvailability = {}
    for timeSlot in timeSlots:
        organizedAvailability[timeSlot['slotsID']] = {startDate + timedelta(days=i): 1 for i in range(14)}
    for availableSLot in availableSlots:
        if availableSLot['slotsID'] in organizedAvailability and availableSLot['date'] in organizedAvailability[timeSlot['slotsID']]:
            organizedAvailability[availableSLot['slotsID']][availableSLot['date']]=0
        # print(organizedAvailability)
        # print(organizedAvailability.values())
        # instructorAvailability[instructor['userID']] = organizedAvailability
    # print(instructorAvailability)
    return render_template("timetable_individualLessons.html", instructorId = int(instructorId), instructorDict = organizedInstructors, availability=organizedAvailability, timeSlots=organizedTimeSlots)


bookingData = {}
@bp.route('/member/book/individual_lessons',methods=['Get', 'POST'])
def bookIndividualLesson():
    bookingData['instructorName']=request.form.get('instructorName')
    bookingData['instructorID']= int(request.form.get('instructorID'))
    bookingData['customerID'] = session['id']
    bookingData['lessonDate']= request.form.get('lessonDate')
    bookingData['lessonTime']= request.form.get('lessonTime')
    bookingData['lessonFee']= request.form.get('lessonFee')
    bookingData['lessonDuration']= int(request.form.get('lessonDuration'))
    bookingData['lessonFee'] = request.form.get('lessonFee')
    bookingData['poolID'] = request.form.get('poolID')
    bookingData['poolType'] = request.form.get('poolType')
    # print(bookingData)
    if checkSubscription(session['id']):
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        startTime = bookingData['lessonTime']
        if checkUserAvailability(session['id'], bookingData['lessonDate'], startTime, bookingData['lessonDuration']):
            cursor.execute('INSERT INTO individual_lesson_bookings(instructorID,customerID,lessonDate,lessonTime,lessonDuration, lessonFee, bookingTime, poolID) VALUES (%s,%s,%s,%s,%s,%s,Now(),%s)', (bookingData['instructorID'], bookingData['customerID'], bookingData['lessonDate'],startTime, bookingData['lessonDuration'],bookingData['lessonFee'],bookingData['poolID']))
            mysql.connection.commit()
            bookingIndex = cursor.lastrowid
            return render_template("payment.html",bookingIndex=bookingIndex,bookingData=bookingData)
        else:
            flash("Ooops! Time crash! Already booked other classes in this time frame.","error")
            return redirect(url_for('memberDashboardFunc.individualLessonsTimetable',instructorId = bookingData['instructorID']))
    else:
        flash("Unable to book class, need to subscribe first.","error")
        return redirect(url_for('memberDashboardFunc.individualLessonsTimetable',instructorId = bookingData['instructorID']))
        
        
    
@bp.route('/member/payment/<bookingIndex>',methods=['Get', 'POST'])
def payment(bookingIndex):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("INSERT INTO payments (customerID, paymentType, amount, paymentTime) VALUES (%s,2,%s,now())",(session['id'],bookingData['lessonFee']))
    cursor.connection.commit()
    paymentID = cursor.lastrowid
    startTime = bookingData['lessonTime']
    cursor.execute("UPDATE individual_lesson_bookings SET paymentID = %s WHERE bookingID = %s",(paymentID,bookingIndex))
    labelUnavailable(session['id'], bookingData['lessonDate'], startTime, bookingData['lessonDuration'])
    labelUnavailable(bookingData['instructorID'], bookingData['lessonDate'], startTime, bookingData['lessonDuration'])
    flash("Booking successfully!","success")
    return redirect(url_for('memberDashboardFunc.individualLessonsTimetable',instructorId = bookingData['instructorID']))   


def getUpcomingBookings():
    sql = '''SELECT * FROM
        (SELECT bookingID, aerobics_bookings.scheduleID, customerID, bookingTime, instructorID, sessionName, maxParticipants, sessionTime, lessonDuration, poolID, 0 as lessonFee
        FROM aerobics_bookings
        LEFT JOIN aerobics_schedule
        ON aerobics_bookings.scheduleID = aerobics_schedule.scheduleID
        WHERE aerobics_bookings.bookingActive is True
        UNION ALL
        SELECT
        bookingID, NULL as scheduleID, customerID, bookingTime, instructorID, "Private lesson" as sessionName, NULL as maxParticipants, cast(concat(lessonDate, ' ', lessonTime) as datetime) as sessionTime, lessonDuration, poolID,lessonFee
        FROM individual_lesson_bookings
        WHERE paymentID is not NULL AND individual_lesson_bookings.bookingActive is True) AS allLessons
        LEFT JOIN instructorinfo
        ON instructorinfo.userID = instructorID
        LEFT JOIN pools
        ON pools.poolID = allLessons.poolID
        WHERE customerID = %s AND sessionTime >= NOW()
        ORDER BY sessionTime ASC;'''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql,(session['id'],))
    upcomingBookings = cursor.fetchall()
    # print(upcomingBookings)
    return upcomingBookings

def getHistoryBookings():
    sql = '''SELECT * FROM
        (SELECT bookingID, aerobics_bookings.scheduleID, customerID, bookingTime, instructorID, sessionName, maxParticipants, sessionTime, lessonDuration, poolID, 0 as lessonFee
        FROM aerobics_bookings
        LEFT JOIN aerobics_schedule
        ON aerobics_bookings.scheduleID = aerobics_schedule.scheduleID
        WHERE aerobics_bookings.bookingActive is True
        UNION ALL
        SELECT
        bookingID, NULL as scheduleID, customerID, bookingTime, instructorID, "Private lesson" as sessionName, NULL as maxParticipants, cast(concat(lessonDate, ' ', lessonTime) as datetime) as sessionTime, lessonDuration, poolID,lessonFee
        FROM individual_lesson_bookings
        WHERE paymentID is not NULL AND individual_lesson_bookings.bookingActive is True) AS allLessons
        LEFT JOIN instructorinfo
        ON instructorinfo.userID = instructorID
        LEFT JOIN pools
        ON pools.poolID = allLessons.poolID
        WHERE customerID = %s AND sessionTime < NOW()
        ORDER BY sessionTime DESC;'''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql,(session['id'],))
    historyBookings = cursor.fetchall()
    return historyBookings

@bp.route('/member/calendar')
def memberCalendar():
    # month = datetime.now().month
    # monthName = datetime.now().strftime('%B')
    # year = datetime.now().year
    #print(month)
    #print(year)
    # firstWeekDayOfTheMonth = (datetime(year,month,1).weekday()+1)%7
    # nextMonth = datetime(year,month,28)+timedelta(days=4)
    # lastDayNumberOfTheMonth = (nextMonth-timedelta(days=nextMonth.day)).day
    # today = datetime.now().day
    #print(firstWeekDayOfTheMonth)
    #print(lastDayNumberOfTheMonth)
    #weedDays = ["Sunday", "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    #print(calendar.month(year,month))
    # calendar = {
    #     'year': year,
    #     'month': month,
    #     'monthName': monthName,
    #     'firstWeekDayOfTheMonth': firstWeekDayOfTheMonth,
    #     'lastDayNumberOfTheMonth': lastDayNumberOfTheMonth,
    #     'today': today
    # }
    # print(calendar)
    upcomingBookings=getUpcomingBookings()
    # print(upcomingBookings)
    historyBookings=getHistoryBookings()
    # print(historyBookings)
    bookings = upcomingBookings + historyBookings
    return render_template("calendar.html", bookings = bookings, session=session)

@bp.route('/member/timetable')
def memberTimetable():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * from time_slots WHERE startTime BETWEEN '05:00:00' AND '22:00:00';")
    timeSlots = cursor.fetchall()
    organizedTimeSlots = {}
    for timeSlot in timeSlots:
        organizedTimeSlots[timeSlot['slotsID']] = (timeSlot['startTime'], timeSlot['endTime'])
    query = '''SELECT availabilityID, userID, user_availability.slotsID, date, availability, startTime, endTime 
                FROM user_availability
                LEFT JOIN time_slots 
                ON user_availability.slotsID = time_slots.slotsID
                WHERE userID = %s AND availability = FALSE;'''
    cursor.execute(query,(session['id'],))
    availableSlots = cursor.fetchall()
    organizedAvailability = {}
    for timeSlot in timeSlots:
        organizedAvailability[timeSlot['slotsID']] = {startDate + timedelta(days=i): 1 for i in range(14)}
    for availableSLot in availableSlots:
        if availableSLot['slotsID'] in organizedAvailability and availableSLot['date'] in organizedAvailability[timeSlot['slotsID']]:
            organizedAvailability[availableSLot['slotsID']][availableSLot['date']]=0
    # print(organizedAvailability)
    # print(organizedTimeSlots)
    bookings = getUpcomingBookings() + getHistoryBookings()
    # print(bookings)
    return render_template("member_timetable.html", availability=organizedAvailability, timeSlots=organizedTimeSlots, bookings = bookings)   


@bp.route('/member/upcomingBookings')
def upcomingBookings():
    return render_template("member_upcomingBookings.html", upcomingBookings = getUpcomingBookings())

@bp.route('/member/historyBookings')
def historyBookings():
    return render_template("member_historyBookings.html", historyBookings = getHistoryBookings())

@bp.route('/member/cancelBookings/<bookingID>',methods=['Get', 'POST'])
def cancelBookings(bookingID):
    calling_page = request.form.get('callingPage')
    print("calling_page:")
    print(calling_page)
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = '''SELECT * FROM
        (SELECT bookingID, customerID, instructorID, sessionTime, lessonDuration
        FROM aerobics_bookings
        LEFT JOIN aerobics_schedule
        ON aerobics_bookings.scheduleID = aerobics_schedule.scheduleID
        WHERE aerobics_bookings.bookingActive is True
        UNION ALL
        SELECT
        bookingID, customerID, instructorID, cast(concat(lessonDate, ' ', lessonTime) as datetime) as sessionTime, lessonDuration
        FROM individual_lesson_bookings
        WHERE paymentID is not NULL AND bookingActive is True) AS allLessons
        WHERE bookingID = %s;'''
    cursor.execute(sql,(bookingID,))
    lessonToCancel = cursor.fetchone()
    if (lessonToCancel['sessionTime'] - datetime.now()).total_seconds()/60 < 60:
        flash("Cannot cancel booking now, need to cancel at least 1 hour in advance. ","error")
        return redirect(url_for(calling_page))   
    else:
        date = lessonToCancel['sessionTime'].date()
        startTime = lessonToCancel['sessionTime'].time()
        endTime = (lessonToCancel['sessionTime'] + timedelta(minutes=lessonToCancel['lessonDuration']-1)).time()
        cursor.execute("SELECT * FROM time_slots WHERE startTime BETWEEN %s AND %s;", (startTime, endTime))
        timeSlots = cursor.fetchall()
        if int(bookingID) >= 200000000:
            cursor.execute('UPDATE individual_lesson_bookings SET bookingActive=False WHERE bookingID=%s',(bookingID,))
            mysql.connection.commit()
            for timeSlot in timeSlots:
                cursor.execute('UPDATE user_availability SET availability = 1 WHERE date=%s AND slotsID=%s AND userID=%s',(date, timeSlot['slotsID'], session['id']))
                mysql.connection.commit()
                cursor.execute('UPDATE user_availability SET availability = 1 WHERE date=%s AND slotsID=%s AND userID=%s',(date, timeSlot['slotsID'], lessonToCancel['instructorID']))
                mysql.connection.commit()
            flash("Booking cancel sucssessfully!","success")
            return redirect(url_for(calling_page))   
        elif int(bookingID) >= 100000000 and int(bookingID) < 200000000:
            cursor.execute('UPDATE aerobics_bookings SET bookingActive=False WHERE bookingID=%s',(bookingID,))
            mysql.connection.commit()
            for timeSlot in timeSlots:
                cursor.execute('UPDATE user_availability SET availability = 1 WHERE date=%s AND slotsID=%s AND userID=%s',(date, timeSlot['slotsID'], session['id']))
                mysql.connection.commit()
            flash("Booking cancel sucssessfully!","success")
            return redirect(url_for(calling_page))   
        
            


            


    