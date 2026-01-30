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
-- Table structure for table `campus_experiences`
--

DROP TABLE IF EXISTS `campus_experiences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `campus_experiences` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '经历ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `has_student_union` tinyint(1) DEFAULT '0' COMMENT '是否有学生会经历：0-否，1-是',
  `student_union_details` text COMMENT '学生会经历详情：职位、时间段、工作内容',
  `has_club` tinyint(1) DEFAULT '0' COMMENT '是否有社团经历：0-否，1-是',
  `club_details` text COMMENT '社团经历详情',
  `has_scholarship` tinyint(1) DEFAULT '0' COMMENT '是否有奖学金：0-否，1-是',
  `scholarship_details` text COMMENT '奖学金详情：名称、金额、时间',
  `has_honor` tinyint(1) DEFAULT '0' COMMENT '是否有其他荣誉：0-否，1-是',
  `honor_details` text COMMENT '荣誉详情',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_resume_id` (`user_id`),
  CONSTRAINT `fk_campus_resume` FOREIGN KEY (`user_id`) REFERENCES `resumes` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='校园经历表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `campus_experiences`
--

LOCK TABLES `campus_experiences` WRITE;
/*!40000 ALTER TABLE `campus_experiences` DISABLE KEYS */;
INSERT INTO `campus_experiences` VALUES (1,1143526543212345678,0,NULL,0,NULL,1,'国家奖学金一次，校级奖学金五次',0,NULL,'2026-01-28 12:40:05','2026-01-28 13:45:13'),(2,1143526543212345679,1,'担任设计学院学生会宣传部部长，任期2021-2022年，负责活动宣传和视觉设计。',1,'创立\"UX设计研究社\"，担任社长，组织设计工作坊和行业分享会。',1,'获得2021-2022年度校级一等奖学金；获得2022年企业设计专项奖学金。',1,'2022年全国大学生工业设计大赛一等奖；2023年\"红点概念设计奖\"入围。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(3,1143526543212345680,1,'担任商学院学生会外联部部长，任期2016-2017年，负责校企合作和赞助洽谈。',1,'参加市场营销协会，担任活动策划负责人。',1,'获得2016-2017年度校级二等奖学金；2017年企业实践奖学金。',1,'2017年\"营销之星\"案例分析大赛冠军；2018年优秀毕业生。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(4,1769529152325,0,NULL,1,'参加软件工程协会，参与开源项目开发和维护。',1,'获得2018-2019年度校级三等奖学金。',1,'2019年校级程序设计竞赛二等奖；2020年\"互联网+\"大学生创新创业大赛校级铜奖。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(5,1143526543212345682,1,'担任计算机学院学生会主席，任期2012-2013年，全面负责学院学生工作。',1,'创立\"前端技术研究社\"，担任技术指导。',1,'连续三年获得国家奖学金（2011-2013）；获得2013年优秀毕业生奖学金。',1,'2012年\"挑战杯\"全国大学生创业计划竞赛金奖；2013年ACM国际大学生程序设计竞赛亚洲区金牌。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(10,1769610432924,0,NULL,0,NULL,0,NULL,0,NULL,'2026-01-28 14:30:00','2026-01-28 14:30:00');
/*!40000 ALTER TABLE `campus_experiences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `certificates`
--

DROP TABLE IF EXISTS `certificates`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `certificates` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '证书ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `cert_type` varchar(30) NOT NULL COMMENT '证书类型：english/computer/professional',
  `cert_name` varchar(100) NOT NULL COMMENT '证书名称',
  `cert_level` varchar(50) DEFAULT NULL COMMENT '等级/分数：如CET-6/550分，雅思/7.5',
  `issue_date` date DEFAULT NULL COMMENT '获取时间',
  `expiry_date` date DEFAULT NULL COMMENT '过期时间（如有）',
  `issuing_authority` varchar(100) DEFAULT NULL COMMENT '发证机构',
  `certificate_no` varchar(100) DEFAULT NULL COMMENT '证书编号',
  `attachment_url` varchar(500) DEFAULT NULL COMMENT '证书附件URL',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_resume_id` (`user_id`),
  KEY `idx_cert_type` (`cert_type`),
  KEY `idx_cert_name` (`cert_name`),
  CONSTRAINT `fk_cert_resume` FOREIGN KEY (`user_id`) REFERENCES `resumes` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='技能证书表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `certificates`
--

LOCK TABLES `certificates` WRITE;
/*!40000 ALTER TABLE `certificates` DISABLE KEYS */;
INSERT INTO `certificates` VALUES (1,1143526543212345678,'english','大学英语六级','CET-6 580分','2020-12-01',NULL,'教育部考试中心','CET62020120001','https://cert-bucket.com/zhangsan_cet6.pdf','2026-01-28 12:40:05'),(2,1143526543212345678,'computer','Oracle Java认证','OCA','2021-06-15','2024-06-15','Oracle公司','OCA20210615001','https://cert-bucket.com/zhangsan_java.pdf','2026-01-28 12:40:05'),(3,1143526543212345678,'professional','软件设计师','中级','2022-03-20',NULL,'人力资源和社会保障部','RJ20220320001',NULL,'2026-01-28 12:40:05'),(4,1143526543212345679,'english','雅思','7.5分','2022-08-10',NULL,'British Council','IELTS20220810001','https://cert-bucket.com/lisi_ielts.pdf','2026-01-28 12:40:05'),(5,1143526543212345679,'professional','Adobe认证设计师','ACA','2023-01-15','2026-01-15','Adobe公司','ACA20230115001','https://cert-bucket.com/lisi_adobe.pdf','2026-01-28 12:40:05'),(6,1143526543212345680,'professional','市场营销师','三级','2019-05-20',NULL,'中国市场营销协会','SC20190520001',NULL,'2026-01-28 12:40:05'),(7,1143526543212345680,'english','商务英语','BEC Higher','2020-11-15',NULL,'剑桥大学考试委员会','BEC20201115001',NULL,'2026-01-28 12:40:05'),(8,1143526543212345682,'english','托福','105分','2018-06-20',NULL,'ETS','TOEFL20180620001',NULL,'2026-01-28 12:40:05'),(9,1143526543212345682,'computer','AWS认证解决方案架构师','Associate','2020-09-10','2023-09-10','Amazon Web Services','AWS20200910001','https://cert-bucket.com/qianqi_aws.pdf','2026-01-28 12:40:05'),(10,1143526543212345682,'professional','PMP项目管理专业人士','PMP','2021-11-05','2024-11-05','PMI','PMP20211105001',NULL,'2026-01-28 12:40:05'),(11,1769529152325,'english','大学英语四级','CET-4 520分','2019-06-01',NULL,'教育部考试中心','CET42019060001',NULL,'2026-01-28 12:40:05'),(12,1769529152325,'computer','全国计算机等级考试','二级Java','2020-03-01',NULL,'教育部考试中心','NCRE20200301001',NULL,'2026-01-28 12:40:05'),(13,1143526543212345678,'english','英语六级','CET-6（优秀）','2021-06-01',NULL,'教育部考试中心','CET621000001',NULL,'2026-01-28 13:45:13'),(14,1143526543212345678,'computer','计算机二级','二级','2020-12-01',NULL,'教育部考试中心','MS202000001',NULL,'2026-01-28 13:45:13'),(15,1143526543212345678,'professional','注册会计师','专业阶段','2022-03-01','2025-03-01','中国注册会计师协会','CPA202200001',NULL,'2026-01-28 13:45:13'),(16,1769610432924,'技术','Python编程证书',NULL,'2023-06-01','2026-01-16','Python官方认证',NULL,NULL,'2026-01-28 14:29:35');
/*!40000 ALTER TABLE `certificates` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `complaint_type`
--

DROP TABLE IF EXISTS `complaint_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `complaint_type` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `type_code` tinyint unsigned NOT NULL COMMENT '投诉类型代码：1-功能，2-BUG，3-建议，4-其他，5-隐私安全',
  `type_name` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '投诉类型名称',
  `sort_order` int DEFAULT '0' COMMENT '排序',
  `is_active` tinyint(1) DEFAULT '1' COMMENT '是否启用：1启用，0禁用',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_type_code` (`type_code`)
) ENGINE=InnoDB AUTO_INCREMENT=136 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='投诉类型字典表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `complaint_type`
--

LOCK TABLES `complaint_type` WRITE;
/*!40000 ALTER TABLE `complaint_type` DISABLE KEYS */;
INSERT INTO `complaint_type` VALUES (1,1,'功能',1,1),(2,2,'BUG',2,1),(3,3,'建议',3,1),(4,4,'其他',4,1),(5,5,'隐私安全',5,1);
/*!40000 ALTER TABLE `complaint_type` ENABLE KEYS */;
UNLOCK TABLES;

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
-- Table structure for table `internship_stats`
--

DROP TABLE IF EXISTS `internship_stats`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internship_stats` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `user_id` bigint unsigned NOT NULL COMMENT '简历ID',
  `total_count` int DEFAULT '0' COMMENT '实习总次数',
  `related_count` int DEFAULT '0' COMMENT '相关行业实习次数',
  `last_updated` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_resume_id` (`user_id`),
  CONSTRAINT `fk_stats_resume` FOREIGN KEY (`user_id`) REFERENCES `resumes` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='实习统计表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internship_stats`
--

LOCK TABLES `internship_stats` WRITE;
/*!40000 ALTER TABLE `internship_stats` DISABLE KEYS */;
INSERT INTO `internship_stats` VALUES (1,1143526543212345678,5,5,'2026-01-28 13:45:13'),(3,1143526543212345679,2,2,'2026-01-28 12:40:05'),(5,1143526543212345680,2,1,'2026-01-28 12:40:05'),(7,1143526543212345682,1,1,'2026-01-28 12:40:05'),(8,1769529152325,2,2,'2026-01-28 12:40:05'),(13,1769610432924,1,0,'2026-01-28 14:29:56');
/*!40000 ALTER TABLE `internship_stats` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `internships`
--

DROP TABLE IF EXISTS `internships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `internships` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '实习ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `company_name` varchar(100) NOT NULL COMMENT '公司名称',
  `position` varchar(50) DEFAULT NULL COMMENT '实习岗位',
  `industry` varchar(50) DEFAULT NULL COMMENT '所属行业',
  `start_date` date DEFAULT NULL COMMENT '开始时间',
  `end_date` date DEFAULT NULL COMMENT '结束时间',
  `is_current` tinyint(1) DEFAULT '0' COMMENT '是否进行中：0-否，1-是',
  `is_related` tinyint(1) DEFAULT '0' COMMENT '是否是相关行业经历：0-否，1-是',
  `work_content` text COMMENT '工作内容描述',
  `achievements` text COMMENT '工作成果',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_resume_id` (`user_id`),
  KEY `idx_industry` (`industry`),
  KEY `idx_intern_company` (`company_name`),
  KEY `idx_intern_dates` (`start_date`,`end_date`),
  CONSTRAINT `fk_intern_resume` FOREIGN KEY (`user_id`) REFERENCES `resumes` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='实习实践表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `internships`
--

LOCK TABLES `internships` WRITE;
/*!40000 ALTER TABLE `internships` DISABLE KEYS */;
INSERT INTO `internships` VALUES (1,1143526543212345678,'阿里巴巴','后端开发实习生','互联网','2021-06-01','2021-09-01',0,1,'参与阿里云日志服务开发，负责日志采集模块的优化和维护。使用Java开发，参与代码评审和单元测试。','优化了日志采集性能，处理速度提升15%；编写了详细的技术文档和单元测试用例。','2026-01-28 12:40:05'),(2,1143526543212345678,'字节跳动','软件开发实习生','互联网','2022-03-01','2022-07-01',0,1,'参与抖音电商中台开发，负责订单管理模块的后端接口开发。使用Go语言，参与微服务架构设计。','独立完成了订单状态流转模块，日均处理订单量达到100万+；获得了团队优秀实习生称号。','2026-01-28 12:40:05'),(3,1143526543212345679,'腾讯','交互设计实习生','互联网','2022-07-01','2022-12-01',0,1,'参与微信小程序用户体验优化项目，负责用户调研和交互设计。使用Figma进行原型设计，参与用户测试。','设计的优化方案使小程序用户留存率提升了8%；获得部门设计创新奖。','2026-01-28 12:40:05'),(4,1143526543212345679,'小米科技','产品设计实习生','硬件/互联网','2023-01-01','2023-06-01',0,1,'参与智能家居APP的产品设计，负责智能灯光控制模块的交互和视觉设计。','设计的灯光控制界面被评为最易用功能之一；参与的设计方案已上线应用商店。','2026-01-28 12:40:05'),(5,1143526543212345680,'宝洁公司','市场部实习生','快消品','2017-06-01','2017-09-01',0,1,'参与海飞丝品牌暑期推广活动，负责市场调研和竞品分析。协助策划校园推广活动。','收集了超过1000份有效问卷，为产品改进提供了数据支持；参与的活动覆盖全国30所高校。','2026-01-28 12:40:05'),(6,1143526543212345680,'奥美广告','客户执行实习生','广告/营销','2017-11-01','2018-03-01',0,0,'协助客户团队服务汽车行业客户，参与广告创意讨论和文案撰写。','参与策划的广告 campaign 获得了行业奖项提名；获得了客户的正面反馈。','2026-01-28 12:40:05'),(7,1143526543212345682,'微软亚洲研究院','研究实习生','互联网','2013-06-01','2013-09-01',0,1,'参与前端性能优化研究项目，研究JavaScript引擎优化技术。','研究成果发表在内部技术期刊上；提出的优化方案被部分采纳到产品中。','2026-01-28 12:40:05'),(8,1769529152325,'杭州某软件公司','前端开发实习生','互联网','2019-07-01','2019-09-01',0,1,'参与公司内部管理系统前端开发，使用Vue.js框架，负责用户管理模块。','独立完成了用户权限管理功能；学习了完整的前端开发流程和团队协作。','2026-01-28 12:40:05'),(9,1769529152325,'某电商创业公司','全栈开发实习生','互联网','2020-03-01','2020-06-01',0,1,'参与电商平台开发，前端使用React，后端使用Node.js，负责商品展示模块。','实现了响应式商品列表页面；学习了全栈开发技术栈。','2026-01-28 12:40:05'),(16,1143526543212345678,'阿里巴巴','高级后端开发实习生','互联网','2022-06-01','2022-09-01',0,1,'参与微服务架构开发，负责订单和支付模块','完成订单系统的重构，提升性能30%','2026-01-28 13:45:13'),(17,1143526543212345678,'腾讯','前端开发实习生','互联网','2021-07-01','2021-10-01',0,1,'参与微信小程序开发，负责用户界面','优化页面加载速度，用户体验评分提升20%','2026-01-28 13:45:13'),(18,1143526543212345678,'字节跳动','数据分析实习生','互联网','2023-01-01','2023-06-01',1,1,'分析用户行为数据，提供产品优化建议','建立用户流失预测模型，准确率达85%','2026-01-28 13:45:13'),(19,1769610432924,'阿里巴巴集团','后端开发实习生',NULL,'2023-07-01','2023-09-30',0,0,NULL,NULL,'2026-01-28 14:29:56');
/*!40000 ALTER TABLE `internships` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_internship_insert` AFTER INSERT ON `internships` FOR EACH ROW BEGIN
    INSERT INTO internship_stats (user_id, total_count, related_count)
    VALUES (NEW.user_id, 1, IF(NEW.is_related = 1, 1, 0))
    ON DUPLICATE KEY UPDATE
        total_count = total_count + 1,
        related_count = related_count + IF(NEW.is_related = 1, 1, 0);
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = gbk */ ;
/*!50003 SET character_set_results = gbk */ ;
/*!50003 SET collation_connection  = gbk_chinese_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `trg_after_internship_delete` AFTER DELETE ON `internships` FOR EACH ROW BEGIN
    UPDATE internship_stats
    SET total_count = total_count - 1,
        related_count = related_count - IF(OLD.is_related = 1, 1, 0)
    WHERE user_id = OLD.user_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

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
-- Table structure for table `job_intentions`
--

DROP TABLE IF EXISTS `job_intentions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_intentions` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `target_industries` json DEFAULT NULL COMMENT '目标行业：["互联网","教育","国企"]',
  `industry_priority` varchar(20) DEFAULT NULL COMMENT '首选行业',
  `target_positions` json DEFAULT NULL COMMENT '目标岗位：["产品","运营","技术"]',
  `position_priority` varchar(20) DEFAULT NULL COMMENT '首选岗位',
  `target_cities` json DEFAULT NULL COMMENT '期望城市：["北京","上海","深圳"]',
  `city_priority` varchar(50) DEFAULT NULL COMMENT '首选城市',
  `salary_min` int DEFAULT NULL COMMENT '最低期望薪资（元/月）',
  `salary_max` int DEFAULT NULL COMMENT '最高期望薪资（元/月）',
  `salary_type` varchar(20) DEFAULT 'monthly' COMMENT '薪资类型：monthly-月薪，annual-年薪',
  `salary_negotiable` tinyint(1) DEFAULT '1' COMMENT '薪资是否可面议：0-否，1-是',
  `availability` varchar(50) DEFAULT NULL COMMENT '到岗时间：随时/一周内/一个月内/具体时间',
  `available_date` date DEFAULT NULL COMMENT '可入职日期',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_resume_id` (`user_id`),
  CONSTRAINT `fk_intention_resume` FOREIGN KEY (`user_id`) REFERENCES `resumes` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='求职意向表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_intentions`
--

LOCK TABLES `job_intentions` WRITE;
/*!40000 ALTER TABLE `job_intentions` DISABLE KEYS */;
INSERT INTO `job_intentions` VALUES (1,1143526543212345678,'[\"互联网\", \"金融科技\", \"人工智能\"]','互联网','[\"后端开发\", \"数据分析\", \"算法工程师\"]','后端开发','[\"北京\", \"上海\", \"深圳\"]','北京',15000,25000,'monthly',1,'立即到岗','2023-07-01','2026-01-28 12:40:05','2026-01-28 13:45:13'),(2,1143526543212345679,'[\"互联网\", \"智能硬件\", \"设计咨询\"]','互联网','[\"交互设计师\", \"产品设计师\", \"UX设计师\"]','交互设计师','[\"上海\", \"北京\", \"深圳\"]','上海',12000,18000,'monthly',1,'随时到岗',NULL,'2026-01-28 12:40:05','2026-01-28 12:40:05'),(3,1143526543212345680,'[\"快消品\", \"互联网\", \"广告传媒\"]','快消品','[\"市场营销\", \"品牌策划\", \"市场推广\"]','市场营销','[\"广州\", \"深圳\", \"上海\"]','广州',15000,22000,'monthly',0,'两周内','2026-02-15','2026-01-28 12:40:05','2026-01-28 12:40:05'),(4,1769529152325,'[\"互联网\", \"软件开发\", \"教育科技\"]','互联网','[\"前端开发\", \"全栈开发\", \"软件工程师\"]','前端开发','[\"杭州\", \"上海\", \"南京\"]','杭州',8000,12000,'monthly',1,'随时到岗',NULL,'2026-01-28 12:40:05','2026-01-28 12:40:05'),(5,1143526543212345682,'[\"互联网\", \"金融科技\", \"企业服务\"]','互联网','[\"前端架构师\", \"技术负责人\", \"高级前端开发\"]','前端架构师','[\"北京\", \"上海\", \"远程\"]','北京',35000,50000,'monthly',1,'一个月内','2026-03-01','2026-01-28 12:40:05','2026-01-28 12:40:05'),(8,1769610432924,'\"互联网,人工智能\"',NULL,'\"软件工程师,算法工程师\"',NULL,'\"北京,上海,杭州\"',NULL,15000,25000,'monthly',1,NULL,NULL,'2026-01-28 14:30:25','2026-01-28 14:30:25');
/*!40000 ALTER TABLE `job_intentions` ENABLE KEYS */;
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
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位主表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_post`
--

LOCK TABLES `job_post` WRITE;
/*!40000 ALTER TABLE `job_post` DISABLE KEYS */;
INSERT INTO `job_post` VALUES (1,'B123456789','Java 后端开发工程师',1,1,'海淀区','中关村软件园 10 号楼 5 层',1001,1,18000.00,25000.00,'18-25K','本科','3-5 年',101,'负责公司核心产品后端研发，参与架构设计、性能优化及技术难点攻关。','[\"Java 基础扎实\", \"熟悉 Spring 全家桶\", \"有高并发经验优先\"]','[\"五险一金\", \"弹性打卡\", \"15 薪\", \"免费三餐\"]','2026-01-20 10:00:00','2026-01-25 09:30:00',1,'2026-01-25 21:21:47','2026-01-25 21:21:47'),(2,'B223344556','UI 设计实习生',2,2,'浦东新区','张江高科技园区碧波路 456 号',1002,3,3000.00,4000.00,'3-4K','本科','无经验',102,'协助完成产品界面视觉设计，参与创意讨论，输出高保真原型。','[\"美术/设计相关专业\", \"熟练使用 Figma、Sketch\", \"每周到岗 ≥4 天\"]','[\"实习证明\", \"下午茶\", \"导师带教\"]','2026-01-18 14:20:00','2026-01-24 16:00:00',1,'2026-01-25 21:21:47','2026-01-25 21:21:47'),(3,'B334455667','区域销售代表',3,3,'天河区','珠江新城华夏路 28 号富力盈凯大厦',1003,1,12000.00,18000.00,'12-18K','大专','1-3 年',103,'负责华南区 B 端客户拓展与维护，完成季度销售指标，定期收集市场信息。','[\"大专及以上学历\", \"热爱销售，抗压能力强\", \"能适应出差\"]','[\"五险一金\", \"高提成\", \"年度旅游\", \"带薪年假\"]','2026-01-22 09:10:00','2026-01-25 11:00:00',1,'2026-01-25 21:21:50','2026-01-25 21:21:50'),(4,'1234567890123456789','高级Java开发工程师',10001,101010100,'海淀区','北京市海淀区中关村软件园二期XX号楼',100101,1,25000.00,35000.00,'25-35K·14薪','本科','3-5年',888888,'负责公司核心业务系统的设计与开发，参与技术架构选型...','[\"精通Java，熟悉Spring Boot\", \"熟悉MySQL、Redis\", \"具备良好的沟通能力\"]','[\"五险一金\", \"带薪年假\", \"股票期权\", \"弹性工作\", \"免费三餐\"]','2025-01-15 10:30:00','2025-01-20 09:00:00',1,'2026-01-29 21:27:34','2026-01-29 21:27:34');
/*!40000 ALTER TABLE `job_post` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `job_preferences`
--

DROP TABLE IF EXISTS `job_preferences`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `job_preferences` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '偏好ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `accept_intern_to_full` tinyint(1) DEFAULT '1' COMMENT '是否接受实习转正：0-否，1-是',
  `accept_remote_city` tinyint(1) DEFAULT '0' COMMENT '是否考虑异地岗位：0-否，1-是',
  `need_campus_referral` tinyint(1) DEFAULT '1' COMMENT '是否需要校招内推：0-否，1-是',
  `accept_overtime` tinyint(1) DEFAULT NULL COMMENT '是否接受加班',
  `accept_business_trip` tinyint(1) DEFAULT NULL COMMENT '是否接受出差',
  `company_size_preference` varchar(20) DEFAULT NULL COMMENT '公司规模偏好：startup-初创，medium-中型，large-大厂',
  `work_type_preference` varchar(20) DEFAULT NULL COMMENT '工作类型偏好：fulltime-全职，intern-实习，both-均可',
  `other_preferences` text COMMENT '其他偏好说明',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_resume_id` (`user_id`),
  CONSTRAINT `fk_preference_resume` FOREIGN KEY (`user_id`) REFERENCES `resumes` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='求职偏好表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_preferences`
--

LOCK TABLES `job_preferences` WRITE;
/*!40000 ALTER TABLE `job_preferences` DISABLE KEYS */;
INSERT INTO `job_preferences` VALUES (1,1143526543212345678,1,0,1,1,1,'大型企业（500人以上）','全职','希望有良好的培训机制和晋升空间','2026-01-28 12:40:05','2026-01-28 13:45:13'),(2,1143526543212345679,1,0,1,1,0,'medium','fulltime','偏好设计驱动型公司，希望有专业的设计团队和设计系统。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(3,1143526543212345680,1,1,0,1,1,'large','fulltime','希望公司有完善的培训体系和明确的职业发展路径。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(4,1769529152325,1,1,1,1,0,'startup','both','希望有机会接触全栈技术，不介意加班，但希望有学习成长空间。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(5,1143526543212345682,0,1,0,1,1,'large','fulltime','希望担任技术管理岗位，带领团队，参与技术决策。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(8,1769610432924,1,0,1,NULL,NULL,NULL,NULL,'希望有良好的团队氛围和职业发展机会。','2026-01-28 14:30:30','2026-01-28 14:30:30');
/*!40000 ALTER TABLE `job_preferences` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `resumes`
--

DROP TABLE IF EXISTS `resumes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `resumes` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '简历ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `real_name` varchar(50) DEFAULT NULL COMMENT '真实姓名',
  `gender` tinyint DEFAULT NULL COMMENT '性别：1-男，2-女，0-保密',
  `birth_date` date DEFAULT NULL COMMENT '出生日期',
  `phone` varchar(20) DEFAULT NULL COMMENT '联系电话',
  `email` varchar(100) DEFAULT NULL COMMENT '联系邮箱',
  `wechat` varchar(50) DEFAULT NULL COMMENT '微信号',
  `city` varchar(50) DEFAULT NULL COMMENT '所在城市',
  `education_level` varchar(20) DEFAULT NULL COMMENT '最高学历：本科/硕士/博士等',
  `school_name` varchar(100) DEFAULT NULL COMMENT '学校名称',
  `major` varchar(100) DEFAULT NULL COMMENT '专业',
  `graduation_year` year DEFAULT NULL COMMENT '毕业年份',
  `gpa` decimal(3,2) DEFAULT NULL COMMENT 'GPA',
  `resume_file_url` varchar(500) DEFAULT NULL COMMENT '简历文件URL',
  `resume_file_name` varchar(200) DEFAULT NULL COMMENT '简历文件名',
  `resume_format` varchar(10) DEFAULT NULL COMMENT '文件格式：pdf/doc/docx',
  `self_introduction` text COMMENT '个人简介/自我评价',
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_resume_edu` (`education_level`,`graduation_year`),
  KEY `idx_resume_school` (`school_name`),
  KEY `idx_resume_city` (`city`),
  CONSTRAINT `fk_resume_user` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='简历基础信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `resumes`
--

LOCK TABLES `resumes` WRITE;
/*!40000 ALTER TABLE `resumes` DISABLE KEYS */;
INSERT INTO `resumes` VALUES (1,1143526543212345678,'张测试',1,'1995-05-20','13800138001','zhangsan@example.com','zhangsan_wechat','北京','本科','清华大学','计算机科学',2022,3.90,'https://resume-bucket.com/zhangsan_resume.pdf','张测试_简历.pdf','pdf','热爱编程，熟悉Python和Java开发，有丰富的项目经验','2026-01-28 12:40:05','2026-01-28 13:45:13'),(2,1143526543212345679,'李思',2,'2000-08-22','13800138002','lisi@example.com','lisi_wechat','上海','硕士','上海交通大学','交互设计',2023,3.70,'https://resume-bucket.com/lisi_resume.pdf','李思_简历.pdf','pdf','交互设计专业硕士，专注于用户体验设计，熟练掌握Figma、Sketch等设计工具，有多个产品设计项目经验。','2026-01-28 12:40:05','2026-01-28 13:45:14'),(3,1143526543212345680,'王五',1,'1995-11-30','13800138003','wangwu@example.com','wangwu_wechat','广州','本科','中山大学','市场营销',2018,3.50,'https://resume-bucket.com/wangwu_resume.docx','王五_简历.docx','docx','拥有4年市场营销经验，擅长品牌策划和市场推广，曾主导多个成功的市场活动。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(4,1143526543212345677,'王五',0,NULL,'13800138222','user3@example.com',NULL,'深圳',NULL,NULL,NULL,NULL,NULL,'https://resume-bucket.com/wangwu2_resume.pdf','王五_简历.pdf','pdf','求职者，希望寻找合适的发展机会。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(5,1769529152325,'李四',1,'1996-11-04','13800138000','user804@example.com','lisi_wechat2','杭州','本科','浙江大学','软件工程',2020,3.60,'https://resume-bucket.com/lisi2_resume.pdf','李四_简历.pdf','pdf','软件工程专业毕业生，熟悉前后端开发，对前端技术有浓厚兴趣，希望成为全栈工程师。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(6,1143526543212345682,'钱七',1,'1992-03-08','13800138005','qianqi@example.com','qianqi_wechat','北京','硕士','北京大学','计算机科学',2014,3.90,'https://resume-bucket.com/qianqi_resume.pdf','钱七_资深前端工程师.pdf','pdf','8年前端开发经验，精通React、Vue等主流框架，有大型项目架构经验，带领过10人前端团队。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(7,1143526543212345681,NULL,0,NULL,'13800138004','zhaoliu@example.com',NULL,NULL,NULL,NULL,NULL,NULL,NULL,'https://resume-bucket.com/zhaoliu_resume.docx','赵六_简历.docx','docx','正在完善个人简历信息。','2026-01-28 12:40:05','2026-01-28 12:40:05'),(11,1769610432924,'王柄屹',NULL,NULL,'15147206048','zhangsan@example.com',NULL,NULL,'本科','清华大学','计算机科学与技术',NULL,NULL,NULL,NULL,NULL,NULL,'2026-01-28 14:28:57','2026-01-28 14:28:57');
/*!40000 ALTER TABLE `resumes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sys_user`
--

DROP TABLE IF EXISTS `sys_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sys_user` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '内部主键（自增，聚簇索引，不对外暴露）',
  `user_id` bigint unsigned NOT NULL COMMENT '用户业务ID（对外关联键，建议雪花ID，如1143526543212345678）',
  `mobile` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '手机号',
  `email` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '邮箱',
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码哈希值',
  `bio` text COLLATE utf8mb4_unicode_ci COMMENT '个人简介',
  `avatar_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '头像URL',
  `status` tinyint unsigned NOT NULL DEFAULT '1' COMMENT '账号状态：0-禁用，1-正常，2-未激活，3-锁定',
  `job_status` tinyint unsigned DEFAULT '0' COMMENT '求职状态：0-待业，1-实习中，2-应届求职',
  `real_name` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '真实姓名',
  `gender` tinyint unsigned DEFAULT '0' COMMENT '性别：0-未知，1-男，2-女',
  `birth_date` date DEFAULT NULL COMMENT '出生日期',
  `education_level` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '学历层次',
  `major` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '专业',
  `enrollment_year` year DEFAULT NULL COMMENT '入学年份',
  `graduation_year` year DEFAULT NULL COMMENT '毕业年份',
  `register_time` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  `last_login_time` datetime DEFAULT NULL COMMENT '最后登录时间',
  `last_login_ip` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最后登录IP',
  `last_device_model` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '最近登录设备型号',
  `last_device_time` datetime DEFAULT NULL COMMENT '最近设备登录时间',
  `last_device_type` tinyint unsigned DEFAULT '0' COMMENT '设备类型：0-未知，1-PC，2-Android，3-iOS，4-小程序',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '记录创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '记录更新时间',
  `deleted_at` datetime DEFAULT NULL COMMENT '软删除时间',
  `is_deleted` tinyint unsigned NOT NULL DEFAULT '0' COMMENT '是否删除：0-否，1-是',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_id` (`user_id`),
  UNIQUE KEY `uk_mobile` (`mobile`),
  UNIQUE KEY `uk_email` (`email`),
  KEY `idx_status` (`status`),
  KEY `idx_job_status` (`job_status`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户基础信息表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sys_user`
--

LOCK TABLES `sys_user` WRITE;
/*!40000 ALTER TABLE `sys_user` DISABLE KEYS */;
INSERT INTO `sys_user` VALUES (1,1143526543212345678,'13800138001','zhangsan@example.com','$2a$10$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJK','这是一个测试用户的个人简介','https://example.com/avatar/new.jpg',1,2,'张测试',1,'1995-05-20','本科','计算机科学',2018,2022,'2022-03-10 09:30:00','2026-01-28 01:11:12','192.168.1.100','iPhone 13 Pro','2026-01-28 01:11:12',3,'2026-01-27 22:22:17','2026-01-28 01:11:12',NULL,0),(2,1143526543212345679,'13800138002','lisi@example.com','$2a$10$bcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKL','产品设计实习生，喜欢用户体验研究','https://example.com/avatars/lisi.jpg',1,1,'李思',2,'2000-08-22','硕士','交互设计',2019,2023,'2022-05-20 14:10:00','2026-01-28 01:11:12','10.0.0.1','Xiaomi 12','2026-01-28 01:11:12',2,'2026-01-27 22:22:17','2026-01-28 01:11:12',NULL,0),(3,1143526543212345680,'13800138003','wangwu@example.com','$2a$10$cdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLM','之前从事市场营销工作，正在寻找新机会',NULL,0,0,'王五',1,'1995-11-30','本科','市场营销',2014,2018,'2022-01-15 11:20:00','2023-09-01 16:40:20','192.168.1.102','Xiaomi 11','2023-09-01 16:40:20',2,'2026-01-27 22:22:17','2026-01-27 22:22:17',NULL,0),(4,1143526543212345681,'13800138004','zhaoliu@example.com','$2a$10$defghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMN',NULL,NULL,2,0,NULL,0,NULL,NULL,NULL,NULL,NULL,'2023-10-16 08:45:00',NULL,NULL,NULL,NULL,0,'2026-01-27 22:22:17','2026-01-27 22:22:17',NULL,0),(5,1143526543212345682,'13800138005','qianqi@example.com','$2a$10$efghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNO','资深前端工程师，React/Vue专家','https://example.com/avatars/qianqi.jpg',3,0,'钱七',1,'1992-03-08','硕士','计算机科学',2010,2014,'2021-11-05 16:30:00','2023-10-13 22:10:15','192.168.1.103','MacBook Pro','2023-10-13 22:10:15',1,'2026-01-27 22:22:17','2026-01-27 22:22:17',NULL,0),(6,1143526543212345683,'13800138006','sunba@example.com','$2a$10$fghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOP','前数据分析师','https://example.com/avatars/sunba.jpg',0,0,'孙八',2,'1993-07-12','博士','统计学',2011,2017,'2022-02-28 10:15:00','2023-08-20 09:30:00','192.168.1.104','iPad Pro','2023-08-20 09:30:00',3,'2026-01-27 22:22:17','2026-01-27 22:22:17','2023-09-01 00:00:00',1),(9,1143526543212345689,'13800138999',NULL,'test_hash_delete',NULL,NULL,1,0,NULL,0,NULL,NULL,NULL,NULL,NULL,'2026-01-27 22:58:53',NULL,NULL,NULL,NULL,0,'2026-01-27 22:58:53','2026-01-27 22:58:53','2026-01-27 22:58:53',1),(10,1143526543212345677,'13800138222','user3@example.com','hash3',NULL,NULL,0,2,'王五',0,NULL,NULL,NULL,NULL,NULL,'2026-01-27 22:58:53',NULL,NULL,NULL,NULL,0,'2026-01-27 22:58:53','2026-01-27 22:58:53',NULL,0),(14,1769529152325,'13800138000','user804@example.com','20c57997be99466830c0de3cfb53ad4ddefa9c493b03645e3a5494205920ae2e','对前端开发感兴趣','https://randomuser.me/api/portraits/men/32.jpg',2,0,'李四',1,'1996-11-04','3','软件工程',NULL,NULL,'2026-01-27 23:52:32','2026-01-28 00:40:41','127.0.0.1','Test Device','2026-01-28 00:40:41',1,'2026-01-27 23:52:32','2026-01-28 01:14:06',NULL,0),(15,1769529744329,'13896608053','test516@example.com','9a931c55ac02bf216550c464b1992a30c522dfabf6cb31deada5c716bc13a263',NULL,NULL,2,0,NULL,0,NULL,NULL,NULL,NULL,NULL,'2026-01-28 00:02:24',NULL,NULL,NULL,NULL,0,'2026-01-28 00:02:24','2026-01-28 00:02:24',NULL,0),(28,1769533982676,'13800813782','test964@example.com','9a931c55ac02bf216550c464b1992a30c522dfabf6cb31deada5c716bc13a263',NULL,NULL,2,0,NULL,0,NULL,NULL,NULL,NULL,NULL,'2026-01-28 01:13:02',NULL,NULL,NULL,NULL,0,'2026-01-28 01:13:02','2026-01-28 01:13:02',NULL,0),(29,1769610432924,'15147206048','test243@example.com','ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f',NULL,NULL,2,0,NULL,0,NULL,NULL,NULL,NULL,NULL,'2026-01-28 22:27:12','2026-01-30 12:37:37','127.0.0.1','Unknown','2026-01-30 12:37:37',0,'2026-01-28 22:27:12','2026-01-30 12:37:37',NULL,0);
/*!40000 ALTER TABLE `sys_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_deliver_jobs`
--

DROP TABLE IF EXISTS `user_deliver_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_deliver_jobs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `boss_job_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '岗位ID',
  `is_canceled` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否取消收藏：0-已投递，1-已结束',
  `job_snapshot` json DEFAULT NULL COMMENT '岗位快照（存储收藏时的岗位标题、薪资、公司名等）',
  `remarks` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间（首次收藏时间）',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间（状态变更时间）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_job` (`user_id`,`boss_job_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_boss_job_id` (`boss_job_id`),
  KEY `idx_is_canceled` (`is_canceled`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏岗位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_deliver_jobs`
--

LOCK TABLES `user_deliver_jobs` WRITE;
/*!40000 ALTER TABLE `user_deliver_jobs` DISABLE KEYS */;
INSERT INTO `user_deliver_jobs` VALUES (1,1,'B123456789',0,'{\"title\": \"Java 后端开发工程师\", \"salary\": \"18-25K\", \"address\": \"中关村软件园 10 号楼 5 层\", \"edu_req\": \"本科\", \"exp_req\": \"3-5 年\", \"location\": \"北京·海淀\", \"company_id\": 1}','符合我的技术栈，准备投递','2026-01-29 20:38:25','2026-01-29 20:38:25'),(2,2,'B223344556',0,'{\"title\": \"UI 设计实习生\", \"salary\": \"3-4K\", \"address\": \"张江高科技园区碧波路 456 号\", \"edu_req\": \"本科\", \"exp_req\": \"无经验\", \"location\": \"上海·浦东\", \"company_id\": 2}','实习机会不错，需要联系导师','2026-01-29 20:38:25','2026-01-29 20:38:25'),(3,1,'B334455667',1,'{\"title\": \"区域销售代表\", \"salary\": \"12-18K\", \"address\": \"珠江新城华夏路 28 号富力盈凯大厦\", \"edu_req\": \"大专\", \"exp_req\": \"1-3 年\", \"location\": \"广州·天河\", \"company_id\": 3}','发现是销售岗，不是技术岗，取消收藏','2026-01-29 20:38:25','2026-01-29 20:38:25'),(4,14,'B123456789',0,'{\"title\": \"Java 后端开发工程师\", \"salary\": \"18-25K\", \"address\": \"中关村软件园 10 号楼 5 层\", \"edu_req\": \"本科\", \"exp_req\": \"3-5 年\", \"location\": \"北京·海淀\", \"company_id\": 1}','前端想转后端，先收藏学习','2026-01-29 20:38:25','2026-01-29 20:38:25'),(5,2,'B123456789',1,'{\"title\": \"Java 后端开发工程师\", \"salary\": \"18-25K\", \"address\": \"中关村软件园 10 号楼 5 层\", \"edu_req\": \"本科\", \"exp_req\": \"3-5 年\", \"location\": \"北京·海淀\", \"company_id\": 1}','我是设计专业，Java岗位不适合我','2026-01-29 20:38:25','2026-01-29 20:38:25'),(6,1769610432924,'1',0,'{\"id\": 1, \"title\": \"Java 后端开发工程师\", \"salary_max\": 25000.0, \"salary_min\": 18000.0, \"salary_desc\": \"18-25K\"}','更新后的投递备注','2026-01-29 21:59:21','2026-01-29 21:59:47');
/*!40000 ALTER TABLE `user_deliver_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_favorite_jobs`
--

DROP TABLE IF EXISTS `user_favorite_jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_favorite_jobs` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID',
  `boss_job_id` varchar(64) COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '岗位ID',
  `is_canceled` tinyint(1) NOT NULL DEFAULT '0' COMMENT '是否取消收藏：0-收藏中，1-已取消',
  `job_snapshot` json DEFAULT NULL COMMENT '岗位快照（存储收藏时的岗位标题、薪资、公司名等）',
  `remarks` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户备注',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间（首次收藏时间）',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间（状态变更时间）',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uk_user_job` (`user_id`,`boss_job_id`),
  KEY `idx_user_id` (`user_id`),
  KEY `idx_boss_job_id` (`boss_job_id`),
  KEY `idx_is_canceled` (`is_canceled`),
  KEY `idx_created_at` (`created_at`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户收藏岗位表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_favorite_jobs`
--

LOCK TABLES `user_favorite_jobs` WRITE;
/*!40000 ALTER TABLE `user_favorite_jobs` DISABLE KEYS */;
INSERT INTO `user_favorite_jobs` VALUES (1,1,'B123456789',0,'{\"title\": \"Java 后端开发工程师\", \"salary\": \"18-25K\", \"address\": \"中关村软件园 10 号楼 5 层\", \"edu_req\": \"本科\", \"exp_req\": \"3-5 年\", \"location\": \"北京·海淀\", \"company_id\": 1}','符合我的技术栈，准备投递','2026-01-29 20:08:55','2026-01-29 20:08:55'),(2,2,'B223344556',0,'{\"title\": \"UI 设计实习生\", \"salary\": \"3-4K\", \"address\": \"张江高科技园区碧波路 456 号\", \"edu_req\": \"本科\", \"exp_req\": \"无经验\", \"location\": \"上海·浦东\", \"company_id\": 2}','实习机会不错，需要联系导师','2026-01-29 20:08:55','2026-01-29 20:08:55'),(3,1,'B334455667',1,'{\"title\": \"区域销售代表\", \"salary\": \"12-18K\", \"address\": \"珠江新城华夏路 28 号富力盈凯大厦\", \"edu_req\": \"大专\", \"exp_req\": \"1-3 年\", \"location\": \"广州·天河\", \"company_id\": 3}','发现是销售岗，不是技术岗，取消收藏','2026-01-29 20:08:55','2026-01-29 20:08:55'),(4,14,'B123456789',0,'{\"title\": \"Java 后端开发工程师\", \"salary\": \"18-25K\", \"address\": \"中关村软件园 10 号楼 5 层\", \"edu_req\": \"本科\", \"exp_req\": \"3-5 年\", \"location\": \"北京·海淀\", \"company_id\": 1}','前端想转后端，先收藏学习','2026-01-29 20:08:55','2026-01-29 20:08:55'),(5,2,'B123456789',1,'{\"title\": \"Java 后端开发工程师\", \"salary\": \"18-25K\", \"address\": \"中关村软件园 10 号楼 5 层\", \"edu_req\": \"本科\", \"exp_req\": \"3-5 年\", \"location\": \"北京·海淀\", \"company_id\": 1}','我是设计专业，Java岗位不适合我','2026-01-29 20:08:55','2026-01-29 20:08:55'),(6,1769610432924,'1',0,'{\"id\": 1, \"title\": \"Java 后端开发工程师\", \"salary_max\": 25000.0, \"salary_min\": 18000.0, \"salary_desc\": \"18-25K\"}','更新后的备注','2026-01-29 21:53:19','2026-01-29 21:54:10');
/*!40000 ALTER TABLE `user_favorite_jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user_feedback`
--

DROP TABLE IF EXISTS `user_feedback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user_feedback` (
  `id` bigint unsigned NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint unsigned NOT NULL COMMENT '用户ID，关联sys_user表的user_id',
  `complaint_type` tinyint unsigned NOT NULL COMMENT '投诉类型：1-功能，2-BUG，3-建议，4-其他，5-隐私安全',
  `description` text COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户投诉描述内容',
  `image_url_1` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户上传图片1的URL',
  `image_url_2` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户上传图片2的URL',
  `image_url_3` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL COMMENT '用户上传图片3的URL',
  `feedback_content` text COLLATE utf8mb4_unicode_ci COMMENT '管理员反馈回复内容',
  `is_resolved` tinyint(1) DEFAULT '0' COMMENT '是否已解决：0-未解决，1-已解决',
  `create_time` datetime DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_time` datetime DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `resolve_time` datetime DEFAULT NULL COMMENT '解决时间',
  `resolved_by` bigint unsigned DEFAULT NULL COMMENT '解决人ID（管理员）',
  `priority` tinyint(1) DEFAULT '1' COMMENT '优先级：1-低，2-中，3-高',
  PRIMARY KEY (`id`),
  KEY `idx_user_id` (`user_id`) COMMENT '用户ID索引，方便查询某用户的所有反馈',
  KEY `idx_complaint_type` (`complaint_type`) COMMENT '投诉类型索引',
  KEY `idx_is_resolved` (`is_resolved`) COMMENT '解决状态索引',
  KEY `idx_create_time` (`create_time`) COMMENT '创建时间索引',
  KEY `idx_priority` (`priority`,`is_resolved`) COMMENT '优先级和状态组合索引',
  CONSTRAINT `fk_feedback_type` FOREIGN KEY (`complaint_type`) REFERENCES `complaint_type` (`type_code`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `fk_feedback_user_id` FOREIGN KEY (`user_id`) REFERENCES `sys_user` (`user_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户投诉及反馈表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user_feedback`
--

LOCK TABLES `user_feedback` WRITE;
/*!40000 ALTER TABLE `user_feedback` DISABLE KEYS */;
INSERT INTO `user_feedback` VALUES (17,1143526543212345678,2,'APP在iOS 17系统下打开设置页面会闪退，每次必现。手机型号：iPhone 15 Pro，系统版本：17.1.2。','https://cdn.example.com/feedback/img_001.jpg','https://cdn.example.com/feedback/img_002.jpg',NULL,NULL,0,'2026-01-28 23:02:52','2026-01-28 23:02:52',NULL,NULL,3),(18,1143526543212345678,1,'找不到修改手机号码的入口，希望能优化用户中心的功能布局。',NULL,NULL,NULL,'您好，修改手机号功能位于：我的 -> 设置 -> 账号与安全 -> 更换手机号。感谢您的反馈，我们已在个人中心增加了快捷入口。',1,'2026-01-28 23:02:52','2026-01-28 23:02:52','2024-01-15 14:30:00',20001,2),(19,1143526543212345678,3,'建议增加夜间模式，晚上使用APP时白色背景太刺眼了。可以参考微信的深色模式设计。','https://cdn.example.com/feedback/img_003.png',NULL,NULL,NULL,0,'2026-01-28 23:02:52','2026-01-28 23:02:52',NULL,NULL,1),(20,1143526543212345678,5,'发现我的个人信息在未经同意的情况下被第三方获取，要求解释并删除数据。','https://cdn.example.com/feedback/img_004.jpg','https://cdn.example.com/feedback/img_005.jpg','https://cdn.example.com/feedback/img_006.jpg','非常抱歉给您带来困扰。经核查，此为第三方SDK异常调用导致，我们已立即下线该SDK并删除相关数据。补偿已发放至您的账户。',1,'2026-01-28 23:02:52','2026-01-28 23:02:52','2024-01-10 09:15:00',20002,3),(21,1143526543212345678,4,'客服电话等待时间太长，建议增加在线客服人数。',NULL,NULL,NULL,NULL,0,'2026-01-28 23:02:52','2026-01-28 23:02:52',NULL,NULL,1),(22,1143526543212345678,1,'支付时提示\"系统繁忙\"，但扣款成功了，订单却显示未支付。','https://cdn.example.com/feedback/img_007.jpg',NULL,NULL,'已收到您的反馈，技术团队正在核查支付流水，预计2小时内给您答复。',0,'2026-01-28 23:02:52','2026-01-28 23:02:52',NULL,20001,2),(23,1143526543212345678,2,'消息推送延迟严重，经常收到几小时前的通知。',NULL,NULL,NULL,'问题已修复，推送服务已升级至最新版本，延迟问题已解决。',1,'2026-01-28 23:02:52','2026-01-28 23:02:52','2024-01-20 16:45:00',20003,2),(24,1143526543212345678,3,'希望能支持指纹登录，每次输密码太麻烦了。',NULL,NULL,NULL,'感谢您的建议！指纹登录功能已在v2.5.0版本上线，请更新体验。',1,'2026-01-28 23:02:52','2026-01-28 23:02:52','2024-01-18 11:20:00',20001,1),(26,1769610432924,2,'这是一条反馈后端接口的测试消息',NULL,NULL,NULL,NULL,0,'2026-01-29 19:44:18','2026-01-29 19:44:18',NULL,NULL,3);
/*!40000 ALTER TABLE `user_feedback` ENABLE KEYS */;
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

-- Dump completed on 2026-01-30 18:45:33
