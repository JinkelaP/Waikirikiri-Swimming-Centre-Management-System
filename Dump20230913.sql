-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: swimmingpool
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `admininfo`
--

DROP TABLE IF EXISTS `admininfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `admininfo` (
  `userID` int NOT NULL,
  `title` varchar(10) NOT NULL,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `position` varchar(20) NOT NULL,
  `phoneNumber` varchar(15) NOT NULL,
  `email` varchar(40) NOT NULL,
  PRIMARY KEY (`userID`),
  CONSTRAINT `admininfo_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `admininfo`
--

LOCK TABLES `admininfo` WRITE;
/*!40000 ALTER TABLE `admininfo` DISABLE KEYS */;
INSERT INTO `admininfo` VALUES (10001,'Mr','Elon','Musk','CEO','0221566511','ceo@swimming.co.nz');
/*!40000 ALTER TABLE `admininfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aerobics_bookings`
--

DROP TABLE IF EXISTS `aerobics_bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aerobics_bookings` (
  `bookingID` int NOT NULL AUTO_INCREMENT,
  `scheduleID` int NOT NULL,
  `customerID` int NOT NULL,
  `bookingTime` datetime NOT NULL,
  `bookingActive` tinyint(1) NOT NULL DEFAULT '1',
  `bookingAttend` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`bookingID`),
  KEY `scheduleID` (`scheduleID`),
  KEY `customerID` (`customerID`),
  CONSTRAINT `aerobics_bookings_ibfk_1` FOREIGN KEY (`scheduleID`) REFERENCES `aerobics_schedule` (`scheduleID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `aerobics_bookings_ibfk_2` FOREIGN KEY (`customerID`) REFERENCES `memberinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=100000077 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aerobics_bookings`
--

LOCK TABLES `aerobics_bookings` WRITE;
/*!40000 ALTER TABLE `aerobics_bookings` DISABLE KEYS */;
INSERT INTO `aerobics_bookings` VALUES (100000002,8,10005,'2023-09-09 22:37:01',0,0),(100000003,10,10005,'2023-09-09 23:31:39',0,0),(100000004,10,10006,'2023-09-12 17:14:06',1,0),(100000005,12,10006,'2023-09-12 17:14:10',1,0),(100000006,13,10006,'2023-09-12 17:14:18',1,0),(100000007,11,10007,'2023-09-12 17:15:45',1,0),(100000008,12,10007,'2023-09-12 17:15:48',1,0),(100000009,10,10008,'2023-09-12 17:19:27',1,0),(100000010,11,10008,'2023-09-12 17:19:30',1,0),(100000011,13,10008,'2023-09-12 17:19:36',1,0),(100000012,10,10009,'2023-09-12 17:21:06',1,0),(100000013,11,10009,'2023-09-12 17:21:12',1,0),(100000014,10,10010,'2023-09-12 17:26:23',1,1),(100000015,11,10010,'2023-09-12 17:26:30',1,1),(100000016,10,10011,'2023-09-12 17:31:31',1,0),(100000017,12,10011,'2023-09-12 17:31:37',1,0),(100000018,14,10012,'2023-09-12 17:32:58',1,0),(100000019,10,10012,'2023-09-12 17:33:03',1,0),(100000020,12,10012,'2023-09-12 17:33:09',1,0),(100000021,10,10013,'2023-09-12 17:35:10',1,0),(100000022,11,10013,'2023-09-12 17:35:14',1,0),(100000023,14,10013,'2023-09-12 17:35:17',1,0),(100000024,12,10013,'2023-09-12 17:35:22',1,0),(100000025,10,10014,'2023-09-12 17:37:05',1,1),(100000026,11,10014,'2023-09-12 17:37:09',1,1),(100000027,14,10014,'2023-09-12 17:37:13',1,1),(100000028,13,10014,'2023-09-12 17:37:18',1,1),(100000029,11,10015,'2023-09-12 17:38:48',1,0),(100000030,10,10015,'2023-09-12 17:38:52',1,0),(100000031,13,10015,'2023-09-12 17:39:00',1,0),(100000032,14,10003,'2023-09-13 09:42:37',1,0),(100000033,11,10003,'2023-09-13 09:42:42',1,0),(100000034,13,10003,'2023-09-13 09:42:47',1,0),(100000035,15,10003,'2023-09-13 10:43:28',1,0),(100000036,15,10026,'2023-09-13 11:23:57',1,0),(100000037,14,10026,'2023-09-13 11:24:03',1,0),(100000038,15,10032,'2023-09-13 12:10:32',1,0),(100000039,16,10032,'2023-09-13 12:10:36',1,0),(100000040,11,10032,'2023-09-13 12:10:56',1,0),(100000041,13,10032,'2023-09-13 12:11:03',1,0),(100000042,15,10030,'2023-09-13 12:21:06',1,0),(100000043,16,10030,'2023-09-13 12:21:10',1,0),(100000044,13,10030,'2023-09-13 12:21:16',1,0),(100000045,14,10030,'2023-09-13 12:21:22',1,0),(100000046,15,10029,'2023-09-13 12:21:59',1,1),(100000047,16,10029,'2023-09-13 12:22:03',1,1),(100000048,14,10029,'2023-09-13 12:22:07',1,1),(100000049,13,10029,'2023-09-13 12:22:11',1,1),(100000050,15,10028,'2023-09-13 12:23:00',1,0),(100000051,16,10028,'2023-09-13 12:23:05',1,0),(100000052,13,10028,'2023-09-13 12:23:08',1,0),(100000053,11,10028,'2023-09-13 12:23:16',1,0),(100000054,14,10028,'2023-09-13 12:26:41',1,0),(100000055,12,10028,'2023-09-13 12:26:45',1,0),(100000056,15,10027,'2023-09-13 12:27:57',1,1),(100000057,14,10027,'2023-09-13 12:28:01',1,1),(100000058,16,10027,'2023-09-13 12:28:04',1,1),(100000059,11,10027,'2023-09-13 12:28:08',1,1),(100000060,12,10027,'2023-09-13 12:28:12',1,1),(100000061,16,10010,'2023-09-13 14:56:05',1,1),(100000062,18,10010,'2023-09-13 14:56:11',1,1),(100000063,12,10010,'2023-09-13 14:56:21',1,1),(100000064,12,10003,'2023-09-13 15:58:12',1,0),(100000065,22,10036,'2023-09-13 18:06:35',1,0),(100000066,22,10032,'2023-09-13 18:07:02',1,0),(100000067,22,10031,'2023-09-13 18:07:25',1,0),(100000068,15,10031,'2023-09-13 18:07:29',1,0),(100000069,11,10031,'2023-09-13 18:07:35',1,0),(100000070,13,10031,'2023-09-13 18:07:40',1,0),(100000071,22,10030,'2023-09-13 18:08:03',1,0),(100000072,12,10030,'2023-09-13 18:08:09',1,0),(100000073,12,10029,'2023-09-13 18:09:24',1,1),(100000074,22,10029,'2023-09-13 18:09:28',1,1),(100000075,11,10029,'2023-09-13 18:10:05',1,1),(100000076,23,10029,'2023-09-13 18:36:17',1,0);
/*!40000 ALTER TABLE `aerobics_bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `aerobics_schedule`
--

DROP TABLE IF EXISTS `aerobics_schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `aerobics_schedule` (
  `scheduleID` int NOT NULL AUTO_INCREMENT,
  `instructorID` int NOT NULL,
  `sessionName` varchar(100) NOT NULL,
  `maxParticipants` int NOT NULL DEFAULT '30',
  `sessionTime` datetime NOT NULL,
  `lessonDuration` int NOT NULL DEFAULT '60',
  `poolID` int NOT NULL,
  `bookingActive` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`scheduleID`),
  KEY `instructorID` (`instructorID`),
  KEY `poolID` (`poolID`),
  CONSTRAINT `aerobics_schedule_ibfk_1` FOREIGN KEY (`instructorID`) REFERENCES `instructorinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `aerobics_schedule_ibfk_2` FOREIGN KEY (`poolID`) REFERENCES `pools` (`poolID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `aerobics_schedule`
--

LOCK TABLES `aerobics_schedule` WRITE;
/*!40000 ALTER TABLE `aerobics_schedule` DISABLE KEYS */;
INSERT INTO `aerobics_schedule` VALUES (1,10002,'Aqua Cardio',30,'2023-08-23 11:00:00',60,2,1),(2,10002,'Aqua First',30,'2023-08-23 12:00:00',60,2,1),(3,10002,'Aqua High',30,'2023-08-26 09:30:00',60,2,1),(4,10002,'Aqua Lite',30,'2023-08-25 15:00:00',60,2,1),(5,10002,'AquaENERGY',30,'2023-08-27 06:00:00',60,2,1),(6,10002,'AquaPOWER',30,'2023-08-24 09:30:00',60,2,1),(7,10004,'fdff',30,'2023-09-22 20:30:00',60,2,0),(8,10002,'tghh',30,'2023-05-18 10:00:00',60,2,0),(9,10004,'Aqua Silver',30,'2023-09-22 17:30:00',60,2,1),(10,10002,'Aqua Gold',30,'2023-09-13 11:30:00',60,2,1),(11,10016,'Aqua Fancy',20,'2023-09-15 11:00:00',60,2,1),(12,10019,'Aqua Love',30,'2023-09-14 14:00:00',30,3,1),(13,10004,'Aqua Awesome',30,'2023-09-16 17:00:00',60,2,1),(14,10016,'Aqua Acme',30,'2023-09-17 09:00:00',60,2,1),(15,10017,'Aqua Crest',30,'2023-09-18 07:00:00',60,3,1),(16,10023,'Aqua Epic',30,'2023-09-19 11:00:00',60,3,1),(17,10019,'Aqua Grand',30,'2023-09-20 08:00:00',60,3,1),(18,10002,'Aqua Peak',30,'2023-09-18 12:00:00',60,2,1),(19,10017,'Aqua Fun',30,'2023-09-20 12:00:00',60,2,1),(20,10017,'Aqua NewZew',30,'2023-08-03 06:00:00',60,3,1),(21,10018,'Aqua Robust',30,'2023-09-13 17:00:00',60,3,1),(22,10035,'Aqua Weida',30,'2023-09-13 20:00:00',60,3,1),(23,10017,'Aqua Tmd',30,'2023-09-13 19:00:00',60,3,1);
/*!40000 ALTER TABLE `aerobics_schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `attendanceID` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `attendanceType` int NOT NULL,
  `attendanceTime` datetime NOT NULL,
  PRIMARY KEY (`attendanceID`),
  KEY `userID` (`userID`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `memberinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES (1,10014,2,'2023-09-13 13:14:52'),(2,10003,3,'2023-09-13 14:49:21'),(3,10029,2,'2023-09-13 18:11:02'),(4,10030,2,'2023-09-13 18:11:10'),(5,10031,2,'2023-09-13 18:11:21'),(6,10032,2,'2023-09-13 18:11:28'),(7,10029,2,'2023-09-13 18:15:32'),(8,10029,3,'2023-09-13 18:15:39'),(9,10028,2,'2023-09-13 18:20:03'),(10,10029,2,'2023-09-13 18:38:11'),(11,10029,3,'2023-09-13 18:38:17');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `individual_lesson_bookings`
--

DROP TABLE IF EXISTS `individual_lesson_bookings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `individual_lesson_bookings` (
  `bookingID` int NOT NULL AUTO_INCREMENT,
  `instructorID` int NOT NULL,
  `customerID` int NOT NULL,
  `lessonDate` date NOT NULL,
  `lessonTime` time NOT NULL,
  `lessonDuration` int NOT NULL,
  `lessonFee` decimal(10,2) NOT NULL,
  `bookingTime` datetime NOT NULL,
  `paymentID` int DEFAULT NULL,
  `poolID` int NOT NULL,
  `bookingActive` tinyint(1) NOT NULL DEFAULT '1',
  `bookingAttend` tinyint(1) NOT NULL DEFAULT '0',
  PRIMARY KEY (`bookingID`),
  KEY `customerID` (`customerID`),
  KEY `instructorID` (`instructorID`),
  KEY `paymentID` (`paymentID`),
  KEY `poolID` (`poolID`),
  CONSTRAINT `individual_lesson_bookings_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `memberinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `individual_lesson_bookings_ibfk_2` FOREIGN KEY (`instructorID`) REFERENCES `instructorinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `individual_lesson_bookings_ibfk_3` FOREIGN KEY (`paymentID`) REFERENCES `payments` (`paymentID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `individual_lesson_bookings_ibfk_4` FOREIGN KEY (`poolID`) REFERENCES `pools` (`poolID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=200000030 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `individual_lesson_bookings`
--

LOCK TABLES `individual_lesson_bookings` WRITE;
/*!40000 ALTER TABLE `individual_lesson_bookings` DISABLE KEYS */;
INSERT INTO `individual_lesson_bookings` VALUES (1,10002,10003,'2023-08-23','11:00:00',30,50.00,'2023-08-23 10:00:00',3,1,1,0),(2,10002,10005,'2023-08-25','11:00:00',30,50.00,'2023-08-23 10:00:00',4,2,1,0),(200000000,10017,10005,'2023-09-14','09:00:00',60,0.00,'2023-09-12 17:04:19',5,1,1,0),(200000001,10004,10005,'2023-09-16','09:00:00',30,0.00,'2023-09-12 17:07:34',6,2,1,0),(200000002,10018,10005,'2023-09-12','12:00:00',60,0.00,'2023-09-12 17:10:05',7,3,1,0),(200000003,10017,10006,'2023-09-16','13:00:00',60,0.00,'2023-09-12 17:14:34',10,1,1,0),(200000004,10020,10007,'2023-09-18','08:00:00',60,0.00,'2023-09-12 17:16:12',13,2,1,0),(200000005,10002,10008,'2023-09-15','10:00:00',60,0.00,'2023-09-12 17:19:48',16,1,1,0),(200000006,10019,10008,'2023-09-18','09:00:00',60,0.00,'2023-09-12 17:20:18',17,4,1,0),(200000007,10020,10009,'2023-09-15','09:00:00',60,0.00,'2023-09-12 17:21:36',19,2,1,0),(200000008,10017,10009,'2023-09-17','10:30:00',30,0.00,'2023-09-12 17:22:09',NULL,4,1,0),(200000009,10018,10010,'2023-09-16','09:00:00',60,0.00,'2023-09-12 17:26:46',21,1,1,0),(200000010,10016,10011,'2023-09-14','09:00:00',60,0.00,'2023-09-12 17:31:09',24,1,1,0),(200000011,10017,10012,'2023-09-15','10:45:00',60,0.00,'2023-09-12 17:33:19',26,2,1,0),(200000012,10019,10012,'2023-09-16','10:00:00',30,0.00,'2023-09-12 17:33:43',27,3,1,0),(200000013,10018,10013,'2023-09-14','10:00:00',60,0.00,'2023-09-12 17:34:47',30,3,1,0),(200000014,10019,10014,'2023-09-15','09:00:00',60,0.00,'2023-09-12 17:36:43',33,4,1,0),(200000015,10020,10015,'2023-09-17','09:00:00',60,0.00,'2023-09-12 17:38:25',36,4,1,0),(200000016,10022,10026,'2023-09-17','11:00:00',60,80.00,'2023-09-13 11:24:28',42,4,1,0),(200000017,10021,10026,'2023-09-19','10:00:00',30,44.00,'2023-09-13 11:25:24',43,3,1,0),(200000018,10022,10028,'2023-09-16','09:00:00',60,80.00,'2023-09-13 12:23:33',49,1,1,0),(200000019,10022,10028,'2023-09-14','09:30:00',60,80.00,'2023-09-13 12:24:50',50,2,1,0),(200000020,10021,10027,'2023-09-18','09:00:00',60,80.00,'2023-09-13 12:27:39',53,4,1,0),(200000021,10002,10025,'2023-09-17','15:00:00',60,80.00,'2023-09-13 14:26:49',54,1,1,0),(200000022,10018,10006,'2023-09-18','09:30:00',60,80.00,'2023-09-13 14:57:33',55,4,1,0),(200000023,10018,10006,'2023-09-17','08:00:00',60,80.00,'2023-09-13 14:58:04',56,2,1,0),(200000024,10018,10003,'2023-09-14','09:00:00',60,80.00,'2023-09-13 15:57:29',57,2,1,0),(200000025,10017,10030,'2023-09-18','09:00:00',60,80.00,'2023-09-13 18:08:29',62,4,1,0),(200000026,10004,10030,'2023-09-13','17:00:00',60,80.00,'2023-09-13 18:08:51',63,2,1,1),(200000027,10017,10029,'2023-09-14','13:00:00',60,80.00,'2023-09-13 18:09:46',64,2,1,0),(200000028,10004,10029,'2023-09-13','16:00:00',60,80.00,'2023-09-13 18:37:12',65,3,1,1),(200000029,10004,10029,'2023-09-13','08:00:00',30,44.00,'2023-09-13 18:37:39',66,1,1,1);
/*!40000 ALTER TABLE `individual_lesson_bookings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `instructorinfo`
--

DROP TABLE IF EXISTS `instructorinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `instructorinfo` (
  `userID` int NOT NULL,
  `title` varchar(10) NOT NULL,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `position` varchar(20) NOT NULL,
  `phoneNumber` varchar(15) NOT NULL,
  `email` varchar(40) NOT NULL,
  `introduction` varchar(1000) NOT NULL,
  PRIMARY KEY (`userID`),
  CONSTRAINT `instructorinfo_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `instructorinfo`
--

LOCK TABLES `instructorinfo` WRITE;
/*!40000 ALTER TABLE `instructorinfo` DISABLE KEYS */;
INSERT INTO `instructorinfo` VALUES (10002,'Miss','Maria','Martinez','Freestyle','0221566511','Maria@swimming.co.nz','Hi, I am a freestyle instructor!'),(10004,'Mr','Stephen','King','Backstroke','027345232','Stephen@gmail.com','Hi, I am an backstroke instructor'),(10016,'Mr','Michael','Brown','Freestyle','027345232','Michael@gmail.com','Hi, I am an freestyle instructor'),(10017,'Miss','Sophia','Lee','Butterfly','027345232','Sophia@gmail.com','Hi, I am an butterfly instructor'),(10018,'Mr','Robert','Davis','Freestyle','027345232','Robert@gmail.com','Hi, I am an freestyle instructor'),(10019,'Mr','David','Garcia','Breaststroke ','027345232','David@gmail.com','Hi, I am an breaststroke instructor'),(10020,'Miss','Emily','Johnson','Breaststroke','027345232','Emily@gmail.com','Hi, I am an breaststroke instructor'),(10021,'Mrs','Nancy','Lewis','Diving','874-797-8100','xugut@gmail.com','Hi, I am a freestyle instructor!'),(10022,'Ms','Steven','Carter','Flip ','181-365-7789','dynvq@gmail.com','Hi, I am a freestyle instructor!'),(10023,'Dr','Karen','Robinson','Sidestroke','234-566-7636','ekygk@gmail.com','Hi, I am an breaststroke instructor'),(10033,'Ms','Andrew','Scott','Safety ','807-726-1055','ijbig@gmail.com','Hi, I am a instructor'),(10034,'Ms','Edward','Baker','Flip ','847-102-4040','vknrk@gmail.com','Hi, I am a instructor'),(10035,'Mrs','Steven','Lewis','Freestyle','113-741-6374','rxgin@gmail.com','Hi, I am a instructor');
/*!40000 ALTER TABLE `instructorinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `memberinfo`
--

DROP TABLE IF EXISTS `memberinfo`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `memberinfo` (
  `userID` int NOT NULL,
  `title` varchar(10) NOT NULL,
  `firstName` varchar(20) NOT NULL,
  `lastName` varchar(20) NOT NULL,
  `position` varchar(20) NOT NULL,
  `phoneNumber` varchar(15) NOT NULL,
  `email` varchar(40) NOT NULL,
  `physicalAddress` varchar(200) NOT NULL,
  `dateOfBirth` date NOT NULL,
  `healthInfo` varchar(200) DEFAULT NULL,
  PRIMARY KEY (`userID`),
  CONSTRAINT `memberinfo_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `memberinfo`
--

LOCK TABLES `memberinfo` WRITE;
/*!40000 ALTER TABLE `memberinfo` DISABLE KEYS */;
INSERT INTO `memberinfo` VALUES (10003,'Mrs','Mary','Jones','Programmer','0221566511','Mary@ggmail.com','456 Elm Avenue, Lincoln 7647','2002-02-14','Good'),(10005,'Miss','Alice','White','Doctor','021234556','Alice@gmail.com','789 Oak Street, Christchurch 7647','2001-04-23','Good'),(10006,'Mr','James','Smith','Teacher','021232456','James@gmail.com','321 Maple Lane, Christchurch 7647','2001-04-23','Good'),(10007,'Mr','William','Johnson','Engineer','021234356','William@gmail.com','567 Birch Road, Christchurch 7647','2001-04-23','Good'),(10008,'Mr','John','Brown','Accountant','021234523','John@gmail.com','890 Pine Drive, Christchurch 7647','2001-04-23','Good'),(10009,'Mr','Robert','Davis','Engineer','021234552','Robert@gmail.com','234 Cedar Court, Christchurch 7647','2001-04-23','Good'),(10010,'Miss','Linda','Clark','Accountant','0213463847','Linda@gmail.com','678 Spruce Lane, Christchurch 7647','2001-04-23','Good'),(10011,'Miss','Patree','Shark','Engineer','021234559','Patricia@gmail.com','123 Willow Street, Christchurch 7647','2001-04-23','Good'),(10012,'Miss','Elizabeth','Turner','Programmer','021264356','Elizabeth@gmail.com','345 Fir Road, Christchurch 7647','2001-04-23','Good'),(10013,'Miss','Susan','Walker','Engineer','021237946','Susan@gmail.com','678 Redwood Avenue, Christchurch 7647','2001-04-23','Good'),(10014,'Miss','Jessica','Scottie','Programmer','021238458','Jessica@gmail.com','901 Ash Street, Christchurch 7647','2001-04-23','Good'),(10015,'Miss','Sarah','Baker','Programmer','021238967','Sarah@gmail.com','234 Mahogany Drive, Christchurch 7647','2001-04-23','Good'),(10024,'Dr','Andrew','Jones','Teacher','465-062-9518','boplb@gmail.com','333 Tuam Street, Christchurch, New Zealand','2008-12-21','Good'),(10025,'Dr','Anthony','Phillips','Doctor','220-845-0696','kfhpz@gmail.com','589 Hereford Street, Christchurch, New Zealand','1966-07-07','Good'),(10026,'Mr','Paul','Phillips','Chef','169-072-5779','qrkqz@gmail.com','267 Fitzgerald Avenue, Christchurch, New Zealand','1978-10-16','Good'),(10027,'Mrs','Lisa','Green','Manager','151-608-5782','vatoh@gmail.com','962 Hereford Street, Christchurch, New Zealand','1974-07-07','Good'),(10028,'Mr','George','Martin','Nurse','977-626-3982','gcqdx@gmail.com','293 Lichfield Street, Christchurch, New Zealand','1980-12-05','Good'),(10029,'Ms','David','Wilson','Driver','092-694-9879','hxkqk@gmail.com','490 Moorhouse Avenue, Christchurch, New Zealand','1987-10-21','Good'),(10030,'Ms','Linda','Lewis','Lawyer','074-502-4876','zagmn@gmail.com','94 Barbadoes Street, Christchurch, New Zealand','2012-07-01','Good'),(10031,'Ms','George','Wilson','Chef','732-635-7948','moftc@gmail.com','209 High Street, Christchurch, New Zealand','1994-11-17','Good'),(10032,'Dr','Christopher','Smith','Artist','162-013-3978','sooxy@gmail.com','89 Fitzgerald Avenue, Christchurch, New Zealand','1969-02-01',NULL),(10036,'Miss','James','Johnsonn','Doctor','6564444444','abcabc5@gmail.com','aljfdlakjfd','2013-11-21','Good');
/*!40000 ALTER TABLE `memberinfo` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `news_updates`
--

DROP TABLE IF EXISTS `news_updates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `news_updates` (
  `newsID` int NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `content` text NOT NULL,
  `publishDate` datetime NOT NULL,
  `adminID` int NOT NULL,
  `newsTypeID` int DEFAULT NULL,
  PRIMARY KEY (`newsID`),
  KEY `adminID` (`adminID`),
  CONSTRAINT `news_updates_ibfk_1` FOREIGN KEY (`adminID`) REFERENCES `admininfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=56 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `news_updates`
--

LOCK TABLES `news_updates` WRITE;
/*!40000 ALTER TABLE `news_updates` DISABLE KEYS */;
INSERT INTO `news_updates` VALUES (1,'fff','fff','2023-09-09 19:34:49',10001,0),(2,'fffd','ddd','2023-09-09 19:54:19',10001,0),(5,'[CHANGE] tghhg has a schedule change.','The schedule of tghhg has been changed. Please check the new details.\n\n                        Status: Active\n\n                        Instructor: instructorF\n\n                        Duration: 30 min\n\n                        Date: 2023-09-11 18:00:00\n\n                        Max Capacity: 30\n\n                        Pool: Hydrotherapy Pool\n\n                        ','2023-09-09 22:37:35',10001,0),(6,'[NEW] Welcome to our new class: waaaaaao','Please see details below. \n                        Status: Active\n                        Instructor: Stephen\n                        Duration: 30 min\n                        Date: 2023-09-22 13:30:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-09 22:48:02',10001,0),(18,'[CANCELLED] tghh has been cancelled','tghh has been cancelled. Please re-book a new class or contact admin.','2023-09-09 23:14:36',10001,0),(19,'[CANCELLED] tghh has been cancelled','tghh has been cancelled. Please re-book a new class or contact admin.','2023-09-09 23:14:36',10001,10005),(21,'[NEW] Welcome to our new class: vsdfdfsv','Please see details below. \n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 30 min\n                        Date: 2023-10-30 15:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-09 23:30:48',10001,0),(22,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-08-13 14:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-09 23:31:12',10001,0),(23,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 30 min\n                        Date: 2023-09-13 21:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-09 23:31:33',10001,0),(24,'[REMOVED] You have been removed from vsdfdfsv.','You have been removed from vsdfdfsv. Please re-book a new class or contact admin.','2023-09-09 23:33:20',10001,10005),(25,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:37',10001,0),(26,'[CHANGE] vsdfdfsv\'s schedule has changed.','The schedule of vsdfdfsv has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:37',10001,10005),(27,'[CHANGE] 23333\'s schedule has changed.','The schedule of 23333 has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:51',10001,0),(28,'[CHANGE] 23333\'s schedule has changed.','The schedule of 23333 has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:11:51',10001,10005),(29,'[CHANGE] 23333ff\'s schedule has changed.','The schedule of 23333ff has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: instructorF\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-10 00:14:23',10001,0),(30,'[REMOVED] Your individual lesson on 2023-08-25 has been cancelled.','Your individual lesson on 2023-08-25 has been cancelled. Please re-book a new class or contact admin.','2023-09-10 01:15:22',10001,10005),(31,'[REMOVED] Your individual lesson on 2023-08-25 has been cancelled.','Your individual lesson on 2023-08-25 has been cancelled. Please re-book a new class or contact admin.','2023-09-10 01:15:22',10001,10002),(32,'[NEW] Welcome to our new class: Aqua Fancy','Please see details below. \n                        Status: Active\n                        Instructor: Michael\n                        Duration: 60 min\n                        Date: 2023-09-15 11:00:00\n                        Max Capacity: 20\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:11:26',10001,0),(33,'[NEW] Welcome to our new class: Aqua Love','Please see details below. \n                        Status: Active\n                        Instructor: David\n                        Duration: 30 min\n                        Date: 2023-09-14 14:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-12 17:12:14',10001,0),(34,'[NEW] Welcome to our new class: Aqua Awesome','Please see details below. \n                        Status: Active\n                        Instructor: Stephen\n                        Duration: 60 min\n                        Date: 2023-09-16 17:00:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:13:04',10001,0),(35,'[CHANGE] Aqua Gold\'s schedule has changed.','The schedule of Aqua Gold has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:28:58',10001,0),(36,'[CHANGE] Aqua Gold\'s schedule has changed.','The schedule of Aqua Gold has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:28:58',10001,10006),(37,'[CHANGE] Aqua Gold\'s schedule has changed.','The schedule of Aqua Gold has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:28:58',10001,10008),(38,'[CHANGE] Aqua Gold\'s schedule has changed.','The schedule of Aqua Gold has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:28:58',10001,10009),(39,'[CHANGE] Aqua Gold\'s schedule has changed.','The schedule of Aqua Gold has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-13 11:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:28:58',10001,10010),(40,'[CHANGE] Aqua Silver\'s schedule has changed.','The schedule of Aqua Silver has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Stephen\n                        Duration: 60 min\n                        Date: 2023-09-22 17:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:29:31',10001,0),(41,'[CHANGE] Aqua First\'s schedule has changed.','The schedule of Aqua First has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-08-23 12:00:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:29:41',10001,0),(42,'[CHANGE] Aqua Lite\'s schedule has changed.','The schedule of Aqua Lite has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-08-25 15:00:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:29:54',10001,0),(43,'[CHANGE] Aqua High\'s schedule has changed.','The schedule of Aqua High has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-08-26 09:30:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:30:21',10001,0),(44,'[NEW] Welcome to our new class: Aqua Acme','Please see details below. \n                        Status: Active\n                        Instructor: Michael\n                        Duration: 60 min\n                        Date: 2023-09-17 09:00:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-12 17:32:27',10001,0),(45,'[NEW] Welcome to our new class: Aqua Crest','Please see details below. \n                        Status: Active\n                        Instructor: Sophia\n                        Duration: 60 min\n                        Date: 2023-09-18 07:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 10:27:10',10001,0),(46,'[NEW] Welcome to our new class: Aqua Epic','Please see details below. \n                        Status: Active\n                        Instructor: Karen\n                        Duration: 60 min\n                        Date: 2023-09-19 11:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 12:02:34',10001,0),(47,'[NEW] Welcome to our new class: Aqua Grand','Please see details below. \n                        Status: Active\n                        Instructor: David\n                        Duration: 60 min\n                        Date: 2023-09-20 08:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 12:03:57',10001,0),(48,'[NEW] Welcome to our new class: Aqua Peak','Please see details below. \n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-21 09:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 12:04:35',10001,0),(49,'[NEW] Welcome to our new class: Aqua Fun','Please see details below. \n                        Status: Active\n                        Instructor: Sophia\n                        Duration: 60 min\n                        Date: 2023-09-23 10:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 12:08:52',10001,0),(50,'[CHANGE] Aqua Peak\'s schedule has changed.','The schedule of Aqua Peak has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Maria\n                        Duration: 60 min\n                        Date: 2023-09-18 12:00:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-13 12:16:40',10001,0),(51,'[CHANGE] Aqua Fun\'s schedule has changed.','The schedule of Aqua Fun has been changed. Please check the new details.\n                        Status: Active\n                        Instructor: Sophia\n                        Duration: 60 min\n                        Date: 2023-09-20 12:00:00\n                        Max Capacity: 30\n                        Pool: Hydrotherapy Pool\n                        ','2023-09-13 12:16:54',10001,0),(52,'[NEW] Welcome to our new class: Aqua NewZew','Please see details below. \n                        Status: Active\n                        Instructor: Sophia\n                        Duration: 60 min\n                        Date: 2023-08-03 06:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 14:43:35',10001,0),(53,'[NEW] Welcome to our new class: Aqua Robust','Please see details below. \n                        Status: Active\n                        Instructor: Robert\n                        Duration: 60 min\n                        Date: 2023-09-13 17:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 18:03:49',10001,0),(54,'[NEW] Welcome to our new class: Aqua Weida','Please see details below. \n                        Status: Active\n                        Instructor: Steven\n                        Duration: 60 min\n                        Date: 2023-09-13 20:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 18:06:12',10001,0),(55,'[NEW] Welcome to our new class: Aqua Tmd','Please see details below. \n                        Status: Active\n                        Instructor: Sophia\n                        Duration: 60 min\n                        Date: 2023-09-13 19:00:00\n                        Max Capacity: 30\n                        Pool: Training Pool\n                        ','2023-09-13 18:35:48',10001,0);
/*!40000 ALTER TABLE `news_updates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `payments`
--

DROP TABLE IF EXISTS `payments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `payments` (
  `paymentID` int NOT NULL AUTO_INCREMENT,
  `customerID` int NOT NULL,
  `paymentType` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `paymentTime` datetime NOT NULL,
  PRIMARY KEY (`paymentID`),
  KEY `customerID` (`customerID`),
  CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`customerID`) REFERENCES `memberinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=67 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `payments`
--

LOCK TABLES `payments` WRITE;
/*!40000 ALTER TABLE `payments` DISABLE KEYS */;
INSERT INTO `payments` VALUES (1,10003,1,70.00,'2023-08-23 11:00:00'),(2,10005,1,70.00,'2023-08-25 11:00:00'),(3,10003,2,80.00,'2023-08-23 10:00:00'),(4,10005,2,80.00,'2023-08-25 10:00:00'),(5,10005,2,80.00,'2023-09-12 17:05:05'),(6,10005,2,80.00,'2023-09-12 17:09:45'),(7,10005,2,80.00,'2023-09-12 17:10:23'),(8,10006,1,70.00,'2023-09-12 17:13:50'),(9,10006,1,70.00,'2023-09-12 00:00:00'),(10,10006,2,80.00,'2023-09-12 17:14:51'),(11,10007,1,70.00,'2023-09-12 17:15:33'),(12,10007,1,70.00,'2023-09-12 00:00:00'),(13,10007,2,80.00,'2023-09-12 17:16:28'),(14,10008,1,70.00,'2023-09-12 17:19:12'),(15,10008,1,70.00,'2023-09-12 00:00:00'),(16,10008,2,80.00,'2023-09-12 17:20:03'),(17,10008,2,80.00,'2023-09-12 17:20:31'),(18,10009,1,70.00,'2023-09-12 17:20:55'),(19,10009,2,80.00,'2023-09-12 17:21:49'),(20,10010,1,70.00,'2023-09-12 17:26:15'),(21,10010,2,80.00,'2023-09-12 17:26:58'),(22,10011,1,70.00,'2023-09-12 17:30:48'),(23,10011,1,70.00,'2023-09-12 00:00:00'),(24,10011,2,80.00,'2023-09-12 17:31:23'),(25,10012,1,70.00,'2023-09-12 17:32:43'),(26,10012,2,80.00,'2023-09-12 17:33:31'),(27,10012,2,80.00,'2023-09-12 17:33:58'),(28,10013,1,70.00,'2023-09-12 17:34:32'),(29,10013,1,70.00,'2023-09-12 00:00:00'),(30,10013,2,80.00,'2023-09-12 17:34:58'),(31,10014,1,70.00,'2023-09-12 17:36:28'),(32,10014,1,70.00,'2023-09-12 00:00:00'),(33,10014,2,80.00,'2023-09-12 17:36:54'),(34,10015,1,70.00,'2023-09-12 17:38:08'),(35,10015,1,70.00,'2023-09-12 00:00:00'),(36,10015,2,80.00,'2023-09-12 17:38:38'),(37,10025,1,70.00,'2023-09-13 11:20:38'),(38,10025,1,70.00,'2023-09-13 00:00:00'),(39,10024,1,70.00,'2023-09-13 11:23:08'),(40,10024,1,70.00,'2023-09-13 00:00:00'),(41,10026,1,70.00,'2023-09-13 11:23:32'),(42,10026,2,80.00,'2023-09-13 11:24:49'),(43,10026,2,44.00,'2023-09-13 11:25:36'),(44,10032,1,70.00,'2023-09-13 12:10:17'),(45,10030,1,70.00,'2023-09-13 12:20:01'),(46,10030,1,70.00,'2023-09-13 00:00:00'),(47,10029,1,70.00,'2023-09-13 12:21:51'),(48,10028,1,70.00,'2023-09-13 12:22:45'),(49,10028,2,80.00,'2023-09-13 12:23:47'),(50,10028,2,80.00,'2023-09-13 12:26:12'),(51,10027,1,70.00,'2023-09-13 12:27:20'),(52,10027,1,70.00,'2023-09-13 00:00:00'),(53,10027,2,80.00,'2023-09-13 12:27:51'),(54,10025,2,80.00,'2023-09-13 14:27:25'),(55,10006,2,80.00,'2023-09-13 14:57:52'),(56,10006,2,80.00,'2023-09-13 15:00:32'),(57,10003,2,80.00,'2023-09-13 15:57:47'),(58,10036,1,70.00,'2023-09-13 16:05:02'),(59,10036,1,70.00,'2023-09-13 00:00:00'),(60,10032,1,70.00,'2023-09-13 00:00:00'),(61,10031,1,70.00,'2023-09-13 18:07:18'),(62,10030,2,80.00,'2023-09-13 18:08:38'),(63,10030,2,80.00,'2023-09-13 18:09:02'),(64,10029,2,80.00,'2023-09-13 18:09:56'),(65,10029,2,80.00,'2023-09-13 18:37:26'),(66,10029,2,44.00,'2023-09-13 18:37:47');
/*!40000 ALTER TABLE `payments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pools`
--

DROP TABLE IF EXISTS `pools`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pools` (
  `poolID` int NOT NULL AUTO_INCREMENT,
  `poolType` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`poolID`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pools`
--

LOCK TABLES `pools` WRITE;
/*!40000 ALTER TABLE `pools` DISABLE KEYS */;
INSERT INTO `pools` VALUES (1,'Olympic Pool','Olympic Pool'),(2,'Hydrotherapy Pool','Hydrotherapy Pool'),(3,'Training Pool','Training Pool'),(4,'Family Pool','For family');
/*!40000 ALTER TABLE `pools` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subscriptions`
--

DROP TABLE IF EXISTS `subscriptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subscriptions` (
  `subscriptionID` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `startDate` date NOT NULL,
  `endDate` date NOT NULL,
  PRIMARY KEY (`subscriptionID`),
  KEY `userID` (`userID`),
  CONSTRAINT `subscriptions_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `memberinfo` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=23 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subscriptions`
--

LOCK TABLES `subscriptions` WRITE;
/*!40000 ALTER TABLE `subscriptions` DISABLE KEYS */;
INSERT INTO `subscriptions` VALUES (1,10003,'2023-08-19','2024-08-18'),(2,10005,'2023-08-22','2024-08-21'),(3,10006,'2023-09-12','2023-11-11'),(4,10007,'2023-09-12','2023-11-11'),(5,10008,'2023-09-12','2023-11-11'),(6,10009,'2023-09-12','2023-10-12'),(7,10010,'2023-09-12','2023-10-12'),(8,10011,'2023-09-12','2023-11-11'),(9,10012,'2023-09-12','2023-10-12'),(10,10013,'2023-09-12','2023-11-11'),(11,10014,'2023-09-12','2023-11-11'),(12,10015,'2023-09-12','2023-11-11'),(13,10025,'2023-09-13','2023-11-12'),(14,10024,'2023-09-13','2023-11-12'),(15,10026,'2023-09-13','2023-10-13'),(16,10032,'2023-09-13','2023-11-12'),(17,10030,'2023-09-13','2023-11-12'),(18,10029,'2023-09-13','2023-10-13'),(19,10028,'2023-09-13','2023-10-13'),(20,10027,'2023-09-13','2023-11-12'),(21,10036,'2023-09-13','2023-11-12'),(22,10031,'2023-09-13','2023-10-13');
/*!40000 ALTER TABLE `subscriptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `time_slots`
--

DROP TABLE IF EXISTS `time_slots`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `time_slots` (
  `slotsID` int NOT NULL AUTO_INCREMENT,
  `startTime` time NOT NULL,
  `endTime` time NOT NULL,
  PRIMARY KEY (`slotsID`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `time_slots`
--

LOCK TABLES `time_slots` WRITE;
/*!40000 ALTER TABLE `time_slots` DISABLE KEYS */;
INSERT INTO `time_slots` VALUES (1,'05:00:00','05:15:00'),(2,'05:15:00','05:30:00'),(3,'05:30:00','05:45:00'),(4,'05:45:00','06:00:00'),(5,'06:00:00','06:15:00'),(6,'06:15:00','06:30:00'),(7,'06:30:00','06:45:00'),(8,'06:45:00','07:00:00'),(9,'07:00:00','07:15:00'),(10,'07:15:00','07:30:00'),(11,'07:30:00','07:45:00'),(12,'07:45:00','08:00:00'),(13,'08:00:00','08:15:00'),(14,'08:15:00','08:30:00'),(15,'08:30:00','08:45:00'),(16,'08:45:00','09:00:00'),(17,'09:00:00','09:15:00'),(18,'09:15:00','09:30:00'),(19,'09:30:00','09:45:00'),(20,'09:45:00','10:00:00'),(21,'10:00:00','10:15:00'),(22,'10:15:00','10:30:00'),(23,'10:30:00','10:45:00'),(24,'10:45:00','11:00:00'),(25,'11:00:00','11:15:00'),(26,'11:15:00','11:30:00'),(27,'11:30:00','11:45:00'),(28,'11:45:00','12:00:00'),(29,'12:00:00','12:15:00'),(30,'12:15:00','12:30:00'),(31,'12:30:00','12:45:00'),(32,'12:45:00','13:00:00'),(33,'13:00:00','13:15:00'),(34,'13:15:00','13:30:00'),(35,'13:30:00','13:45:00'),(36,'13:45:00','14:00:00'),(37,'14:00:00','14:15:00'),(38,'14:15:00','14:30:00'),(39,'14:30:00','14:45:00'),(40,'14:45:00','15:00:00'),(41,'15:00:00','15:15:00'),(42,'15:15:00','15:30:00'),(43,'15:30:00','15:45:00'),(44,'15:45:00','16:00:00'),(45,'16:00:00','16:15:00'),(46,'16:15:00','16:30:00'),(47,'16:30:00','16:45:00'),(48,'16:45:00','17:00:00'),(49,'17:00:00','17:15:00'),(50,'17:15:00','17:30:00'),(51,'17:30:00','17:45:00'),(52,'17:45:00','18:00:00'),(53,'18:00:00','18:15:00'),(54,'18:15:00','18:30:00'),(55,'18:30:00','18:45:00'),(56,'18:45:00','19:00:00'),(57,'19:00:00','19:15:00'),(58,'19:15:00','19:30:00'),(59,'19:30:00','19:45:00'),(60,'19:45:00','20:00:00'),(61,'20:00:00','20:15:00'),(62,'20:15:00','20:30:00'),(63,'20:30:00','20:45:00'),(64,'20:45:00','21:00:00'),(65,'21:00:00','21:15:00'),(66,'21:15:00','21:30:00'),(67,'21:30:00','21:45:00'),(68,'21:45:00','22:00:00');
/*!40000 ALTER TABLE `time_slots` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_availability`
--

DROP TABLE IF EXISTS `user_availability`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_availability` (
  `availabilityID` int NOT NULL AUTO_INCREMENT,
  `userID` int NOT NULL,
  `slotsID` int NOT NULL,
  `date` date NOT NULL,
  `availability` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`availabilityID`),
  KEY `userID` (`userID`),
  KEY `slotsID` (`slotsID`),
  CONSTRAINT `user_availability_ibfk_1` FOREIGN KEY (`userID`) REFERENCES `users` (`userID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `user_availability_ibfk_2` FOREIGN KEY (`slotsID`) REFERENCES `time_slots` (`slotsID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=690 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_availability`
--

LOCK TABLES `user_availability` WRITE;
/*!40000 ALTER TABLE `user_availability` DISABLE KEYS */;
INSERT INTO `user_availability` VALUES (1,10002,25,'2023-08-23',0),(2,10002,26,'2023-08-23',0),(3,10002,27,'2023-08-23',0),(4,10002,28,'2023-08-23',0),(9,10002,19,'2023-08-24',0),(10,10002,20,'2023-08-24',0),(11,10002,21,'2023-08-24',0),(12,10002,22,'2023-08-24',0),(21,10002,5,'2023-08-27',0),(22,10002,6,'2023-08-27',0),(23,10002,7,'2023-08-27',0),(24,10002,8,'2023-08-27',0),(33,10005,49,'2023-09-10',0),(34,10005,50,'2023-09-10',0),(35,10005,51,'2023-09-10',0),(36,10005,52,'2023-09-10',0),(37,10002,53,'2023-09-10',0),(38,10002,54,'2023-09-10',0),(39,10002,55,'2023-09-10',0),(40,10002,56,'2023-09-10',0),(45,10005,5,'2023-09-10',0),(46,10005,6,'2023-09-10',0),(47,10005,7,'2023-09-10',0),(48,10005,8,'2023-09-10',0),(53,10005,59,'2023-09-10',0),(54,10005,60,'2023-09-10',0),(55,10005,61,'2023-09-10',0),(56,10005,62,'2023-09-10',0),(81,10002,53,'2023-10-06',0),(82,10002,54,'2023-10-06',0),(83,10002,55,'2023-10-06',0),(84,10002,56,'2023-10-06',0),(85,10002,53,'2023-07-20',0),(86,10002,54,'2023-07-20',0),(87,10002,55,'2023-07-20',0),(88,10002,56,'2023-07-20',0),(89,10002,37,'2023-08-17',0),(90,10002,38,'2023-08-17',0),(91,10002,39,'2023-08-17',0),(92,10002,40,'2023-08-17',0),(105,10005,67,'2023-09-13',0),(106,10005,68,'2023-09-13',0),(126,10005,17,'2023-09-14',0),(127,10005,18,'2023-09-14',0),(128,10005,19,'2023-09-14',0),(129,10005,20,'2023-09-14',0),(130,10017,17,'2023-09-14',0),(131,10017,18,'2023-09-14',0),(132,10017,19,'2023-09-14',0),(133,10017,20,'2023-09-14',0),(134,10005,17,'2023-09-16',0),(135,10005,18,'2023-09-16',0),(136,10004,17,'2023-09-16',0),(137,10004,18,'2023-09-16',0),(138,10005,29,'2023-09-12',0),(139,10005,30,'2023-09-12',0),(140,10005,31,'2023-09-12',0),(141,10005,32,'2023-09-12',0),(142,10018,29,'2023-09-12',0),(143,10018,30,'2023-09-12',0),(144,10018,31,'2023-09-12',0),(145,10018,32,'2023-09-12',0),(146,10016,25,'2023-09-15',0),(147,10016,26,'2023-09-15',0),(148,10016,27,'2023-09-15',0),(149,10016,28,'2023-09-15',0),(150,10019,37,'2023-09-14',0),(151,10019,38,'2023-09-14',0),(152,10004,49,'2023-09-16',0),(153,10004,50,'2023-09-16',0),(154,10004,51,'2023-09-16',0),(155,10004,52,'2023-09-16',0),(156,10006,27,'2023-09-13',0),(157,10006,28,'2023-09-13',0),(158,10006,29,'2023-09-13',0),(159,10006,30,'2023-09-13',0),(160,10006,37,'2023-09-14',0),(161,10006,38,'2023-09-14',0),(162,10006,49,'2023-09-16',0),(163,10006,50,'2023-09-16',0),(164,10006,51,'2023-09-16',0),(165,10006,52,'2023-09-16',0),(166,10006,33,'2023-09-16',0),(167,10006,34,'2023-09-16',0),(168,10006,35,'2023-09-16',0),(169,10006,36,'2023-09-16',0),(170,10017,33,'2023-09-16',0),(171,10017,34,'2023-09-16',0),(172,10017,35,'2023-09-16',0),(173,10017,36,'2023-09-16',0),(174,10007,25,'2023-09-15',0),(175,10007,26,'2023-09-15',0),(176,10007,27,'2023-09-15',0),(177,10007,28,'2023-09-15',0),(178,10007,37,'2023-09-14',0),(179,10007,38,'2023-09-14',0),(180,10007,13,'2023-09-18',0),(181,10007,14,'2023-09-18',0),(182,10007,15,'2023-09-18',0),(183,10007,16,'2023-09-18',0),(184,10020,13,'2023-09-18',0),(185,10020,14,'2023-09-18',0),(186,10020,15,'2023-09-18',0),(187,10020,16,'2023-09-18',0),(188,10008,27,'2023-09-13',0),(189,10008,28,'2023-09-13',0),(190,10008,29,'2023-09-13',0),(191,10008,30,'2023-09-13',0),(192,10008,25,'2023-09-15',0),(193,10008,26,'2023-09-15',0),(194,10008,27,'2023-09-15',0),(195,10008,28,'2023-09-15',0),(196,10008,49,'2023-09-16',0),(197,10008,50,'2023-09-16',0),(198,10008,51,'2023-09-16',0),(199,10008,52,'2023-09-16',0),(200,10008,21,'2023-09-15',0),(201,10008,22,'2023-09-15',0),(202,10008,23,'2023-09-15',0),(203,10008,24,'2023-09-15',0),(204,10002,21,'2023-09-15',0),(205,10002,22,'2023-09-15',0),(206,10002,23,'2023-09-15',0),(207,10002,24,'2023-09-15',0),(208,10008,17,'2023-09-18',0),(209,10008,18,'2023-09-18',0),(210,10008,19,'2023-09-18',0),(211,10008,20,'2023-09-18',0),(212,10019,17,'2023-09-18',0),(213,10019,18,'2023-09-18',0),(214,10019,19,'2023-09-18',0),(215,10019,20,'2023-09-18',0),(216,10009,27,'2023-09-13',0),(217,10009,28,'2023-09-13',0),(218,10009,29,'2023-09-13',0),(219,10009,30,'2023-09-13',0),(220,10009,25,'2023-09-15',0),(221,10009,26,'2023-09-15',0),(222,10009,27,'2023-09-15',0),(223,10009,28,'2023-09-15',0),(224,10009,17,'2023-09-15',0),(225,10009,18,'2023-09-15',0),(226,10009,19,'2023-09-15',0),(227,10009,20,'2023-09-15',0),(228,10020,17,'2023-09-15',0),(229,10020,18,'2023-09-15',0),(230,10020,19,'2023-09-15',0),(231,10020,20,'2023-09-15',0),(232,10010,27,'2023-09-13',0),(233,10010,28,'2023-09-13',0),(234,10010,29,'2023-09-13',0),(235,10010,30,'2023-09-13',0),(236,10010,25,'2023-09-15',0),(237,10010,26,'2023-09-15',0),(238,10010,27,'2023-09-15',0),(239,10010,28,'2023-09-15',0),(240,10010,17,'2023-09-16',0),(241,10010,18,'2023-09-16',0),(242,10010,19,'2023-09-16',0),(243,10010,20,'2023-09-16',0),(244,10018,17,'2023-09-16',0),(245,10018,18,'2023-09-16',0),(246,10018,19,'2023-09-16',0),(247,10018,20,'2023-09-16',0),(248,10002,27,'2023-09-13',0),(249,10002,28,'2023-09-13',0),(250,10002,29,'2023-09-13',0),(251,10002,30,'2023-09-13',0),(252,10004,51,'2023-09-22',0),(253,10004,52,'2023-09-22',0),(254,10004,53,'2023-09-22',0),(255,10004,54,'2023-09-22',0),(256,10002,29,'2023-08-23',0),(257,10002,30,'2023-08-23',0),(258,10002,31,'2023-08-23',0),(259,10002,32,'2023-08-23',0),(260,10002,41,'2023-08-25',0),(261,10002,42,'2023-08-25',0),(262,10002,43,'2023-08-25',0),(263,10002,44,'2023-08-25',0),(264,10002,19,'2023-08-26',0),(265,10002,20,'2023-08-26',0),(266,10002,21,'2023-08-26',0),(267,10002,22,'2023-08-26',0),(268,10011,17,'2023-09-14',0),(269,10011,18,'2023-09-14',0),(270,10011,19,'2023-09-14',0),(271,10011,20,'2023-09-14',0),(272,10016,17,'2023-09-14',0),(273,10016,18,'2023-09-14',0),(274,10016,19,'2023-09-14',0),(275,10016,20,'2023-09-14',0),(276,10011,27,'2023-09-13',0),(277,10011,28,'2023-09-13',0),(278,10011,29,'2023-09-13',0),(279,10011,30,'2023-09-13',0),(280,10011,37,'2023-09-14',0),(281,10011,38,'2023-09-14',0),(282,10016,17,'2023-09-17',0),(283,10016,18,'2023-09-17',0),(284,10016,19,'2023-09-17',0),(285,10016,20,'2023-09-17',0),(286,10012,17,'2023-09-17',0),(287,10012,18,'2023-09-17',0),(288,10012,19,'2023-09-17',0),(289,10012,20,'2023-09-17',0),(290,10012,27,'2023-09-13',0),(291,10012,28,'2023-09-13',0),(292,10012,29,'2023-09-13',0),(293,10012,30,'2023-09-13',0),(294,10012,37,'2023-09-14',0),(295,10012,38,'2023-09-14',0),(296,10012,24,'2023-09-15',0),(297,10012,25,'2023-09-15',0),(298,10012,26,'2023-09-15',0),(299,10012,27,'2023-09-15',0),(300,10017,24,'2023-09-15',0),(301,10017,25,'2023-09-15',0),(302,10017,26,'2023-09-15',0),(303,10017,27,'2023-09-15',0),(304,10012,21,'2023-09-16',0),(305,10012,22,'2023-09-16',0),(306,10019,21,'2023-09-16',0),(307,10019,22,'2023-09-16',0),(308,10013,21,'2023-09-14',0),(309,10013,22,'2023-09-14',0),(310,10013,23,'2023-09-14',0),(311,10013,24,'2023-09-14',0),(312,10018,21,'2023-09-14',0),(313,10018,22,'2023-09-14',0),(314,10018,23,'2023-09-14',0),(315,10018,24,'2023-09-14',0),(316,10013,27,'2023-09-13',0),(317,10013,28,'2023-09-13',0),(318,10013,29,'2023-09-13',0),(319,10013,30,'2023-09-13',0),(320,10013,25,'2023-09-15',0),(321,10013,26,'2023-09-15',0),(322,10013,27,'2023-09-15',0),(323,10013,28,'2023-09-15',0),(324,10013,17,'2023-09-17',0),(325,10013,18,'2023-09-17',0),(326,10013,19,'2023-09-17',0),(327,10013,20,'2023-09-17',0),(328,10013,37,'2023-09-14',0),(329,10013,38,'2023-09-14',0),(330,10014,17,'2023-09-15',0),(331,10014,18,'2023-09-15',0),(332,10014,19,'2023-09-15',0),(333,10014,20,'2023-09-15',0),(334,10019,17,'2023-09-15',0),(335,10019,18,'2023-09-15',0),(336,10019,19,'2023-09-15',0),(337,10019,20,'2023-09-15',0),(338,10014,27,'2023-09-13',0),(339,10014,28,'2023-09-13',0),(340,10014,29,'2023-09-13',0),(341,10014,30,'2023-09-13',0),(342,10014,25,'2023-09-15',0),(343,10014,26,'2023-09-15',0),(344,10014,27,'2023-09-15',0),(345,10014,28,'2023-09-15',0),(346,10014,17,'2023-09-17',0),(347,10014,18,'2023-09-17',0),(348,10014,19,'2023-09-17',0),(349,10014,20,'2023-09-17',0),(350,10014,49,'2023-09-16',0),(351,10014,50,'2023-09-16',0),(352,10014,51,'2023-09-16',0),(353,10014,52,'2023-09-16',0),(354,10015,17,'2023-09-17',0),(355,10015,18,'2023-09-17',0),(356,10015,19,'2023-09-17',0),(357,10015,20,'2023-09-17',0),(358,10020,17,'2023-09-17',0),(359,10020,18,'2023-09-17',0),(360,10020,19,'2023-09-17',0),(361,10020,20,'2023-09-17',0),(362,10015,25,'2023-09-15',0),(363,10015,26,'2023-09-15',0),(364,10015,27,'2023-09-15',0),(365,10015,28,'2023-09-15',0),(366,10015,27,'2023-09-13',0),(367,10015,28,'2023-09-13',0),(368,10015,29,'2023-09-13',0),(369,10015,30,'2023-09-13',0),(370,10015,49,'2023-09-16',0),(371,10015,50,'2023-09-16',0),(372,10015,51,'2023-09-16',0),(373,10015,52,'2023-09-16',0),(374,10003,17,'2023-09-17',0),(375,10003,18,'2023-09-17',0),(376,10003,19,'2023-09-17',0),(377,10003,20,'2023-09-17',0),(378,10003,25,'2023-09-15',0),(379,10003,26,'2023-09-15',0),(380,10003,27,'2023-09-15',0),(381,10003,28,'2023-09-15',0),(382,10003,49,'2023-09-16',0),(383,10003,50,'2023-09-16',0),(384,10003,51,'2023-09-16',0),(385,10003,52,'2023-09-16',0),(386,10017,9,'2023-09-18',0),(387,10017,10,'2023-09-18',0),(388,10017,11,'2023-09-18',0),(389,10017,12,'2023-09-18',0),(390,10003,9,'2023-09-18',0),(391,10003,10,'2023-09-18',0),(392,10003,11,'2023-09-18',0),(393,10003,12,'2023-09-18',0),(394,10026,9,'2023-09-18',0),(395,10026,10,'2023-09-18',0),(396,10026,11,'2023-09-18',0),(397,10026,12,'2023-09-18',0),(398,10026,17,'2023-09-17',0),(399,10026,18,'2023-09-17',0),(400,10026,19,'2023-09-17',0),(401,10026,20,'2023-09-17',0),(402,10026,25,'2023-09-17',0),(403,10026,26,'2023-09-17',0),(404,10026,27,'2023-09-17',0),(405,10026,28,'2023-09-17',0),(406,10022,25,'2023-09-17',0),(407,10022,26,'2023-09-17',0),(408,10022,27,'2023-09-17',0),(409,10022,28,'2023-09-17',0),(410,10026,21,'2023-09-19',0),(411,10026,22,'2023-09-19',0),(412,10021,21,'2023-09-19',0),(413,10021,22,'2023-09-19',0),(414,10023,25,'2023-09-19',0),(415,10023,26,'2023-09-19',0),(416,10023,27,'2023-09-19',0),(417,10023,28,'2023-09-19',0),(418,10019,13,'2023-09-20',0),(419,10019,14,'2023-09-20',0),(420,10019,15,'2023-09-20',0),(421,10019,16,'2023-09-20',0),(430,10032,9,'2023-09-18',0),(431,10032,10,'2023-09-18',0),(432,10032,11,'2023-09-18',0),(433,10032,12,'2023-09-18',0),(434,10032,25,'2023-09-19',0),(435,10032,26,'2023-09-19',0),(436,10032,27,'2023-09-19',0),(437,10032,28,'2023-09-19',0),(438,10032,25,'2023-09-15',0),(439,10032,26,'2023-09-15',0),(440,10032,27,'2023-09-15',0),(441,10032,28,'2023-09-15',0),(442,10032,49,'2023-09-16',0),(443,10032,50,'2023-09-16',0),(444,10032,51,'2023-09-16',0),(445,10032,52,'2023-09-16',0),(446,10002,29,'2023-09-18',0),(447,10002,30,'2023-09-18',0),(448,10002,31,'2023-09-18',0),(449,10002,32,'2023-09-18',0),(450,10017,29,'2023-09-20',0),(451,10017,30,'2023-09-20',0),(452,10017,31,'2023-09-20',0),(453,10017,32,'2023-09-20',0),(454,10030,9,'2023-09-18',0),(455,10030,10,'2023-09-18',0),(456,10030,11,'2023-09-18',0),(457,10030,12,'2023-09-18',0),(458,10030,25,'2023-09-19',0),(459,10030,26,'2023-09-19',0),(460,10030,27,'2023-09-19',0),(461,10030,28,'2023-09-19',0),(462,10030,49,'2023-09-16',0),(463,10030,50,'2023-09-16',0),(464,10030,51,'2023-09-16',0),(465,10030,52,'2023-09-16',0),(466,10030,17,'2023-09-17',0),(467,10030,18,'2023-09-17',0),(468,10030,19,'2023-09-17',0),(469,10030,20,'2023-09-17',0),(470,10029,9,'2023-09-18',0),(471,10029,10,'2023-09-18',0),(472,10029,11,'2023-09-18',0),(473,10029,12,'2023-09-18',0),(474,10029,25,'2023-09-19',0),(475,10029,26,'2023-09-19',0),(476,10029,27,'2023-09-19',0),(477,10029,28,'2023-09-19',0),(478,10029,17,'2023-09-17',0),(479,10029,18,'2023-09-17',0),(480,10029,19,'2023-09-17',0),(481,10029,20,'2023-09-17',0),(482,10029,49,'2023-09-16',0),(483,10029,50,'2023-09-16',0),(484,10029,51,'2023-09-16',0),(485,10029,52,'2023-09-16',0),(486,10028,9,'2023-09-18',0),(487,10028,10,'2023-09-18',0),(488,10028,11,'2023-09-18',0),(489,10028,12,'2023-09-18',0),(490,10028,25,'2023-09-19',0),(491,10028,26,'2023-09-19',0),(492,10028,27,'2023-09-19',0),(493,10028,28,'2023-09-19',0),(494,10028,49,'2023-09-16',0),(495,10028,50,'2023-09-16',0),(496,10028,51,'2023-09-16',0),(497,10028,52,'2023-09-16',0),(498,10028,25,'2023-09-15',0),(499,10028,26,'2023-09-15',0),(500,10028,27,'2023-09-15',0),(501,10028,28,'2023-09-15',0),(502,10028,17,'2023-09-16',0),(503,10028,18,'2023-09-16',0),(504,10028,19,'2023-09-16',0),(505,10028,20,'2023-09-16',0),(506,10022,17,'2023-09-16',0),(507,10022,18,'2023-09-16',0),(508,10022,19,'2023-09-16',0),(509,10022,20,'2023-09-16',0),(510,10028,19,'2023-09-14',0),(511,10028,20,'2023-09-14',0),(512,10028,21,'2023-09-14',0),(513,10028,22,'2023-09-14',0),(514,10022,19,'2023-09-14',0),(515,10022,20,'2023-09-14',0),(516,10022,21,'2023-09-14',0),(517,10022,22,'2023-09-14',0),(518,10028,17,'2023-09-17',0),(519,10028,18,'2023-09-17',0),(520,10028,19,'2023-09-17',0),(521,10028,20,'2023-09-17',0),(522,10028,37,'2023-09-14',0),(523,10028,38,'2023-09-14',0),(524,10027,17,'2023-09-18',0),(525,10027,18,'2023-09-18',0),(526,10027,19,'2023-09-18',0),(527,10027,20,'2023-09-18',0),(528,10021,17,'2023-09-18',0),(529,10021,18,'2023-09-18',0),(530,10021,19,'2023-09-18',0),(531,10021,20,'2023-09-18',0),(532,10027,9,'2023-09-18',0),(533,10027,10,'2023-09-18',0),(534,10027,11,'2023-09-18',0),(535,10027,12,'2023-09-18',0),(536,10027,17,'2023-09-17',0),(537,10027,18,'2023-09-17',0),(538,10027,19,'2023-09-17',0),(539,10027,20,'2023-09-17',0),(540,10027,25,'2023-09-19',0),(541,10027,26,'2023-09-19',0),(542,10027,27,'2023-09-19',0),(543,10027,28,'2023-09-19',0),(544,10027,25,'2023-09-15',0),(545,10027,26,'2023-09-15',0),(546,10027,27,'2023-09-15',0),(547,10027,28,'2023-09-15',0),(548,10027,37,'2023-09-14',0),(549,10027,38,'2023-09-14',0),(550,10025,41,'2023-09-17',0),(551,10025,42,'2023-09-17',0),(552,10025,43,'2023-09-17',0),(553,10025,44,'2023-09-17',0),(554,10002,41,'2023-09-17',0),(555,10002,42,'2023-09-17',0),(556,10002,43,'2023-09-17',0),(557,10002,44,'2023-09-17',0),(558,10017,5,'2023-08-03',0),(559,10017,6,'2023-08-03',0),(560,10017,7,'2023-08-03',0),(561,10017,8,'2023-08-03',0),(562,10010,25,'2023-09-19',0),(563,10010,26,'2023-09-19',0),(564,10010,27,'2023-09-19',0),(565,10010,28,'2023-09-19',0),(566,10010,29,'2023-09-18',0),(567,10010,30,'2023-09-18',0),(568,10010,31,'2023-09-18',0),(569,10010,32,'2023-09-18',0),(570,10010,37,'2023-09-14',0),(571,10010,38,'2023-09-14',0),(572,10006,19,'2023-09-18',0),(573,10006,20,'2023-09-18',0),(574,10006,21,'2023-09-18',0),(575,10006,22,'2023-09-18',0),(576,10018,19,'2023-09-18',0),(577,10018,20,'2023-09-18',0),(578,10018,21,'2023-09-18',0),(579,10018,22,'2023-09-18',0),(580,10006,13,'2023-09-17',0),(581,10006,14,'2023-09-17',0),(582,10006,15,'2023-09-17',0),(583,10006,16,'2023-09-17',0),(584,10018,13,'2023-09-17',0),(585,10018,14,'2023-09-17',0),(586,10018,15,'2023-09-17',0),(587,10018,16,'2023-09-17',0),(588,10003,17,'2023-09-14',0),(589,10003,18,'2023-09-14',0),(590,10003,19,'2023-09-14',0),(591,10003,20,'2023-09-14',0),(592,10018,17,'2023-09-14',0),(593,10018,18,'2023-09-14',0),(594,10018,19,'2023-09-14',0),(595,10018,20,'2023-09-14',0),(596,10003,37,'2023-09-14',0),(597,10003,38,'2023-09-14',0),(598,10018,49,'2023-09-13',0),(599,10018,50,'2023-09-13',0),(600,10018,51,'2023-09-13',0),(601,10018,52,'2023-09-13',0),(602,10035,61,'2023-09-13',0),(603,10035,62,'2023-09-13',0),(604,10035,63,'2023-09-13',0),(605,10035,64,'2023-09-13',0),(606,10036,61,'2023-09-13',0),(607,10036,62,'2023-09-13',0),(608,10036,63,'2023-09-13',0),(609,10036,64,'2023-09-13',0),(610,10032,61,'2023-09-13',0),(611,10032,62,'2023-09-13',0),(612,10032,63,'2023-09-13',0),(613,10032,64,'2023-09-13',0),(614,10031,61,'2023-09-13',0),(615,10031,62,'2023-09-13',0),(616,10031,63,'2023-09-13',0),(617,10031,64,'2023-09-13',0),(618,10031,9,'2023-09-18',0),(619,10031,10,'2023-09-18',0),(620,10031,11,'2023-09-18',0),(621,10031,12,'2023-09-18',0),(622,10031,25,'2023-09-15',0),(623,10031,26,'2023-09-15',0),(624,10031,27,'2023-09-15',0),(625,10031,28,'2023-09-15',0),(626,10031,49,'2023-09-16',0),(627,10031,50,'2023-09-16',0),(628,10031,51,'2023-09-16',0),(629,10031,52,'2023-09-16',0),(630,10030,61,'2023-09-13',0),(631,10030,62,'2023-09-13',0),(632,10030,63,'2023-09-13',0),(633,10030,64,'2023-09-13',0),(634,10030,37,'2023-09-14',0),(635,10030,38,'2023-09-14',0),(636,10030,17,'2023-09-18',0),(637,10030,18,'2023-09-18',0),(638,10030,19,'2023-09-18',0),(639,10030,20,'2023-09-18',0),(640,10017,17,'2023-09-18',0),(641,10017,18,'2023-09-18',0),(642,10017,19,'2023-09-18',0),(643,10017,20,'2023-09-18',0),(644,10030,49,'2023-09-13',0),(645,10030,50,'2023-09-13',0),(646,10030,51,'2023-09-13',0),(647,10030,52,'2023-09-13',0),(648,10004,49,'2023-09-13',0),(649,10004,50,'2023-09-13',0),(650,10004,51,'2023-09-13',0),(651,10004,52,'2023-09-13',0),(652,10029,37,'2023-09-14',0),(653,10029,38,'2023-09-14',0),(654,10029,61,'2023-09-13',0),(655,10029,62,'2023-09-13',0),(656,10029,63,'2023-09-13',0),(657,10029,64,'2023-09-13',0),(658,10029,33,'2023-09-14',0),(659,10029,34,'2023-09-14',0),(660,10029,35,'2023-09-14',0),(661,10029,36,'2023-09-14',0),(662,10017,33,'2023-09-14',0),(663,10017,34,'2023-09-14',0),(664,10017,35,'2023-09-14',0),(665,10017,36,'2023-09-14',0),(666,10029,25,'2023-09-15',0),(667,10029,26,'2023-09-15',0),(668,10029,27,'2023-09-15',0),(669,10029,28,'2023-09-15',0),(670,10017,57,'2023-09-13',0),(671,10017,58,'2023-09-13',0),(672,10017,59,'2023-09-13',0),(673,10017,60,'2023-09-13',0),(674,10029,57,'2023-09-13',0),(675,10029,58,'2023-09-13',0),(676,10029,59,'2023-09-13',0),(677,10029,60,'2023-09-13',0),(678,10029,45,'2023-09-13',0),(679,10029,46,'2023-09-13',0),(680,10029,47,'2023-09-13',0),(681,10029,48,'2023-09-13',0),(682,10004,45,'2023-09-13',0),(683,10004,46,'2023-09-13',0),(684,10004,47,'2023-09-13',0),(685,10004,48,'2023-09-13',0),(686,10029,13,'2023-09-13',0),(687,10029,14,'2023-09-13',0),(688,10004,13,'2023-09-13',0),(689,10004,14,'2023-09-13',0);
/*!40000 ALTER TABLE `user_availability` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `userID` int NOT NULL AUTO_INCREMENT,
  `userPermission` int NOT NULL,
  `userName` varchar(80) NOT NULL,
  `userPassword` varchar(80) NOT NULL,
  `userActive` tinyint(1) NOT NULL DEFAULT '1',
  PRIMARY KEY (`userID`)
) ENGINE=InnoDB AUTO_INCREMENT=10037 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (10001,1,'adminPool1','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10002,2,'instructorPool1','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10003,3,'customerPool1','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10004,2,'Stephen','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10005,3,'AliceWhite','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10006,3,'JamesSmith','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10007,3,'WilliamJohn','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10008,3,'JohnBrown','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10009,3,'RobertDav','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10010,3,'LindaClark','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10011,3,'Patreeee','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10012,3,'Elizabeth','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10013,3,'SusanWak','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10014,3,'Jessie','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10015,3,'SaraSara','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10016,2,'MichaelBR','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10017,2,'SophiaLee','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10018,2,'RobertDavis','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10019,2,'DavidGarcia','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10020,2,'EmilyJohns','$2b$12$gJ3wlX6SdOYOx0k./7zdJ.dLzu9a6fQ5beTQVLf4bwBGHv7.cGY36',1),(10021,2,'xugut','$2b$12$/Aw9korptDCoqYEbtYAvSOxub1OVKWLmI137j0yXfenZcrDgjEXvK',1),(10022,2,'dynvq','$2b$12$WtWArgcG0CJkESQukDfmLe.NvKyLr8Gm2nH2M9NorsGbDGbSIUaIO',1),(10023,2,'ekygk','$2b$12$0H3nWyXiNgG.rqHWjL1lpuib3nGOflvn3u3ouDLmsihnYaQ.bEVCC',1),(10024,3,'boplb','$2b$12$5vQakXni7FmFy9OdffU1B.fkkT5hgokWMUOkfI7pmKF6/UDDYyy6W',1),(10025,3,'kfhpz','$2b$12$rf2AryKkL1cPH4Up8HLEsu8U5DWscaHCdSZMuKNLAJlL8oawYVa6C',1),(10026,3,'qrkqz','$2b$12$yX9GIBW2LqHPrwkyz./hae2szn02mKcVhUBJgQvGL9obFLp0nWA56',1),(10027,3,'vatoh','$2b$12$fGNzkkFaRb7X2g/prxNSDODMpJlnCvevuv.peTSxsUD6kk3zNX68W',1),(10028,3,'gcqdx','$2b$12$Gcmxc6P4iTFB.iYF1xY.HuKp7b8JbEiKTy4CDCb.U14GECc1VoUmK',1),(10029,3,'hxkqk','$2b$12$viJifcpBVriVDfhJyly38uGiakciKx2PE.2Hd/dp9dxBeNgRgPs52',1),(10030,3,'zagmn','$2b$12$WV.TkORNkpEAq33cJyGvjuvkG/vBnnlhiiHZBXER8p/T53L8BVvbO',1),(10031,3,'moftc','$2b$12$VzEt0qVsi60Iw4M2zCjW9.fudT.mcqpV8RXMw8gNi96F1RUTKgOTa',1),(10032,3,'sooxy','$2b$12$sPXs2SmSsm.j/10X5v2O5eWgiWgYgmTSaoOl8WEUUHhFFHigDw/4y',1),(10033,2,'ijbig','$2b$12$Q8xjuKGPqVrdHRkt8RMa3OPTiu86Wr6ll3e2W8NSOnTgzLNedbiwy',1),(10034,2,'vknrk','$2b$12$CnStSfkHloXF/58WPh.SV.sRfYMy9v2rnz64PgBoI/3OWNAGvrzMG',1),(10035,2,'rxgin','$2b$12$IOLe2byDqA5ZP.0oHmorQuXS23a18VIfexjHzBmPyEGUclStOkrp2',1),(10036,3,'JamesJohn','$2b$12$qSFebN9EgaxP6Twos2ePHeQC8ycCSKzTkzTqFB9W3Cu7gcRjiut9W',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-09-13 20:20:26