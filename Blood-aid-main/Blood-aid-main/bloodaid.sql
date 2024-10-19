-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: bloodaid
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `blood_stock`
--
DROP Database bloodaid;
CREATE Database bloodaid;
USE database bloodaid;
DROP TABLE IF EXISTS `blood_stock`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `blood_stock` (
  `bloodgroup` varchar(5) NOT NULL,
  `units` int DEFAULT NULL,
  PRIMARY KEY (`bloodgroup`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `blood_stock`
--

LOCK TABLES `blood_stock` WRITE;
/*!40000 ALTER TABLE `blood_stock` DISABLE KEYS */;
INSERT INTO `blood_stock` VALUES ('A-',200),('A+',100),('AB-',100),('AB+',0),('B-',0),('B+',0),('O-',0),('O+',0);
/*!40000 ALTER TABLE `blood_stock` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donation`
--

DROP TABLE IF EXISTS `donation`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donation` (
  `donation_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `units` double DEFAULT NULL,
  `donated_date` date DEFAULT NULL,
  `disease` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`donation_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `donation_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donation`
--

LOCK TABLES `donation` WRITE;
/*!40000 ALTER TABLE `donation` DISABLE KEYS */;
INSERT INTO `donation` VALUES (1,1,100,'2024-05-04','none','pending'),(2,1,200,'2014-06-09','none','accept'),(3,2,111,'2015-09-09','none','reject');
/*!40000 ALTER TABLE `donation` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `donor_details`
--

DROP TABLE IF EXISTS `donor_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `donor_details` (
  `username` varchar(50) NOT NULL,
  `bloodgroup` varchar(10) DEFAULT NULL,
  `units` int NOT NULL,
  `disease` varchar(30) DEFAULT NULL,
  `age` int NOT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  `password` varchar(45) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `donor_details`
--

LOCK TABLES `donor_details` WRITE;
/*!40000 ALTER TABLE `donor_details` DISABLE KEYS */;
INSERT INTO `donor_details` VALUES ('anusha','A+',100,'none',27,'Accepted',''),('jayadeep','A+',10,'none',23,'Pending','password'),('john','A-',100,'none',20,'Pending','abc'),('poojitha','AB-',100,'none',23,'Accepted',''),('ravi','A-',100,'none',47,'Accepted',''),('rerfedf','A+',122,'wwdwq',34,'Pending','');
/*!40000 ALTER TABLE `donor_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient_request`
--

DROP TABLE IF EXISTS `patient_request`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient_request` (
  `request_id` int NOT NULL,
  `user_id` int DEFAULT NULL,
  `units` double DEFAULT NULL,
  `requested_date` date DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`request_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `patient_request_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient_request`
--

LOCK TABLES `patient_request` WRITE;
/*!40000 ALTER TABLE `patient_request` DISABLE KEYS */;
/*!40000 ALTER TABLE `patient_request` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patients_details`
--

DROP TABLE IF EXISTS `patients_details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patients_details` (
  `username` varchar(50) NOT NULL,
  `age` int NOT NULL,
  `bloodgroup` varchar(10) DEFAULT NULL,
  `reason` varchar(255) DEFAULT NULL,
  `units` int DEFAULT NULL,
  `status` varchar(20) DEFAULT 'Pending',
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patients_details`
--

LOCK TABLES `patients_details` WRITE;
/*!40000 ALTER TABLE `patients_details` DISABLE KEYS */;
INSERT INTO `patients_details` VALUES ('jayadeep',25,'A-','cancer',100,'Accepted');
/*!40000 ALTER TABLE `patients_details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `role`
--

DROP TABLE IF EXISTS `role`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `role` (
  `role_id` int NOT NULL,
  `role_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`role_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `role`
--

LOCK TABLES `role` WRITE;
/*!40000 ALTER TABLE `role` DISABLE KEYS */;
INSERT INTO `role` VALUES (1,'admin'),(2,'user');
/*!40000 ALTER TABLE `role` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `phone_number` varchar(255) DEFAULT NULL,
  `blood_group` varchar(255) DEFAULT NULL,
  `dob` date DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `city` varchar(255) DEFAULT NULL,
  `state` varchar(255) DEFAULT NULL,
  `pin_code` varchar(255) DEFAULT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  KEY `role_id` (`role_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `role` (`role_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (1,'jay','123','1232344','A+','2013-01-01','EFR','WEF','DR','123234',2),(2,'admin','123','1222222','B-','2014-05-04','frf','dds','dsd','123123',1);
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'bloodaid'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-08-07  0:42:19
