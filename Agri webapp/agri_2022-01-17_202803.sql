/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ agri /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE agri;

DROP TABLE IF EXISTS customers;
CREATE TABLE `customers` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(25) NOT NULL,
  `c_pwd` varchar(150) NOT NULL,
  `ph_no` varchar(10) NOT NULL,
  PRIMARY KEY (`c_id`),
  UNIQUE KEY `c_name` (`c_name`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS farmers;
CREATE TABLE `farmers` (
  `f_id` int NOT NULL AUTO_INCREMENT,
  `f_name` varchar(25) NOT NULL,
  `f_pwd` varchar(150) NOT NULL,
  `ph_no` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`f_id`),
  UNIQUE KEY `f_name` (`f_name`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS land;
CREATE TABLE `land` (
  `land_reg_no` varchar(30) NOT NULL,
  `area` int DEFAULT NULL,
  `loc` varchar(25) DEFAULT NULL,
  `f_id` int DEFAULT NULL,
  PRIMARY KEY (`land_reg_no`),
  KEY `f_id` (`f_id`),
  CONSTRAINT `land_ibfk_1` FOREIGN KEY (`f_id`) REFERENCES `farmers` (`f_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS orderpk;
CREATE TABLE `orderpk` (
  `order_id` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS orders;
CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `crops` varchar(25) NOT NULL,
  `quantity` int NOT NULL,
  `price` int NOT NULL,
  `c_id` int NOT NULL,
  `f_id` int NOT NULL,
  KEY `order_id` (`order_id`),
  KEY `c_id` (`c_id`),
  KEY `f_id` (`f_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orderpk` (`order_id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`c_id`) REFERENCES `customers` (`c_id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`f_id`) REFERENCES `farmers` (`f_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS stock;
CREATE TABLE `stock` (
  `crop` varchar(25) NOT NULL,
  `f_id` int NOT NULL,
  `quantity` int NOT NULL,
  `price` int NOT NULL,
  `imgLocation` varchar(80) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`crop`,`f_id`),
  KEY `f_id` (`f_id`),
  CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`f_id`) REFERENCES `farmers` (`f_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

CREATE OR REPLACE VIEW `products` AS select `l`.`f_id` AS `f_id`,`l`.`loc` AS `loc`,`s`.`crop` AS `crop`,`s`.`quantity` AS `quantity`,((`s`.`price` * 1.35) / `s`.`quantity`) AS `(S.price*1.35)/S.quantity`,`s`.`imgLocation` AS `imgLocation`,`s`.`description` AS `description` from (`land` `l` join `stock` `s` on((`l`.`f_id` = `s`.`f_id`)));

INSERT INTO customers(c_id,c_name,c_pwd,ph_no) VALUES(2,'okay','pbkdf2:sha256:260000$qSY$3b1d68f4bbe589602e72d09b0ff1e7a86ef6e7e9cb79ad81ca1ad40bd709ce6c','5689998978'),(3,'Prajwal','pbkdf2:sha256:260000$q6k$3415dfc49b89c95a5caba969a99e6aabb6282aaece65756df6109feb5e4faed9','98765');

INSERT INTO farmers(f_id,f_name,f_pwd,ph_no) VALUES(8,'Shreesha','pbkdf2:sha256:260000$mSe$3952a41a6df83a36fc0c769a360ca779ac2c63d917703c13568436b2833b35e5','5689998978'),(9,'John','pbkdf2:sha256:260000$9wg$186aff7f1a307c65d8b6186a7e59edf07175ab914738bcfb991dbf5963cf4736','776545'),(10,'Prajwal','pbkdf2:sha256:260000$vIr$32a6357a32a3f9ff3609130ca2bb23a86b3e8c81f9f09057e893c1e0c4aebc87','123456'),(13,'Sanjeev','pbkdf2:sha256:260000$XSd$43a794fb5d8d0deea32c4c5b4d052ecae6b4c0ef84755b49e7f5710bed537fdf','5689998978');

INSERT INTO land(land_reg_no,area,loc,f_id) VALUES('1KS99011',25,'Bengaluru Rural',9),('1KS99012',30,'Chikmagalur',10);

INSERT INTO orderpk(order_id) VALUES(1);

INSERT INTO stock(crop,f_id,quantity,price,imgLocation,description) VALUES('Basmati Rice',9,200,5000,'../static/images/BasmatiRice.jpg','this good.'),('Kabuli Chana',10,200,3000,'../static/images/KabuliChana.jpg','this bad.'),('Rajma',10,150,6000,'../static/images/Rajma.jpg','ok.'),('Toor Dal',9,200,4000,'../static/images/ToorDal.jpg','this really good.');