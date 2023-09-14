DROP DATABASE IF EXISTS swimmingpool;
CREATE DATABASE swimmingpool;
USE swimmingpool;

CREATE TABLE IF NOT EXISTS users
(
userID INT auto_increment PRIMARY KEY NOT NULL,
userPermission INT NOT NULL,
-- 1 is admin, 2 is instructor, 3 is member
userName VARCHAR(80) NOT NULL,
userPassword VARCHAR(80) NOT NULL,
userActive BOOLEAN NOT NULL DEFAULT TRUE
);


CREATE TABLE IF NOT EXISTS admininfo
(
userID INT PRIMARY KEY NOT NULL,
title VARCHAR(10) NOT NULL,
firstName VARCHAR(20) NOT NULL,
lastName VARCHAR(20) NOT NULL,
position VARCHAR(20) NOT NULL,
phoneNumber VARCHAR(15) NOT NULL,
email VARCHAR(40) NOT NULL,

FOREIGN KEY (userID) REFERENCES users(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS instructorinfo
(
userID INT PRIMARY KEY NOT NULL,
title VARCHAR(10) NOT NULL,
firstName VARCHAR(20) NOT NULL,
lastName VARCHAR(20) NOT NULL,
position VARCHAR(20) NOT NULL,
phoneNumber VARCHAR(15) NOT NULL,
email VARCHAR(40) NOT NULL,
introduction VARCHAR(1000) NOT NULL,

FOREIGN KEY (userID) REFERENCES users(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS memberinfo
(
userID INT PRIMARY KEY NOT NULL,
title VARCHAR(10) NOT NULL,
firstName VARCHAR(20) NOT NULL,
lastName VARCHAR(20) NOT NULL,
position VARCHAR(20) NOT NULL,
phoneNumber VARCHAR(15) NOT NULL,
email VARCHAR(40) NOT NULL,
physicalAddress VARCHAR(200) NOT NULL,
dateOfBirth DATE NOT NULL,
healthInfo VARCHAR(200),

FOREIGN KEY (userID) REFERENCES users(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS pools
(
poolID INT auto_increment PRIMARY KEY NOT NULL,
poolType VARCHAR(50) NOT NULL,
-- "Olympic", "Hydrotherapy", "Training", "Family"
description VARCHAR(255)
);


CREATE TABLE IF NOT EXISTS subscriptions
(
subscriptionID INT auto_increment PRIMARY KEY NOT NULL,
userID INT NOT NULL,
startDate DATE NOT NULL,
endDate DATE NOT NULL,

FOREIGN KEY (userID) REFERENCES memberinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS attendance
(
attendanceID INT auto_increment PRIMARY KEY NOT NULL,
userID INT NOT NULL,
attendanceType INT NOT NULL,
-- 1 for using the pool, 2 for attending individual swimming class, 3 for aqua aerobics classes
attendanceTime DATETIME NOT NULL,

FOREIGN KEY (userID) REFERENCES memberinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);



CREATE TABLE IF NOT EXISTS aerobics_schedule
(
scheduleID INT auto_increment PRIMARY KEY NOT NULL,
instructorID INT NOT NULL,
sessionName VARCHAR(100) NOT NULL,
maxParticipants INT DEFAULT 30 NOT NULL,  -- max 30 participants
sessionTime DATETIME NOT NULL,
lessonDuration INT DEFAULT 60 NOT NULL, -- default 60 minutes
poolID INT NOT NULL, -- only 2 and 3
bookingActive BOOLEAN NOT NULL DEFAULT TRUE,
FOREIGN KEY (instructorID) REFERENCES instructorinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (poolID) REFERENCES pools(poolID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS aerobics_bookings
(
bookingID INT auto_increment PRIMARY KEY NOT NULL,
scheduleID INT NOT NULL,
customerID INT NOT NULL,
bookingTime DATETIME NOT NULL,
bookingActive BOOLEAN NOT NULL DEFAULT TRUE,
bookingAttend BOOLEAN NOT NULL DEFAULT FALSE,
FOREIGN KEY (scheduleID) REFERENCES aerobics_schedule(scheduleID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (customerID) REFERENCES memberinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) AUTO_INCREMENT = 100000000;




CREATE TABLE IF NOT EXISTS payments
(
paymentID INT auto_increment PRIMARY KEY NOT NULL,
customerID INT NOT NULL,
paymentType INT NOT NULL,
-- 1 for subscription, 2 for swimming class
amount DECIMAL(10, 2) NOT NULL,
paymentTime DATETIME NOT NULL,

FOREIGN KEY (customerID) REFERENCES memberinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS news_updates
(
newsID INT auto_increment PRIMARY KEY NOT NULL,
title VARCHAR(255) NOT NULL,
content TEXT NOT NULL,
publishDate DATETIME NOT NULL,
adminID INT NOT NULL,
newsTypeID INT,
-- if typeid equals 0 means public
-- Otherwise means private message by storing userID in newsTypeID
FOREIGN KEY (adminID) REFERENCES admininfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS time_slots
(
slotsID INT auto_increment PRIMARY KEY NOT NULL,
startTime TIME NOT NULL,
endTime TIME NOT NULL  
);

CREATE TABLE IF NOT EXISTS user_availability
(
availabilityID INT auto_increment PRIMARY KEY NOT NULL,
userID INT NOT NULL,
slotsID INT NOT NULL,
date DATE NOT NULL,
availability BOOLEAN NOT NULL DEFAULT TRUE,

FOREIGN KEY (userID) REFERENCES users(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (slotsID) REFERENCES time_slots(slotsID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
);


CREATE TABLE IF NOT EXISTS individual_lesson_bookings
(
bookingID INT auto_increment PRIMARY KEY NOT NULL,
instructorID INT NOT NULL,
customerID INT NOT NULL,
lessonDate DATE NOT NULL,
lessonTime TIME NOT NULL,
lessonDuration INT NOT NULL, -- 30 or 60 min
lessonFee DECIMAL(10, 2) NOT NULL, -- $44 for 30 min; $80 for 60 min
bookingTime DATETIME NOT NULL,
paymentID INT,
poolID INT NOT NULL,
bookingActive BOOLEAN NOT NULL DEFAULT TRUE,
bookingAttend BOOLEAN NOT NULL DEFAULT FALSE,

FOREIGN KEY (customerID) REFERENCES memberinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (instructorID) REFERENCES instructorinfo(userID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (paymentID) REFERENCES payments(paymentID)
    ON UPDATE CASCADE
    ON DELETE CASCADE,
FOREIGN KEY (poolID) REFERENCES pools(poolID)
    ON UPDATE CASCADE
    ON DELETE CASCADE
) AUTO_INCREMENT = 200000000;




INSERT INTO users VALUES
-- test password: rental-HaochenZhu
(10001, 1, 'adminPool1', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10002, 2, 'instructorPool1', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10003, 3, 'customerPool1', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10004, 2, 'instructor2', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10005, 3, 'member2', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10006, 3, 'member3', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10007, 3, 'member4', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10008, 3, 'member5', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10009, 3, 'member6', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10010, 3, 'member7', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10011, 3, 'member8', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10012, 3, 'member9', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10013, 3, 'member10', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10014, 3, 'member11', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10015, 3, 'member12', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10016, 2, 'instructor3', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10017, 2, 'instructor4', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10018, 2, 'instructor5', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10019, 2, 'instructor6', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True),
(10020, 2, 'instructor7', '$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36', True);

INSERT INTO admininfo VALUES
(10001, 'Mr', 'Yang', 'Yang', 'CEO', '0221566511', 'ceo@swimming.co.nz');

INSERT INTO instructorinfo VALUES
(10002, 'Miss', 'Maria', 'Martinez', 'Freestyle', '0221566511', 'Maria@swimming.co.nz', 'Hi, I am a freestyle instructor!'),
(10004, 'Mr', 'Stephen', 'King', 'Backstroke', '027345232', 'Stephen@gmail.com', 'Hi, I am an backstroke instructor'),
(10016, 'Mr', 'Michael', 'Brown', 'Freestyle', '027345232', 'Michael@gmail.com', 'Hi, I am an freestyle instructor'),
(10017, 'Miss', 'Sophia', 'Lee', 'Butterfly', '027345232', 'Sophia@gmail.com', 'Hi, I am an butterfly instructor'),
(10018, 'Mr', 'Robert', 'Davis', 'Freestyle', '027345232', 'Robert@gmail.com', 'Hi, I am an freestyle instructor'),
(10019, 'Mr', 'David', 'Garcia', 'Breaststroke ', '027345232', 'David@gmail.com', 'Hi, I am an breaststroke instructor'),
(10020, 'Miss', 'Emily', 'Johnson', 'Breaststroke', '027345232', 'Emily@gmail.com', 'Hi, I am an breaststroke instructor');

INSERT INTO memberinfo VALUES
(10003, 'Mrs', 'Mary', 'Jones', 'Programmer', '0221566511', 'Mary@ggmail.com', '456 Elm Avenue, Lincoln 7647', "2002-02-14", 'Not bad'),
(10005, 'Miss', 'Alice', 'White', 'Doctor', '021234556', 'Alice@gmail.com', '789 Oak Street, Christchurch 7647', '2001-04-23', 'Good'),
(10006, 'Mr', 'James', 'Smith', 'Teacher', '021232456', 'James@gmail.com', '321 Maple Lane, Christchurch 7647', '2001-04-23', 'Good'),
(10007, 'Mr', 'William', 'Johnson', 'Engineer', '021234356', 'William@gmail.com', '567 Birch Road, Christchurch 7647', '2001-04-23', 'Good'),
(10008, 'Mr', 'John', 'Brown', 'Accountant', '021234523', 'John@gmail.com', '890 Pine Drive, Christchurch 7647', '2001-04-23', 'Good'),
(10009, 'Mr', 'Robert', 'Davis', 'Engineer', '021234552', 'Robert@gmail.com', '234 Cedar Court, Christchurch 7647', '2001-04-23', 'Good'),
(10010, 'Miss', 'Linda', 'Clark', 'Accountant', '0213463847', 'Linda@gmail.com', '678 Spruce Lane, Christchurch 7647', '2001-04-23', 'Good'),
(10011, 'Miss', 'Patricia', 'Patricia', 'Engineer', '021234559', 'Patricia@gmail.com', '123 Willow Street, Christchurch 7647', '2001-04-23', 'Good'),
(10012, 'Miss', 'Elizabeth', 'Turner', 'Programmer', '021264356', 'Elizabeth@gmail.com', '345 Fir Road, Christchurch 7647', '2001-04-23', 'Good'),
(10013, 'Miss', 'Susan', 'Walker', 'Engineer', '021237946', 'Susan@gmail.com', '678 Redwood Avenue, Christchurch 7647', '2001-04-23', 'Good'),
(10014, 'Miss', 'Jessica', 'Scott', 'Programmer', '021238458', 'Jessica@gmail.com', '901 Ash Street, Christchurch 7647', '2001-04-23', 'Good'),
(10015, 'Miss', 'Sarah', 'Baker', 'Programmer', '021238967', 'Sarah@gmail.com', '234 Mahogany Drive, Christchurch 7647', '2001-04-23', 'Good');

INSERT INTO pools VALUES
(1, 'Olympic Pool', 'Olympic Pool'),
(2, 'Hydrotherapy Pool', 'Hydrotherapy Pool'),
(3, 'Training Pool', 'Training Pool'),
(4, 'Family Pool', 'For family');


INSERT INTO aerobics_schedule VALUES
(1, 10002, 'Aqua Cardio', 30, '2023-08-23 11:00:00', 60, 2, TRUE),
(2, 10002, 'Aqua 2', 30, '2023-08-23 12:00:00', 60, 2, TRUE),
(3, 10002, 'AquaHIIT', 15, '2023-08-26 9:30:00', 60, 2, TRUE),
(4, 10002, 'AquaLITE', 20, '2023-08-25 15:00:00', 60, 2, TRUE),
(5, 10002, 'AquaENERGY', 30, '2023-08-27 06:00:00', 60, 2, TRUE),
(6, 10002, 'AquaPOWER', 30, '2023-08-24 9:30:00', 60, 2, TRUE),
(7,10004,'fdff',30,'2023-09-22 20:30:00',60,2,0),
(8,10002,'tghh',30,'2023-05-18 10:00:00',60,2,0),
(9,10004,'waaaaaao',30,'2023-09-22 17:30:00',60,3,1),
(10,10002,'23333ff',30,'2023-09-13 11:30:00',60,2,1);


INSERT INTO subscriptions VALUES
(1, 10003, '2023-08-19', '2024-08-18'),
(2, 10005, '2023-08-22', '2024-08-21');

DELIMITER //
CREATE PROCEDURE InsertTimeSlots()
BEGIN
    DECLARE slotsID INT;
    DECLARE startTime TIME;
    DECLARE endTime TIME;

    SET slotsID := 1;
    SET startTime := '05:00:00';
    SET endTime := '05:15:00';

    WHILE endTime <= '22:00:00' DO
        INSERT INTO time_slots (slotsID, startTime, endTime)
        VALUES (slotsID, startTime, endTime);

        SET startTime := ADDTIME(startTime, '00:15:00');
        SET endTime := ADDTIME(endTime, '00:15:00');
        SET slotsID := slotsID + 1;
    END WHILE;
END //
DELIMITER ;

-- Call the procedure to insert time slots
CALL InsertTimeSlots();
 
INSERT INTO user_availability VALUES
(1,10002,25,'2023-08-23', FALSE),
(2,10002,26,'2023-08-23', FALSE),
(3,10002,27,'2023-08-23', FALSE),
(4,10002,28,'2023-08-23', FALSE),
(5,10002,29,'2023-08-23', FALSE),
(6,10002,30,'2023-08-23', FALSE),
(7,10002,31,'2023-08-23', FALSE),
(8,10002,32,'2023-08-23', FALSE),
(9,10002,19,'2023-08-24', FALSE),
(10,10002,20,'2023-08-24', FALSE),
(11,10002,21,'2023-08-24', FALSE),
(12,10002,22,'2023-08-24', FALSE),
(13,10002,41,'2023-08-25', FALSE),
(14,10002,42,'2023-08-25', FALSE),
(15,10002,43,'2023-08-25', FALSE),
(16,10002,44,'2023-08-25', FALSE),
(17,10002,19,'2023-08-26', FALSE),
(18,10002,20,'2023-08-26', FALSE),
(19,10002,21,'2023-08-26', FALSE),
(20,10002,22,'2023-08-26', FALSE),
(21,10002,5,'2023-08-27', FALSE),
(22,10002,6,'2023-08-27', FALSE),
(23,10002,7,'2023-08-27', FALSE),
(24,10002,8,'2023-08-27', FALSE),
(33,10005,49,'2023-09-10',0),
(34,10005,50,'2023-09-10',0),
(35,10005,51,'2023-09-10',0),
(36,10005,52,'2023-09-10',0),
(37,10002,53,'2023-09-10',0),
(38,10002,54,'2023-09-10',0),
(39,10002,55,'2023-09-10',0),(40,10002,56,'2023-09-10',0),(45,10005,5,'2023-09-10',0),(46,10005,6,'2023-09-10',0),
(47,10005,7,'2023-09-10',0),(48,10005,8,'2023-09-10',0),(53,10005,59,'2023-09-10',0),(54,10005,60,'2023-09-10',0),
(55,10005,61,'2023-09-10',0),(56,10005,62,'2023-09-10',0),(61,10004,51,'2023-09-22',0),(62,10004,52,'2023-09-22',0),
(63,10004,53,'2023-09-22',0),(64,10004,54,'2023-09-22',0),(81,10002,53,'2023-10-06',0),(82,10002,54,'2023-10-06',0),
(83,10002,55,'2023-10-06',0),(84,10002,56,'2023-10-06',0),(85,10002,53,'2023-07-20',0),(86,10002,54,'2023-07-20',0),
(87,10002,55,'2023-07-20',0),(88,10002,56,'2023-07-20',0),(89,10002,37,'2023-08-17',0),(90,10002,38,'2023-08-17',0),
(91,10002,39,'2023-08-17',0),(92,10002,40,'2023-08-17',0),(105,10005,67,'2023-09-13',0),(106,10005,68,'2023-09-13',0),
(122,10002,27,'2023-09-13',0),(123,10002,28,'2023-09-13',0),(124,10002,29,'2023-09-13',0),(125,10002,30,'2023-09-13',0);

INSERT INTO payments VALUES
(1,10003,1,50.00, '2023-08-23 11:00:00'),
(2,10005,1,50.00, '2023-08-25 11:00:00'),
(3,10003,2,50.00, '2023-08-23 10:00:00'),
(4,10005,2,50.00, '2023-08-25 10:00:00');

INSERT INTO individual_lesson_bookings VALUES
(1,10002,10003,'2023-08-23', '11:00:00', 30, 50.00,'2023-08-23 10:00:00', 3, 1, 1,0),
(2,10002,10005,'2023-08-25', '11:00:00', 30, 50.00,'2023-08-23 10:00:00', 4, 2, 1,0);

INSERT INTO `aerobics_bookings` VALUES 
(100000002,8,10005,'2023-09-09 22:37:01',0,0),
(100000003,10,10005,'2023-09-09 23:31:39',0,0);

INSERT INTO `news_updates` VALUES 
(1,'fff','fff','2023-09-09 19:34:49',10001,0),
(2,'fffd','ddd','2023-09-09 19:54:19',10001,0),
(5,'[CHANGE] tghhg has a schedule change.','The schedule of tghhg has been changed. Please check the new details.\n\n                        Status: Active\n\n                        Instructor: instructorF\n\n                        Duration: 30 min\n\n                        Date: 2023-09-11 18:00:00\n\n                        Max Capacity: 30\n\n                        Pool: Hydrotherapy Pool\n\n                        ','2023-09-09 22:37:35',10001,0),
(6,'[NEW] Welcome to our new class: waaaaaao','Please see details below. \n                        Status: Active\n                        Instructor: Stephen\n                        Duration: 30 min\n                        Date: 2023-09-22 13:30:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-09 22:48:02',10001,0),
(18,'[CANCELLED] tghh has been cancelled','tghh has been cancelled. Please re-book a new class or contact admin.','2023-09-09 23:14:36',10001,0),
(19,'[CANCELLED] tghh has been cancelled','tghh has been cancelled. Please re-book a new class or contact admin.','2023-09-09 23:14:36',10001,10005),
(21,'[NEW] Welcome to our new class: vsdfdfsv','Please see details below. \n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 30 min\n                        Date: 2023-10-30 15:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-09 23:30:48',10001,0),
(22,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-08-13 14:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-09 23:31:12',10001,0),
(23,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 30 min\n                        Date: 2023-09-13 21:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-09 23:31:33',10001,0),
(24,'[REMOVED] You have been removed from vsdfdfsv.','You have been removed from vsdfdfsv. Please re-book a new class or contact admin.','2023-09-09 23:33:20',10001,10005),
(25,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:37',10001,0),
(26,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:37',10001,10005),
(27,'[CHANGE] 23333\'s schedule has changed.','The schedule of 23333 has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:51',10001,0),
(28,'[CHANGE] 23333\'s schedule has changed.','The schedule of 23333 has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:51',10001,10005),
(29,'[CHANGE] 23333ff\'s schedule has changed.','The schedule of 23333ff has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:14:23',10001,0),
(30,'[REMOVED] Your individual lesson on 2023-08-25 has been cancelled.','Your individual lesson on 2023-08-25 has been cancelled. Please re-book a new class or contact admin.','2023-09-10 01:15:22',10001,10005),
(31,'[REMOVED] Your individual lesson on 2023-08-25 has been cancelled.','Your individual lesson on 2023-08-25 has been cancelled. Please re-book a new class or contact admin.','2023-09-10 01:15:22',10001,10002);


