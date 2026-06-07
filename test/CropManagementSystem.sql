/*
 Navicat Premium Dump SQL

 Source Server         : wsl
 Source Server Type    : MySQL
 Source Server Version : 80045 (8.0.45-0ubuntu0.24.04.1)
 Source Host           : localhost:3306
 Source Schema         : CropManagementSystem

 Target Server Type    : MySQL
 Target Server Version : 80045 (8.0.45-0ubuntu0.24.04.1)
 File Encoding         : 65001

 Date: 16/04/2026 18:35:28
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for agrochemical_categories
-- ----------------------------
DROP TABLE IF EXISTS `agrochemical_categories`;
CREATE TABLE `agrochemical_categories`  (
  `id` int UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '分类名称',
  `parent_id` bigint NULL DEFAULT NULL,
  `description` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '分类描述',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_parent_name`(`parent_id` ASC, `name` ASC) USING BTREE,
  INDEX `idx_parent_id`(`parent_id` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 40 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '农资分类表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of agrochemical_categories
-- ----------------------------
INSERT INTO `agrochemical_categories` VALUES (1, '杀虫剂', 36, '杀虫剂是农业生产中用于防治各种害虫的重要农药', '2026-03-31 09:01:25', '2026-03-31 15:53:28');
INSERT INTO `agrochemical_categories` VALUES (2, '有机磷类杀虫剂', 36, '有机磷类杀虫剂是杀虫剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 15:53:35');
INSERT INTO `agrochemical_categories` VALUES (3, '氨基甲酸酯类杀虫剂', 1, '氨基甲酸酯类杀虫剂是杀虫剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (4, '拟除虫菊酯类杀虫剂', 1, '拟除虫菊酯类杀虫剂是杀虫剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (5, '新烟碱类杀虫剂', 1, '新烟碱类杀虫剂是杀虫剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (6, '双酰胺类杀虫剂', 1, '双酰胺类杀虫剂是杀虫剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (7, '生物源杀虫剂', 1, '生物源杀虫剂是杀虫剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (8, '杀菌剂', NULL, '杀菌剂是农业生产中用于预防和治疗植物病害的农药', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (9, '三唑类杀菌剂', 8, '三唑类杀菌剂是杀菌剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (10, '甲氧基丙烯酸酯类杀菌剂', 8, '甲氧基丙烯酸酯类杀菌剂是杀菌剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (11, 'SDHI类杀菌剂', 8, 'SDHI类杀菌剂是杀菌剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (12, '无机杀菌剂', 8, '无机杀菌剂是杀菌剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (13, '有机硫杀菌剂', 8, '有机硫杀菌剂是杀菌剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (14, '苯并咪唑类杀菌剂', 8, '苯并咪唑类杀菌剂是杀菌剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (15, '除草剂', NULL, '除草剂是农业生产中用于防除农田杂草的农药', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (16, '灭生性除草剂', 15, '灭生性除草剂是除草剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (17, '选择性除草剂', 15, '选择性除草剂是除草剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (18, 'HPPD抑制剂类除草剂', 15, 'HPPD抑制剂类除草剂是除草剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (19, '磺酰脲类除草剂', 15, '磺酰脲类除草剂是除草剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (20, '酰胺类除草剂', 15, '酰胺类除草剂是除草剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (21, '三嗪类除草剂', 15, '三嗪类除草剂是除草剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (22, '植物生长调节剂', NULL, '植物生长调节剂是农业生产中用于调节植物生长发育的农药', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (23, '生长素类调节剂', 22, '生长素类调节剂是植物生长调节剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (24, '细胞分裂素类调节剂', 22, '细胞分裂素类调节剂是植物生长调节剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (25, '赤霉素类调节剂', 22, '赤霉素类调节剂是植物生长调节剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (26, '乙烯释放剂', 22, '乙烯释放剂是植物生长调节剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (27, '芸苔素内酯类', 22, '芸苔素内酯类是植物生长调节剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (28, 'S-诱抗素类', 22, 'S-诱抗素类是植物生长调节剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (29, '杀螨剂', NULL, '杀螨剂是农业生产中用于防治螨类（红蜘蛛）的农药', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (30, '触杀型杀螨剂', 29, '触杀型杀螨剂是杀螨剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (31, '内吸型杀螨剂', 29, '内吸型杀螨剂是杀螨剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (32, '生物杀螨剂', 29, '生物杀螨剂是杀螨剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (33, '杀鼠剂', NULL, '杀鼠剂是农业生产中用于防治鼠害的农药', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (34, '抗凝血类杀鼠剂', 33, '抗凝血类杀鼠剂是杀鼠剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (35, '急性杀鼠剂', 33, '急性杀鼠剂是杀鼠剂的一个重要分类', '2026-03-31 09:01:25', '2026-03-31 09:01:25');
INSERT INTO `agrochemical_categories` VALUES (36, '农药', NULL, '', '2026-03-31 15:53:00', '2026-03-31 15:53:00');
INSERT INTO `agrochemical_categories` VALUES (37, '化肥', NULL, '', '2026-03-31 15:53:08', '2026-03-31 15:53:08');
INSERT INTO `agrochemical_categories` VALUES (38, '农机', NULL, '', '2026-03-31 15:53:14', '2026-03-31 15:53:14');
INSERT INTO `agrochemical_categories` VALUES (39, '农具', NULL, '', '2026-03-31 15:53:20', '2026-03-31 15:53:20');

-- ----------------------------
-- Table structure for agrochemicals
-- ----------------------------
DROP TABLE IF EXISTS `agrochemicals`;
CREATE TABLE `agrochemicals`  (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `product_code` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '商品编号',
  `category_id` int UNSIGNED NOT NULL COMMENT '分类ID',
  `product_name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '商品全称',
  `brand` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '品牌',
  `monthly_sales` int UNSIGNED NULL DEFAULT 0 COMMENT '月销量',
  `price` decimal(10, 2) NULL DEFAULT NULL COMMENT '价格',
  `manufacturer` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '生产厂家',
  `registration_no` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '农药登记证号',
  `formulation` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '剂型代码/名称',
  `content_spec` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '含量规格',
  `main_image` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '产品展示图 URL',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '商品描述',
  `purchase_links` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '适用农作物',
  `use_crops` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '多平台购买链接',
  `usage_method` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '用法说明',
  `precautions` text CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL COMMENT '注意事项',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` datetime NULL DEFAULT NULL COMMENT '软删除时间戳',
  PRIMARY KEY (`id`) USING BTREE,
  INDEX `idx_registration_no`(`registration_no` ASC) USING BTREE,
  INDEX `idx_category_id`(`category_id` ASC) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at` ASC) USING BTREE,
  CONSTRAINT `fk_agro_category` FOREIGN KEY (`category_id`) REFERENCES `agrochemical_categories` (`id`) ON DELETE RESTRICT ON UPDATE RESTRICT
) ENGINE = InnoDB AUTO_INCREMENT = 101 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '农资商品信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of agrochemicals
-- ----------------------------
INSERT INTO `agrochemicals` VALUES (1, NULL, 9, '敌敌畏', '禾信优选', 2000, 23.00, '山东华阳农药化工集团', 'PD20090001', '乳油', '80%', 'https://att.191.cn/attachment/Mon_2301/17_21_470ed1bc75ea181f2.jpg?72', '好用耐用', 'https://example.com/buy/1', '水稻、小麦、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (2, NULL, 4, '毒死蜱', '禾信优选', 2000, 23.00, '江苏扬农化工股份有限公司', 'PD20090002', '乳油', '40%', 'http://cdncha.191.cn/ueditor_cha/20231115/1700025883878081.jpg', '好用耐用', 'https://example.com/buy/2', '水稻、玉米、大豆', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (3, NULL, 17, '辛硫磷', '禾信优选', 2000, 23.00, '安徽华星化工有限公司', 'PD20090003', '乳油', '50%', 'https://image.cnhnb.com/change/image/tos/pro/jpg/details/2025/03/05/f6583208057b4037aa93035f161d6926.jpg?x-tos-process=image/resize,m_fill,w_525,h_525/interlace,1/quality,Q_100/format,jpg', '好用耐用', 'https://example.com/buy/3', '小麦、玉米、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (4, NULL, 25, '敌百虫', '禾信优选', 2000, 23.00, '湖南海利化工股份有限公司', 'PD20090004', '可溶性粉剂', '90%', 'http://cdncha.191.cn/Base/Mon_2206/62ac155fa521b.png', '好用耐用', 'https://example.com/buy/4', '水稻、棉花、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (5, NULL, 21, '乐果', '禾信优选', 2000, 23.00, '江苏长青农化股份有限公司', 'PD20090005', '乳油', '40%', 'http://www.jscq.com/Uploads/_thumb/400x400_65a8e56b3c680.jpg', '好用耐用', 'https://example.com/buy/5', '棉花、果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (6, NULL, 4, '呋喃丹', '禾信优选', 2000, 23.00, '河北威远生物化工有限公司', 'PD20090006', '颗粒剂', '3%', 'http://mall-sourcing-prod-rongchuang.oss-cn-beijing.aliyuncs.com/V1.0.0/goods/5C4CDC47D42546A49BB7E4CE1FF7CD28.jpeg', '好用耐用', 'https://example.com/buy/6', '水稻、玉米、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (7, NULL, 32, '涕灭威', '禾信优选', 2000, 23.00, '山东潍坊润丰化工股份有限公司', 'PD20090007', '颗粒剂', '5%', 'http://cdncha.191.cn/Base/Mon_2210/635104c406820.png', '好用耐用', 'https://example.com/buy/7', '棉花、花生', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (8, NULL, 14, '异丙威', '禾信优选', 2000, 23.00, '江苏快达农化股份有限公司', 'PD20090008', '乳油', '20%', 'http://cdncha.191.cn/ueditor_cha/20231031/1698724296722462.jpg', '好用耐用', 'https://example.com/buy/8', '水稻、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (9, NULL, 31, '灭多威', '禾信优选', 2000, 23.00, '山东滨农科技有限公司', 'PD20090009', '可溶性粉剂', '40%', 'http://www.heyiagro.com/upload/201783161718.jpg', '好用耐用', 'https://example.com/buy/9', '棉花、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (10, NULL, 13, '克百威', '禾信优选', 2000, 23.00, '湖北沙隆达股份有限公司', 'PD20090010', '颗粒剂', '3%', 'https://att.191.cn/attachment/Mon_2006/365_358242_99f77fb8e1e2217.jpg', '好用耐用', 'https://example.com/buy/10', '水稻、玉米', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (11, NULL, 34, '氯氰菊酯', '禾信优选', 2000, 23.00, '广东立威化工有限公司', 'PD20090011', '乳油', '10%', 'http://mall-sourcing-prod-rongchuang.oss-cn-beijing.aliyuncs.com/V1.0.0/goods/B1BEDE65E5B64920A6A3217DE7F5AEED.jpeg?x-oss-process=image/resize,m_fill,h_400,w_400/rotate,0', '好用耐用', 'https://example.com/buy/11', '棉花、蔬菜、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (12, NULL, 23, '溴氰菊酯', '禾信优选', 2000, 23.00, '天津农药股份有限公司', 'PD20090012', '乳油', '2.5%', 'http://www.zpnongyao.com/newUpload/zpnongyao/20210729/162753730055887bbca40.jpg?from=90', '好用耐用', 'https://example.com/buy/12', '棉花、蔬菜、茶树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (13, NULL, 31, '氰戊菊酯', '禾信优选', 2000, 23.00, '江苏辉丰农化股份有限公司', 'PD20090013', '乳油', '20%', 'http://cdncha.191.cn/ueditor_cha/20230215/1676445061866395.jpg', '好用耐用', 'https://example.com/buy/13', '棉花、果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (14, NULL, 10, '高效氯氟氰菊酯', '禾信优选', 2000, 23.00, '深圳诺普信农化股份有限公司', 'PD20090014', '乳油', '5%', 'http://cdncha.191.cn/Base/Mon_2106/60c2d956b710f.jpg', '好用耐用', 'https://example.com/buy/14', '小麦、玉米、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (15, NULL, 25, '联苯菊酯', '禾信优选', 2000, 23.00, '江苏七洲绿色化工股份有限公司', 'PD20090015', '乳油', '10%', 'https://job.191.cn/Uploads/Company/Gallery/2021070795905.jpg', '好用耐用', 'https://example.com/buy/15', '茶树、棉花、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (16, NULL, 17, '吡虫啉', '禾信优选', 2000, 23.00, '江苏扬农化工股份有限公司', 'PD20090016', '可湿性粉剂', '10%', 'http://cdncha.191.cn/Base/Mon_2212/639bcb5fe5bf2.png', '好用耐用', 'https://example.com/buy/16', '水稻、小麦、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (17, NULL, 23, '啶虫脒', '禾信优选', 2000, 23.00, '山东海利尔化工有限公司', 'PD20090017', '乳油', '5%', 'http://cdncha.191.cn/ueditor_cha/20210603/1622707078473211.jpg', '好用耐用', 'https://example.com/buy/17', '棉花、果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (18, NULL, 21, '噻虫嗪', '禾信优选', 2000, 23.00, '瑞士先正达作物保护有限公司', 'PD20090018', '水分散粒剂', '25%', 'http://cdncha.191.cn/Base/Mon_2106/60bec696f3b01.jpg', '好用耐用', 'https://example.com/buy/18', '水稻、玉米、大豆', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (19, NULL, 35, '噻虫胺', '禾信优选', 2000, 23.00, '巴斯夫植物保护(江苏)有限公司', 'PD20090019', '悬浮剂', '20%', 'http://cdncha.191.cn/ueditor_cha/20210517/1621235168752595.jpg', '好用耐用', 'https://example.com/buy/19', '水稻、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (20, NULL, 32, '呋虫胺', '禾信优选', 2000, 23.00, '日本三井化学AGRO株式会社', 'PD20090020', '颗粒剂', '1%', 'http://cdncha.191.cn/ueditor_cha/20210918/1631935833584563.jpg', '好用耐用', 'https://example.com/buy/20', '水稻、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (21, NULL, 14, '氯虫苯甲酰胺', '禾信优选', 2000, 23.00, '美国杜邦公司', 'PD20090021', '悬浮剂', '20%', 'http://cdncha.191.cn/ueditor_cha/20220616/1655370283839016.jpg', '好用耐用', 'https://example.com/buy/21', '水稻、玉米、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (22, NULL, 28, '氟苯虫酰胺', '禾信优选', 2000, 23.00, '日本农药株式会社', 'PD20090022', '悬浮剂', '20%', 'http://cdncha.191.cn/ueditor_cha/20230926/1695709932544230.jpg', '好用耐用', 'https://example.com/buy/22', '蔬菜、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (23, NULL, 32, '溴氰虫酰胺', '禾信优选', 2000, 23.00, '美国杜邦公司', 'PD20090023', '悬浮剂', '10%', 'http://cdncha.191.cn/Base/Mon_2305/646735644b6d9.jpg', '好用耐用', 'https://example.com/buy/23', '棉花、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (24, NULL, 9, '四氯虫酰胺', '禾信优选', 2000, 23.00, '沈阳化工研究院有限公司', 'PD20090024', '悬浮剂', '10%', 'http://cdncha.191.cn/ueditor_cha/20210923/1632377859170556.jpg', '好用耐用', 'https://example.com/buy/24', '水稻、玉米', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (25, NULL, 12, '环溴虫酰胺', '禾信优选', 2000, 23.00, '日本石原产业株式会社', 'PD20090025', '悬浮剂', '5%', 'http://img01.114nz.com/12015060921711/Product/577df341e979c.jpg', '好用耐用', 'https://example.com/buy/25', '蔬菜、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (26, NULL, 20, '戊唑醇', '禾信优选', 2000, 23.00, '江苏剑牌农化股份有限公司', 'PD20090026', '悬浮剂', '25%', 'https://cbu01.alicdn.com/img/ibank/O1CN01XPYYXN2GG6BHTcOQ3_!!2213124848987-0-cib.jpg', '好用耐用', 'https://example.com/buy/26', '小麦、水稻、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (27, NULL, 25, '苯醚甲环唑', '禾信优选', 2000, 23.00, '瑞士先正达作物保护有限公司', 'PD20090027', '乳油', '10%', 'http://cdncha.191.cn/Base/Mon_2105/6093dfe75a24b.jpg', '好用耐用', 'https://example.com/buy/27', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (28, NULL, 18, '丙环唑', '禾信优选', 2000, 23.00, '江苏丰登作物保护股份有限公司', 'PD20090028', '乳油', '25%', 'http://cdncha.191.cn/ueditor_cha/20240529/1716969141929877.jpg', '好用耐用', 'https://example.com/buy/28', '水稻、香蕉', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (29, NULL, 28, '氟环唑', '禾信优选', 2000, 23.00, '巴斯夫植物保护(江苏)有限公司', 'PD20090029', '悬浮剂', '12.5%', 'http://cdncha.191.cn/Base/Mon_2208/630723756231f.jpg', '好用耐用', 'https://example.com/buy/29', '小麦、水稻', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (30, NULL, 20, '三环唑', '禾信优选', 2000, 23.00, '江苏长青农化股份有限公司', 'PD20090030', '可湿性粉剂', '75%', 'http://cdncha.191.cn/ueditor_cha/20231017/1697512600133305.jpg', '好用耐用', 'https://example.com/buy/30', '水稻', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (31, NULL, 24, '嘧菌酯', '禾信优选', 2000, 23.00, '瑞士先正达作物保护有限公司', 'PD20090031', '悬浮剂', '25%', 'http://cdncha.191.cn/Base/Mon_2303/641907ae47769.jpg', '好用耐用', 'https://example.com/buy/31', '水稻、小麦、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (32, NULL, 30, '醚菌酯', '禾信优选', 2000, 23.00, '巴斯夫植物保护(江苏)有限公司', 'PD20090032', '悬浮剂', '30%', 'http://cdncha.191.cn/Base/Mon_2106/60d3dbb907274.jpg', '好用耐用', 'https://example.com/buy/32', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (33, NULL, 20, '吡唑醚菌酯', '禾信优选', 2000, 23.00, '巴斯夫植物保护(江苏)有限公司', 'PD20090033', '乳油', '25%', 'http://cdncha.191.cn/Base/Mon_2208/630717735a3df.jpg', '好用耐用', 'https://example.com/buy/33', '小麦、果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (34, NULL, 9, '肟菌酯', '禾信优选', 2000, 23.00, '拜耳作物科学(中国)有限公司', 'PD20090034', '悬浮剂', '50%', 'http://cdncha.191.cn/Base/Mon_2208/630da9bc33883.png', '好用耐用', 'https://example.com/buy/34', '水稻、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (35, NULL, 10, '啶氧菌酯', '禾信优选', 2000, 23.00, '美国杜邦公司', 'PD20090035', '悬浮剂', '22.5%', 'http://cdncha.191.cn/Base/Mon_2210/634e49ccaae90.jpg', '好用耐用', 'https://example.com/buy/35', '小麦、大豆', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (36, NULL, 14, '氟唑菌酰胺', '禾信优选', 2000, 23.00, '巴斯夫植物保护(江苏)有限公司', 'PD20090036', '悬浮剂', '20%', 'http://cdncha.191.cn/Base/Mon_2203/624124c67cd5f.jpg', '好用耐用', 'https://example.com/buy/36', '小麦、大豆', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (37, NULL, 2, '啶酰菌胺', '禾信优选', 2000, 23.00, '巴斯夫植物保护(江苏)有限公司', 'PD20090037', '水分散粒剂', '50%', 'http://cdncha.191.cn/Base/Mon_2208/630475bfe0ae9.jpg', '好用耐用', 'https://example.com/buy/37', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (38, NULL, 2, '吡唑萘菌胺', '禾信优选', 2000, 23.00, '瑞士先正达作物保护有限公司', 'PD20090038', '乳油', '12.5%', 'http://cdncha.191.cn/Base/Mon_2105/609b7efd6bb29.png', '好用耐用', 'https://example.com/buy/38', '小麦、大麦', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (39, NULL, 23, '联苯吡菌胺', '禾信优选', 2000, 23.00, '拜耳作物科学(中国)有限公司', 'PD20090039', '悬浮剂', '15%', 'http://cdncha.191.cn/Base/Mon_2308/64c86bd46d540.jpg', '好用耐用', 'https://example.com/buy/39', '小麦、大豆', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (40, NULL, 30, '氟吡菌酰胺', '禾信优选', 2000, 23.00, '拜耳作物科学(中国)有限公司', 'PD20090040', '悬浮剂', '41.7%', 'http://cdncha.191.cn/Base/Mon_2305/64549852a4c47.jpg', '好用耐用', 'https://example.com/buy/40', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (41, NULL, 11, '草甘膦', '禾信优选', 2000, 23.00, '浙江新安化工集团股份有限公司', 'PD20090041', '水剂', '41%', 'http://cdncha.191.cn/Base/Mon_2105/609ce50138f75.jpg', '好用耐用', 'https://example.com/buy/41', '非耕地、果园', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (42, NULL, 7, '草铵膦', '禾信优选', 2000, 23.00, '利尔化学股份有限公司', 'PD20090042', '水剂', '20%', 'http://cdncha.191.cn/Base/Mon_2410/6714647278b63.jpg', '好用耐用', 'https://example.com/buy/42', '非耕地、果园', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (43, NULL, 5, '敌草快', '禾信优选', 2000, 23.00, '江苏红太阳股份有限公司', 'PD20090043', '水剂', '20%', 'http://cdncha.191.cn/ueditor_cha/20220919/1663574625354887.jpg', '好用耐用', 'https://example.com/buy/43', '非耕地、果园', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (44, NULL, 20, '百草枯', '禾信优选', 2000, 23.00, '山东绿霸化工股份有限公司', 'PD20090044', '水剂', '20%', 'http://i05.c.aliimg.com/img/product/50/06/44/50064406.jpg', '好用耐用', 'https://example.com/buy/44', '非耕地', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (45, NULL, 23, '草硫膦', '禾信优选', 2000, 23.00, '浙江新安化工集团股份有限公司', 'PD20090045', '可溶粒剂', '75%', 'http://cdncha.191.cn/Base/Mon_2307/64a76642ecca3.jpg', '好用耐用', 'https://example.com/buy/45', '非耕地、果园', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (46, NULL, 14, '乙草胺', '禾信优选', 2000, 23.00, '江苏长青农化股份有限公司', 'PD20090046', '乳油', '50%', 'http://cdncha.191.cn/ueditor_cha/20230926/1695693925921655.jpg', '好用耐用', 'https://example.com/buy/46', '玉米、大豆、花生', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (47, NULL, 17, '异丙甲草胺', '禾信优选', 2000, 23.00, '瑞士先正达作物保护有限公司', 'PD20090047', '乳油', '72%', 'http://cdncha.191.cn/ueditor_cha/20210629/1624949970503789.jpg', '好用耐用', 'https://example.com/buy/47', '玉米、大豆、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (48, NULL, 11, '精喹禾灵', '禾信优选', 2000, 23.00, '安徽丰乐农化有限责任公司', 'PD20090048', '乳油', '10%', 'http://cdncha.191.cn/ueditor_cha/20240222/1708570290537724.jpg', '好用耐用', 'https://example.com/buy/48', '大豆、花生、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (49, NULL, 5, '高效氟吡甲禾灵', '禾信优选', 2000, 23.00, '陶氏益农农业科技(中国)有限公司', 'PD20090049', '乳油', '10.8%', 'http://cdncha.191.cn/ueditor_cha/20250503/1746244608500952.png', '好用耐用', 'https://example.com/buy/49', '大豆、油菜、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (50, NULL, 24, '烯草酮', '禾信优选', 2000, 23.00, '江苏辉丰农化股份有限公司', 'PD20090050', '乳油', '24%', 'http://cdncha.191.cn/Base/Mon_2107/60e669e7751ab.jpg', '好用耐用', 'https://example.com/buy/50', '大豆、油菜、花生', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (51, NULL, 12, '吲哚乙酸', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090051', '可溶液剂', '0.1%', 'http://cdncha.191.cn/ueditor_cha/20230926/1695698490164210.jpg', '好用耐用', 'https://example.com/buy/51', '水稻、小麦、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (52, NULL, 27, '萘乙酸', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090052', '水剂', '5%', 'http://cdncha.191.cn/Base/Mon_2209/63201f646ca98.jpg', '好用耐用', 'https://example.com/buy/52', '水稻、果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (53, NULL, 34, '2,4-滴', '禾信优选', 2000, 23.00, '山东潍坊润丰化工股份有限公司', 'PD20090053', '乳油', '72%', 'http://cdncha.191.cn/ueditor_cha/20231010/1696902243375247.jpg', '好用耐用', 'https://example.com/buy/53', '小麦、玉米', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (54, NULL, 27, '防落素', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090054', '可溶液剂', '0.1%', 'http://cdncha.191.cn/ueditor_cha/20230926/1695698505922509.jpg', '好用耐用', 'https://example.com/buy/54', '番茄、茄子', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (55, NULL, 35, '增产灵', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090055', '可湿性粉剂', '95%', 'http://cdncha.191.cn/Base/Mon_2209/63365acfa8df1.jpg', '好用耐用', 'https://example.com/buy/55', '水稻、小麦', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (56, NULL, 27, '苄氨基嘌呤', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090056', '可溶液剂', '2%', 'http://cdncha.191.cn/Base/Mon_2306/648bfc47221ce.jpg', '好用耐用', 'https://example.com/buy/56', '水稻、果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (57, NULL, 12, '氯吡脲', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090057', '可溶液剂', '0.1%', 'http://cdncha.191.cn/Base/Mon_2206/62b6791aa7f9f.jpg', '好用耐用', 'https://example.com/buy/57', '西瓜、甜瓜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (58, NULL, 9, '噻苯隆', '禾信优选', 2000, 23.00, '江苏辉丰农化股份有限公司', 'PD20090058', '可湿性粉剂', '50%', 'http://img.rqhg.com/UserDocument/mallpic/zq9876/Picture/250304134115173.jpg', '好用耐用', 'https://example.com/buy/58', '棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (59, NULL, 32, '激动素', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090059', '可溶液剂', '0.1%', 'http://cdncha.191.cn/Base/Mon_2209/63212dc286832.png', '好用耐用', 'https://example.com/buy/59', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (60, NULL, 9, '玉米素', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090060', '可溶液剂', '1%', 'http://cdncha.191.cn/Base/Mon_2209/6320304b4b10f.jpg', '好用耐用', 'https://example.com/buy/60', '水稻、玉米', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (61, NULL, 4, '赤霉酸', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090061', '可溶粉剂', '20%', 'http://cdncha.191.cn/ueditor_cha/20231012/1697089580212738.jpg', '好用耐用', 'https://example.com/buy/61', '水稻、柑橘、葡萄', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (62, NULL, 12, '赤霉素A4+A7', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090062', '乳油', '4%', 'http://cdncha.191.cn/ueditor_cha/20210510/1620624919968394.jpg', '好用耐用', 'https://example.com/buy/62', '苹果、梨', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (63, NULL, 17, '赤霉素GA3', '禾信优选', 2000, 23.00, '江西新瑞丰生化股份有限公司', 'PD20090063', '结晶粉', '90%', 'http://cbu01.alicdn.com/img/ibank/2020/844/349/15404943448_437780512.jpg', '好用耐用', 'https://example.com/buy/63', '水稻、棉花、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (64, NULL, 3, '赤霉素GA4', '禾信优选', 2000, 23.00, '江西新瑞丰生化股份有限公司', 'PD20090064', '结晶粉', '90%', 'https://cbu01.alicdn.com/img/ibank/O1CN015iiaEp1VNczTh4AjL_!!2216200002641-0-cib.310x310.jpg', '好用耐用', 'https://example.com/buy/64', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (65, NULL, 19, '赤霉素GA7', '禾信优选', 2000, 23.00, '江西新瑞丰生化股份有限公司', 'PD20090065', '结晶粉', '90%', 'http://cdncha.191.cn/Base/Mon_2301/63b78908ed0b0.png', '好用耐用', 'https://example.com/buy/65', '苹果、梨', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (66, NULL, 14, '芸苔素内酯', '禾信优选', 2000, 23.00, '云南云大科技农化有限公司', 'PD20090066', '乳油', '0.01%', 'http://cdncha.191.cn/Base/Mon_2007/5f114e6024293.jpg', '好用耐用', 'https://example.com/buy/66', '水稻、小麦、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (67, NULL, 23, '28-高芸苔素内酯', '禾信优选', 2000, 23.00, '云南云大科技农化有限公司', 'PD20090067', '可溶液剂', '0.01%', 'http://cdncha.191.cn/Base/Mon_2212/639fcf5ec60a7.jpg', '好用耐用', 'https://example.com/buy/67', '蔬菜、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (68, NULL, 24, '24-表芸苔素内酯', '禾信优选', 2000, 23.00, '云南云大科技农化有限公司', 'PD20090068', '可溶液剂', '0.01%', 'http://cdncha.191.cn/Base/Mon_2007/5f114e6024293.jpg', '好用耐用', 'https://example.com/buy/68', '水稻、玉米', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (69, NULL, 21, '丙酰芸苔素内酯', '禾信优选', 2000, 23.00, '云南云大科技农化有限公司', 'PD20090069', '乳油', '0.01%', 'http://cdncha.191.cn/ueditor_cha/20240616/1718518642568699.jpg', '好用耐用', 'https://example.com/buy/69', '小麦、大豆', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (70, NULL, 25, '28-表高芸苔素内酯', '禾信优选', 2000, 23.00, '云南云大科技农化有限公司', 'PD20090070', '可溶液剂', '0.01%', 'http://cdncha.191.cn/Base/Mon_2212/639fcf5ec60a7.jpg', '好用耐用', 'https://example.com/buy/70', '棉花、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (71, NULL, 13, '哒螨灵', '禾信优选', 2000, 23.00, '江苏克胜集团股份有限公司', 'PD20090071', '乳油', '15%', 'http://cdncha.191.cn/ueditor_cha/20240627/1719469591501392.jpg', '好用耐用', 'https://example.com/buy/71', '柑橘、苹果、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (72, NULL, 4, '四螨嗪', '禾信优选', 2000, 23.00, '江苏克胜集团股份有限公司', 'PD20090072', '悬浮剂', '20%', 'http://cdncha.191.cn/ueditor_cha/20231031/1698731947923716.jpg', '好用耐用', 'https://example.com/buy/72', '柑橘、苹果', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (73, NULL, 4, '噻螨酮', '禾信优选', 2000, 23.00, '江苏克胜集团股份有限公司', 'PD20090073', '乳油', '5%', 'http://cdncha.191.cn/Base/Mon_2303/6424f4aa963a5.jpg', '好用耐用', 'https://example.com/buy/73', '柑橘、苹果', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (74, NULL, 27, '苯丁锡', '禾信优选', 2000, 23.00, '江苏克胜集团股份有限公司', 'PD20090074', '可湿性粉剂', '25%', 'http://cdncha.191.cn/ueditor_cha/20231117/1700191583544637.jpg', '好用耐用', 'https://example.com/buy/74', '柑橘、棉花', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (75, NULL, 30, '三唑锡', '禾信优选', 2000, 23.00, '江苏克胜集团股份有限公司', 'PD20090075', '悬浮剂', '25%', 'http://cdncha.191.cn/ueditor_cha/20231117/1700191583544637.jpg', '好用耐用', 'https://example.com/buy/75', '柑橘、苹果', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (76, NULL, 32, '阿维菌素', '禾信优选', 2000, 23.00, '华北制药集团爱诺有限公司', 'PD20090076', '乳油', '1.8%', 'http://cdncha.191.cn/Base/Mon_2207/62ce6b62dc983.jpg', '好用耐用', 'https://example.com/buy/76', '柑橘、棉花、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (77, NULL, 18, '甲氨基阿维菌素', '禾信优选', 2000, 23.00, '华北制药集团爱诺有限公司', 'PD20090077', '乳油', '2%', 'http://cdncha.191.cn/ueditor_cha/20220713/1657695056782343.png', '好用耐用', 'https://example.com/buy/77', '蔬菜、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (78, NULL, 34, '螺螨酯', '禾信优选', 2000, 23.00, '拜耳作物科学(中国)有限公司', 'PD20090078', '悬浮剂', '24%', 'http://cdncha.191.cn/Base/Mon_2205/6294373399d5c.jpg', '好用耐用', 'https://example.com/buy/78', '柑橘、苹果', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (79, NULL, 35, '乙螨唑', '禾信优选', 2000, 23.00, '日本住友化学株式会社', 'PD20090079', '悬浮剂', '11%', 'http://cdncha.191.cn/Base/Mon_2212/63904c4ee8113.png', '好用耐用', 'https://example.com/buy/79', '柑橘、苹果', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (80, NULL, 23, '联苯肼酯', '禾信优选', 2000, 23.00, '美国科聚亚公司', 'PD20090080', '悬浮剂', '24%', 'https://ecdn6-nc.globalso.com/upload/p/3284/image_product/2025-03/10-bispyribac-sodium-sc.jpg', '好用耐用', 'https://example.com/buy/80', '草莓、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (81, NULL, 26, '溴敌隆', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090081', '母液', '0.5%', 'http://mall-sourcing-prod-rongchuang.oss-cn-beijing.aliyuncs.com/V1.0.0/goods/8D681B3DE2384F41AEB09D98D0CA1619.jpeg?x-oss-process=image/resize,m_fill,h_400,w_400/rotate,0', '好用耐用', 'https://example.com/buy/81', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (82, NULL, 16, '溴鼠灵', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090082', '母液', '0.5%', 'https://pointagrochina.com/wp-content/uploads/Brodifacoum_Taxat-Cebo_Chile.png', '好用耐用', 'https://example.com/buy/82', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (83, NULL, 18, '杀鼠醚', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090083', '母粉', '0.75%', 'http://cdncha.191.cn/ueditor_cha/20231031/1698733200200647.jpg', '好用耐用', 'https://example.com/buy/83', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (84, NULL, 23, '敌鼠钠盐', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090084', '母粉', '0.1%', 'http://www.lunuoyaoye.net/upfile/images/2018/12/27/small4_15459052203689420.jpg', '好用耐用', 'https://example.com/buy/84', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (85, NULL, 19, '氯鼠酮', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090085', '母液', '0.25%', 'http://static-cdn.gongyingshi.com/img/item/4110/20170628/batch-import_105305122/pic/1/1.jpg', '好用耐用', 'https://example.com/buy/85', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (86, NULL, 32, '磷化锌', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090086', '毒饵', '3%', 'http://www.chinapesticide.org.cn/nyupload/image/202212/e8634616-cf62-4113-819e-34d4d0ae622e.jpg', '好用耐用', 'https://example.com/buy/86', '仓库、农田', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (87, NULL, 25, '毒鼠磷', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090087', '毒饵', '0.5%', 'http://mall-sourcing-prod-rongchuang.oss-cn-beijing.aliyuncs.com/V1.0.0/goods/3ACD97128B8E494A9BCFF69FB9020853.jpeg?x-oss-process=image/resize,m_fill,h_400,w_400/rotate,0', '好用耐用', 'https://example.com/buy/87', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (88, NULL, 2, '灭鼠优', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090088', '毒饵', '2%', 'http://www.jinglongkeji.com/Mobile/uploadfiles/pictures/product/20231025112029_0055.jpg_280.jpg', '好用耐用', 'https://example.com/buy/88', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (89, NULL, 18, '灭鼠安', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090089', '毒饵', '2%', 'http://mall-sourcing-prod-rongchuang.oss-cn-beijing.aliyuncs.com/V1.0.0/goods/FD4D7B0E71574D3DB8C22B75A715A51B.jpeg', '好用耐用', 'https://example.com/buy/89', '农田、仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (90, NULL, 25, '硫酸铊', '禾信优选', 2000, 23.00, '辽宁省化工研究院', 'PD20090090', '毒饵', '1%', 'http://cdncha.191.cn/ueditor_cha/20221117/1668662469491140.jpg', '好用耐用', 'https://example.com/buy/90', '仓库', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (91, NULL, 17, '波尔多液', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090091', '悬浮剂', '80%', 'http://cdncha.191.cn/Base/Mon_2105/609e0e28b8316.jpg', '好用耐用', 'https://example.com/buy/91', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (92, NULL, 20, '石硫合剂', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090092', '水剂', '45%', 'http://cdncha.191.cn/Base/Mon_2303/641966802e76e.png', '好用耐用', 'https://example.com/buy/92', '果树、花卉', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (93, NULL, 30, '硫酸铜', '禾信优选', 2000, 23.00, '四川国光农化股份有限公司', 'PD20090093', '可湿性粉剂', '96%', 'http://cdncha.191.cn/Base/Mon_2209/63365acfa8df1.jpg', '好用耐用', 'https://example.com/buy/93', '水稻、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (94, NULL, 21, '氢氧化铜', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090094', '悬浮剂', '53.8%', 'http://cdncha.191.cn/ueditor_cha/20231017/1697525994821069.jpg', '好用耐用', 'https://example.com/buy/94', '蔬菜、果树', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (95, NULL, 7, '氧化亚铜', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090095', '可湿性粉剂', '86.2%', 'http://cdncha.191.cn/ueditor_cha/20230901/1693533558475006.jpg', '好用耐用', 'https://example.com/buy/95', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (96, NULL, 26, '代森锰锌', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090096', '可湿性粉剂', '80%', 'http://cdncha.191.cn/Base/Mon_2210/634f96548fe4c.jpg', '好用耐用', 'https://example.com/buy/96', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (97, NULL, 7, '代森锌', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090097', '可湿性粉剂', '65%', 'http://cdncha.191.cn/Base/Mon_2303/6411752c7b987.jpg', '好用耐用', 'https://example.com/buy/97', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (98, NULL, 9, '福美双', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090098', '可湿性粉剂', '50%', 'http://cdncha.191.cn/Base/Mon_2112/61c2d38656880.jpg', '好用耐用', 'https://example.com/buy/98', '水稻、小麦', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (99, NULL, 30, '代森铵', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090099', '水剂', '45%', 'http://cdncha.191.cn/Base/Mon_2207/62cf753a5178e.png', '好用耐用', 'https://example.com/buy/99', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);
INSERT INTO `agrochemicals` VALUES (100, NULL, 14, '代森联', '禾信优选', 2000, 23.00, '江苏龙灯化学有限公司', 'PD20090100', '水分散粒剂', '70%', 'http://cdncha.191.cn/Base/Mon_2008/5f2a48384be5b.jpg', '好用耐用', 'https://example.com/buy/100', '果树、蔬菜', '稀释', '严禁口服！', '2026-03-31 09:01:25', '2026-04-16 18:28:00', NULL);

-- ----------------------------
-- Table structure for crops
-- ----------------------------
DROP TABLE IF EXISTS `crops`;
CREATE TABLE `crops`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '通用名 (如：水稻)',
  `scientific_name` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '学名 (如：Oryza sativa)',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
  `deleted_at` datetime NULL DEFAULT NULL COMMENT '软删除时间戳',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_scientific_name`(`scientific_name` ASC) USING BTREE,
  INDEX `idx_name`(`name` ASC) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 70 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '农作物基础信息表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of crops
-- ----------------------------
INSERT INTO `crops` VALUES (1, '水稻', 'Oryza sativa L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (2, '小麦', 'Triticum aestivum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (3, '玉米', 'Zea mays L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (4, '大豆', 'Glycine max (L.) Merr.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (5, '高粱', 'Sorghum bicolor (L.) Moench', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (6, '谷子', 'Setaria italica (L.) Beauv.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (7, '大麦', 'Hordeum vulgare L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (8, '燕麦', 'Avena sativa L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (9, '黑麦', 'Secale cereale L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (10, '荞麦', 'Fagopyrum esculentum Moench', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (11, '甘薯', 'Ipomoea batatas (L.) Lam.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (12, '马铃薯', 'Solanum tuberosum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (13, '木薯', 'Manihot esculenta Crantz', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (14, '棉花', 'Gossypium spp.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (15, '油菜', 'Brassica napus L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (16, '花生', 'Arachis hypogaea L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (17, '向日葵', 'Helianthus annuus L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (18, '芝麻', 'Sesamum indicum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (19, '亚麻', 'Linum usitatissimum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (20, '大麻', 'Cannabis sativa L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (21, '甜菜', 'Beta vulgaris L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (22, '甘蔗', 'Saccharum officinarum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (23, '烟草', 'Nicotiana tabacum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (24, '茶树', 'Camellia sinensis (L.) O. Kuntze', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (25, '咖啡', 'Coffea arabica L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (26, '可可', 'Theobroma cacao L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (27, '橡胶', 'Hevea brasiliensis (Willd. ex A. Juss.) Muell. Arg.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (28, '白菜', 'Brassica rapa var. glabra Regel', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (29, '萝卜', 'Raphanus sativus L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (30, '胡萝卜', 'Daucus carota var. sativa DC.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (31, '芹菜', 'Apium graveolens L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (32, '菠菜', 'Spinacia oleracea L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (33, '生菜', 'Lactuca sativa L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (34, '黄瓜', 'Cucumis sativus L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (35, '番茄', 'Solanum lycopersicum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (36, '茄子', 'Solanum melongena L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (37, '辣椒', 'Capsicum annuum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (38, '南瓜', 'Cucurbita moschata (Duch. ex Lam.) Duch. ex Poiret', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (39, '西瓜', 'Citrullus lanatus (Thunb.) Matsum. et Nakai', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (40, '甜瓜', 'Cucumis melo L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (41, '菜豆', 'Phaseolus vulgaris L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (42, '豌豆', 'Pisum sativum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (43, '洋葱', 'Allium cepa L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (44, '大蒜', 'Allium sativum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (45, '韭菜', 'Allium tuberosum Rottl. ex Spreng.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (46, '大葱', 'Allium fistulosum L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (47, '生姜', 'Zingiber officinale Rosc.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (48, '苹果', 'Malus pumila Mill.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (49, '梨', 'Pyrus spp.', '2026-03-31 09:01:25', '2026-04-14 18:07:49', NULL);
INSERT INTO `crops` VALUES (50, '桃', 'Prunus persica (L.) Batsch', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (51, '杏', 'Prunus armeniaca L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (52, '李', 'Prunus salicina Lindl.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (53, '樱桃', 'Prunus avium L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (54, '葡萄', 'Vitis vinifera L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (55, '柑橘', 'Citrus reticulata Blanco', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (56, '橙', 'Citrus sinensis (L.) Osbeck', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (57, '柚', 'Citrus maxima (Burm.) Merr.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (58, '柠檬', 'Citrus limon (L.) Burm. f.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (59, '香蕉', 'Musa paradisiaca L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (60, '菠萝', 'Ananas comosus (L.) Merr.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (61, '芒果', 'Mangifera indica L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (62, '荔枝', 'Litchi chinensis Sonn.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (63, '龙眼', 'Dimocarpus longan Lour.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (64, '猕猴桃', 'Actinidia chinensis Planch.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (65, '草莓', 'Fragaria × ananassa Duch.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (66, '蓝莓', 'Vaccinium spp.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (67, '核桃', 'Juglans regia L.', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (68, '板栗', 'Castanea mollissima Blume', '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `crops` VALUES (69, 'ss', 'dd', '2026-04-14 17:01:18', '2026-04-14 17:01:22', '2026-04-14 17:01:22');

-- ----------------------------
-- Table structure for user_crops
-- ----------------------------
DROP TABLE IF EXISTS `user_crops`;
CREATE TABLE `user_crops`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `user_id` bigint UNSIGNED NOT NULL COMMENT '用户ID',
  `crop_id` bigint UNSIGNED NOT NULL COMMENT '农作物ID',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '关联创建时间',
  `updated_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '关联更新时间',
  `deleted_at` datetime NULL DEFAULT NULL COMMENT '软删除时间戳',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_user_crop`(`user_id` ASC, `crop_id` ASC) USING BTREE,
  INDEX `idx_crop_id`(`crop_id` ASC) USING BTREE,
  INDEX `idx_deleted_at`(`deleted_at` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户与农作物关联表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of user_crops
-- ----------------------------
INSERT INTO `user_crops` VALUES (1, 2, 67, '2026-03-31 09:01:25', '2026-03-31 09:28:53', '2026-03-31 09:28:53');
INSERT INTO `user_crops` VALUES (2, 2, 4, '2026-03-31 09:01:25', '2026-03-31 09:28:54', '2026-03-31 09:28:54');
INSERT INTO `user_crops` VALUES (3, 2, 1, '2026-03-31 09:01:25', '2026-03-31 09:28:35', '2026-03-31 09:28:35');
INSERT INTO `user_crops` VALUES (4, 2, 36, '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `user_crops` VALUES (5, 2, 56, '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `user_crops` VALUES (6, 2, 14, '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `user_crops` VALUES (7, 2, 13, '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `user_crops` VALUES (8, 2, 7, '2026-03-31 09:01:25', '2026-03-31 09:01:25', NULL);
INSERT INTO `user_crops` VALUES (10, 2, 2, '2026-03-31 09:28:58', '2026-03-31 09:28:58', NULL);
INSERT INTO `user_crops` VALUES (11, 2, 48, '2026-03-31 15:51:37', '2026-03-31 15:51:37', NULL);
INSERT INTO `user_crops` VALUES (12, 3, 1, '2026-03-31 16:12:04', '2026-03-31 16:12:04', NULL);
INSERT INTO `user_crops` VALUES (13, 4, 2, '2026-04-02 09:44:05', '2026-04-02 09:44:05', NULL);
INSERT INTO `user_crops` VALUES (14, 5, 3, '2026-04-15 11:06:32', '2026-04-15 11:06:32', NULL);
INSERT INTO `user_crops` VALUES (15, 5, 2, '2026-04-15 11:39:48', '2026-04-15 11:39:48', NULL);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `id` bigint UNSIGNED NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `username` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '用户名/登录名',
  `phone_number` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '手机号码',
  `avatar` varchar(2048) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NULL DEFAULT NULL COMMENT '头像URL',
  `password` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL COMMENT '密码哈希值',
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL DEFAULT 'USER' COMMENT '角色 (USER, ADMIN, FARMER等)',
  `created_at` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '注册时间',
  PRIMARY KEY (`id`) USING BTREE,
  UNIQUE INDEX `uk_username`(`username` ASC) USING BTREE,
  UNIQUE INDEX `uk_phone`(`phone_number` ASC) USING BTREE,
  INDEX `idx_role`(`role` ASC) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci COMMENT = '用户账户表' ROW_FORMAT = DYNAMIC;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (5, '1234', '18962901710', '/uploads/avatar/1776224587269_微信图片_20260413163213_40_29.jpg', '$2a$10$ytLoAm7uVgxe9u9IWwEAuOm7gKPDY0f0swEfeE89y.NkzpFmy.YYy', 'ADMIN', '2026-04-14 18:29:54');
INSERT INTO `users` VALUES (6, 'albie', NULL, '/uploads/avatar/1776335661783_微信图片_20260413155823_33_29.jpg', '$2a$10$0HBokoOgAjRCqc6E2ccfcuADhNZP9H60qbyiR6vq4zEKN5RKBp8Ne', 'USER', '2026-04-16 18:33:53');

SET FOREIGN_KEY_CHECKS = 1;
