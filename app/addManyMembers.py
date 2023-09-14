from flask import Flask, redirect, url_for, Blueprint
import random
import string
import bcrypt
from flask_mysqldb import MySQL
from datetime import datetime, timedelta
from app import mysql

bp = Blueprint('addManyMembers', __name__, )

@bp.route('/generate-members')
def generate_members():
    # Establish connection to the MySQL database
    cur = mysql.connection.cursor()

    # Sample data for generating random member information
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", 
    "Linda", "Jennifer", "Patricia", "Jessica", "Elizabeth", "Mary", "Susan", "Karen", "Nancy", "Lisa", 
    "Daniel", "Matthew", "Andrew", "Christopher", "George", "Anthony", "Edward", "Paul", "Steven", "Kevin"]

    last_names = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Davis", "White", "Jones", "Martin", 
    "Hall", "Thomas", "Robinson", "Harris", "Moore", "Clark", "Jackson", "Green", "Lewis", "Baker", 
    "Allen", "Young", "King", "Scott", "Mitchell", "Turner", "Carter", "Phillips", "Evans", "Adams"]

    streets = ["Hereford Street", "Colombo Street", "Durham Street North", "Cashel Street", "Worcester Street", 
    "High Street", "Lichfield Street", "Manchester Street", "Madras Street", "Tuam Street", 
    "Riccarton Road", "Papanui Road", "Bealey Avenue", "Moorhouse Avenue", "St Asaph Street", 
    "Blenheim Road", "Barbadoes Street", "Ferry Road", "Linwood Avenue", "Fitzgerald Avenue"]

    for _ in range(3):
        # Generate a random username and its hashed password
        user_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        hashed_password = bcrypt.hashpw(user_name.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the 'users' table
        cur.execute('INSERT INTO users (userPermission, userName, userPassword, userActive) VALUES (%s, %s, %s, %s)',
                    (3, user_name, hashed_password, True))
        
        mysql.connection.commit()

        # Retrieve the ID of the user just inserted    
        cur.execute('SELECT LAST_INSERT_ID()')
        user_id = cur.fetchone()[0]

        # Generate random member details
        titles = ['Mr', 'Mrs', 'Ms', 'Dr']
        positions = ['Engineer', 'Doctor', 'Lawyer', 'Teacher', 'Manager', 'Nurse', 'Artist', 'Driver', 'Guard', 'Chef']
        phone_number = ''.join(random.choices(string.digits, k=3)) + '-' + ''.join(random.choices(string.digits, k=3)) + '-' + ''.join(random.choices(string.digits, k=4))
        email = user_name + "@gmail.com"
        address = str(random.randint(1,999)) + " " + random.choice(streets) + ", Christchurch, New Zealand"
        dob = str(random.randint(1963,2013)) + "-" + str(random.randint(1,12)).zfill(2) + "-" + str(random.randint(1,28)).zfill(2)

        # Insert the generated member details into the 'memberinfo' table
        cur.execute('INSERT INTO memberinfo (userID, title, firstName, lastName, position, phoneNumber, email, physicalAddress, dateOfBirth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)',
                    (user_id, random.choice(titles), random.choice(first_names), random.choice(last_names), random.choice(positions), phone_number, email, address, dob))
        mysql.connection.commit()

    # Close the database connection    
    cur.close()

    # Redirect the user to the login page
    return redirect(url_for('login.login'))

@bp.route('/generate-instructors')
def generate_instructors():

    # Establish a connection to the MySQL database
    cur = mysql.connection.cursor()

    # Pre-defined lists for generating random instructor information
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Charles", "Thomas", 
    "Linda", "Jennifer", "Patricia", "Jessica", "Elizabeth", "Mary", "Susan", "Karen", "Nancy", "Lisa", 
    "Daniel", "Matthew", "Andrew", "Christopher", "George", "Anthony", "Edward", "Paul", "Steven", "Kevin"]

    last_names = ["Smith", "Johnson", "Brown", "Taylor", "Miller", "Wilson", "Davis", "White", "Jones", "Martin", 
    "Hall", "Thomas", "Robinson", "Harris", "Moore", "Clark", "Jackson", "Green", "Lewis", "Baker", 
    "Allen", "Young", "King", "Scott", "Mitchell", "Turner", "Carter", "Phillips", "Evans", "Adams"]

    streets = ["Hereford Street", "Colombo Street", "Durham Street North", "Cashel Street", "Worcester Street", 
    "High Street", "Lichfield Street", "Manchester Street", "Madras Street", "Tuam Street", 
    "Riccarton Road", "Papanui Road", "Bealey Avenue", "Moorhouse Avenue", "St Asaph Street", 
    "Blenheim Road", "Barbadoes Street", "Ferry Road", "Linwood Avenue", "Fitzgerald Avenue"]

    for _ in range(3):
        # Generate a random username and its hashed password
        user_name = ''.join(random.choices(string.ascii_lowercase, k=5))
        hashed_password = bcrypt.hashpw(user_name.encode('utf-8'), bcrypt.gensalt())

        # Insert the new user into the 'users' table with instructor permissions (value of 2)
        cur.execute('INSERT INTO users (userPermission, userName, userPassword, userActive) VALUES (%s, %s, %s, %s)',
                    (2, user_name, hashed_password, True))
        
        mysql.connection.commit()

        # Retrieve the ID of the user just inserted
        cur.execute('SELECT LAST_INSERT_ID()')
        user_id = cur.fetchone()[0]

        # Generate random instructor details
        titles = ['Mr', 'Mrs', 'Ms', 'Dr']
        positions = ['Freestyle', 'Backstroke', 'Breaststroke', 'Butterfly', 'Sidestroke', 'Diving', 'Endurance', 'Safety ', 'Flip ', 'Breathing']
        phone_number = ''.join(random.choices(string.digits, k=3)) + '-' + ''.join(random.choices(string.digits, k=3)) + '-' + ''.join(random.choices(string.digits, k=4))
        email = user_name + "@gmail.com"

        # Insert the generated instructor details into the 'instructorinfo' table
        cur.execute('INSERT INTO instructorinfo (userID, title, firstName, lastName, position, phoneNumber, email, introduction) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)',
                    (user_id, random.choice(titles), random.choice(first_names), random.choice(last_names), random.choice(positions), phone_number, email, "Hi, I am a instructor"))
        mysql.connection.commit()

    # Close the database connection    
    cur.close()

    # Redirect the user to the login page
    return redirect(url_for('login.login'))


@bp.route('/generate-news')
def generate10News():
    # Function to generate news titles and contents
    def generate_fake_news():
        news_titles = [
            "New Swimming Course Available",
            "Annual Swimming Championship Announced",
            "Maintenance Notice: Public Pool Closure",
            "Special Discount for Group Classes",
            "Upcoming Summer Swimming Camp",
            "Introducing Advanced Diving Techniques Workshop",
            "Pool Safety Reminders for Parents",
            "New Instructors Join Our Team",
            "Private Lessons: Personalized Training",
            "Team Relay Event: Register Now"
        ]

        news_contents = [
            "We are thrilled to announce our brand new advanced swimming course tailored specifically for professional athletes and those looking to take their skills to the next level. This course offers intensive training sessions, personalized feedback from seasoned instructors, and state-of-the-art equipment to ensure an optimal learning experience. Limited slots available, so be sure to register early and dive into a transformative swimming journey.",
            "Get ready for the splash of the year! Our annual swimming championship is back, and it's bigger than ever. We invite swimmers of all age groups to showcase their talent, endurance, and passion. Compete against the best, and stand a chance to win exclusive prizes, scholarships, and even sponsorship deals. Training sessions available for those who want to hone their techniques. Register today and make waves!",
            "Attention all swimmers! Please note that our main public pool will undergo essential maintenance next week. This decision was made to ensure the safety and well-being of our members. During this period, we encourage our swimmers to explore our smaller practice pools or participate in our alternative fitness classes. We apologize for the inconvenience and appreciate your understanding.",
            "It's always more fun with friends! For a limited period, enjoy special discounts on our group swimming lessons. Our group classes focus on collaborative exercises, synchronized swimming techniques, and team-building activities. Led by certified instructors, this program is perfect for those looking to make new friends while enjoying a healthy workout. Dive in with friends and save more!",
            "Summer is almost here, and what better way to spend it than at our exclusive Summer Swimming Camp? Open to all age groups, our camp offers a mix of fun activities, competitive races, and intensive training sessions. Whether you're a newbie looking to learn or an advanced swimmer keen on perfecting your stroke, we've got something for everyone. Plus, there's a special early bird discount for the first 50 registrants!",
            "Dive deep into the world of advanced swimming with our upcoming diving techniques workshop. This two-day intensive workshop will cover various diving styles, safety protocols, and tips on perfecting your dive. Our expert trainers will provide hands-on guidance, ensuring you emerge more confident and skilled. Suitable for intermediate and advanced swimmers. Slots are limited, so sign up soon!",
            "The safety of our young swimmers is of utmost importance to us. We'd like to remind all parents to ensure their children are supervised at all times while at the pool. While our staff and lifeguards are always on alert, parental supervision provides an added layer of safety. Also, consider enrolling your kids in our 'Water Safety' classes, designed to teach them essential safety skills.",
            "We are expanding our team and are excited to introduce our new batch of certified instructors from around the globe! Each brings a unique teaching style, advanced techniques, and a passion for swimming. They're eager to share their expertise with our members. Check out their profiles on our website and book a session with them today. Let's make waves together!",
            "Looking for a bespoke swimming experience? Our private lessons are just what you need. Get one-on-one training, detailed feedback, and a personalized training regimen tailored to your needs. Whether it's preparing for a competition or mastering a particular stroke, our instructors will provide undivided attention to ensure you achieve your goals. Book your personalized session today!",
            "Ready for a thrilling team challenge? Teams of four are invited to our Team Relay Event next month. This exciting event will test speed, endurance, and teamwork. So gather your squad, start practicing, and stand a chance to win amazing prizes, including a year's free membership! Register your team now and showcase the power of teamwork!"
        ]

        return news_titles, news_contents

    # Call the above function to get news titles and contents
    titles, contents = generate_fake_news()

    # Database operations to insert news
    cursor = mysql.connection.cursor()

    for i in range(10):
        date = datetime.now() - timedelta(days=i)
        formatted_date = date.replace(hour=14, minute=0)  # Set the time to 2 PM
        cursor.execute('INSERT INTO news_updates (title, content, publishDate, adminID) VALUES (%s, %s, %s, %s)', 
                        (titles[i], contents[i], formatted_date, 10001))

    mysql.connection.commit()
    cursor.close()

    return redirect(url_for('login.login'))
