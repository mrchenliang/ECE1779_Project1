-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema estore
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `memcache` ;
CREATE SCHEMA IF NOT EXISTS `memcache` DEFAULT CHARACTER SET utf8 ;
USE `memcache` ;

DROP TABLE IF EXISTS `memcache`.`image` ;

CREATE TABLE IF NOT EXISTS `memcache`.`image` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `tag` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `memcache`.`cache_properties` ;

CREATE TABLE IF NOT EXISTS `memcache`.`cache_properties` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `max_capacity` INT NOT NULL,
  `replacement_method` VARCHAR(255) NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

DROP TABLE IF EXISTS `memcache`.`cache_stats` ;

CREATE TABLE IF NOT EXISTS `memcache`.`cache_stats` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `cache_size` INT NOT NULL,
  `key_count` INT NOT NULL,
  `request_count` INT NOT NULL,
  `miss_count` INT NOT NULL,
  `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;

DROP USER IF EXISTS 'ece1779'@'localhost';
CREATE USER 'ece1779'@'localhost' IDENTIFIED BY '12345678';
GRANT ALL PRIVILEGES ON memcache.* TO 'ece1779'@'localhost';