-- MySQL dump 10.13  Distrib 8.0.35, for Win64 (x86_64)
--
-- Host: localhost    Database: forex
-- ------------------------------------------------------
-- Server version	8.0.35

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auto_change_riskfree_level`
--

DROP TABLE IF EXISTS `auto_change_riskfree_level`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auto_change_riskfree_level` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `ticket` int unsigned NOT NULL,
  `type_of_autochange` varchar(45) NOT NULL,
  `amount` float NOT NULL,
  `new_riskfree_level` float NOT NULL,
  `new_money_involved` float NOT NULL,
  `time` datetime NOT NULL,
  `achieve` enum('yes','no','close','stop') NOT NULL DEFAULT 'no',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auto_change_riskfree_level`
--

LOCK TABLES `auto_change_riskfree_level` WRITE;
/*!40000 ALTER TABLE `auto_change_riskfree_level` DISABLE KEYS */;
/*!40000 ALTER TABLE `auto_change_riskfree_level` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `inputs`
--

DROP TABLE IF EXISTS `inputs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `inputs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `input_type` varchar(255) NOT NULL,
  `value` varchar(255) DEFAULT NULL,
  `time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `inputs_id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `inputs`
--

LOCK TABLES `inputs` WRITE;
/*!40000 ALTER TABLE `inputs` DISABLE KEYS */;
/*!40000 ALTER TABLE `inputs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loss_money`
--

DROP TABLE IF EXISTS `loss_money`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loss_money` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `amount` float unsigned NOT NULL,
  `management_level` int unsigned NOT NULL,
  `parameters` varchar(200) NOT NULL,
  `ticket` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loss_money`
--

LOCK TABLES `loss_money` WRITE;
/*!40000 ALTER TABLE `loss_money` DISABLE KEYS */;
/*!40000 ALTER TABLE `loss_money` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `main_trend_positions`
--

DROP TABLE IF EXISTS `main_trend_positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_trend_positions` (
  `ticket` bigint unsigned NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `main_trend` enum('bullish','bearish') NOT NULL,
  `management_level` int NOT NULL,
  `fix_price` float unsigned NOT NULL,
  `volume` float unsigned NOT NULL,
  `pip_part` int unsigned NOT NULL,
  `zone` int unsigned NOT NULL,
  `riskfree_wait` int unsigned NOT NULL DEFAULT '6',
  `riskfree_level` float unsigned NOT NULL,
  `time` datetime NOT NULL,
  `magic` bigint unsigned DEFAULT NULL,
  `loss_level` float unsigned DEFAULT NULL,
  `money_involved` float NOT NULL,
  `spread` int unsigned NOT NULL,
  `number_auto_change_riskfree` int unsigned DEFAULT '0',
  `sum_loss` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`ticket`),
  UNIQUE KEY `ticket_UNIQUE` (`ticket`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_trend_positions`
--

LOCK TABLES `main_trend_positions` WRITE;
/*!40000 ALTER TABLE `main_trend_positions` DISABLE KEYS */;
/*!40000 ALTER TABLE `main_trend_positions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `no_loss_money`
--

DROP TABLE IF EXISTS `no_loss_money`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `no_loss_money` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `amount` float unsigned NOT NULL,
  `management_level` int unsigned NOT NULL,
  `parameters` varchar(200) NOT NULL,
  `ticket` int unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `no_loss_money`
--

LOCK TABLES `no_loss_money` WRITE;
/*!40000 ALTER TABLE `no_loss_money` DISABLE KEYS */;
/*!40000 ALTER TABLE `no_loss_money` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `program_log`
--

DROP TABLE IF EXISTS `program_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `program_log` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `log` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `program_log`
--

LOCK TABLES `program_log` WRITE;
/*!40000 ALTER TABLE `program_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `program_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `riskfree_positions`
--

DROP TABLE IF EXISTS `riskfree_positions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `riskfree_positions` (
  `ticket` bigint unsigned NOT NULL,
  `main_pos_ticket` bigint unsigned NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `main_trend` enum('bullish','bearish') NOT NULL,
  `management_level` int NOT NULL,
  `fix_price` float unsigned NOT NULL,
  `volume` float unsigned NOT NULL,
  `pip_part` int unsigned NOT NULL,
  `zone` int unsigned NOT NULL,
  `riskfree_wait` int unsigned NOT NULL DEFAULT '6',
  `riskfree_level` float unsigned NOT NULL,
  `time` datetime NOT NULL,
  `spread` int unsigned NOT NULL,
  `magic` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`ticket`),
  UNIQUE KEY `main_pos_ticket_UNIQUE` (`main_pos_ticket`),
  UNIQUE KEY `ticket_UNIQUE` (`ticket`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `riskfree_positions`
--

LOCK TABLES `riskfree_positions` WRITE;
/*!40000 ALTER TABLE `riskfree_positions` DISABLE KEYS */;
/*!40000 ALTER TABLE `riskfree_positions` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-02-28 15:33:44
