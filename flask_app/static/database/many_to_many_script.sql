-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema creations_db
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema creations_db
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `creations_db` DEFAULT CHARACTER SET utf8mb3 ;
USE `creations_db` ;

-- -----------------------------------------------------
-- Table `creations_db`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `creations_db`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 3
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `creations_db`.`creations`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `creations_db`.`creations` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `description` TEXT NULL DEFAULT NULL,
  `price` INT NULL DEFAULT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` DATETIME NULL DEFAULT CURRENT_TIMESTAMP,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_creations_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_creations_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `creations_db`.`users` (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 5
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `creations_db`.`purchases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `creations_db`.`purchases` (
  `creation_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`creation_id`, `user_id`),
  INDEX `fk_purchases_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_purchases_creations1`
    FOREIGN KEY (`creation_id`)
    REFERENCES `creations_db`.`creations` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_purchases_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `creations_db`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
