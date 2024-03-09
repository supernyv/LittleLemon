-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema LittleLemonDB
-- -----------------------------------------------------
-- For meta db capstone project

-- -----------------------------------------------------
-- Schema LittleLemonDB
--
-- For meta db capstone project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `LittleLemonDB` DEFAULT CHARACTER SET utf8 COLLATE utf8_bin ;
USE `LittleLemonDB` ;

-- -----------------------------------------------------
-- Table `LittleLemonDB`.`address`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`address` (
  `address_id` INT NOT NULL,
  `street` VARCHAR(45) NOT NULL,
  `city` VARCHAR(45) NOT NULL,
  `zip` VARCHAR(45) NULL,
  `country` VARCHAR(45) NULL,
  PRIMARY KEY (`address_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`customer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`customer` (
  `customer_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `telephone` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `address_id` INT NOT NULL,
  PRIMARY KEY (`customer_id`),
  INDEX `customer_address_idx` (`address_id` ASC) VISIBLE,
  CONSTRAINT `customer_address`
    FOREIGN KEY (`address_id`)
    REFERENCES `LittleLemonDB`.`address` (`address_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`staff`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`staff` (
  `staff_id` INT NOT NULL,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `role` VARCHAR(50) NOT NULL,
  `salary` DECIMAL(10,2) NOT NULL,
  `dob` DATE NOT NULL,
  `gender` VARCHAR(45) NOT NULL,
  `phone` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `address_id` INT NOT NULL,
  PRIMARY KEY (`staff_id`),
  INDEX `staff_address_idx` (`address_id` ASC) VISIBLE,
  CONSTRAINT `staff_address`
    FOREIGN KEY (`address_id`)
    REFERENCES `LittleLemonDB`.`address` (`address_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`menu_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`menu_items` (
  `item_id` INT NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `type` VARCHAR(45) NULL,
  `price` DECIMAL(10,2) NOT NULL,
  `producer` VARCHAR(45) NULL,
  `quantity_in_stock` INT NULL,
  PRIMARY KEY (`item_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`orders` (
  `order_id` INT NOT NULL,
  `order_date` DATE NOT NULL,
  `total_cost` DECIMAL(10,2) NOT NULL,
  `total_quantity` INT NOT NULL,
  `customer_id` INT NOT NULL,
  `staff_id` INT NOT NULL,
  `delivery_date` DATE NULL,
  `order_status` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`order_id`),
  INDEX `order_customer_idx` (`customer_id` ASC) VISIBLE,
  INDEX `order_staff_idx` (`staff_id` ASC) VISIBLE,
  CONSTRAINT `orders_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `LittleLemonDB`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `orders_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `LittleLemonDB`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`menu`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`menu` (
  `menu_id` INT NOT NULL,
  `menu_name` VARCHAR(250) NOT NULL,
  `cuisine` VARCHAR(45) NOT NULL,
  `starter_item_id` INT NULL,
  `course_item_id` INT NULL,
  `dessert_item_id` INT NULL,
  `price` VARCHAR(45) NULL,
  PRIMARY KEY (`menu_id`),
  INDEX `menu_starter_idx` (`starter_item_id` ASC) VISIBLE,
  INDEX `menu_course_item_idx` (`course_item_id` ASC) VISIBLE,
  INDEX `menu_dessert_item_idx` (`dessert_item_id` ASC) VISIBLE,
  CONSTRAINT `menu_starter_item`
    FOREIGN KEY (`starter_item_id`)
    REFERENCES `LittleLemonDB`.`menu_items` (`item_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `menu_course_item`
    FOREIGN KEY (`course_item_id`)
    REFERENCES `LittleLemonDB`.`menu_items` (`item_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `menu_dessert_item`
    FOREIGN KEY (`dessert_item_id`)
    REFERENCES `LittleLemonDB`.`menu_items` (`item_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`order_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`order_items` (
  `order_item_id` INT NOT NULL,
  `order_id` INT NOT NULL,
  `menu_id` INT NOT NULL,
  `quantity` INT NOT NULL,
  `discount` DECIMAL(10,2) NOT NULL DEFAULT 0,
  PRIMARY KEY (`order_item_id`),
  INDEX `booking_order_idx` (`order_id` ASC) VISIBLE,
  INDEX `menu_item_menu_idx` (`menu_id` ASC) VISIBLE,
  CONSTRAINT `order_items_order`
    FOREIGN KEY (`order_id`)
    REFERENCES `LittleLemonDB`.`orders` (`order_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `order_items_menu`
    FOREIGN KEY (`menu_id`)
    REFERENCES `LittleLemonDB`.`menu` (`menu_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`restaurant_table`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`restaurant_table` (
  `table_id` INT NOT NULL,
  `table_length` DECIMAL(10,2) NOT NULL,
  `table_with` DECIMAL(10,2) NOT NULL,
  `table_height` DECIMAL(10,2) NOT NULL,
  `table_capacity` INT NOT NULL,
  `table_location` VARCHAR(50) NOT NULL,
  PRIMARY KEY (`table_id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `LittleLemonDB`.`booking`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `LittleLemonDB`.`booking` (
  `booking_id` INT NOT NULL AUTO_INCREMENT,
  `booking_date` DATE NOT NULL,
  `table_id` INT NOT NULL,
  `number_of_guests` INT NOT NULL DEFAULT 1,
  `time_slot` TIME NOT NULL DEFAULT '19:00:00',
  `customer_id` INT NOT NULL,
  `staff_id` INT NOT NULL DEFAULT 1,
  PRIMARY KEY (`booking_id`),
  INDEX `booking_customer_idx` (`customer_id` ASC) VISIBLE,
  INDEX `booking_staff_idx` (`staff_id` ASC) VISIBLE,
  INDEX `booking_table_idx` (`table_id` ASC) VISIBLE,
  CONSTRAINT `booking_customer`
    FOREIGN KEY (`customer_id`)
    REFERENCES `LittleLemonDB`.`customer` (`customer_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `booking_staff`
    FOREIGN KEY (`staff_id`)
    REFERENCES `LittleLemonDB`.`staff` (`staff_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE,
  CONSTRAINT `booking_table`
    FOREIGN KEY (`table_id`)
    REFERENCES `LittleLemonDB`.`restaurant_table` (`table_id`)
    ON DELETE CASCADE
    ON UPDATE CASCADE)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
