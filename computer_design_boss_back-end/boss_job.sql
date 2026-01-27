-- MySQL dump 10.13  Distrib 8.0.39, for Win64 (x86_64)
--
-- Host: localhost    Database: boss_job
-- ------------------------------------------------------
-- Server version	8.0.39

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
-- Table structure for table `forum_comments`
--

DROP TABLE IF EXISTS `forum_comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `forum_comments` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '评论ID（主键）',
  `category_id` int DEFAULT NULL COMMENT '关联的岗位类别ID',
  `user_id` int NOT NULL COMMENT '发布评论的用户ID',
  `parent_id` int DEFAULT NULL COMMENT '回复的父评论ID（自关联）',
  `content` text NOT NULL COMMENT '评论内容',
  `level` int NOT NULL DEFAULT '1' COMMENT '评论层级：1=一级评论 2=二级回复',
  `sort_order` int NOT NULL DEFAULT '0' COMMENT '排序值（在同一父评论下）',
  `is_deleted` tinyint NOT NULL DEFAULT '0' COMMENT '是否删除：1=删除 0=正常',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_content_parent` (`user_id`,`content`(100),`parent_id`),
  KEY `idx_category` (`category_id`),
  KEY `idx_user` (`user_id`),
  KEY `idx_parent` (`parent_id`),
  KEY `idx_created` (`created_at`),
  KEY `idx_category_parent` (`category_id`,`parent_id`),
  KEY `idx_user_category` (`user_id`,`category_id`),
  CONSTRAINT `fk_comment_category` FOREIGN KEY (`category_id`) REFERENCES `job_category_simple` (`next_category_id`) ON DELETE SET NULL ON UPDATE CASCADE,
  CONSTRAINT `fk_comment_parent` FOREIGN KEY (`parent_id`) REFERENCES `forum_comments` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_comment_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=79 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='论坛评论表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_comments`
--

LOCK TABLES `forum_comments` WRITE;
/*!40000 ALTER TABLE `forum_comments` DISABLE KEYS */;
INSERT INTO `forum_comments` VALUES (63,1,1,NULL,'技术岗位的发展前景很好，尤其是人工智能和大数据方向！',1,1,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(64,2,2,NULL,'后端开发需要掌握哪些核心技术栈？求大神指点！',1,1,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(65,3,3,NULL,'前端框架更新太快了，Vue和React哪个更值得深入学习？',1,1,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(66,4,4,NULL,'产品经理需要懂技术吗？到什么程度比较合适？',1,1,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(67,6,5,NULL,'运维工程师的日常工作有哪些？需要24小时待命吗？',1,1,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(68,1,6,NULL,'技术岗位的薪资待遇如何？不同级别差距大吗？',1,2,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(69,2,7,NULL,'Java、Go、Python哪个更适合后端开发？',1,2,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(70,3,8,NULL,'前端开发需要掌握UI设计吗？',1,2,0,'2026-01-26 10:51:53','2026-01-26 10:51:53'),(71,1,2,63,'确实，AI方向现在很火，但门槛也比较高。',2,1,0,'2026-01-26 10:55:19','2026-01-26 10:55:19'),(72,1,4,71,'数学主要是线性代数和概率论，最好还懂点微积分。',2,1,0,'2026-01-26 10:57:26','2026-01-26 10:57:26'),(73,2,1,69,'你说的特别的对',2,2,1,'2026-01-26 11:34:47','2026-01-26 11:39:33'),(75,2,3,NULL,'我是一个大二的学生，我想知道，我的该怎么做才能有工作',1,1,1,'2026-01-26 17:16:26','2026-01-26 17:19:29'),(76,2,3,NULL,'我是一个大二的学生，我想知道，我的该怎么做才能有工作',1,1,0,'2026-01-26 17:18:49','2026-01-26 17:18:49');
/*!40000 ALTER TABLE `forum_comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_category_simple`
--

DROP TABLE IF EXISTS `job_category_simple`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_category_simple` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键',
  `name` varchar(100) NOT NULL COMMENT '类别名称',
  `intro` text COMMENT '岗位类别简介（长文本）',
  `parent_id` int DEFAULT NULL COMMENT '上级类别ID',
  `next_category_id` int DEFAULT NULL COMMENT '下一个关联类别ID（用于特殊关联需求）',
  `sort_order` int NOT NULL DEFAULT '0' COMMENT '排序值',
  `is_active` tinyint NOT NULL DEFAULT '1' COMMENT '是否启用：1=启用 0=禁用',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_name` (`name`),
  KEY `idx_parent` (`parent_id`),
  KEY `idx_next` (`next_category_id`),
  CONSTRAINT `fk_category_next` FOREIGN KEY (`next_category_id`) REFERENCES `job_category_simple` (`id`) ON DELETE SET NULL ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位类别表（扁平结构）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_category_simple`
--

LOCK TABLES `job_category_simple` WRITE;
/*!40000 ALTER TABLE `job_category_simple` DISABLE KEYS */;
INSERT INTO `job_category_simple` VALUES (1,'技术','技术类岗位涵盖软件开发、测试、运维等多个方向，需要扎实的编程基础和解决问题的能力。',NULL,2,100,1,'2026-01-26 09:52:12','2026-01-26 10:48:54'),(2,'后端开发','后端开发主要负责服务器端逻辑、数据库设计和API接口开发，常用技术栈包括Java、Python、Go等。',1,3,110,1,'2026-01-26 09:52:12','2026-01-26 10:48:54'),(3,'前端开发','前端开发专注于用户界面和用户体验，涉及HTML、CSS、JavaScript及React、Vue等框架。',1,4,120,1,'2026-01-26 09:52:12','2026-01-26 10:48:54'),(4,'产品经理','产品经理负责产品规划、需求分析和项目管理，连接技术、设计和市场部门。',NULL,6,200,1,'2026-01-26 09:52:12','2026-01-26 10:48:54'),(6,'运维','运维类岗位涵盖软件开发、测试、运维等多个方向，需要扎实的编程基础和解决问题的能力。',1001,1,1001,1,'2026-01-26 09:55:28','2026-01-26 10:48:54');
/*!40000 ALTER TABLE `job_category_simple` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_post`
--

DROP TABLE IF EXISTS `job_post`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_post` (
  `id` bigint NOT NULL AUTO_INCREMENT COMMENT '主键',
  `boss_job_id` varchar(64) NOT NULL COMMENT 'Boss 直聘平台原始ID',
  `title` varchar(200) NOT NULL COMMENT '岗位名称',
  `company_id` bigint NOT NULL COMMENT '所属公司（关联 company 表）',
  `city_id` int NOT NULL COMMENT '城市ID（关联 city 表）',
  `district` varchar(100) DEFAULT NULL COMMENT '区县/商圈',
  `address` varchar(500) DEFAULT NULL COMMENT '详细工作地址',
  `category_id` int NOT NULL COMMENT '职位类别ID',
  `emp_type` tinyint NOT NULL DEFAULT '1' COMMENT '1=全职 2=兼职 3=实习',
  `salary_min` decimal(10,2) DEFAULT NULL COMMENT '薪资下限（元/月）',
  `salary_max` decimal(10,2) DEFAULT NULL COMMENT '薪资上限（元/月）',
  `salary_desc` varchar(200) DEFAULT NULL COMMENT '原始薪资文本，如“5-6K”',
  `edu_req` varchar(50) DEFAULT NULL COMMENT '学历要求',
  `exp_req` varchar(50) DEFAULT NULL COMMENT '经验要求',
  `recruiter_id` bigint DEFAULT NULL COMMENT '招聘者ID（关联 recruiter 表）',
  `description` text COMMENT '职位描述',
  `require_list` json DEFAULT NULL COMMENT '任职要求数组，方便快速搜索',
  `welfare_list` json DEFAULT NULL COMMENT '福利标签数组',
  `publish_time` datetime DEFAULT NULL COMMENT '发布时间',
  `refresh_time` datetime DEFAULT NULL COMMENT '刷新时间',
  `status` tinyint NOT NULL DEFAULT '1' COMMENT '1=在招 2=下架 3=暂停',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_boss_job_id` (`boss_job_id`),
  KEY `idx_company` (`company_id`),
  KEY `idx_city` (`city_id`),
  KEY `idx_category` (`category_id`),
  KEY `idx_publish` (`publish_time`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位主表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_post`
--

LOCK TABLES `job_post` WRITE;
/*!40000 ALTER TABLE `job_post` DISABLE KEYS */;
INSERT INTO `job_post` VALUES (1,'B123456789','Java 后端开发工程师',1,1,'海淀区','中关村软件园 10 号楼 5 层',1001,1,18000.00,25000.00,'18-25K','本科','3-5 年',101,'负责公司核心产品后端研发，参与架构设计、性能优化及技术难点攻关。','[\"Java 基础扎实\", \"熟悉 Spring 全家桶\", \"有高并发经验优先\"]','[\"五险一金\", \"弹性打卡\", \"15 薪\", \"免费三餐\"]','2026-01-20 10:00:00','2026-01-25 09:30:00',1,'2026-01-25 21:21:47','2026-01-25 21:21:47'),(2,'B223344556','UI 设计实习生',2,2,'浦东新区','张江高科技园区碧波路 456 号',1002,3,3000.00,4000.00,'3-4K','本科','无经验',102,'协助完成产品界面视觉设计，参与创意讨论，输出高保真原型。','[\"美术/设计相关专业\", \"熟练使用 Figma、Sketch\", \"每周到岗 ≥4 天\"]','[\"实习证明\", \"下午茶\", \"导师带教\"]','2026-01-18 14:20:00','2026-01-24 16:00:00',1,'2026-01-25 21:21:47','2026-01-25 21:21:47'),(3,'B334455667','区域销售代表',3,3,'天河区','珠江新城华夏路 28 号富力盈凯大厦',1003,1,12000.00,18000.00,'12-18K','大专','1-3 年',103,'负责华南区 B 端客户拓展与维护，完成季度销售指标，定期收集市场信息。','[\"大专及以上学历\", \"热爱销售，抗压能力强\", \"能适应出差\"]','[\"五险一金\", \"高提成\", \"年度旅游\", \"带薪年假\"]','2026-01-22 09:10:00','2026-01-25 11:00:00',1,'2026-01-25 21:21:50','2026-01-25 21:21:50');
/*!40000 ALTER TABLE `job_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '用户ID',
  `username` varchar(50) NOT NULL COMMENT '用户名',
  `email` varchar(100) NOT NULL COMMENT '邮箱',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_username` (`username`),
  UNIQUE KEY `uk_email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='用户表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'张三','zhangsan@example.com','2026-01-26 10:41:59'),(2,'李四','lisi@example.com','2026-01-26 10:41:59'),(3,'王五','wangwu@example.com','2026-01-26 10:41:59'),(4,'赵六','zhaoliu@example.com','2026-01-26 10:41:59'),(5,'钱七','qianqi@example.com','2026-01-26 10:41:59'),(6,'孙八','sunba@example.com','2026-01-26 10:41:59'),(7,'周九','zhoujiu@example.com','2026-01-26 10:41:59'),(8,'吴十','wushi@example.com','2026-01-26 10:41:59');
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

-- Dump completed on 2026-01-27 18:08:56
