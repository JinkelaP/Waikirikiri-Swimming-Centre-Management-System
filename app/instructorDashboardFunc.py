from app import mysql
from flask import flash, render_template, request, redirect, url_for, session, Blueprint
from flask_mysqldb import MySQL
from datetime import date, datetime, timedelta
import MySQLdb.cursors
import bcrypt
import math
import os


bp = Blueprint('instructorDashboardFunc', __name__, )

startDate = date.today()

def getInstructorUpcomingBookings(id):
    sql = '''SELECT * FROM
        (SELECT NULL AS bookingID, scheduleID, NULL AS customerID, NULL AS bookingTime, instructorID, sessionName, maxParticipants, sessionTime, lessonDuration, poolID, 0 as lessonFee
        FROM aerobics_schedule
        WHERE aerobics_schedule.bookingActive is True
        UNION ALL
        SELECT
        bookingID, NULL as scheduleID, customerID, bookingTime, instructorID, "Private lesson" as sessionName, NULL as maxParticipants, cast(concat(lessonDate, ' ', lessonTime) as datetime) as sessionTime, lessonDuration, poolID,lessonFee
        FROM individual_lesson_bookings
        WHERE paymentID is not NULL AND individual_lesson_bookings.bookingActive is True) AS allLessons
        LEFT JOIN memberinfo
        ON memberinfo.userID = customerID
        LEFT JOIN pools
        ON pools.poolID = allLessons.poolID
        WHERE instructorID = %s AND sessionTime >= NOW()
        ORDER BY sessionTime ASC;'''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql,(id,))
    upcomingBookings = cursor.fetchall()
    # print(upcomingBookings)
    return upcomingBookings

def getInstructorHistoryBookings(id):
    sql = '''SELECT * FROM
        (SELECT NULL AS bookingID, scheduleID, NULL AS customerID, NULL AS bookingTime, instructorID, sessionName, maxParticipants, sessionTime, lessonDuration, poolID, 0 as lessonFee
        FROM aerobics_schedule
        WHERE aerobics_schedule.bookingActive is True
        UNION ALL
        SELECT
        bookingID, NULL as scheduleID, customerID, bookingTime, instructorID, "Private lesson" as sessionName, NULL as maxParticipants, cast(concat(lessonDate, ' ', lessonTime) as datetime) as sessionTime, lessonDuration, poolID,lessonFee
        FROM individual_lesson_bookings
        WHERE paymentID is not NULL AND individual_lesson_bookings.bookingActive is True) AS allLessons
        LEFT JOIN memberinfo
        ON memberinfo.userID = customerID
        LEFT JOIN pools
        ON pools.poolID = allLessons.poolID
        WHERE instructorID = %s AND sessionTime < NOW()
        ORDER BY sessionTime DESC;'''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute(sql,(id,))
    historyBookings = cursor.fetchall()
    return historyBookings

def getInstructorByUserId(userId):
    cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cur.execute('SELECT * FROM instructorinfo WHERE userID = %s', (userId,))
    instructor = cur.fetchone()
    cur.close()
    return instructor

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
            

@bp.route('/instructor/timetable')
def instructorTimetable():
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
    bookings = getInstructorUpcomingBookings(session['id']) + getInstructorHistoryBookings(session['id'])
    return render_template("instructor_timetable.html", availability=organizedAvailability, timeSlots=organizedTimeSlots, bookings = bookings)  

@bp.route('/instructor/calendar')
def instructorCalendar(): 
    bookings = getInstructorUpcomingBookings(session['id']) + getInstructorHistoryBookings(session['id'])
    # print(bookings)
    return render_template("calendar.html", bookings = bookings, session=session)


@bp.route('/instructor/set-unavailable-time', methods=['Get', 'POST'])
def setUnavailableTime():
    setAllDayUnavailable = request.form.get('allDayCheckbox')
    startTime_str = request.form.get('startTime')
    endTime_str = request.form.get('endTime')
    date = request.form.get('date')

    startTimeNoDate = datetime.strptime(startTime_str, "%H:%M:%S").time()
    combined_end_datetime_str = f"{date} {endTime_str}"
    endTime = datetime.strptime(combined_end_datetime_str, "%Y-%m-%d %H:%M:%S")
    combined_start_datetime_str = f"{date} {startTime_str}"
    startTime = datetime.strptime(combined_start_datetime_str, "%Y-%m-%d %H:%M:%S")

    # print("startTime:", startTime)
    # print("endTime:",endTime)
    # print("type of endTime:", type(endTime))

    if setAllDayUnavailable:
        startTime = datetime.strptime("05:00:00", "%H:%M:%S")
        endTime = datetime.strptime("22:00:00", "%H:%M:%S")
    duration = (endTime - startTime).total_seconds() / 60
    # print("startTimeNoDate:", startTimeNoDate)
    # print("duration:", duration)
    # print("date:", date)
    # if there's booking in this period, cancel the bookings
    if not checkUserAvailability(session['id'], date, startTimeNoDate, duration):
        # find the bookings in this period
        bookings = getInstructorUpcomingBookings() 
        for booking in bookings:
            # print(booking)
            # print("booking['sessionTime']:", booking['sessionTime'])
            # print("type of booking['sessionTime']:", type(booking['sessionTime']))
            session_date_str = str(booking['sessionTime'])[:10]

            if session_date_str == date and booking['sessionTime'].time() < endTime.time():
                # Rest of your code here
               
                date = booking['sessionTime'].date()
                startTime = booking['sessionTime'].time()
                endTime = (booking['sessionTime'] + timedelta(minutes=booking['lessonDuration']-1)).time()
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                cursor.execute("SELECT * FROM time_slots WHERE startTime BETWEEN %s AND %s;", (startTime, endTime))
                timeSlots = cursor.fetchall()
                if int(booking['bookingID']) >= 200000000:
                    cursor.execute('UPDATE individual_lesson_bookings SET bookingActive=False WHERE bookingID=%s',(booking['bookingID'],))
                    mysql.connection.commit()
                    for timeSlot in timeSlots:
                        cursor.execute('UPDATE user_availability SET availability = 1 WHERE date=%s AND slotsID=%s AND userID=%s',(date, timeSlot['slotsID'], session['id']))
                        mysql.connection.commit()
                        cursor.execute('UPDATE user_availability SET availability = 1 WHERE date=%s AND slotsID=%s AND userID=%s',(date, timeSlot['slotsID'], booking['customerID']))
                        mysql.connection.commit()
                    flash("Individual lesson with "+booking['firstName'] +" canceled sucssessfully!","success")

                    title = f"[REMOVED] Your individual lesson on {date} has been cancelled."
                    content = f"""Your individual lesson on {date} has been cancelled. Please re-book a new class or contact admin."""
    

                    if booking['customerID']:
                        cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
            (title, content, datetime.now(), session['id'], booking['customerID']))
                    
                    mysql.connection.commit()

                    # notice the members 
                elif int(booking['bookingID']) >= 100000000 and int(booking['bookingID']) < 200000000:
                    # cursor.execute('UPDATE aerobics_bookings SET ',(booking['bookingID'],))
                    # mysql.connection.commit()

                    # inform admin to change instructor
                    for timeSlot in timeSlots:
                        cursor.execute('UPDATE user_availability SET availability = 1 WHERE date=%s AND slotsID=%s AND userID=%s',(date, timeSlot['slotsID'], session['id']))
                        mysql.connection.commit()
                    flash("Group class " + booking['sessionName'] + " canceled sucssessfully!","success")

                    title = f"[REMOVED] Your aqua aerobics class on {date} has been cancelled."
                    content = f"""Your aqua aerobics class on {date} has been cancelled. Please re-book a new class or contact admin."""
    


                    cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
            (title, content, datetime.now(), session['id'], booking['customerID']))
                    cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID, newsTypeID) VALUES (%s, %s, %s, %s, %s)', 
            (title, content, datetime.now(), session['id'], 0))
                    mysql.connection.commit()

    labelUnavailable(session['id'], date, startTime, duration)
    return redirect(url_for('instructorDashboardFunc.instructorTimetable'))


@bp.route('/instructor/upcomingBookings')
def upcomingBookings():
    upcomingBookings = getInstructorUpcomingBookings(session['id'])
    # print(upcomingBookings)
    return render_template("instructor_upcomingBookings.html",upcomingBookings = upcomingBookings)

@bp.route('/instructor/historyBookings')
def historyBookings():
    return render_template("instructor_historyBookings.html", historyBookings = getInstructorHistoryBookings(session['id']))  


