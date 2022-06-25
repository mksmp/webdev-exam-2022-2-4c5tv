-- MySQL dump 10.13  Distrib 8.0.29, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_1655_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

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
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('47468863e619');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_collection`
--

DROP TABLE IF EXISTS `book_collection`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_collection` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `collection_id` int(11) DEFAULT NULL,
  `book_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_book_collection_book_id_books` (`book_id`),
  KEY `fk_book_collection_collection_id_collections` (`collection_id`),
  CONSTRAINT `fk_book_collection_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_book_collection_collection_id_collections` FOREIGN KEY (`collection_id`) REFERENCES `collections` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_collection`
--

LOCK TABLES `book_collection` WRITE;
/*!40000 ALTER TABLE `book_collection` DISABLE KEYS */;
INSERT INTO `book_collection` VALUES (4,2,22),(5,2,28),(6,2,27),(7,3,23),(8,2,23),(9,5,28),(10,5,22);
/*!40000 ALTER TABLE `book_collection` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_genre`
--

DROP TABLE IF EXISTS `book_genre`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) DEFAULT NULL,
  `genre_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_book_genre_book_id_books` (`book_id`),
  KEY `fk_book_genre_genre_id_genres` (`genre_id`),
  CONSTRAINT `fk_book_genre_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_book_genre_genre_id_genres` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=68 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_genre`
--

LOCK TABLES `book_genre` WRITE;
/*!40000 ALTER TABLE `book_genre` DISABLE KEYS */;
INSERT INTO `book_genre` VALUES (34,23,6),(35,23,2),(36,23,8),(37,22,6),(38,22,5),(39,22,10),(40,22,9),(60,28,5),(61,28,3),(62,28,10),(63,28,9),(64,27,10);
/*!40000 ALTER TABLE `book_genre` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `short_desc` text NOT NULL,
  `rating_sum` int(11) NOT NULL,
  `rating_num` int(11) NOT NULL,
  `year` year(4) NOT NULL,
  `publisher` varchar(100) NOT NULL,
  `author` varchar(100) NOT NULL,
  `vol_pages` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=35 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (22,'Linux глазами хакера. 4-е изд.','Рассмотрены вопросы настройки ОС Linux на максимальную производительность и безопасность. Описано базовое администрирование и управление доступом, настройка Firewall, файлообменный сервер, WEB-, FTP- и Proxy-сервера, программы для доставки электронной почты, службы DNS, а также политика мониторинга системы и архивирование данных. Приведены потенциальные уязвимости, даны рекомендации по предотвращению возможных атак и показано, как действовать при атаке или взломе системы, чтобы максимально быстро восстановить ее работоспособность и предотвратить потерю данных. Операционная система Linux динамична и меняется постоянно, поэтому в четвертом издании некоторые главы полностью переписаны или дополнены новой информацией. На сайте издательства размещены дополнительная документация и программы в исходных кодах.',14,5,2021,'БХВ-Петербург','Фленов Михаил Евгеньевич',300),(23,'Bash и кибербезопасность: атака, защита и анализ из командной строки Linux','Командная строка может стать идеальным инструментом для обеспечения кибербезопасности. Невероятная гибкость и абсолютная доступность превращают стандартный интерфейс командной строки (CLI) в фундаментальное решение, если у вас есть соответствующий опыт.\nАвторы Пол Тронкон и Карл Олбинг рассказывают об инструментах и хитростях командной строки, помогающих собирать данные при упреждающей защите, анализировать логи и отслеживать состояние сетей. Пентестеры узнают, как проводить атаки, используя колоссальный функционал, встроенный практически в любую версию Linux.',0,0,2022,'Питер','Тронкон Пол, Олбинг Карл',250),(27,'Ядро Linux','В книге обсуждается большинство структур данных, алгоритмы и приемы программирования, применяемые в ядре, излагается подробная информация о строении современной операционной системы. Рассматривается управление памятью, в том числе буферизация файлов, выгрузка процессов и прямой доступ к памяти (DMA); виртуальная файловая система, Ext2 и Ext3, создание процессов и планирование их выполнения, сигналы, прерывания и важнейшие интерфейсы драйверов устройств, хронометрирование, синхронизация внутри ядра, межпроцессорное взаимодействие (IPC), выполнение программ. Приводится построчный комментарий соответствующих фрагментов кода. Материал книги базируется на версии ядра 2.6. Для системных администраторов и программистов.',8,2,2002,'БХВ-Петербург','Д. Бовет, М. Чезати',342),(28,'Безопасность Linux. Руководство администратора по системам защиты с открытым исходным кодом','В книге рассказывается об инсталляции, конфигурировании и сопровождении **Linux**-систем с точки зрения безопасности. Это руководство администратора по реализации стратегии защиты **Linux**, а также по утилитам защиты, существующим в **Linux**. Книга не претендует на исчерпывающее описание темы компьютерной безопасности, но в тоже время является хорошей отправной точкой к построению и сопровождению защищенных систем. Придерживаясь описанных в книге процедур и правил, читатели снизят общий уровень уязвимости своих систем и научатся перекрывать наиболее опасные бреши в системной и сетевой защите. *Книга предназначена для пользователей средней и высокой квалификации*.\n',5,1,2003,'Вильямс','Скотт Манн, Эллен Митчелл, Митчелл Крелл',351);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `collections`
--

DROP TABLE IF EXISTS `collections`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `collections` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_collections_user_id_users` (`user_id`),
  CONSTRAINT `fk_collections_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `collections`
--

LOCK TABLES `collections` WRITE;
/*!40000 ALTER TABLE `collections` DISABLE KEYS */;
INSERT INTO `collections` VALUES (1,'абоба',3),(2,'test test',4),(3,'test1 test1',4),(4,'test2 test2',4),(5,'вавапавп',7);
/*!40000 ALTER TABLE `collections` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (1,'Бизнес-книги'),(6,'Детективы'),(5,'Детские книги'),(3,'Зарубежная литература'),(2,'Классическая литература'),(10,'Приключения'),(4,'Русская литература'),(9,'Современная проза'),(8,'Фантастика'),(7,'Фэнтези');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `images`
--

DROP TABLE IF EXISTS `images`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `images` (
  `id` varchar(100) NOT NULL,
  `file_name` varchar(100) NOT NULL,
  `mime_type` varchar(100) NOT NULL,
  `md5_hash` varchar(100) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_images_md5_hash` (`md5_hash`),
  KEY `fk_images_book_id_books` (`book_id`),
  CONSTRAINT `fk_images_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `images`
--

LOCK TABLES `images` WRITE;
/*!40000 ALTER TABLE `images` DISABLE KEYS */;
INSERT INTO `images` VALUES ('0fb069fb-1ff8-4373-865f-2ab6fe60d6bc','11936281-1.jpg','image/jpeg','6712b6ceee37c67c284bfa211529ee3e','2022-06-23 14:58:02',23),('85cb7850-5834-4c99-b11d-190e130124d7','Bezopasnost_Linux._Rukovodstvo_administratora_po_sistemam_zaschity_s_otkrytym_is.jpg','image/jpeg','73d04aff56cc5a46e0e289bc4f5d2029','2022-06-24 15:15:41',28),('cc854961-4d6c-4046-af6f-62c393bb435b','978597753333.jpg','image/jpeg','41c6b2ff949cae82215056f372dc8aac','2022-06-23 14:57:09',22),('eb4c50f0-5155-463d-a86c-5395bc71661b','91OK4D97mVL._AC_UL960_QL65_.jpg','image/jpeg','e6071e315a097f03816eceb7caa3f923','2022-06-24 02:18:01',27);
/*!40000 ALTER TABLE `images` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `book_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book_id_books` (`book_id`),
  KEY `fk_reviews_user_id_users` (`user_id`),
  CONSTRAINT `fk_reviews_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_reviews_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (3,5,'### TestTest  *fgfg*','2022-06-24 15:41:51',22,1),(5,5,'*  sffdsfds','2022-06-24 15:54:22',22,2),(6,2,'&gt; bc cv vbvbbf','2022-06-24 15:56:13',22,3),(7,3,'errreger','2022-06-24 16:16:23',27,5),(8,2,'# gdfgfdgfdg','2022-06-24 17:46:28',22,4),(9,0,'ffgfgfg*gfgf**fgfggfgfg***\n1. dvd','2022-06-25 15:55:01',22,7),(10,5,'**cvvdfv**','2022-06-25 15:55:58',28,7),(11,5,'***Круто!***\n### ввпвп','2022-06-25 15:56:27',27,7);
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `desciption` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'Администратор','Суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'Модератор','Может редактировать данные книг и производить модерацию рецензий'),(3,'Пользователь','Может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `last_name` varchar(100) NOT NULL,
  `first_name` varchar(100) NOT NULL,
  `middle_name` varchar(100) NOT NULL,
  `login` varchar(100) NOT NULL,
  `password_hash` varchar(200) NOT NULL,
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `role_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  UNIQUE KEY `uq_users_password_hash` (`password_hash`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Админов','Админ','Админович','admin','pbkdf2:sha256:150000$IiI2optN$faa37951144668b3335dfe71cc7f4da3c13a1a746795f830a3963ad38baa933f','2022-06-14 01:01:07',1),(2,'Модеров','Модер','Модератович','moder','pbkdf2:sha256:150000$XWNsF54o$e89654503f3a277ed49df13a5eaf214489437d48b89b17dd5debea7598036216','2022-06-14 01:01:07',2),(3,'Юзеров','Юзер','Юзерович','user','pbkdf2:sha256:150000$FUCMgdyl$2c0a2add7938b024ca0673cc0dfd9052238ed8d1ea712f1765a762321eafedf7','2022-06-14 01:01:07',3),(4,'Юзеров1','Юзер1','Юзерович1','user_1','pbkdf2:sha256:150000$d3M2G3q2$e1339f03089a26f71fe0bedda30b6c7bca99676ed2d223726bc24361ddc0155c','2022-06-23 01:01:07',3),(5,'Юзеров2','Юзер2','Юзерович2','user_2','pbkdf2:sha256:150000$8wiu88oj$c99021ade443c84a22422290b2d6fcb5328db3c6ca6041f219314fba4d767082','2022-06-15 01:01:07',3),(6,'Юзеров3','Юзер3','Юзерович3','user_3','pbkdf2:sha256:150000$ZGzMzrbP$593b949349e4950dc3633f11c5d5dcf2662b9f3d2bfa58d44d6e90cff5e6953e','2022-04-13 01:01:07',3),(7,'Юзеров4','Юзер4','Юзерович4','user_4','pbkdf2:sha256:150000$bxAshUpV$c63205b9cee9b5276e5c14813d8bbb10ed7bb718431a23172a40df0815cacee9','2021-09-16 01:01:07',3);
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

-- Dump completed on 2022-06-25 16:58:40
