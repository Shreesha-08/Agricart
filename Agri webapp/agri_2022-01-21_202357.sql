/*!40101 SET NAMES utf8 */;
/*!40014 SET FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/ agri /*!40100 DEFAULT CHARACTER SET utf8mb4 */;
USE agri;

DROP TABLE IF EXISTS cart;
CREATE TABLE `cart` (
  `pid` int NOT NULL,
  `quantity` int NOT NULL,
  PRIMARY KEY (`pid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

DROP TABLE IF EXISTS customers;
CREATE TABLE `customers` (
  `c_id` int NOT NULL AUTO_INCREMENT,
  `c_name` varchar(25) NOT NULL,
  `c_pwd` varchar(150) NOT NULL,
  `ph_no` varchar(10) NOT NULL,
  PRIMARY KEY (`c_id`),
  UNIQUE KEY `c_name` (`c_name`)
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS farmers;
CREATE TABLE `farmers` (
  `f_id` int NOT NULL AUTO_INCREMENT,
  `f_name` varchar(25) NOT NULL,
  `f_pwd` varchar(150) NOT NULL,
  `ph_no` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`f_id`),
  UNIQUE KEY `f_name` (`f_name`)
) ENGINE=InnoDB AUTO_INCREMENT=15 DEFAULT CHARSET=utf8mb3;

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
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS orders;
CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `crops` varchar(25) NOT NULL,
  `quantity` int NOT NULL,
  `price` int NOT NULL,
  `c_id` int NOT NULL,
  `f_id` int NOT NULL,
  `pick_up_loc` varchar(30) DEFAULT NULL,
  `ordered_date` date NOT NULL,
  KEY `order_id` (`order_id`),
  KEY `c_id` (`c_id`),
  KEY `f_id` (`f_id`),
  CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orderpk` (`order_id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_2` FOREIGN KEY (`c_id`) REFERENCES `customers` (`c_id`) ON DELETE CASCADE,
  CONSTRAINT `orders_ibfk_3` FOREIGN KEY (`f_id`) REFERENCES `farmers` (`f_id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;

DROP TABLE IF EXISTS stock;
CREATE TABLE `stock` (
  `stock_no` int NOT NULL AUTO_INCREMENT,
  `crop` varchar(25) NOT NULL,
  `f_id` int NOT NULL,
  `quantity` int DEFAULT NULL,
  `price` int DEFAULT NULL,
  `imgLocation` varchar(80) DEFAULT NULL,
  `description` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`crop`,`f_id`),
  UNIQUE KEY `stock_no` (`stock_no`),
  KEY `f_id` (`f_id`),
  CONSTRAINT `stock_ibfk_1` FOREIGN KEY (`f_id`) REFERENCES `farmers` (`f_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;

CREATE OR REPLACE VIEW `products` AS select `s`.`stock_no` AS `stock_no`,`l`.`f_id` AS `f_id`,`l`.`loc` AS `loc`,`s`.`crop` AS `crop`,`s`.`quantity` AS `quantity`,cast((`s`.`price` * 1.3) as decimal(16,0)) AS `price`,`s`.`imgLocation` AS `imgLocation`,`s`.`description` AS `description` from (`land` `l` join `stock` `s` on((`l`.`f_id` = `s`.`f_id`)));


INSERT INTO customers(c_id,c_name,c_pwd,ph_no) VALUES(2,'okay','pbkdf2:sha256:260000$qSY$3b1d68f4bbe589602e72d09b0ff1e7a86ef6e7e9cb79ad81ca1ad40bd709ce6c','5689998978'),(3,'Prajwal','pbkdf2:sha256:260000$q6k$3415dfc49b89c95a5caba969a99e6aabb6282aaece65756df6109feb5e4faed9','98765'),(4,'Shreesha','pbkdf2:sha256:260000$j4f$a71bd6f679de9b5dcacffa9a2a227791848fbc90b63aaf450f47de84beade5cd','7878675645');

INSERT INTO farmers(f_id,f_name,f_pwd,ph_no) VALUES(8,'Shreesha','pbkdf2:sha256:260000$mSe$3952a41a6df83a36fc0c769a360ca779ac2c63d917703c13568436b2833b35e5','5689998978'),(9,'John','pbkdf2:sha256:260000$9wg$186aff7f1a307c65d8b6186a7e59edf07175ab914738bcfb991dbf5963cf4736','776545'),(10,'Prajwal','pbkdf2:sha256:260000$vIr$32a6357a32a3f9ff3609130ca2bb23a86b3e8c81f9f09057e893c1e0c4aebc87','123456'),(13,'Sanjeev','pbkdf2:sha256:260000$XSd$43a794fb5d8d0deea32c4c5b4d052ecae6b4c0ef84755b49e7f5710bed537fdf','5689998978'),(14,'Shreesha08','pbkdf2:sha256:260000$Gc3$9d92c0e134cd3777483778de185979d443f453957afde6cb8df18f02e15aef89','9090878790');

INSERT INTO land(land_reg_no,area,loc,f_id) VALUES('1KS99011',25,'Bengaluru Rural',9),('1KS99012',30,'Chikmagalur',10),('8870755',35,'Raichur',13),('9992223Ad7',60,'Shivamogga',14);

INSERT INTO orderpk(order_id) VALUES(1),(6),(7),(8),(9),(10),(11),(12),(13);

INSERT INTO orders(order_id,crops,quantity,price,c_id,f_id,pick_up_loc,ordered_date) VALUES(6,'Kabuli Chana',100,7800,2,10,'Chikmagalur','2022-01-18'),(6,'Toor Dal',100,10400,2,9,'Bengaluru Rural','2022-01-18'),(7,'Kabuli Chana',200,15600,2,10,'Chikmagalur','2022-01-18'),(8,'Basmati Rice',100,13000,4,9,'Bengaluru Rural','2022-01-19'),(8,'Green Moong Dal',200,70200,4,13,'Raichur','2022-01-19'),(9,'Kabuli Chana',200,15600,4,10,'Chikmagalur','2022-01-19'),(9,'Green Moong Dal',100,35100,4,13,'Raichur','2022-01-19'),(10,'Green Moong Dal',200,70200,2,13,'Raichur','2022-01-19'),(11,'Toor Dal',100,10400,2,9,'Bengaluru Rural','2022-01-19'),(12,'Basmati Rice',100,6500,4,9,'Bengaluru Rural','2022-01-19'),(12,'Groundnut Oil',200,23400,4,13,'Raichur','2022-01-19'),(13,'Basmati Rice',100,6500,4,9,'Bengaluru Rural','2022-01-19');
INSERT INTO stock(stock_no,crop,f_id,quantity,price,imgLocation,description) VALUES(6,'Brown Rice',14,200,3000,'../static/images/BrownRice.jpg',''),(5,'Green Moong Dal',13,100,9000,'../static/images/GreenMoongDal.jpg','premium quality'),(7,'Groundnut Oil',13,300,9000,'../static/images/GroundnutOil.jpg','liquid'),(2,'Kabuli Chana',10,200,3000,'../static/images/KabuliChana.jpg','this bad.'),(3,'Rajma',10,150,6000,'../static/images/Rajma.jpg','ok.'),(4,'Toor Dal',9,100,4000,'../static/images/ToorDal.jpg','this really good.');DROP PROCEDURE IF EXISTS getProduct;
CREATE PROCEDURE `getProduct`()
BEGIN
    SELECT * FROM products;
END;