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
) ENGINE=InnoDB AUTO_INCREMENT=103 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='论坛评论表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `forum_comments`
--

LOCK TABLES `forum_comments` WRITE;
/*!40000 ALTER TABLE `forum_comments` DISABLE KEYS */;
INSERT INTO `forum_comments` VALUES (1,101,1,NULL,'前端现在越来越卷了，Vue3和React到底该深耕哪个？',1,10,0,'2026-01-15 09:30:00','2026-01-15 09:30:00'),(2,101,2,NULL,'刚转行做前端，求推荐学习路线，HTML/CSS基础已经掌握了',1,20,0,'2026-01-15 14:20:00','2026-01-15 14:20:00'),(3,101,3,NULL,'性能优化有什么实战经验吗？首屏加载一直优化不上去',1,30,0,'2026-01-16 11:45:00','2026-01-16 11:45:00'),(4,101,4,1,'建议React，生态更完善，大厂用的多，Vue3也不错但岗位相对少',2,10,0,'2026-01-15 10:15:00','2026-01-15 10:15:00'),(5,101,5,1,'Vue3组合式API写起来很爽，中小型项目首选',2,20,0,'2026-01-15 16:30:00','2026-01-15 16:30:00'),(6,101,6,2,'建议直接上React，同时学TypeScript，现在都是标配了',2,10,0,'2026-01-15 15:00:00','2026-01-15 15:00:00'),(7,101,7,3,'试试SSR或者SSG，Next.js/Nuxt.js能大幅提升首屏速度',2,10,0,'2026-01-16 13:20:00','2026-01-16 13:20:00'),(8,102,8,NULL,'Spring Cloud Alibaba现在还是主流吗？要不要转Spring Boot 3.x？',1,10,0,'2026-01-10 09:00:00','2026-01-10 09:00:00'),(9,102,9,NULL,'Java 21的新特性有在生产环境用的吗？虚拟线程稳定性如何？',1,20,0,'2026-01-12 16:45:00','2026-01-12 16:45:00'),(10,102,10,NULL,'微服务拆分粒度怎么把握？我们拆得太细，运维成本爆炸了',1,30,0,'2026-01-14 11:20:00','2026-01-14 11:20:00'),(11,102,11,8,'依然主流，但Spring Boot 3.x + GraalVM原生镜像值得尝试',2,10,0,'2026-01-10 10:30:00','2026-01-10 10:30:00'),(12,102,12,10,'建议按业务域聚合，避免过度拆分，3-5个服务一个团队维护比较合适',2,10,0,'2026-01-14 14:00:00','2026-01-14 14:00:00'),(13,102,13,NULL,'FastAPI和Django怎么选？做数据API服务的话',1,40,0,'2026-01-18 10:00:00','2026-01-18 10:00:00'),(14,102,14,13,'FastAPI异步性能更好，自动生成文档，适合API服务',2,10,0,'2026-01-18 11:30:00','2026-01-18 11:30:00'),(15,102,15,NULL,'Go的泛型用了这么久，感觉如何？代码可读性有提升吗？',1,50,0,'2026-01-20 09:15:00','2026-01-20 09:15:00'),(16,102,16,NULL,'微服务框架选Gin还是直接上gRPC？',1,60,0,'2026-01-21 14:30:00','2026-01-21 14:30:00'),(17,103,17,NULL,'Kotlin协程在实际项目中怎么避免内存泄漏？',1,10,0,'2026-01-08 16:00:00','2026-01-08 16:00:00'),(18,103,18,NULL,'Jetpack Compose现在能用于生产环境了吗？',1,20,0,'2026-01-11 09:30:00','2026-01-11 09:30:00'),(19,103,19,18,'完全可以，我们新项目全用Compose了，开发效率提升明显',2,10,0,'2026-01-11 11:00:00','2026-01-11 11:00:00'),(20,103,20,18,'注意性能优化，复杂列表还是建议用RecyclerView',2,20,0,'2026-01-11 15:20:00','2026-01-11 15:20:00'),(21,103,21,NULL,'SwiftUI 5.0有重大突破吗？还在用UIKit的要不要转？',1,30,0,'2026-01-13 10:45:00','2026-01-13 10:45:00'),(22,103,22,NULL,'App Store审核最近是不是更严格了？被拒了三次了',1,40,0,'2026-01-17 14:00:00','2026-01-17 14:00:00'),(23,103,23,NULL,'HarmonyOS NEXT纯血鸿蒙开发体验如何？生态够完善吗？',1,50,0,'2026-01-22 09:00:00','2026-01-22 09:00:00'),(24,103,24,23,'ArkTS上手挺快，但第三方库还是不如Android丰富',2,10,0,'2026-01-22 10:30:00','2026-01-22 10:30:00'),(25,104,25,NULL,'Flink和Spark Streaming怎么选？实时性要求高的话',1,10,0,'2026-01-05 11:00:00','2026-01-05 11:00:00'),(26,104,26,NULL,'数据倾斜问题除了加随机前缀还有什么好办法？',1,20,0,'2026-01-09 15:30:00','2026-01-09 15:30:00'),(27,104,27,25,'Flink延迟更低，毫秒级，Spark Streaming是秒级',2,10,0,'2026-01-05 13:20:00','2026-01-05 13:20:00'),(28,104,28,26,'试试Salting技术，或者自定义Partitioner',2,10,0,'2026-01-09 17:00:00','2026-01-09 17:00:00'),(29,104,29,NULL,'模型部署用TorchServe还是Triton Inference Server？',1,30,0,'2026-01-12 09:00:00','2026-01-12 09:00:00'),(30,104,30,NULL,'特征工程现在还有必要手动做吗？AutoML能替代多少？',1,40,0,'2026-01-16 14:00:00','2026-01-16 14:00:00'),(31,104,31,NULL,'推荐系统冷启动问题除了用热门推荐还有什么策略？',1,50,0,'2026-01-19 10:30:00','2026-01-19 10:30:00'),(32,104,32,31,'可以试试基于内容的推荐，或者利用用户画像做相似用户推荐',2,10,0,'2026-01-19 11:45:00','2026-01-19 11:45:00'),(33,104,33,NULL,'大模型微调用LoRA还是全参数？数据量多少才值得全参数？',1,60,0,'2026-01-23 09:00:00','2026-01-23 09:00:00'),(34,104,34,NULL,'RAG和微调怎么选？企业知识库场景',1,70,0,'2026-01-25 11:20:00','2026-01-25 11:20:00'),(35,105,35,NULL,'手工测试还有前途吗？要不要转自动化？',1,10,0,'2026-01-07 14:00:00','2026-01-07 14:00:00'),(36,105,36,NULL,'接口自动化用Python还是Java？团队技术栈比较杂',1,20,0,'2026-01-10 09:30:00','2026-01-10 09:30:00'),(37,105,37,35,'建议转，但不会完全替代，业务理解能力还是核心',2,10,0,'2026-01-07 15:30:00','2026-01-07 15:30:00'),(38,105,38,36,'Python上手快，pytest + requests很好用',2,10,0,'2026-01-10 11:00:00','2026-01-10 11:00:00'),(39,105,39,NULL,'Playwright真的比Selenium好用吗？稳定性如何？',1,30,0,'2026-01-14 10:00:00','2026-01-14 10:00:00'),(40,105,40,NULL,'移动端自动化用Appium还是直接上Airtest？',1,40,0,'2026-01-18 16:00:00','2026-01-18 16:00:00'),(41,105,41,NULL,'JMeter 5.6和Locust怎么选？需要高并发的场景',1,50,0,'2026-01-20 09:00:00','2026-01-20 09:00:00'),(42,105,42,41,'JMeter功能更全，Locust写Python脚本更灵活，看团队技术栈',2,10,0,'2026-01-20 10:30:00','2026-01-20 10:30:00'),(43,106,43,NULL,'传统运维如何转型SRE？需要补哪些技能？',1,10,0,'2026-01-06 11:00:00','2026-01-06 11:00:00'),(44,106,44,NULL,'Prometheus + Grafana监控方案生产环境稳定吗？',1,20,0,'2026-01-09 14:30:00','2026-01-09 14:30:00'),(45,106,45,43,'重点学Python/Go，懂开发才能做自动化，再学K8s和云原生',2,10,0,'2026-01-06 13:00:00','2026-01-06 13:00:00'),(46,106,46,NULL,'GitLab CI和GitHub Actions哪个更适合企业级？',1,30,0,'2026-01-11 09:00:00','2026-01-11 09:00:00'),(47,106,47,NULL,'IaC用Terraform还是Pulumi？团队开发背景强',1,40,0,'2026-01-15 15:00:00','2026-01-15 15:00:00'),(48,106,48,47,'Pulumi可以用Python/TypeScript写，学习曲线低，但Terraform生态更成熟',2,10,0,'2026-01-15 16:30:00','2026-01-15 16:30:00'),(49,106,49,NULL,'SLA定99.9%还是99.99%？成本差距太大了',1,50,0,'2026-01-17 10:00:00','2026-01-17 10:00:00'),(50,106,50,NULL,'故障演练（Chaos Engineering）有必要定期做吗？',1,60,0,'2026-01-21 14:00:00','2026-01-21 14:00:00'),(51,106,51,NULL,'Kubernetes 1.29有什么值得关注的新特性？',1,70,0,'2026-01-24 09:30:00','2026-01-24 09:30:00'),(52,106,52,NULL,'Service Mesh用Istio还是Linkerd？性能敏感场景',1,80,0,'2026-01-26 11:00:00','2026-01-26 11:00:00'),(53,106,53,NULL,'MySQL 8.0迁移后性能反而下降了，有人遇到过吗？',1,90,0,'2026-01-08 10:00:00','2026-01-08 10:00:00'),(54,106,54,53,'检查optimizer_switch设置，8.0默认开启了一些新优化器特性可能有影响',2,10,0,'2026-01-08 11:30:00','2026-01-08 11:30:00'),(55,107,55,NULL,'零信任架构落地最大的难点是什么？技术还是管理？',1,10,0,'2026-01-13 09:00:00','2026-01-13 09:00:00'),(56,107,56,NULL,'WAF规则太多误报，怎么平衡安全和业务？',1,20,0,'2026-01-16 14:30:00','2026-01-16 14:30:00'),(57,107,57,55,'主要是管理，需要全公司配合改造网络架构，技术反而是其次',2,10,0,'2026-01-13 10:30:00','2026-01-13 10:30:00'),(58,107,58,NULL,'Burp Suite Professional值得买正版吗？还是社区版够用？',1,30,0,'2026-01-18 11:00:00','2026-01-18 11:00:00'),(59,107,59,NULL,'SRC漏洞挖掘现在还有搞头吗？感觉越来越卷了',1,40,0,'2026-01-22 09:00:00','2026-01-22 09:00:00'),(60,108,60,NULL,'RTOS选FreeRTOS还是RT-Thread？国产芯片支持如何？',1,10,0,'2026-01-12 10:00:00','2026-01-12 10:00:00'),(61,108,61,NULL,'嵌入式Linux裁剪到最小需要保留哪些模块？',1,20,0,'2026-01-15 15:00:00','2026-01-15 15:00:00'),(62,108,62,60,'RT-Thread国产支持更好，社区活跃，文档也中文友好',2,10,0,'2026-01-12 11:30:00','2026-01-12 11:30:00'),(63,108,63,NULL,'MQTT Broker用Eclipse Mosquitto还是EMQX？',1,30,0,'2026-01-19 09:00:00','2026-01-19 09:00:00'),(64,108,64,NULL,'边缘计算用KubeEdge还是K3s？资源受限设备',1,40,0,'2026-01-23 14:00:00','2026-01-23 14:00:00'),(65,200,65,NULL,'技术型产品经理需要写到什么程度的PRD？伪代码要吗？',1,10,0,'2026-01-04 11:00:00','2026-01-04 11:00:00'),(66,200,66,NULL,'如何平衡技术债务和产品迭代速度？',1,20,0,'2026-01-08 09:30:00','2026-01-08 09:30:00'),(67,200,67,65,'不用伪代码，但要定义清楚接口字段和状态流转，开发能看懂即可',2,10,0,'2026-01-04 12:30:00','2026-01-04 12:30:00'),(68,200,68,66,'建议每个迭代留20%时间还债，不然越积越多最后爆炸',2,10,0,'2026-01-08 11:00:00','2026-01-08 11:00:00'),(69,200,69,NULL,'Figma自动布局（Auto Layout）用熟练了真的能提升效率吗？',1,30,0,'2026-01-14 10:00:00','2026-01-14 10:00:00'),(70,200,70,NULL,'设计系统和组件库维护成本好高，小团队值得做吗？',1,40,0,'2026-01-17 14:30:00','2026-01-17 14:30:00'),(71,200,71,NULL,'交互文档需要写到什么粒度？开发总说看不懂',1,50,0,'2026-01-20 09:00:00','2026-01-20 09:00:00'),(72,200,72,71,'异常状态、空状态、加载状态都要覆盖，最好配流程图',2,10,0,'2026-01-20 10:30:00','2026-01-20 10:30:00'),(73,300,73,NULL,'技术管理岗还要不要写代码？占比多少合适？',1,10,0,'2026-01-03 10:00:00','2026-01-03 10:00:00'),(74,300,74,NULL,'团队成员技术成长慢，怎么有效培养？',1,20,0,'2026-01-07 14:00:00','2026-01-07 14:00:00'),(75,300,75,73,'建议30%时间写核心代码，70%做架构设计和Code Review',2,10,0,'2026-01-03 11:30:00','2026-01-03 11:30:00'),(76,300,76,74,'制定技术成长路线图，分配有挑战性的任务，定期技术分享',2,10,0,'2026-01-07 15:30:00','2026-01-07 15:30:00'),(77,300,77,NULL,'技术选型时如何说服业务方接受新技术栈的风险？',1,30,0,'2026-01-11 09:00:00','2026-01-11 09:00:00'),(78,300,78,NULL,'微服务拆分时数据一致性怎么保证？Saga还是TCC？',1,40,0,'2026-01-16 11:00:00','2026-01-16 11:00:00'),(79,300,79,NULL,'多产品线资源冲突怎么协调？各产品线都喊缺人',1,50,0,'2026-01-21 10:00:00','2026-01-21 10:00:00'),(80,300,80,79,'建立资源池和优先级机制，核心项目保障，边缘项目外包或暂缓',2,10,0,'2026-01-21 11:30:00','2026-01-21 11:30:00'),(81,300,81,NULL,'技术战略规划如何与公司业务战略对齐？',1,60,0,'2026-01-25 09:00:00','2026-01-25 09:00:00'),(82,300,82,NULL,'技术中台建设投入大见效慢，怎么向CEO解释价值？',1,70,0,'2026-01-28 14:00:00','2026-01-28 14:00:00'),(83,101,83,NULL,'微信小程序和抖音小程序开发差异大吗？能一套代码多端发布吗？',1,70,0,'2026-01-27 10:00:00','2026-01-27 10:00:00'),(84,101,84,NULL,'Flutter 3.19性能有提升吗？还在用2.x的建议升级吗？',1,80,0,'2026-01-29 09:30:00','2026-01-29 09:30:00'),(85,101,85,NULL,'微前端qiankun和Module Federation怎么选？',1,90,0,'2026-01-30 11:00:00','2026-01-30 11:00:00'),(86,101,86,NULL,'Nest.js和Egg.js在生产环境稳定性如何？高并发场景',1,100,0,'2026-01-31 14:00:00','2026-01-31 14:00:00'),(87,102,87,NULL,'C++20协程在实际项目中好用吗？编译器支持如何？',1,70,0,'2026-01-24 10:00:00','2026-01-24 10:00:00'),(88,102,88,NULL,'Service Mesh sidecar模式资源占用太高，有没有替代方案？',1,80,0,'2026-01-26 09:00:00','2026-01-26 09:00:00'),(89,103,89,NULL,'Unity 6和Unreal Engine 5手游开发怎么选？',1,60,0,'2026-01-28 11:00:00','2026-01-28 11:00:00'),(90,104,90,NULL,'ClickHouse和Doris在OLAP场景怎么选？',1,80,0,'2026-01-27 09:00:00','2026-01-27 09:00:00'),(91,104,91,NULL,'模型量化后精度损失严重，有什么优化技巧？',1,90,0,'2026-01-29 14:00:00','2026-01-29 14:00:00'),(92,104,92,NULL,'YOLOv8部署到移动端，TensorRT还是NCNN？',1,100,0,'2026-01-30 10:00:00','2026-01-30 10:00:00'),(93,104,93,NULL,'SQL优化到极致还是慢，是不是该上ClickHouse了？',1,110,0,'2026-01-31 09:00:00','2026-01-31 09:00:00'),(94,104,94,NULL,'埋点方案设计怎么平衡全面性和性能影响？',1,120,0,'2026-02-01 11:00:00','2026-02-01 11:00:00'),(95,105,95,NULL,'测试平台开发用Django还是Spring Boot？团队有Python基础',1,60,0,'2026-01-25 10:00:00','2026-01-25 10:00:00'),(96,105,96,NULL,'OWASP Top 10 2024有什么新变化值得关注？',1,70,0,'2026-01-27 14:00:00','2026-01-27 14:00:00'),(97,107,97,NULL,'SIEM系统选型，Splunk还是ELK Stack？预算有限',1,50,0,'2026-01-24 09:00:00','2026-01-24 09:00:00'),(98,107,98,NULL,'Android 14加固方案有什么新动向？脱壳难度加大了',1,60,0,'2026-01-29 11:00:00','2026-01-29 11:00:00'),(99,107,99,NULL,'密码学方案设计，国密SM2/SM3/SM4替换RSA/SHA/AES要注意什么？',1,70,0,'2026-01-31 10:00:00','2026-01-31 10:00:00'),(100,108,100,NULL,'字符设备和块设备驱动开发，哪个更适合入门？',1,50,0,'2026-01-26 09:30:00','2026-01-26 09:30:00'),(101,108,101,NULL,'Verilog和VHDL现在哪个更主流？新人学哪个？',1,60,0,'2026-01-30 14:00:00','2026-01-30 14:00:00'),(102,200,102,NULL,'可用性测试样本量多少合适？5个用户真的够吗？',1,60,0,'2026-01-23 10:00:00','2026-01-23 10:00:00');
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
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位类别表（扁平结构）';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_category_simple`
--

LOCK TABLES `job_category_simple` WRITE;
/*!40000 ALTER TABLE `job_category_simple` DISABLE KEYS */;
INSERT INTO `job_category_simple` VALUES (1,'Web前端工程师','负责Web应用界面开发，使用HTML5/CSS3/JavaScript及React/Vue/Angular等框架，实现用户交互逻辑与视觉还原，优化页面性能与兼容性',101,101,10,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(2,'移动端前端工程师','专注于H5页面及混合应用开发，适配iOS/Android多平台，解决移动端兼容性、触摸交互、性能优化及离线缓存等问题',101,101,20,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(3,'小程序开发工程师','开发微信/支付宝/百度/鸿蒙等平台小程序，掌握各平台SDK与组件化开发，实现轻量级应用功能与Native能力调用',101,101,30,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(4,'跨平台开发工程师','使用Flutter/React Native/Uni-app等技术进行跨平台开发，实现一套代码多端运行，兼顾性能与开发效率',101,101,40,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(5,'前端架构师','负责前端技术选型、工程化建设、微前端架构设计、性能优化体系搭建，制定团队开发规范与代码标准',101,101,50,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(6,'Node.js全栈工程师','基于Node.js生态（Express/Nest.js/Egg.js）开发服务端应用，处理高并发请求，实现前后端同构渲染与BFF层',101,101,60,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(7,'Java开发工程师','使用Java语言及Spring生态（Spring Boot/Cloud）开发企业级后端服务，擅长微服务架构、分布式事务及高并发系统',102,102,70,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(8,'Python开发工程师','基于Python进行Web开发（Django/Flask/FastAPI）或数据服务开发，涉及爬虫、自动化脚本、AI模型部署等场景',102,102,80,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(9,'Go开发工程师','使用Go语言开发高性能后端服务，擅长云原生应用、微服务治理、中间件开发及高并发分布式系统',102,102,90,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(10,'C++开发工程师','开发高性能后端服务、游戏服务器、量化交易系统或分布式存储，注重内存管理、多线程优化及底层网络编程',102,102,100,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(11,'PHP开发工程师','使用PHP及Laravel/ThinkPHP等框架开发Web应用，擅长CMS、电商平台及快速原型开发，注重LAMP/LNMP优化',102,102,110,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(12,'微服务架构师','设计分布式系统架构，掌握Service Mesh、分布式事务、服务治理、容器编排，保障系统高可用与可扩展性',102,102,120,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(13,'Android开发工程师','使用Kotlin/Java开发Android原生应用，掌握Jetpack组件、性能优化、Android Studio及鸿蒙系统适配',103,103,130,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(14,'iOS开发工程师','使用Swift/Objective-C开发iOS应用，熟悉UIKit/SwiftUI、Xcode工具链、App Store发布流程及苹果生态集成',103,103,140,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(15,'鸿蒙开发工程师','基于ArkTS语言与HarmonyOS SDK开发鸿蒙原生应用，掌握鸿蒙分布式能力、原子化服务及多设备协同',103,103,150,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(16,'移动游戏开发工程师','使用Unity3D或Cocos2d-x开发手游客户端，涉及游戏逻辑、图形渲染、物理引擎、资源管理及热更新技术',103,103,160,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(17,'大数据开发工程师','基于Hadoop/Spark/Flink生态开发数据平台，擅长数据ETL、实时计算、离线数仓建设及海量数据处理',104,104,170,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(18,'数据仓库工程师','构建企业级数据仓库，设计维度建模，优化Hive/ClickHouse/Doris等OLAP引擎，支撑业务数据分析',104,104,180,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(19,'机器学习工程师','开发并部署机器学习模型，使用TensorFlow/PyTorch/Scikit-learn，涉及特征工程、模型训练、A/B测试及模型监控',104,104,190,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(20,'深度学习工程师','专注于深度学习算法研发，应用CNN/RNN/Transformer等网络结构，从事CV、NLP或推荐算法工程化落地',104,104,200,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(21,'算法工程师（推荐/广告）','构建推荐系统、广告算法或搜索排序模型，掌握协同过滤、深度学习推荐、用户画像及实时特征计算',104,104,210,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(22,'自然语言处理工程师','研发NLP应用如文本分类、情感分析、对话系统、大模型微调（LLM），掌握BERT/GPT等预训练模型',104,104,220,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(23,'计算机视觉工程师','开发图像识别、目标检测、OCR、视频分析等CV应用，使用OpenCV及深度学习框架进行模型优化与部署',104,104,230,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(24,'数据分析师','通过SQL/Python进行数据提取与统计分析，制作BI报表（Tableau/PowerBI），输出业务洞察与决策支持',104,104,240,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(25,'数据产品经理','负责数据产品规划（BI工具、埋点系统、数据平台），协调数据需求，设计指标体系与数据可视化方案',104,104,250,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(26,'测试工程师','执行功能测试，编写测试用例，进行缺陷管理与质量评估，保障软件发布质量，熟悉敏捷测试流程',105,105,260,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(27,'自动化测试工程师','开发自动化测试脚本与框架（Selenium/Appium/Playwright），实现UI/接口自动化，提升测试效率与覆盖率',105,105,270,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(28,'性能测试工程师','使用JMeter/LoadRunner进行压力测试、负载测试与稳定性测试，分析系统瓶颈，输出性能优化建议',105,105,280,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(29,'测试开发工程师','介于开发与测试之间，开发测试平台、Mock服务、质量保障工具链，推动DevOps中的质量内建',105,105,290,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(30,'安全测试工程师','进行渗透测试、漏洞扫描、代码审计，发现Web/移动应用安全漏洞，提出修复方案与安全加固建议',105,105,300,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(31,'运维工程师','负责服务器、操作系统及中间件维护，处理故障排查、系统部署、备份恢复，保障线上服务稳定运行',106,106,310,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(32,'DevOps工程师','构建CI/CD流水线（Jenkins/GitLab CI/GitHub Actions），推进IaC（Terraform/Ansible）与自动化发布，提升研发效能',106,106,320,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(33,'SRE工程师','通过软件工程方法保障系统可靠性，制定SLA/SLO，设计监控告警体系，主导故障应急响应与容量规划',106,106,330,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(34,'云原生工程师','深度掌握Kubernetes/Docker/容器网络，负责云原生架构落地、Service Mesh实施及多云环境管理',106,106,340,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(35,'数据库管理员(DBA)','管理MySQL/PostgreSQL/Oracle/MongoDB等数据库，负责架构设计、性能调优、分库分表及数据安全保障',106,106,350,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(36,'网络工程师','设计企业网络架构，配置交换机/路由器/防火墙/F5负载均衡，管理CDN、VPN及云网络（VPC）环境',106,106,360,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(37,'网络安全工程师','设计网络安全策略，配置防火墙/IDS/IPS/WAF，进行安全加固、日志审计及合规检查（等保/ISO27001）',107,107,370,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(38,'渗透测试工程师','模拟黑客攻击进行Web/APP/内网渗透测试，使用Burp Suite/Metasploit挖掘漏洞，输出渗透测试报告',107,107,380,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(39,'安全运维工程师','负责安全设备运维、威胁情报分析、应急响应处置，建设SOC安全运营中心，进行溯源分析与取证',107,107,390,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(40,'逆向工程师','进行软件逆向分析、病毒木马分析、移动APP脱壳加固，掌握汇编、调试器（IDA Pro/GDB）及二进制安全',107,107,400,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(41,'安全架构师','规划零信任安全体系，设计身份认证、数据加密、访问控制方案，制定企业级安全标准与架构蓝图',107,107,410,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(42,'嵌入式软件工程师','开发MCU单片机程序（C/C++），掌握RTOS（FreeRTOS/RT-Thread）、嵌入式Linux及硬件驱动开发',108,108,420,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(43,'Linux驱动工程师','开发Linux内核驱动（字符设备/块设备/网络驱动），进行硬件抽象层（HAL）与板级支持包（BSP）开发',108,108,430,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(44,'物联网(IoT)工程师','开发物联网终端应用，掌握MQTT/CoAP协议、边缘计算、LoRa/NB-IoT通信及智能硬件云平台对接',108,108,440,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(45,'FPGA工程师','使用Verilog/VHDL进行FPGA逻辑设计，开发高速数据采集、图像处理或通信协议（PCIe/Ethernet）IP核',108,108,450,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(46,'产品经理（技术型）','负责产品规划与需求分析，具备技术背景能理解API与数据库，主导PRD撰写、原型设计及项目推进',200,200,460,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(47,'UI设计师','负责产品界面视觉设计，掌握Figma/Sketch/PS，建立设计规范与组件库，确保视觉还原度与品牌一致性',200,200,470,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(48,'交互设计师(IXD)','设计用户操作流程与交互原型，进行信息架构设计、可用性测试，优化用户体验路径与交互细节',200,200,480,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(49,'UX研究员','开展用户调研、深度访谈、可用性测试，分析用户行为数据，为产品设计提供定性定量研究支持',200,200,490,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(50,'技术经理/组长','带领5-10人技术团队，负责项目技术方案评审、代码Review、团队培养及跨部门沟通协调',300,300,500,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(51,'架构师','主导系统总体架构设计，进行技术选型、性能容量规划、技术难题攻关，保障架构合理性与先进性',300,300,510,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(52,'研发总监','管理多条产品线技术团队，制定技术战略与研发流程，推动技术创新与工程效能提升，向CTO汇报',300,300,520,1,'2026-02-02 17:58:10','2026-02-02 17:58:10'),(53,'CTO/技术VP','公司技术最高负责人，规划技术战略方向，搭建技术团队与基础设施，支撑业务战略落地与技术创新',300,300,530,1,'2026-02-02 17:58:10','2026-02-02 17:58:10');
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
  `company` varchar(200) NOT NULL COMMENT '所属公司名称',
  `city` varchar(100) NOT NULL COMMENT '城市名称',
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
  KEY `idx_category` (`category_id`),
  KEY `idx_publish` (`publish_time`),
  KEY `idx_company` (`company`),
  KEY `idx_city` (`city`)
) ENGINE=InnoDB AUTO_INCREMENT=72 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci COMMENT='岗位主表';
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `job_post`
--

LOCK TABLES `job_post` WRITE;
/*!40000 ALTER TABLE `job_post` DISABLE KEYS */;
INSERT INTO `job_post` VALUES (1,'BJ001','高级Web前端工程师','字节跳动','北京','海淀区','中关村软件园二期',101,1,25000.00,40000.00,'25-40K','本科','3-5年',NULL,'负责抖音创作者平台前端架构设计与开发，优化首屏加载性能，建设前端工程化体系','[\"精通React/Vue\", \"熟悉Webpack/Vite\", \"有大型SPA开发经验\", \"了解Node.js\"]','[\"六险一金\", \"免费三餐\", \"租房补贴\", \"股票期权\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(2,'SH001','React前端开发','美团','上海','长宁区','金钟路968号凌空SOHO',101,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'参与美团外卖商家端前端开发，负责复杂表单引擎与数据可视化组件开发','[\"2年以上React经验\", \"熟悉TypeScript\", \"了解微前端架构\"]','[\"五险一金\", \"带薪年假\", \"定期体检\", \"餐补\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(3,'GZ001','Vue.js前端工程师','唯品会','广州','海珠区','琶洲互联网创新集聚区',101,1,15000.00,25000.00,'15-25K','本科','1-3年',NULL,'负责电商运营后台系统开发，实现商品管理、订单处理等模块','[\"精通Vue2/Vue3\", \"熟悉Element UI\", \"了解前端性能优化\"]','[\"五险一金\", \"年终奖\", \"节日福利\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(4,'SZ001','移动端H5开发工程师','腾讯','深圳','南山区','深南大道10000号腾讯大厦',101,1,22000.00,38000.00,'22-38K','本科','3-5年',NULL,'负责微信生态内H5活动页开发，解决iOS/Android兼容性难题，优化移动端性能','[\"3年以上移动端开发经验\", \"熟悉移动端适配方案\", \"了解JSBridge通信\"]','[\"六险一金\", \"免费食堂\", \"健身房\", \"年度旅游\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(5,'HZ001','移动端前端工程师','阿里巴巴','杭州','余杭区','文一西路969号西溪园区',101,1,18000.00,30000.00,'18-30K','本科','2-4年',NULL,'参与淘宝特价版APP内嵌H5页面开发，负责复杂交互实现与动画效果','[\"熟悉Vue/React\", \"了解Hybrid开发\", \"有性能优化经验\"]','[\"五险一金\", \"股票期权\", \"无息贷款\", \"免费体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(6,'CD001','微信小程序开发','滴滴出行','成都','高新区','天府软件园',101,1,16000.00,28000.00,'16-28K','本科','2-4年',NULL,'负责滴滴出行小程序开发与维护，优化启动速度与页面流畅度','[\"精通微信小程序开发\", \"熟悉Taro/Uni-app\", \"了解小程序性能优化\"]','[\"五险一金\", \"补充医疗\", \"打车补贴\", \"下午茶\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(7,'WH001','支付宝小程序工程师','蚂蚁集团','杭州','西湖区','西溪路556号',101,1,20000.00,35000.00,'20-35K','本科','3-5年',NULL,'参与支付宝生活号小程序开发，实现支付、会员、营销等核心功能','[\"熟悉支付宝/微信小程序\", \"了解前端安全\", \"有金融项目经验优先\"]','[\"六险一金\", \"期权激励\", \"租房补贴\", \"带薪年假\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(8,'BJ002','Flutter开发工程师','百度','北京','海淀区','上地十街10号百度大厦',101,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责百度网盘跨平台客户端开发，使用Flutter实现iOS/Android双端复用','[\"精通Flutter/Dart\", \"熟悉原生开发\", \"了解状态管理方案\"]','[\"五险一金\", \"免费早餐\", \"健身房\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(9,'SH002','React Native工程师','小红书','上海','黄浦区','马当路388号SOHO复兴广场',101,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'参与小红书APP核心模块开发，使用RN实现社交、内容发布等功能','[\"2年以上RN经验\", \"熟悉iOS/Android原生\", \"了解热更新机制\"]','[\"六险一金\", \"带薪年假\", \"节日礼品\", \"弹性打卡\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(10,'SZ002','前端架构师','大疆创新','深圳','南山区','仙元路55号大疆天空之城',101,1,40000.00,70000.00,'40-70K','本科','5-10年',NULL,'负责大疆官网及电商系统前端架构升级，设计微前端方案，建设前端基础设施','[\"5年以上前端经验\", \"精通前端工程化\", \"有大型架构设计经验\", \"技术视野开阔\"]','[\"五险一金\", \"高额年终奖\", \"股权激励\", \"免费公寓\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(11,'BJ003','前端技术专家','京东','北京','大兴区','亦庄经济开发区科创十一街',101,1,35000.00,60000.00,'35-60K','本科','5-8年',NULL,'主导京东零售前端技术体系建设，推动低代码平台与组件库建设','[\"精通前端全栈技术\", \"有团队管理经验\", \"熟悉电商业务\"]','[\"六险一金\", \"补充公积金\", \"内购优惠\", \"定期体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(12,'SH003','Node.js全栈工程师','哔哩哔哩','上海','杨浦区','政立路485号国正中心',101,1,22000.00,40000.00,'22-40K','本科','3-5年',NULL,'负责B站创作中心全栈开发，使用Node.js + React实现服务端渲染与BFF层','[\"精通Node.js\", \"熟悉React/Vue\", \"了解微服务架构\", \"有SSR经验\"]','[\"五险一金\", \"带薪年假\", \"二次元文化\", \"免费工作餐\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(13,'GZ002','Node.js高级开发','网易','广州','天河区','科韵路16号广州信息港',101,1,18000.00,32000.00,'18-32K','本科','2-4年',NULL,'参与网易云音乐Node.js服务端开发，负责高并发API设计与实现','[\"精通Node.js/TypeScript\", \"熟悉MySQL/Redis\", \"了解消息队列\"]','[\"五险一金\", \"年终奖\", \"免费三餐\", \"健身房\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(14,'HZ002','Java高级开发工程师','阿里巴巴','杭州','余杭区','文一西路969号',102,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责淘宝交易核心系统开发，参与双11大促技术保障，设计高并发分布式方案','[\"精通Java/Spring\", \"熟悉分布式系统\", \"了解微服务治理\", \"有电商经验\"]','[\"六险一金\", \"股票期权\", \"无息购房贷款\", \"免费体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(15,'BJ004','Java开发工程师','美团','北京','朝阳区','望京东路4号恒电大厦',102,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'参与美团外卖订单系统开发，负责订单生命周期管理与状态机设计','[\"2年以上Java开发\", \"熟悉Spring Boot\", \"了解MySQL优化\", \"有Redis经验\"]','[\"五险一金\", \"餐补\", \"定期团建\", \"技术分享\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(16,'CD002','Java后端开发','成都字节','成都','高新区','天府四街158号',102,1,18000.00,30000.00,'18-30K','本科','2-4年',NULL,'负责企业协作平台后端开发，实现IM、文档协同等核心功能模块','[\"精通Java\", \"熟悉Netty\", \"了解分布式存储\", \"有高并发经验\"]','[\"六险一金\", \"免费三餐\", \"租房补贴\", \"年度体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(17,'SZ003','Java资深开发','平安科技','深圳','福田区','益田路5033号平安金融中心',102,1,25000.00,40000.00,'25-40K','本科','4-6年',NULL,'参与平安银行核心系统建设，负责金融级分布式事务与风控系统设计','[\"4年以上Java经验\", \"熟悉金融系统\", \"了解分布式事务\", \"有银行项目经验\"]','[\"六险二金\", \"补充医疗\", \"节日福利\", \"培训机会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(18,'WH002','Java开发工程师','小米','武汉','东湖高新区','光谷大道77号光谷金融港',102,1,15000.00,25000.00,'15-25K','本科','1-3年',NULL,'参与小米IoT平台后端开发，负责设备接入与消息推送服务','[\"1年以上Java经验\", \"熟悉Spring Cloud\", \"了解MQTT协议\"]','[\"五险一金\", \"股票期权\", \"餐补\", \"健身房\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(19,'BJ005','微服务架构师','快手','北京','海淀区','上地西路6号快手总部',102,1,45000.00,80000.00,'45-80K','本科','5-10年',NULL,'负责快手电商微服务架构演进，设计Service Mesh方案，优化服务治理能力','[\"5年以上架构经验\", \"精通微服务\", \"熟悉K8s/Istio\", \"有大规模系统经验\"]','[\"六险一金\", \"高额期权\", \"免费三餐\", \"租房补贴\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(20,'SH004','分布式架构师','拼多多','上海','长宁区','娄山关路533号金虹桥国际中心',102,1,50000.00,90000.00,'50-90K','本科','5-10年',NULL,'主导拼多多推荐系统架构设计，支撑亿级DAU高并发场景','[\"精通分布式系统\", \"熟悉大数据生态\", \"了解机器学习工程\", \"有电商背景\"]','[\"六险一金\", \"股票期权\", \"年度旅游\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(21,'BJ006','Python高级开发工程师','字节跳动','北京','海淀区','中关村软件园',102,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责飞书多维表格后端开发，使用Python + Django实现复杂业务逻辑与数据同步','[\"精通Python\", \"熟悉Django/FastAPI\", \"了解分布式系统\", \"有SaaS经验\"]','[\"六险一金\", \"免费三餐\", \"租房补贴\", \"股票期权\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(22,'SH005','Python开发工程师','饿了么','上海','普陀区','金沙江路1518弄近铁城市广场',102,1,18000.00,32000.00,'18-32K','本科','2-4年',NULL,'参与配送算法调度系统开发，使用Python进行路径规划与ETA预测','[\"2年以上Python经验\", \"熟悉算法与数据结构\", \"了解机器学习基础\"]','[\"五险一金\", \"餐补\", \"定期体检\", \"团建活动\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(23,'SZ004','Go开发工程师','腾讯','深圳','南山区','深南大道10000号',102,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责微信支付核心网关开发，使用Go实现高并发支付路由与风控系统','[\"精通Go语言\", \"熟悉高并发编程\", \"了解分布式存储\", \"有支付经验\"]','[\"六险一金\", \"免费食堂\", \"健身房\", \"年度旅游\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(24,'BJ007','Go高级开发','猿辅导','北京','朝阳区','望京SOHO塔3',102,1,28000.00,50000.00,'28-50K','本科','3-5年',NULL,'参与在线教育直播系统开发，使用Go实现实时音视频信令服务','[\"3年以上Go经验\", \"熟悉WebSocket\", \"了解RTC技术\", \"有高并发经验\"]','[\"六险一金\", \"免费晚餐\", \"租房补贴\", \"期权激励\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(25,'HZ003','Go后端工程师','网易严选','杭州','滨江区','网商路599号',102,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'负责电商供应链系统开发，使用Go重构Java服务，提升系统性能','[\"精通Go语言\", \"熟悉gRPC\", \"了解微服务\", \"有电商经验\"]','[\"五险一金\", \"年终奖\", \"免费三餐\", \"健身房\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(26,'GZ003','C++开发工程师','微信事业群','广州','海珠区','TIT创意园',102,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责微信基础组件开发，使用C++实现高性能网络库与存储引擎','[\"精通C++\", \"熟悉Linux系统编程\", \"了解网络协议\", \"有高性能系统经验\"]','[\"六险一金\", \"免费三餐\", \"租房补贴\", \"股票期权\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(27,'SH006','C++游戏服务器开发','米哈游','上海','徐汇区','漕河泾开发区',102,1,30000.00,60000.00,'30-60K','本科','3-5年',NULL,'参与原神服务端开发，使用C++实现游戏逻辑服务器与实时通信系统','[\"精通C++11/14\", \"熟悉游戏开发\", \"了解ECS架构\", \"有MMO经验\"]','[\"六险一金\", \"高额年终奖\", \"游戏周边\", \"二次元氛围\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(28,'BJ008','PHP高级开发工程师','新浪微博','北京','海淀区','中关村软件园',102,1,20000.00,35000.00,'20-35K','本科','3-5年',NULL,'负责微博Feed流系统维护与优化，使用PHP + Swoole实现高并发服务','[\"精通PHP/Swoole\", \"熟悉MySQL优化\", \"了解缓存策略\", \"有社交平台经验\"]','[\"五险一金\", \"餐补\", \"定期体检\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(29,'BJ009','Android高级开发工程师','字节跳动','北京','海淀区','中关村软件园',103,1,28000.00,50000.00,'28-50K','本科','3-5年',NULL,'负责抖音APP核心功能开发，优化启动速度与内存占用，研究鸿蒙系统适配','[\"精通Kotlin/Java\", \"熟悉Android性能优化\", \"了解鸿蒙开发\", \"有大厂经验\"]','[\"六险一金\", \"免费三餐\", \"租房补贴\", \"股票期权\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(30,'SH007','Android开发工程师','携程','上海','长宁区','金钟路968号',103,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'参与携程旅行APP开发，负责酒店预订模块重构与性能优化','[\"2年以上Android经验\", \"熟悉Jetpack组件\", \"了解组件化开发\"]','[\"五险一金\", \"带薪年假\", \"旅游基金\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(31,'SZ005','iOS高级开发工程师','腾讯','深圳','南山区','深南大道10000号',103,1,28000.00,50000.00,'28-50K','本科','3-5年',NULL,'负责微信iOS客户端开发，研究SwiftUI新特性，优化包体积与启动速度','[\"精通Swift/Objective-C\", \"熟悉iOS性能优化\", \"了解SwiftUI\", \"有大型APP经验\"]','[\"六险一金\", \"免费食堂\", \"健身房\", \"年度旅游\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(32,'HZ004','iOS开发工程师','网易云音乐','杭州','滨江区','网商路599号',103,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'参与网易云音乐iOS版开发，负责播放器核心模块与音频特效实现','[\"2年以上iOS经验\", \"熟悉AVFoundation\", \"了解音频处理\", \"热爱音乐\"]','[\"五险一金\", \"年终奖\", \"免费三餐\", \"音乐会门票\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(33,'BJ010','鸿蒙开发工程师','华为','北京','海淀区','上地信息路3号',103,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责鸿蒙原生应用开发，研究分布式能力与多设备协同特性','[\"精通ArkTS\", \"熟悉HarmonyOS SDK\", \"了解分布式软总线\", \"有鸿蒙项目经验\"]','[\"六险一金\", \"股票期权\", \"免费宿舍\", \"食堂补贴\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(34,'CD003','Unity游戏开发工程师','完美世界','成都','高新区','天府软件园',103,1,18000.00,35000.00,'18-35K','本科','2-4年',NULL,'参与MMORPG手游客户端开发，使用Unity实现战斗系统与UI框架','[\"精通Unity3D\", \"熟悉C#\", \"了解游戏引擎原理\", \"有上线项目经验\"]','[\"五险一金\", \"项目奖金\", \"游戏福利\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(35,'BJ011','大数据开发工程师','百度','北京','海淀区','上地十街10号',104,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责百度地图实时数据处理平台开发，使用Flink实现轨迹数据实时计算','[\"精通Spark/Flink\", \"熟悉Hadoop生态\", \"了解实时计算\", \"有地理信息经验\"]','[\"六险一金\", \"免费早餐\", \"健身房\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(36,'SH008','数据仓库工程师','拼多多','上海','长宁区','娄山关路533号',104,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'建设拼多多电商数据仓库，设计维度模型，优化ClickHouse查询性能','[\"精通数据仓库理论\", \"熟悉ClickHouse/Doris\", \"了解ETL流程\", \"有电商经验\"]','[\"六险一金\", \"股票期权\", \"年度旅游\", \"技术分享\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(37,'HZ005','机器学习工程师','阿里巴巴','杭州','余杭区','文一西路969号',104,1,30000.00,60000.00,'30-60K','硕士','3-5年',NULL,'负责淘宝推荐算法工程化，实现特征工程、模型训练与在线Serving','[\"精通Python/TensorFlow\", \"熟悉推荐系统\", \"了解大规模机器学习\", \"有电商背景\"]','[\"六险一金\", \"股票期权\", \"无息贷款\", \"免费体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(38,'SZ006','深度学习工程师','商汤科技','深圳','南山区','高新南一道009号',104,1,35000.00,70000.00,'35-70K','硕士','3-5年',NULL,'研发计算机视觉算法，优化人脸识别模型在边缘设备的部署效率','[\"精通PyTorch\", \"熟悉CV算法\", \"了解模型压缩\", \"有顶会论文\"]','[\"六险一金\", \"期权激励\", \"租房补贴\", \"技术前沿\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(39,'BJ012','推荐算法工程师','快手','北京','海淀区','上地西路6号',104,1,35000.00,70000.00,'35-70K','硕士','3-5年',NULL,'负责快手短视频推荐算法优化，提升用户时长与互动率','[\"精通推荐算法\", \"熟悉深度学习\", \"了解大规模系统\", \"有短视频经验\"]','[\"六险一金\", \"高额期权\", \"免费三餐\", \"租房补贴\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(40,'SH009','NLP工程师','科大讯飞','上海','浦东新区','张江高科技园区',104,1,25000.00,50000.00,'25-50K','硕士','3-5年',NULL,'研发智能客服对话系统，基于大模型进行微调与Prompt工程优化','[\"精通NLP技术\", \"熟悉BERT/GPT\", \"了解大模型微调\", \"有对话系统经验\"]','[\"五险一金\", \"项目奖金\", \"培训机会\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(41,'CD004','计算机视觉工程师','旷视科技','成都','高新区','天府软件园',104,1,20000.00,40000.00,'20-40K','本科','2-4年',NULL,'开发工业质检视觉系统，实现缺陷检测与OCR识别算法落地','[\"熟悉OpenCV\", \"了解深度学习\", \"有CV项目经验\", \"了解模型部署\"]','[\"五险一金\", \"年终奖\", \"技术分享\", \"定期体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(42,'BJ013','数据分析师','京东','北京','大兴区','亦庄经济开发区',104,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'负责京东零售业务数据分析，搭建指标体系，输出业务洞察报告','[\"精通SQL/Python\", \"熟悉Tableau\", \"了解统计学\", \"有电商分析经验\"]','[\"六险一金\", \"补充公积金\", \"内购优惠\", \"定期体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(43,'HZ006','数据产品经理','网易','杭州','滨江区','网商路599号',104,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责网易有数BI产品规划，设计数据可视化方案与埋点体系','[\"熟悉数据产品\", \"了解数据分析\", \"有BI工具经验\", \"具备技术背景\"]','[\"五险一金\", \"年终奖\", \"免费三餐\", \"健身房\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(44,'BJ014','高级测试工程师','美团','北京','朝阳区','望京东路4号',105,1,20000.00,35000.00,'20-35K','本科','3-5年',NULL,'负责美团外卖核心链路质量保障，设计测试策略，推进质量左移','[\"3年以上测试经验\", \"熟悉测试方法论\", \"了解自动化测试\", \"有业务测试经验\"]','[\"五险一金\", \"餐补\", \"定期团建\", \"技术分享\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(45,'SH010','自动化测试工程师','哔哩哔哩','上海','杨浦区','政立路485号',105,1,18000.00,32000.00,'18-32K','本科','2-4年',NULL,'开发B站APP自动化测试框架，使用Appium实现UI自动化与性能监控','[\"精通Python/Java\", \"熟悉Selenium/Appium\", \"了解CI/CD\", \"有APP测试经验\"]','[\"五险一金\", \"二次元文化\", \"免费工作餐\", \"带薪年假\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(46,'SZ007','性能测试工程师','腾讯','深圳','南山区','深南大道10000号',105,1,22000.00,40000.00,'22-40K','本科','3-5年',NULL,'负责王者荣耀服务器性能测试，设计压测方案，分析系统瓶颈','[\"精通JMeter/LoadRunner\", \"熟悉Linux性能分析\", \"了解游戏服务器\", \"有大厂经验\"]','[\"六险一金\", \"免费食堂\", \"健身房\", \"年度旅游\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(47,'BJ015','测试开发工程师','字节跳动','北京','海淀区','中关村软件园',105,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'开发质量保障平台，建设Mock服务与自动化测试工具链','[\"精通Java/Python\", \"熟悉测试框架开发\", \"了解DevOps\", \"有平台开发经验\"]','[\"六险一金\", \"免费三餐\", \"租房补贴\", \"股票期权\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(48,'GZ004','安全测试工程师','唯品会','广州','海珠区','琶洲互联网创新集聚区',105,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'负责电商平台安全测试，进行渗透测试与漏洞挖掘，建设安全扫描流水线','[\"熟悉渗透测试\", \"了解Web安全\", \"掌握Burp Suite\", \"有安全认证优先\"]','[\"五险一金\", \"年终奖\", \"节日福利\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(49,'BJ016','运维工程师','小米','北京','海淀区','清河中街68号',106,1,15000.00,25000.00,'15-25K','本科','2-4年',NULL,'负责小米云服务运维，处理线上故障，优化监控告警体系','[\"熟悉Linux系统\", \"了解Shell/Python\", \"掌握Nginx/MySQL\", \"有云平台经验\"]','[\"五险一金\", \"股票期权\", \"餐补\", \"健身房\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(50,'SH011','DevOps工程师','蔚来汽车','上海','嘉定区','安亭镇安拓路56号',106,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'建设汽车软件CI/CD流水线，推进IaC与GitOps实践，提升研发效能','[\"精通K8s/Docker\", \"熟悉Jenkins/GitLab CI\", \"了解Terraform\", \"有汽车行业经验\"]','[\"六险一金\", \"股票期权\", \"购车优惠\", \"免费工作餐\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(51,'HZ007','SRE工程师','阿里巴巴','杭州','余杭区','文一西路969号',106,1,30000.00,55000.00,'30-55K','本科','4-6年',NULL,'负责阿里云产品稳定性保障，制定SLO体系，主导故障应急响应','[\"精通SRE体系\", \"熟悉分布式系统\", \"了解云原生技术\", \"有大厂SRE经验\"]','[\"六险一金\", \"股票期权\", \"无息贷款\", \"免费体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(52,'BJ017','云原生工程师','青云科技','北京','朝阳区','望京东路8号锐创国际中心',106,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责Kubernetes平台开发与维护，实现多集群管理与Service Mesh落地','[\"精通K8s生态\", \"熟悉Go/Python\", \"了解容器网络\", \"有云厂商经验\"]','[\"五险一金\", \"技术前沿\", \"弹性工作\", \"定期体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(53,'CD005','数据库管理员','成都银行','成都','锦江区','顺城大街154号',106,1,20000.00,35000.00,'20-35K','本科','3-5年',NULL,'负责银行核心系统数据库管理，进行Oracle/MySQL性能调优与容灾建设','[\"精通Oracle/MySQL\", \"熟悉数据库优化\", \"了解金融系统\", \"有银行经验\"]','[\"六险二金\", \"补充医疗\", \"节日福利\", \"稳定工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(54,'BJ018','网络工程师','中国移动','北京','东城区','东直门南大街7号',106,1,18000.00,30000.00,'18-30K','本科','3-5年',NULL,'负责运营商核心网络运维，配置路由器/交换机，保障网络高可用','[\"熟悉TCP/IP\", \"掌握华为/思科设备\", \"了解SDN\", \"有运营商经验\"]','[\"六险二金\", \"补充医疗\", \"节日福利\", \"工作稳定\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(55,'SH012','网络安全工程师','交通银行','上海','浦东新区','银城中路188号',107,1,22000.00,40000.00,'22-40K','本科','3-5年',NULL,'负责银行网络安全防护，配置WAF/IPS，进行安全加固与合规审计','[\"熟悉网络安全\", \"了解等保2.0\", \"掌握安全设备\", \"有金融经验\"]','[\"六险二金\", \"补充公积金\", \"节日福利\", \"培训机会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(56,'SZ008','渗透测试工程师','腾讯安全','深圳','南山区','深南大道10000号',107,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'进行腾讯产品安全测试，挖掘Web/APP漏洞，研究APT攻击手法','[\"精通渗透测试\", \"熟悉代码审计\", \"了解漏洞挖掘\", \"有CTF经验\"]','[\"六险一金\", \"免费食堂\", \"健身房\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(57,'BJ019','安全运维工程师','奇安信','北京','西城区','西直门外南路26号',107,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'负责政企客户SOC运营，进行威胁情报分析与应急响应处置','[\"熟悉安全运营\", \"了解威胁情报\", \"掌握日志分析\", \"有安全厂商经验\"]','[\"五险一金\", \"项目奖金\", \"培训机会\", \"弹性工作\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(58,'GZ005','逆向工程师','腾讯科恩实验室','广州','天河区','华穗路406号',107,1,30000.00,60000.00,'30-60K','本科','3-5年',NULL,'进行移动端APP安全研究，进行脱壳加固分析与漏洞挖掘','[\"精通汇编/C++\", \"熟悉IDA Pro\", \"了解移动安全\", \"有漏洞挖掘经验\"]','[\"六险一金\", \"高额奖金\", \"技术前沿\", \"自由氛围\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(59,'SH013','安全架构师','蚂蚁集团','上海','浦东新区','民生路1199号',107,1,50000.00,90000.00,'50-90K','本科','5-10年',NULL,'设计支付宝零信任安全架构，规划身份认证与数据安全体系','[\"5年以上安全经验\", \"精通安全架构\", \"熟悉金融安全\", \"有大型系统经验\"]','[\"六险一金\", \"股票期权\", \"租房补贴\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(60,'SZ009','嵌入式软件工程师','大疆创新','深圳','南山区','仙元路55号',108,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责无人机飞控系统开发，使用C/C++实现姿态解算与电机控制','[\"精通C/C++\", \"熟悉RTOS\", \"了解飞行控制\", \"有硬件基础\"]','[\"五险一金\", \"高额年终奖\", \"股权激励\", \"免费公寓\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(61,'BJ020','Linux驱动工程师','小米','北京','海淀区','清河中街68号',108,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责手机/IoT设备Linux驱动开发，进行内核移植与性能优化','[\"精通Linux驱动\", \"熟悉ARM架构\", \"了解内核原理\", \"有手机开发经验\"]','[\"六险一金\", \"股票期权\", \"餐补\", \"健身房\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(62,'HZ008','物联网工程师','海康威视','杭州','滨江区','阡陌路555号',108,1,18000.00,32000.00,'18-32K','本科','2-4年',NULL,'开发智能安防物联网平台，实现设备接入与边缘计算节点管理','[\"熟悉MQTT/CoAP\", \"了解嵌入式开发\", \"掌握云平台对接\", \"有安防经验\"]','[\"五险一金\", \"年终奖\", \"免费三餐\", \"技术分享\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(63,'CD006','FPGA工程师','华为成都','成都','高新区','西部园区',108,1,25000.00,45000.00,'25-45K','硕士','3-5年',NULL,'负责通信设备FPGA逻辑设计，开发高速数据处理IP核','[\"精通Verilog/VHDL\", \"熟悉FPGA开发流程\", \"了解通信协议\", \"有芯片设计经验\"]','[\"六险一金\", \"股票期权\", \"免费宿舍\", \"食堂补贴\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(64,'BJ021','技术产品经理','百度','北京','海淀区','上地十街10号',200,1,25000.00,45000.00,'25-45K','本科','3-5年',NULL,'负责百度AI开放平台产品规划，设计API与SDK产品方案','[\"熟悉产品方法论\", \"了解AI技术\", \"有B端产品经验\", \"具备技术背景\"]','[\"六险一金\", \"免费早餐\", \"健身房\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(65,'SH014','UI设计师','小红书','上海','黄浦区','马当路388号',200,1,18000.00,30000.00,'18-30K','本科','2-4年',NULL,'负责小红书APP界面设计，建立设计规范，推动组件库建设','[\"精通Figma/Sketch\", \"熟悉设计系统\", \"了解移动端设计\", \"有互联网经验\"]','[\"六险一金\", \"年轻氛围\", \"节日礼品\", \"弹性打卡\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(66,'SZ010','交互设计师','腾讯','深圳','南山区','深南大道10000号',200,1,20000.00,35000.00,'20-35K','本科','2-4年',NULL,'设计微信新功能交互流程，进行用户研究与可用性测试','[\"熟悉交互设计\", \"了解用户研究\", \"掌握原型工具\", \"有社交产品经验\"]','[\"六险一金\", \"免费食堂\", \"健身房\", \"年度旅游\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(67,'HZ009','UX研究员','阿里巴巴','杭州','余杭区','文一西路969号',200,1,20000.00,35000.00,'20-35K','硕士','2-4年',NULL,'开展淘宝用户体验研究，进行深度访谈与数据分析，输出研究报告','[\"熟悉用研方法\", \"了解数据分析\", \"掌握SPSS/Python\", \"有电商研究经验\"]','[\"六险一金\", \"股票期权\", \"无息贷款\", \"免费体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(68,'BJ022','前端技术经理','京东','北京','大兴区','亦庄经济开发区',300,1,35000.00,60000.00,'35-60K','本科','5-8年',NULL,'带领10人前端团队，负责京东零售前端技术规划与团队建设','[\"5年以上前端经验\", \"有团队管理经验\", \"熟悉电商业务\", \"具备技术视野\"]','[\"六险一金\", \"补充公积金\", \"内购优惠\", \"定期体检\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(69,'SH015','系统架构师','拼多多','上海','长宁区','娄山关路533号',300,1,50000.00,90000.00,'50-90K','本科','5-10年',NULL,'主导拼多多交易系统架构设计，解决高并发场景技术难题','[\"精通分布式架构\", \"有大规模系统经验\", \"熟悉电商业务\", \"技术领导力强\"]','[\"六险一金\", \"股票期权\", \"年度旅游\", \"技术大会\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(70,'SZ011','研发总监','腾讯音乐','深圳','南山区','深南大道10000号',300,1,60000.00,120000.00,'60-120K','本科','8-15年',NULL,'管理QQ音乐技术团队，制定技术战略，推动音视频技术创新','[\"8年以上技术经验\", \"有大型团队管理经验\", \"熟悉音视频技术\", \"战略思维强\"]','[\"六险一金\", \"高额期权\", \"免费食堂\", \"年度旅游\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15'),(71,'HZ010','CTO','某独角兽公司','杭州','余杭区','未来科技城',300,1,80000.00,200000.00,'80-200K','本科','10年以上',NULL,'全面负责公司技术战略，搭建技术团队，支撑业务快速扩张','[\"10年以上技术经验\", \"有创业/独角兽经验\", \"全栈技术背景\", \"商业敏感度高\"]','[\"股权激励\", \"高额年薪\", \"决策权\", \"成长空间\"]',NULL,NULL,1,'2026-02-02 22:03:15','2026-02-02 22:03:15');
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

-- Dump completed on 2026-02-02 22:04:38
